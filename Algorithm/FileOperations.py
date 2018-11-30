import csv

def importData(path):
    input_pieces = []
    csv_file = open(path)
    csv_reader = csv.reader(csv_file, delimiter=',')
    for p in csv_reader:
        input_pieces.append((p[0], p[1], p[2], p[3]))  # (x,y,z,culoare) tupla
    return input_pieces