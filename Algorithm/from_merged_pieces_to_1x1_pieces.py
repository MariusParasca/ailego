from sys import argv


PIECES_TYPES = ((1, 1), (1, 2), (1, 3), (1, 4), (1, 6),
                (1, 8), (2, 2), (2, 3), (2, 4), (2, 6), (2, 8))


def create_1x1_pieces(x, y, pieces_type, orientation):
    result = []
    if orientation == 0:
        for i in range(x, x + PIECES_TYPES[pieces_type][0]):
            for j in range(y, y + PIECES_TYPES[pieces_type][1]):
                result.append((i, j))
    else:
        for i in range(x, x + PIECES_TYPES[pieces_type][1]):
            for j in range(y, y + PIECES_TYPES[pieces_type][0]):
                result.append((i, j))

    return result


if (len(argv) <= 1):
    print("usage: 'python from_merged_pieces_to_1x1_pieces.py <file_path>")
    raise SystemExit


with open('input_1x1.csv', 'w') as f:
    with open(argv[1]) as fd:
        for line in fd.readlines():
            data = line.split(',')
            coordonates = create_1x1_pieces(int(data[1]), int(data[3]), int(data[0]), int(data[5]))
            print(data, '->', coordonates)
            for coordonate in coordonates:
                f.write(str(0) + ',' + str(coordonate[0]) + ',' + data[2] + ',' +
                        str(coordonate[1]) + ',' + data[4] + ',' + data[5][0] + '\n')
print("Result written in input_1x1.csv")
