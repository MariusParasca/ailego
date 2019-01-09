from copy import deepcopy


class Piece:
    PIECES_TYPES = ((1,1),(1,2),(1,3),(1,4),(1,6),(1,8),(2,2),(2,3),(2,4),(2,6),(2,8))
    PIECES_TYPES_INVERT = ((1,1),(2,1),(3,1),(4,1),(6,1),(8,1),(2,2),(3,2),(4,2),(6,2),(8,2))

    # x = 0
    # y = 0
    # z = 0
    # color = 0
    # size_x = 1
    # size_y = 1
    # piece_type = 0
    # orientation = False

    def __init__(self, piece_type, color=None, x=0, y=0, z=0, orientation=False):
        if color is None:                               # deoarece in python nu este posibila supraincarcea metodelor
            piece_model = deepcopy(piece_type)          # am ales aceasta abordare pentru a putea folosi constructorul
            self.piece_type = piece_model.piece_type    # in doua moduri. Odata cand se dau toti parametrii pentru
            self.color = piece_model.color              # a construi o piesa si a doua varianta verific daca am primit
            self.x = piece_model.x                      # doar un parametru inseamna ca am primit un model de piesa
            self.y = piece_model.y                      # pe care o voi clona
            self.z = piece_model.z
            self.orientation = piece_model.orientation
        else:
            self.piece_type = piece_type
            self.color = color
            self.x = x
            self.y = y
            self.z = z
            self.orientation = orientation
        self.set_size()

    def set_size(self):
        if self.orientation is False:
            self.size_x = self.PIECES_TYPES_INVERT[self.piece_type][0] # pentru a fi mai usor de lucrat am decis ca sa descriu
            self.size_y = self.PIECES_TYPES_INVERT[self.piece_type][1] # dimensiunea piesei in functie de orientarea ei, in felul 
        else:                                                          # acesta nu vom mai tine cont mereu de orientarea piesei
            self.size_x = self.PIECES_TYPES_INVERT[self.piece_type][1] # ci doar de dimensiunea acesteia
            self.size_y = self.PIECES_TYPES_INVERT[self.piece_type][0]

    def set_type_by_size(self, size_x, size_y):
        for i in range(len(self.PIECES_TYPES_INVERT)):
            if self.PIECES_TYPES_INVERT[i][0] == size_x and self.PIECES_TYPES_INVERT[i][1] == size_y:
                self.piece_type = i
                self.orientation = False
                self.set_size()
                break
            elif self.PIECES_TYPES_INVERT[i][0] == size_y and self.PIECES_TYPES_INVERT[i][1] == size_x:
                self.piece_type = i
                self.orientation = True
                self.set_size()
                break

    def get_regular_type(self):
        for i in range(len(self.PIECES_TYPES)):
            if self.size_x == self.PIECES_TYPES[i][1] and self.size_y == self.PIECES_TYPES[i][0]:
                return i
                
    def get_invert_type(self):
        for i in range(len(self.PIECES_TYPES_INVERT)):
            if self.size_x == self.PIECES_TYPES_INVERT[i][0] and self.size_y == self.PIECES_TYPES_INVERT[i][1]:
                return i

    def __str__(self):
        return "type=" + str(self.piece_type) + ", x=" + str(self.x) + ", y=" + str(self.y) + ", z=" + str(self.z) + \
               ", size_x=" + str(self.size_x) + ", size_y=" + str(self.size_y) + \
               ", orientation=" + str(self.orientation) + ", color=" + self.color

    def serialize(self):
        return str(self.piece_type) + ", " + str(self.y)  + ", " + str(self.z) + ", " + str(self.x) + \
               ", " + self.color + ", " + ("1\n" if self.orientation else "0\n")

    def export(self):
        txt = []
        for i in range(0, self.PIECES_TYPES[self.piece_type][0]):
            for j in range(0, self.PIECES_TYPES[self.piece_type][1]):
                if self.orientation is True:
                    txt.append((self.x+i, self.y+j, self.z))
                else:
                    txt.append((self.x+j, self.y+i, self.z))
        return txt

