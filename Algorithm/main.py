import os.path
from Algorithm.file_operations import import_data, export_data
from Algorithm.layer import Layer
from Algorithm.model import Model
from Algorithm.center_of_mass import *
# from graph_stability_method import create_stability_graph

def break_input_in_layers(input_pieces):
    max = 0
    for piece in input_pieces:
        if piece[2] > max:
            max = piece[2]
    for i in range(max+1):
        yield Layer(list(filter(lambda x : x[2] == i, input_pieces)))


def merge_input_pieces(input_pieces):
    model = Model()
    orientation = False
    for layer in break_input_in_layers(input_pieces):
        layer.merge_pieces(orientation)
        model.layers.append(layer)
        orientation = not orientation
    return model


if __name__ == '__main__':
    input_pieces = import_data(os.path.join(os.path.dirname(os.path.realpath(__file__)),'input.csv'))
    model = merge_input_pieces(input_pieces)
    export_data(os.path.join(os.path.dirname(os.path.realpath(__file__)), r'..\AI_Interface\input.csv'), model)
    array = []
    # Portiune de cod echipa cu testaterea stabilitati cu metoda grafurilor
    # for layer in model.layers:
    #     dic = {}
    #     for piece in layer.merged_pieces:
    #         dic[(piece.x, piece.y, piece.z)] = piece.export()
    #     array.append(dic)
    # print(dic)
    # create_stability_graph(array)



    # for center of masss using geometry
    is_structure_stable_1(model.layers)
    #print('main')
    # ends here



    for layer in model.layers:
       [print(piece) for piece in layer.merged_pieces]