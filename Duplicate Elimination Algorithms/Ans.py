s = set()
for d in open('/media/New Volume/work/Reliscore/Duplicate Elimination Algorithms/100ints.txt').readlines():
    if d not in s:
        s.add(d)
    else:
        print "Found : " +str(d)
        break
