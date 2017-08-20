import struct


def decompress(data):
    """
    Decompress LZ10-compressed data.
    This code is ported from NSMBe, which was converted from Elitemap.
    """
    assert data[0] == 0x10

    dataLen = struct.unpack_from('<I', data)[0] >> 8

    out = bytearray(dataLen)
    inPos, outPos = 4, 0

    while dataLen > 0:
        d = data[inPos]; inPos += 1

        if d:
            for i in range(8):
                if d & 0x80:
                    thing, = struct.unpack_from('>H', data, inPos); inPos += 2

                    length = (thing >> 12) + 3
                    offset = thing & 0xFFF
                    windowOffset = outPos - offset - 1

                    for j in range(length):
                        out[outPos] = out[windowOffset]
                        outPos += 1; windowOffset += 1; dataLen -= 1

                        if dataLen == 0:
                            return bytes(out)

                else:
                    out[outPos] = data[inPos]
                    outPos += 1; inPos += 1; dataLen -= 1

                    if dataLen == 0:
                        return bytes(out)

                d <<= 1
        else:
            for i in range(8):
                out[outPos] = data[inPos]
                outPos += 1; inPos += 1; dataLen -= 1

                if dataLen == 0:
                    return bytes(out)

    return bytes(out)


def compress(data):
    """
    LZ10-compress data (pure-Python implementation).
    This code is ported from NSMBe.
    """

    def compressionSearch(pos):
        """
        Find the longest match in `data` (nonlocal) at or after `pos`.
        This function has been rewritten in place of NSMBe's,
        to optimize its performance in Python.
        (A straight port of NSMBe's algorithm caused some files to take
        over 40 seconds to compress. With this version, all files I've
        tested take less than one second, and the compressed files
        match the old algorithm's output byte for byte.)
        """
        maxMatchDiff = 0x1000
        maxMatchLen = 18
        match = length = 0

        start = max(0, pos - maxMatchDiff)

        # Strategy: do a binary search of potential match sizes, to
        # find the longest match that exists in the data.

        lower = 0
        upper = min(maxMatchLen, len(data) - pos)

        recordMatchPos = recordMatchLen = 0
        while lower <= upper:
            # Attempt to find a match at the middle length
            matchLen = (lower + upper) // 2
            match = data[pos : pos + matchLen]
            matchPos = data.find(match, start, pos)

            if matchPos == -1:
                # No such match -- any matches will be smaller than this
                upper = matchLen - 1
            else:
                # Match found!
                if matchLen > recordMatchLen:
                    recordMatchPos, recordMatchLen = matchPos, matchLen
                lower = matchLen + 1

        return recordMatchPos, recordMatchLen

    result = bytearray()
    result.extend(struct.pack('<I', (len(data) << 8) | 0x10))

    current = 0 # Index of current byte to compress

    while current < len(data):
        blockFlags = 0

        # We'll go back and fill in blockFlags at the end of the loop.
        blockFlagsOffset = len(result)
        result.append(0)

        for i in range(8):

            # Not sure if this is needed. The DS probably ignores this data.
            if current >= len(data):
                result.append(0)
                continue

            searchPos, searchLen = compressionSearch(current)
            searchDisp = current - searchPos - 1

            if searchLen > 2:
                # We found a big match; let's write a compressed block
                blockFlags |= 1 << (7 - i)

                result.append((((searchLen - 3) & 0xF) << 4) + ((searchDisp >> 8) & 0xF))
                result.append(searchDisp & 0xFF)
                current += searchLen

            else:
                result.append(data[current])
                current += 1

        result[blockFlagsOffset] = blockFlags

    return bytes(result)