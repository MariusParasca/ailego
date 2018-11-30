import csv

def importData(path):
    input_pieces = []
    csv_file = open(path)
    csv_reader = csv.reader(csv_file, delimiter=',')
    for p in csv_reader:
        input_pieces.append((int(p[0]), int(p[1]), int(p[2]), str(p[3])))  # (x,y,z,culoare) tupla
    return input_pieces