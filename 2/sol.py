def execute(pos, prg):
    if prg[pos] == 99:
        return [] # HALT
    elif prg[pos] == 1:
        s1 = prg[pos + 1]
        s2 = prg[pos + 2]
        d = prg[pos + 3]
        prg[d] = prg[s1] + prg[s2]
    elif prg[pos] == 2:
        s1 = prg[pos + 1]
        s2 = prg[pos + 2]
        d = prg[pos + 3]
        prg[d] = prg[s1] * prg[s2]
    else:
        return []

    return prg

def run_prg(prg):
    assert prg
    prg = [int(x) for x in prg]

    pos = 0
    while True:
        retval = execute(pos, prg)
        if not retval:
            return prg[0]
        prg = retval
        pos += 4

def main_prg_test():
    prg = []
    with open('input.txt') as f:
        prg = f.readline().split(',')
        while prg and prg != ['']:
            run_prg(prg)
            prg = f.readline().split(',')

def main():
    with open('input.txt') as f:
        prg = f.readline().split(',')
        prg = [int(x) for x in prg]

        for n in range(0, 99):
            for v in range(0, 99):
                prg[1] = n
                prg[2] = v
                ret = run_prg(prg)
                if ret == 19690720:
                    print("END", 100 * n + v)


if __name__ == "__main__":
    main()