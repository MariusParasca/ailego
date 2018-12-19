def is_structure_stable(layers):
    building_contour = contour(layers)
    base = save_base(building_contour)
    base = extract_2d_from_2d(base)
    print(base)
    center_coordinates = center_of_mass(building_contour)
    print('Centru de greutate:', center_coordinates)
    if point_inside_polygon(center_coordinates[0], center_coordinates[1], base):
        print("Structure stable.")
    else:
        print("Unstable.")


def save_base(building_contour):
    base = list()
    for point in building_contour:
        if point[2] == 0:
            base.append(point)
    return base


def extract_2d_from_2d(list):
    new_list = []
    for i in list:
        new_list.append([i[0], i[1]])
    return new_list


def center_of_mass(building_contour):
    length = 0
    width = 0
    height = 0
    number = 0

    for point in building_contour:
        length = length + point[0]
        width = width + point[1]
        height = height + point[2]
        number += 1
    return [length / number, width / number, height / number]


def contour(layers):
    building_contour = list()
    types = ((1, 1), (1, 2), (1, 3), (1, 4), (1, 6), (1, 8), (2, 2), (2, 3), (2, 4), (2, 6), (2, 8))
    for layer in layers:
        for piece in layer.merged_pieces:
            building_contour.append([piece.x, piece.y, piece.z])
            building_contour.append([piece.x, piece.y + types[piece.piece_type][1], piece.z])
            building_contour.append([piece.x + types[piece.piece_type][0], piece.y + types[piece.piece_type][1], piece.z])
            building_contour.append([piece.x + types[piece.piece_type][0], piece.y, piece.z])
            building_contour.append([piece.x, piece.y, piece.z+1])
            building_contour.append([piece.x, piece.y + types[piece.piece_type][1], piece.z+1])
            building_contour.append([piece.x + types[piece.piece_type][0], piece.y + types[piece.piece_type][1], piece.z+1])
            building_contour.append([piece.x + types[piece.piece_type][0], piece.y, piece.z+1])
    #return pop_not_relevant_points(building_contour)
    return building_contour


def pop_not_relevant_points(building_contour):
    for point in building_contour:
        min_x = 50
        min_y = 50
        max_x = 0
        max_y = 0
        for subpoint in building_contour:
            if subpoint[2] == point[2]:
                if subpoint[0] < min_x: min_x = subpoint[0]
                if subpoint[0] > max_x: max_x = subpoint[0]
                if subpoint[1] < min_y: min_y = subpoint[1]
                if subpoint[1] > max_y: max_y = subpoint[1]
        for useless_point in building_contour:
            if useless_point != [min_x, min_y, point[2]] or useless_point != [max_x, max_y, point[2]]:
                building_contour.remove(useless_point)
    print('now: ',building_contour)
    return building_contour


def pop_not_relevant_points_2(building_contour):
    for point_1 in building_contour:
        for point_2 in building_contour:
            if point_1==point_2 and building_contour.index(point_1)!=building_contour.index(point_2):
                building_contour.remove(point_2)
    return building_contour


def point_inside_polygon(x, y, poly, include_edges=True):
    '''
    Test if point (x,y) is inside polygon poly.

    poly is N-vertices polygon defined as
    [(x1,y1),...,(xN,yN)] or [(x1,y1),...,(xN,yN),(x1,y1)]
    (function works fine in both cases)

    Geometrical idea: point is inside polygon if horisontal beam
    to the right from point crosses polygon even number of times.
    Works fine for non-convex polygons.
    '''
    n = len(poly)
    inside = False

    p1x, p1y = poly[0]
    for i in range(1, n + 1):
        p2x, p2y = poly[i % n]
        if p1y == p2y:
            if y == p1y:
                if min(p1x, p2x) <= x <= max(p1x, p2x):
                    # point is on horisontal edge
                    inside = include_edges
                    break
                elif x < min(p1x, p2x):  # point is to the left from current edge
                    inside = not inside
        else:  # p1y!= p2y
            if min(p1y, p2y) <= y <= max(p1y, p2y):
                xinters = (y - p1y) * (p2x - p1x) / float(p2y - p1y) + p1x

                if x == xinters:  # point is right on the edge
                    inside = include_edges
                    break

                if x < xinters:  # point is to the left from current edge
                    inside = not inside

        p1x, p1y = p2x, p2y

    return inside
