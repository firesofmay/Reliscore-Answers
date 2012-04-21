#http://reliscore.com/activity/ap/4225/
import operator
from collections import defaultdict
import sys

def main():
    itemlist = []

    for line in sys.stdin:
        itemlist.append(line.rstrip('\n'))

    d = defaultdict(int)
    
    for i in itemlist:
        d[i] += 1
    
    print max(d.iteritems(), key=operator.itemgetter(1))[0]

if __name__ == '__main__':
    main()
