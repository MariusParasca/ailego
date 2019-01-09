import networkx as nx
import matplotlib.pyplot as plt
from piece import Piece
from layer import Layer


def is_piece_combined(piece_parts, layer_):
    for piece, parts in layer_.items():
        for part in parts:
            for piece_part in piece_parts:
                if piece_part[0] == part[0] and piece_part[1] == part[1]:
                    return piece
    return None


def create_nodes_old(G, layers_):
    for i in range(0, len(layers_)):
        for piece, parts in layers_[i].items():
            G.add_node(piece)


def create_stability_graph_old(layers_):
    G = nx.Graph()
    create_nodes_old(G, layers_)
    for i in range(0, len(layers_)-1):
        for piece, parts in layers_[i].items():
            result = is_piece_combined(parts, layers_[i + 1])
            if result is not None:
                G.add_edge(piece, result)
    nx.draw(G)
    plt.show()


def is_overlapping(x1, y1, x2, y2):
    s1 = set(range(x1, y1 + 1))
    s2 = set(range(x2, y2 + 1))
    if s1 & s2:
        return True
    else:
        return False


def get_interval_margin(piece):
    if piece.orientation:
        piece_x = Piece.PIECES_TYPES_INVERT[piece.piece_type][1] - 1 + piece.x
        piece_y = Piece.PIECES_TYPES_INVERT[piece.piece_type][0] - 1 + piece.y
    else:
        piece_x = Piece.PIECES_TYPES_INVERT[piece.piece_type][0] - 1 + piece.x
        piece_y = Piece.PIECES_TYPES_INVERT[piece.piece_type][1] - 1 + piece.y

    return piece_x, piece_y


def create_nodes(G, layers_):
    for i in range(0, len(layers_)):
        for piece in layers_[i].merged_pieces:
            G.add_node(piece)

def is_on_last_layer(graph, el):
    if len(graph[el]) == 1:
        return True
    return False

def dfs(graph, start):
    visited = []
    visited.append(start)
    stack = set()

    for el in graph[start]:
        if is_on_last_layer(graph, el):
            visited.append(el)

    for el in graph[start]:
        if el not in visited:
            stack.add(el)
            break

    while stack:
        nod = stack.pop()
        if nod not in visited:
            visited.append(nod)
            for el in graph[nod]:
                if el not in visited:
                    stack.add(el)
    #print(visited)
    return len(visited)


def check_graph_stability(G):
    gr = nx.Graph()
    '''gr.add_node('A')
    gr.add_node('B')
    gr.add_node('C')
    gr.add_node('D')
    gr.add_node('E')
    gr.add_node('F')
    gr.add_node('H')
    gr.add_node('I')
    gr.add_node('J')

    gr.add_edge('A', 'D')
    gr.add_edge('B', 'D')
    gr.add_edge('B', 'E')
    gr.add_edge('B', 'F')
    gr.add_edge('C', 'F')
    gr.add_edge('C', 'G')
    gr.add_edge('D', 'H')
    gr.add_edge('E', 'H')
    gr.add_edge('E', 'I')
    gr.add_edge('F', 'I')
    gr.add_edge('F', 'J')
    gr.add_edge('G', 'J')
    gr.add_edge('E', 'J')
    #gr.add_edge('A', 'E')
    '''
    gr = G
    for node in gr.nodes:
        #print(dfs(gr, node))
        if dfs(gr, node) != len(gr.nodes):
            return [False, node]
    return True

def create_stability_graph(layers_):
    G = nx.Graph()
    create_nodes(G, layers_)
    for i in range(0, len(layers_) - 1):
        for piece1 in layers_[i].merged_pieces:
            for piece2 in layers_[i + 1].merged_pieces:
                piece1_x, piece1_y = get_interval_margin(piece1)
                piece2_x, piece2_y = get_interval_margin(piece2)
                if is_overlapping(piece1.x, piece1_x, piece2.x, piece2_x) and \
                   is_overlapping(piece1.y, piece1_y, piece2.y, piece2_y):
                    G.add_edge(piece1, piece2)
    nx.draw(G)
    plt.show()
    return G


def read_output_from_file(file_path):
    layers = []
    piece_list = []
    layer_number = 0
    with open(file_path) as fd:
        for line in fd.readlines():
            if not line.strip():
                continue
            data = line.split(',')
            if int(data[5]) == 0:
                piece = Piece(int(data[0]), data[4], int(data[1]), int(data[3]), int(data[2]), False)
            else:
                piece = Piece(int(data[0]), data[4], int(data[1]), int(data[3]), int(data[2]), True)
            if layer_number == int(data[2]):
                piece_list.append(piece)
            else:
                layer = Layer([])
                layer.merged_pieces = piece_list
                layers.append(layer)
                layer_number += 1
                piece_list = [piece]
    layer = Layer([])
    layer.merged_pieces = piece_list
    layers.append(layer)
    return layers

def read_from_list_of_pieces(pieces):
    layers = []
    piece_list = []
    layer_number = 0
    for piece in pieces:
        if layer_number == piece.z:
            piece_list.append(piece)
        else:
            layer = Layer([])
            layer.merged_pieces = piece_list
            layers.append(layer)
            layer_number += 1
            piece_list = [piece]
    layer = Layer([])
    layer.merged_pieces = piece_list
    layers.append(layer)
    return layers
