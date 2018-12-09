import os.path
from file_operations import import_data, export_data
from layer import Layer
from model import Model


def break_input_in_layers(input_pieces):
    layer = []
    for piece in input_pieces:
        if layer == []:
            layer.append(piece)
        elif layer[-1][2] == piece[2]:
            layer.append(piece)
        else:
            yield Layer(layer)
            layer = []
            layer.append(piece)
    yield Layer(layer)


def merge_input_pieces(input_pieces):
    model = Model()
    orientation = False
    for layer in break_input_in_layers(input_pieces):
        layer.merge_pieces(orientation)
        model.model.append(layer)
        orientation = not orientation
    return model


if __name__ == '__main__':
    input_pieces = import_data(os.path.join(os.path.dirname(os.path.realpath(__file__)),'input.csv'))
    model = merge_input_pieces(input_pieces)
    export_data('output.csv', model)

    for layer in model.model:
       [print(piece) for piece in layer.merged_pieces]