from collections import Counter

def check_decrease(num):
    digs = [int(x) for x in str(num)]
    last = digs[0]
    for i in range(1, len(digs)):
        if last > digs[i]:
            return False
        else:
            last = digs[i]
    return True

def check_properties(num, rangelow, rangehigh):
    # 6 digit number
    length_ok = len(str(num)) == 6
    # within range
    range_ok = rangelow <= num and num < rangehigh
    # two adjecent digits are the same
    adj_ok = False
    digits = [int(x) for x in str(num)]
    counter = Counter(digits)
    for o in counter:
        occs = counter[o]
        if occs == 2:
            adj_ok = True
    # only decrease
    decrease_ok = check_decrease(num)
#    print(num,length_ok, range_ok, adj_ok, decrease_ok)
    return length_ok and range_ok and adj_ok and decrease_ok


def solve_1(low, high):
    counter = 0
    for i in range(low, high):
        if check_properties(i, low, high):
            counter += 1

    return counter


def main():
    low = 372304 
    high = 847060

    print(solve_1(low, high))


if __name__ == "__main__":
    print(check_properties(111111, 0, 1000000000))
    print(check_properties(223450, 0, 1000000000))
    print(check_properties(123789, 0, 1000000000))
    main()
