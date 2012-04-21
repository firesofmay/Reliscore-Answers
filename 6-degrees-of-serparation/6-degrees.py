#http://reliscore.com/activity/ap/4226/

from collections import defaultdict
import sys

def find_shortest_path(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if not graph.has_key(start):
            return None
        shortest = None
        for node in graph[start]:
            if node not in path:
                newpath = find_shortest_path(graph, node, end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest


def main():
    itemlist = []

    for line in sys.stdin:
        itemlist.append(line.rstrip('\n'))


    d = defaultdict(list)
    
    for line in itemlist:
        person1 = line.split(',')[0]
        person2 = line.split(',')[1].strip()
        d[person1].append(person2)


    print len(find_shortest_path(d,'Sonia Gandhi', 'Bal Thackeray'))

if __name__ == '__main__':
    main()
