#http://reliscore.com/activity/ap/4230/

import sys

def main():
    nums = []

    for line in sys.stdin:
        nums.append(int(line.rstrip('\n')))

    nums.sort()

    for line in nums:
        print line


if __name__ == '__main__':
    main()
