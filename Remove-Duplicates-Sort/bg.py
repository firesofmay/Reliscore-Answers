#!/usr/bin/env python

# Remove Duplicates and Sort
# http://reliscore.com/activity/ap/853/

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


def dedup(ls):
    """Given an iterator with duplicates, return a
    new iterator with duplicates removed.
    """
    seen = set()
    for l in ls:
        if l[0] not in seen:
            yield l
            seen.add(l[0])
        else:
            continue


def process_file(f):
    """Given a pipe separated file, remove duplicates
    and return in sorted order.
    """
    with open(f, "r") as fp:
        lines = (l.split("|") for l in fp)
        return sorted(dedup(lines), key=lambda x: -float(x[1]))

@timeit
def main():
    with open("bgoutput.txt", "w+") as fp:
        for l in process_file("input.txt"):
            fp.write("|".join(l))

if __name__=='__main__':
    main()


# The file contains a sequence of tweets containing interesting keywords.
# There are duplicates because some tweets got retweeted.

