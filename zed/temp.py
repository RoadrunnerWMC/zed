
import common
import zclb_zcib

with open('../RETAIL/st/root/Course/courseinit.cib', 'rb') as f:
    ci = f.read()
with open('../RETAIL/st/root/Course/courselist.clb', 'rb') as f:
    cl = f.read()

x = zclb_zcib.loadCourseListAndInit(common.Game.SpiritTracks, cl, ci)
for y in x:
    if y.name == 'f_first':
        for m in y.maps:
            print('----')
            print(m.mapID)
            print(m.unk01)
            print(m.unk02)