import csv
from piece import Piece

def import_data(path):
    input_pieces = []
    csv_file = open(path)
    csv_reader = csv.reader(csv_file, delimiter=',')
    for p in csv_reader:
        input_pieces.append((int(p[0]), int(p[2]), int(p[1]), str(p[3])))  # (x,y,z,culoare) tupla
    return input_pieces


def export_data(path, model):
    with open(path, 'w+') as fd:
        for layer in model.layers:
            [fd.write(piece.serialize()) for piece in layer.merged_pieces]


def import_test_data(path):
    input_pieces = []
    csv_file = open(path)
    csv_reader = csv.reader(csv_file, delimiter=',')
    for p in csv_reader:
        input_pieces.append((int(p[0]), int(p[1]), int(p[3]), int(p[2]), int(p[5])))  # (x,y,z,culoare) tupla
    return input_pieces

