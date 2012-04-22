#http://reliscore.com/activity/ap/496/

#The data set is from twitter.

import time                                                

def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print '%r (%r, %r) %2.7f sec' % \
              (method.__name__, args, kw, te-ts)
        return result

    return timed

@timeit
def main():
    f = open("input.txt")
    txt = f.readlines()
    mainlist = []
    s = set()
    for line in txt:
        list = line.split("|")
        if list[0] not in s:
            mainlist.append((list[0], list[1],list[2],list[3]))
            s.add(list[0])

    sw = sorted(mainlist,key=lambda student: student[1], reverse=True)
    fw = open("output.txt", 'w')
    for line in sw:
        fw.write(line[0] + "|" + line[1] + "|" + line[2] + "|" + line[3])    
    fw.close()

if __name__ == "__main__":
    main()


