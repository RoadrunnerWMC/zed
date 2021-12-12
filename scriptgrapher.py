import os, os.path
import textwrap

import ndspy.bmg
import pygraphviz

import zeldaScripts


def nextInstructions(inst, bmg):
    """
    Return a list of (name, Label)s that the given instruction is able
    to branch to.
    """
    if inst.type == 'SAY':
        return [(None, inst.nextLabel)]

    elif inst.type.startswith('SW'):
        labels = []
        for i, L in enumerate(bmg.labels[inst.firstLabel : inst.firstLabel + inst.numLabels]):
            labels.append((inst.nameForBranch(i), zeldaScripts.Label(*L)))
        return labels

    else:
        return [(None, zeldaScripts.Label(*bmg.labels[inst.labelNumber]))]


def nextInstructions_filterBmg(inst, bmg):
    """
    Runs nextInstructions, but only returns results with the given BMG.
    And returns raw indices instead of Label instances.
    """
    indices = []
    for name, L in nextInstructions(inst, bmg):
        if L.bmg == bmg.id and not L.isNull():
            indices.append((name, L.index))
    return indices


def findRuns(bmg, insts, labels):
    """
    Find run indices in this BMG.
    """

    xrefs = [set() for _ in insts] # "None" = is a script start
    for i, inst in enumerate(insts):
        for _, n in nextInstructions_filterBmg(inst, bmg):
            xrefs[n].add(i)
    for id, idx in bmg.scripts.items():
        xrefs[idx].add(None)

    runs = [[i] for i, _ in enumerate(insts)]

    i = 0
    while i < len(runs):
        g = runs[i]

        next = nextInstructions_filterBmg(insts[g[-1]], bmg)

        # If this run leads to exactly one other, and nothing else leads to that one...
        if len(next) == 1 and len(xrefs[next[0][1]]) == 1:

            # (Find the run it leads to)
            for g2 in runs:
                if g2[0] == next[0][1]:
                    break
            else:
                raise RuntimeError("Didn't find the run :|")

            if g is not g2: # ...and if that run isn't ourself...
                # Combine the runs.
                g.extend(g2)
                runs.remove(g2)

        else:
            # That's as much as we can extend this run by -- move on to
            # the next one.
            i += 1

    # Sanity checks:
    runMembers = [idx for run in runs for idx in run]
    # - Check that the total number of run members == the number of indices
    assert len(runMembers) == len(insts)
    # - Check that every index is present
    assert set(runMembers) == set(range(len(insts)))

    return runs


def analyze(filename, rawData, bmg, allBmgs):
    if b'FLW1' not in rawData:
        print(f'{filename} does not have scripts.')
        return

    print(filename)

    bmgID = [a for (a,(b,c)) in allBmgs.items() if c is bmg][0]

    insts = zeldaScripts.disassembleInstructions(bmg.instructions)
    labels = zeldaScripts.disassembleLabels(bmg.labels)

    # Make strings for each instruction
    instStrings = []
    for i, inst in enumerate(insts):
        if isinstance(inst, zeldaScripts.SayInstruction):
            messageBMG = allBmgs[inst.messageBMG][1]
            msg = str(messageBMG.messages[inst.messageID]).replace('\n', ' ')
            name = f'"{textwrap.fill(textwrap.shorten(msg, 40*6), 40)}"'
        elif isinstance(inst, zeldaScripts.SwitchInstruction):
            name = inst.type + f'({inst.condition}): %08X' % inst.parameter
        else:
            name = inst.type + f'({inst.action}): %016X' % inst.parameter
        name = ('[%x] ' % i) + name
        instStrings.append(name)

    runs = findRuns(bmg, insts, labels)

    # Make text blocks for each run
    runTexts = []
    for g in runs:
        runTexts.append('\n'.join(instStrings[i] for i in g))

    def findRunStartingWith(idx):
        for i, g in enumerate(runs):
            if g[0] == idx:
                return i
        raise RuntimeError(f"Can't find a run starting with {idx}")

    # Make a graph
    G = pygraphviz.AGraph(directed=True, strict=False)

    def nodeAttrs(insts):
        """
        For debugging.
        """
        MARK_1 = {'color': 'green', 'penwidth': 10}

        attrs = {}
        #print(list(insts))
        for inst in insts:
            # if isinstance(inst, zeldaScripts.DoInstruction) and inst.action == 9 and 101 <= inst.parameter <= 105:
            #     print(f'Instruction found! Parameter = {inst.parameter}')
            #     attrs.update(MARK_1)
            if isinstance(inst, zeldaScripts.SayInstruction) and inst.messageBMG == 0xF and inst.messageID == 188:
                print(f'Instruction found!')# Parameter = {inst.parameter}')
                attrs.update(MARK_1)

        return attrs

    for text, r in zip(runTexts, runs):

        lastInst = insts[r[-1]]
        nextIdxs = nextInstructions_filterBmg(lastInst, bmg)

        if text not in G:
            G.add_node(text, **nodeAttrs(insts[i] for i in r))

        for nextName, nextIdx in nextIdxs:
            nextRun = findRunStartingWith(nextIdx)
            nextText = runTexts[nextRun]

            if nextText not in G:
                G.add_node(nextText, **nodeAttrs(insts[i] for i in runs[nextRun]))

            if nextName:
                G.add_edge(text, runTexts[nextRun], label=nextName)
            else:
                G.add_edge(text, runTexts[nextRun])

        for id, idx in bmg.scripts.items():
            if r[0] == idx:
                # Add a script launch node
                nodeName = f'({id >> 16}, {id & 0xFFFF})'
                G.add_node(nodeName, color='red')
                G.add_edge(nodeName, text)

    # circo is good but sometimes crashes; fdp is worse but reliable
    try:
        H = G.copy()
        H.layout('circo')
        H.draw(f'graphs/{filename.split(".")[0]}.png')
    except:
        H = G.copy()
        H.layout('fdp')
        H.draw(f'graphs/{filename.split(".")[0]}.png')



def main():
    dir = '/home/user/zed/Testing/st/root/English/Message/'
    dir2 = '/home/user/zed/Testing/stResavedBMGs/'

    BMGs = {}

    for fn in os.listdir(dir):
        fullfn = os.path.join(dir, fn)
        with open(fullfn, 'rb') as f:
            d = f.read()

        bmg = ndspy.bmg.BMG(d)
        BMGs[bmg.id] = (fn, bmg)


    allScripts = {}
    for id, (fn, bmg) in BMGs.items():
        for id in bmg.scripts:
            a, b = id >> 16, id & 0xFFFF
            if a not in allScripts:
                allScripts[a] = set()
            allScripts[a].add(b)
    for a in sorted(allScripts):
        print(f'{a}:')
        for b in sorted(allScripts[a]):
            print(f'    {b}:')
    return


    for id, (fn, bmg) in BMGs.items():
        analyze(fn, d, bmg, BMGs)

main()