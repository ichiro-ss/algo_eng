def read_points(f) -> dict:
    """Read the input file"""
    indexofpoint = {}
    for line in f:
        if line and 0x30 <= ord(line[0]) <=0x39:    # only 0-9
            i, x, y = (float(s) for s in line.split())
            indexofpoint[(x, y)] = int(i)-1
    return indexofpoint
