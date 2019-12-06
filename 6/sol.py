from collections import defaultdict
GRAPH = defaultdict(list)
INV_GRAPH = defaultdict(str)

def DFS(root, orb):
    total = orb
    for planet in GRAPH[root]:
        total += DFS(planet, orb + 1)
    return total


def process_line(line):
    line = line[:-1].split(')')
    assert len(line) == 2
    src = line[0]
    dst = line[1]
    GRAPH[src].append(dst)
    assert INV_GRAPH[dst] == str()
    INV_GRAPH[dst] = src

def to_root(start):
    cur = INV_GRAPH[start]
    route = [cur]
    while INV_GRAPH[cur] != str():
        cur = INV_GRAPH[cur]
        route.append(cur)

    return route


def main():
    with open("input") as fp:
        line = fp.readline()
        while line:
            process_line(line)
            line = fp.readline()

    # print(GRAPH)
    assert GRAPH

    # find root
    is_orbited = [key for key in GRAPH]
    orbitting = []
    for key in GRAPH:
        orbitting += GRAPH[key]

    orbitting = set(orbitting)
    roots = [x for x in is_orbited if x not in orbitting]
    print("Roots are:", roots)

    # Part 1, DFS
    total = 0
    for r in roots:
        total += DFS(r, 0)

    print(total)

    # Part 2, lowest common ancestor
    you = to_root("YOU")
    santa = to_root("SAN")
    print("Y", you, "SAN", santa)
    same = None
    santa_pos = None
    for i in range(0, len(santa)):
        if santa[i] in you:
            same = santa[i]
            santa_pos = i
            break
    
    print(same, santa_pos)
    you_pos = None
    for i in range(0, len(you)):
        if you[i] == same:
            you_pos = i
            break
    print(santa_pos, you_pos)
    print(santa_pos + you_pos)

    


if __name__ == "__main__":
    main()
