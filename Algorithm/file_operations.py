from layer import Layer
from model import Model
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
        for layer in model.model:
            [fd.write(piece.serialize()) for piece in layer.merged_pieces]


def import_data_into_model(path):
    input_pieces = []
    csv_reader = csv.reader(open(path, "r"), delimiter=',')
    for p in csv_reader:
        input_pieces.append((int(p[0]), int(p[1]), int(p[2]), int(p[3]), str(p[4]), int(p[5])))  # (type, x, z, y, culoare, orientare) tupla
    max_heigh = 0
    for piece in input_pieces:
        if max_heigh < piece[2]:
            max_heigh = piece[2]
    model = Model()
    for i in range(max_heigh+1):
        merged_pieces = []
        for p in list(filter(lambda x : x[2] == i, input_pieces)):
            merged_pieces.append(Piece(p[0], p[4], p[1], p[3], p[2], False if p[5] == 0 else True))
        model.layers.append(Layer(merged_pieces))
    return model