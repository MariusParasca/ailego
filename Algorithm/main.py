import os.path
from file_operations import import_data, export_data, export_data_by_pieces
from layer import Layer
from graph_stability_method import *
import itertools
import copy

combinations = [[0,0,1],[1,1,0]]

def initialize_pieces(in_pieces):
    pieces = []
    for p in in_pieces:
        pieces.append(Piece(0, p[3], p[0], p[1], p[2]))
    return pieces

def apply_combination(layer,ordine):
    for i in ordine:
        if(int(i) == 0):
            layer.pieces_iteration()
        else:
            layer.pieces_iteration_invert()

def merge_layer(layer):
    aux = copy.deepcopy(layer)
    max_score = 0
    combination = 0
    for j in range(len(combinations)):
        layer = copy.deepcopy(aux)
        apply_combination(layer, combinations[j])
        merge_test = []
        merge_test.extend(merged_pieces)
        merge_test.extend(layer.pieces)
        layers = read_from_list_of_pieces(merge_test)
        G = create_stability_graph(layers)
        gscore = graph_stability_new_with_score(G)
        if(gscore > max_score):
            max_score = gscore
            combination = j
    layer = copy.deepcopy(aux)
    apply_combination(layer, combinations[combination])
    return layer


if __name__ == '__main__':
    input_pieces = import_data(os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'input.csv'))
    pieces = initialize_pieces(input_pieces)

    pieces.sort(key=lambda p: (p.z, p.y, p.z))
    max_z = pieces[-1].z
    merged_pieces = []
    #combinations = [[0,0,0],[0,0,1],[0,1,0],[0,1,1],[1,0,0],[1,0,1],[1,1,0],[1,1,1]]
    first_layer = True
    layer2 = None

    for i in range(max_z):
        layer = Layer([p for p in pieces if p.z == i])
        layer2 = Layer([p for p in pieces if p.z == i+1])
        layer.empty_inside(layer2)
        
        if first_layer == True:
            layer.pieces_iteration()
            layer.pieces_iteration()
            layer.pieces_iteration_invert()
            first_layer = False
        else:
            layer = merge_layer(layer)
            #layer.print_pieces()
        #print("\n")
        merged_pieces.extend(layer.pieces)
    layer2 = merge_layer(layer2)
    merged_pieces.extend(layer2.pieces)

    export_data_by_pieces(os.path.join(os.path.dirname(
        os.path.realpath(__file__)), r'..\AI_Interface\input.csv'), merged_pieces)
    # layers = read_output_from_file(r'..\AI_Interface\input.csv') # trebuie schimbat in PIECES_TYPES daca vrem sa citim din fisier
    layers = read_from_list_of_pieces(merged_pieces)
    # layers = read_output_from_file(r'E:\Dropbox\Facultate\Inteligenta artificiala\ailego-Greedy-Merging\AI_Interface\input.csv')
    # layers = read_output_from_file(r'E:\Dropbox\Facultate\Inteligenta artificiala\inputs\input.csv')

    G = create_stability_graph(layers)
    print_graph(G)

