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
    return max(x1, y1) >= min(x2, y2)


def get_interval_margin(piece):
    if piece.orientation:
        piece_x = Piece.PIECES_TYPES[piece.piece_type][1] - 1 + piece.x
        piece_y = Piece.PIECES_TYPES[piece.piece_type][0] - 1 + piece.y
    else:
        piece_x = Piece.PIECES_TYPES[piece.piece_type][0] - 1 + piece.x
        piece_y = Piece.PIECES_TYPES[piece.piece_type][1] - 1 + piece.y

    return piece_x, piece_y


def create_nodes(G, layers_):
    for i in range(0, len(layers_)):
        for piece in layers_[i].merged_pieces:
            G.add_node(piece)


def create_stability_graph(layers_):
    G = nx.Graph()
    create_nodes(G, layers_)
    for i in range(0, len(layers_) - 1):
        for piece1 in layers_[i].merged_pieces:
            for piece2 in layers_[i + 1].merged_pieces:
                piece1_x, piece1_y = get_interval_margin(piece1)
                piece2_x, piece2_y = get_interval_margin(piece2)
                if is_overlapping(piece1.x, piece1_x, piece2.x, piece2_x) and \
                   is_overlapping(piece1.z, piece1_y, piece2.z, piece2_y):
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
                piece = Piece(int(data[0]), data[4], int(data[1]), int(data[2]), int(data[3]), False)
            else:
                piece = Piece(int(data[0]), data[4], int(data[1]), int(data[2]), int(data[3]), True)
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


