import networkx as nx
import matplotlib.pyplot as plt


def is_piece_combined(piece_parts, layer_):
    for piece, parts in layer_.items():
        for part in parts:
            for piece_part in piece_parts:
                if piece_part[0] == part[0] and piece_part[1] == part[1]:
                    return piece
    return None


def create_nodes(G, layers_):
    for i in range(0, len(layers_)):
        for piece, parts in layers_[i].items():
            G.add_node(piece)
    # nx.draw(G)
    # plt.show()


def create_stability_graph(layers_):
    G = nx.Graph()
    create_nodes(G, layers_)
    for i in range(0, len(layers_)-1):
        for piece, parts in layers_[i].items():
            result = is_piece_combined(parts, layers_[i + 1])
            if result is not None:
                G.add_edge(piece, result)
    nx.draw(G)
    plt.show()
