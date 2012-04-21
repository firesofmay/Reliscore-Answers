#http://reliscore.com/activity/ap/4225/
import operator
from collections import defaultdict
import sys

def find_all_paths(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if not graph.has_key(start):
            return []
        paths = []
        for node in graph[start]:
            if node not in path:
                newpaths = find_all_paths(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

def main():
    itemlist = []

    for line in sys.stdin:
        itemlist.append(line.rstrip('\n'))


    d = defaultdict(list)
    
    for line in itemlist:
        emp = line.split(',')[0]
        boss = line.split(',')[2].strip()
        d[boss].append(emp)


    maxdepth = -1
    answer = ""

    for i in d.itervalues():
        for a in i:
            temp = find_all_paths(d, 'NOBODY', a)
            count = len(temp[0])
            emp = temp[0][-1]

        if maxdepth < count:
            maxdepth = count
            answer = emp
            
    print answer


if __name__ == '__main__':
    main()
