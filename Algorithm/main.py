import os.path
from file_operations import import_data, export_data
from layer import Layer
from model import Model
from graph_stability_method import *
import copy


def break_input_in_layers(input_pieces):
    max = 0
    master_list = []
    for piece in input_pieces:
        if piece[1] > max:
            max = piece[1]
    for i in range(max+1):
        master_list.append(Layer(list(filter(lambda x : x[1] == i, input_pieces))))
    return master_list


def merge_input_pieces(input_pieces):
    model = Model()
    best_model = copy.deepcopy(model)
    nr = 0
    iterations = 0
    layers = break_input_in_layers(input_pieces)
    layer = 0
    go_back = [2 for i in range(len(layers))]
    while layer < len(layers):
        if layer == 10:
            layer = 10
        model.layers.append(layers[layer])
        model.layers[-1].merge_pieces()
        print('Layer',layer,'done.',check_graph_stability(create_stability_graph(model.layers)))
        if layer == 2:
            iterations = 0
            if check_graph_stability(create_stability_graph(model.layers)) is False:
                print('Problem with layer' + str(layer) + ', trying to reassambly...')
                while check_graph_stability(create_stability_graph(model.layers)) is False:
                    iterations += 1
                    if iterations % 10 == 0:
                        print(iterations)
                    for l in model.layers:
                        l.merge_pieces()
                print(check_graph_stability(create_stability_graph(model.layers)))
                print('Layer',layer,'done with',iterations,'tries.',check_graph_stability(create_stability_graph(model.layers)))
        elif layer > 2:
            iterations = 0
            if check_graph_stability(create_stability_graph(model.layers)) is False:
                print('Problem with layer' + str(layer) + ', trying to reassambly...')
                while check_graph_stability(create_stability_graph(model.layers)) is False:
                    iterations += 1
                    model.layers[-1].merge_pieces()
                    if iterations == 300:
                        if go_back[layer] >= len(model.layers):
                            print(go_back)
                            while layer < len(layers):
                                best_model.layers.append(layers[layer])
                                best_model.layers[-1].merge_pieces()
                                layer += 1
                            print(check_graph_stability(create_stability_graph(model.layers)))
                            return best_model
                        print("Couldn't assambly. Get back with",go_back[layer]-1,'layers')
                        for i in range(go_back[layer]):
                            model.layers.pop()
                        go_back[layer] += 1
                        layer -= go_back[layer] - 1
                        break
                        #create_stability_graph(model.layers, show=True)
                        #create_stability_graph(best_model.layers, show=True)
                        #return best_model
                if iterations != 300:
                    print('Layer', layer, 'done with',iterations,'tries.',check_graph_stability(create_stability_graph(model.layers)))
        if iterations != 300:
            if len(best_model.layers) < len(model.layers):
                best_model = copy.deepcopy(model)
            go_back[layer] = 2
        layer += 1
    return model


def get_detailed_layers(model):
    array = []
    for layer in model.layers:
        dic = {}
        for piece in layer.merged_pieces:
            dic[(piece.x, piece.y, piece.z)] = piece.export()
        array.append(dic)
    return array


if __name__ == '__main__':
    import time
    start_time = time.time()
    input_pieces = import_data(os.path.join(os.path.dirname(os.path.realpath(__file__)),'input.csv'))
    model = merge_input_pieces(input_pieces)
    export_data(os.path.join(os.path.dirname(os.path.realpath(__file__)), r'..\AI_Interface\house.csv'), model)
    print(time.time()-start_time)
    # Portiune cod pentru cei de la metoda cu grafuri
    # layers = read_output_from_file('E:\Dropbox\Facultate\Inteligenta artificiala\AI_Interface\input.csv')
    #G = create_stability_graph(model.layers)
    #print(check_graph_stability(G))
    # for layer in model.layers:
    #     [print(piece) for piece in layer.merged_pieces]
