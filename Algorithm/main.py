import os.path
from file_operations import import_data, export_data, export_data_by_pieces
from layer import Layer
from model import Model
from graph_stability_method import *

def initialize_pieces(in_pieces):
    pieces = []
    for p in in_pieces:
        pieces.append(Piece(0,p[3],p[0],p[1],p[2]))
    return pieces

if __name__ == '__main__':
    input_pieces = import_data(os.path.join(os.path.dirname(os.path.realpath(__file__)),'input.csv'))
    pieces = initialize_pieces(input_pieces)
 
    pieces.sort(key = lambda p: (p.z, p.y, p.z))
    max_z = pieces[-1].z
    merged_pieces = []

    for i in range(max_z+1):
        layer = Layer([p for p in pieces if p.z == i])
        layer.empty_inside()

        if int(i%2) == 0:
            layer.pieces_iteration()
            layer.pieces_iteration()
            layer.pieces_iteration_invert()
        else:
            layer.pieces_iteration_invert()
            layer.pieces_iteration_invert()
            layer.pieces_iteration() 
        layer.print_pieces()
        print("\n")
        merged_pieces.extend(layer.pieces)
    
    export_data_by_pieces(os.path.join(os.path.dirname(os.path.realpath(__file__)), r'..\AI_Interface\input.csv'), merged_pieces)
    
    
    # model = merge_input_pieces(input_pieces)
    # export_data(os.path.join(os.path.dirname(os.path.realpath(__file__)), r'..\AI_Interface\input.csv'), model)
    # Portiune cod pentru cei de la metoda cu grafuri
    #layers = read_output_from_file('E:\Dropbox\Facultate\Inteligenta artificiala\AI_Interface\input.csv')
    #G = create_stability_graph(layers)
    #print(check_graph_stability(G))
    # for layer in model.layers:
    #     [print(piece) for piece in layer.merged_pieces]