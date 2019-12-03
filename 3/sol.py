import timeit

class Pt:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.x) + ":" + str(self.y)

    def __repr__(self):
        return str(self)

class Line:
    def __init__(self, p1, p2):
        self.orig1 = p1
        self.orig2 = p2
        zero = Pt(0,0)
        p1d = manhat_dst(zero, p1)
        p2d = manhat_dst(zero, p2)
        self.p1 = None
        self.p2 = None
        if p1d < p2d:
            self.p1 = p1
            self.p2 = p2
        else:
            self.p1 = p2
            self.p2 = p1
        self.dir = None
        if p1.x - p2.x == 0:
            self.dir = "Y"
        elif p1.y - p2.y == 0:
            self.dir = "X"
        else:
            raise RuntimeError("Dir, F.")

    def intersects(self, line2):
        # oversimplification?
        if self.dir == line2.dir:
            return []
        if self.dir == "X":
            assert line2.p1.x == line2.p2.x
            if self.p1.x < line2.p1.x and self.p2.x > line2.p1.x:
                if line2.p1.y < self.p1.y and line2.p2.y > self.p1.y:
                    return [Pt(line2.p1.x, self.p1.y)]
                else:
                    return []
            else:
                return []
        elif self.dir == "Y":
            assert line2.dir == "X"
            return line2.intersects(self)
        else:
            raise RuntimeError("Hm, F.")

    def pt_on_line(self, point):
        if self.dir == "X":
            if point.y == self.p1.y:
                if self.p1.x < point.x and self.p2.x > point.x:
                    return True
            return False
        elif self.dir == "Y":
            if point.x == self.p1.x:
                if self.p1.y < point.y and self.p2.y > point.y:
                    return True
            return False
        else:
            return False

    def length(self):
        return manhat_dst(self.p1, self.p2)

    def __str__(self):
        return str(self.p1) + "-" + str(self.p2)

    def __repr__(self):
        return str(self)


def manhat_dst(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)

def parse_instr(instr):
    direction = instr[0]
    dist = int(instr[1:])

    if direction == 'R':
        return (dist, 0)
    elif direction == 'L':
        return (-dist, 0)
    elif direction == 'U':
        return (0, dist)
    elif direction == 'D':
        return (0, -dist)
    else:
        raise RuntimeError("F.")

def build_pt_string(line):
    pts = [Pt(0,0)]
    for v in line:
        dx, dy = parse_instr(v)
        pt_last = pts[-1]
        pts.append(Pt(pt_last.x + dx, pt_last.y + dy))
    return pts

def get_min(oldmin, newone):
    zero = Pt(0,0)
    dst_old = manhat_dst(zero, oldmin)
    dst_new = manhat_dst(zero, newone)
    if dst_new < dst_old:
        return newone
    else:
        return oldmin

def get_traveled_len(pt, line):
    cur_len = 0
    for seg in line:
        if seg.pt_on_line(pt):
            cur_len += manhat_dst(seg.orig1, pt)
            #print("+part", manhat_dst(seg.orig1, pt), " | ", seg.orig1, pt)
            break
        else:
            cur_len += seg.length()
            #print("+whole", seg.length())
    return cur_len

def get_len_min(old_pt, old_len, line1, line2, new_pt):
    len1 = get_traveled_len(new_pt, line1)
    #print(len1)
    len2 = get_traveled_len(new_pt, line2)
    #print(len2)
    new_len = len1 + len2
    if new_len < old_len:
        return new_pt, new_len
    else:
        return old_pt, old_len

def solve(l1, l2):
    l1 = l1.split(',')
    l2 = l2.split(',')
    pts1 = build_pt_string(l1)
    pts2 = build_pt_string(l2)

    lines1 = []
    for i in range(0, len(pts1) - 1):
        lines1.append(Line(pts1[i], pts1[i+1]))

    lines2 = []
    for i in range(0, len(pts2) - 1):
        lines2.append(Line(pts2[i], pts2[i+1]))

    min_intersect = Pt(999999999999999,999999999999999)
    min_len = 2 * 999999999999999

    for i in range(0, len(pts2) - 1):
        curline = Line(pts2[i], pts2[i+1])
        for interline in lines1:
            check_inter = interline.intersects(curline)
            if check_inter:
                check_inter = check_inter[0]
                # print(check_inter)
                # min_intersect = get_min(min_intersect, check_inter)
                min_intersect, min_len = get_len_min(min_intersect, min_len, lines1, lines2, check_inter)

    # return manhat_dst(Pt(0,0), min_intersect)
    return min_len

def main():
    with open('input-true.txt') as f:
        temp = f.read().splitlines()
        line1 = temp[0]
        line2 = temp[1]
        assert len(temp) == 2
        print(solve(line1, line2))

if __name__ == "__main__":
    p1 = Pt(0,0)
    p2 = Pt(5,5)
    p3 = Pt(2,3)
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    print('Time: ', stop - start)