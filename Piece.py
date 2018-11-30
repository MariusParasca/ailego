from copy import deepcopy

class Piece:
    PIECES_TYPES = ((1,1),(1,2),(1,3),(1,4),(1,6),(1,8),(2,2),(2,3),(2,4),(2,6),(2,8))

    x = 0
    y = 0
    z = 0
    color = 0
    size_x = 1
    size_y = 1
    piece_type = 0
    orientation = False

    def __init__(self, piece_type, color=None, x=0, y=0, z=0, orientation=False):
        if color == None:                               # deoarece in python nu este posibila supraincarcea metodelor
            piece_model = deepcopy(piece_type)          # am ales aceasta abordare pentru a putea folosi constructorul
            self.piece_type = piece_model.piece_type    # in doua moduri. Odata cand se dau toti parametrii pentru
            self.color = piece_model.color              # a construi o piesa si a doua varianta verific daca am primit
            self.x = piece_model.x                      # doar in parametru inseamna ca am primit un model de piesa
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

    def setSize(self):
        if self.orientation == False:
            self.size_x = self.PIECES_TYPES[self.piece_type][0] # pentru a fi mai usor de lucrat am decis ca sa descriu
            self.size_y = self.PIECES_TYPES[self.piece_type][1] # dimensiunea piesei in functie de orientarea ei, in felul 
        else:                                                   # acesta nu vom mai tine cont mereu de orientarea piesei
            self.size_x = self.PIECES_TYPES[self.piece_type][1] # ci doar de dimensiunea acesteia
            self.size_y = self.PIECES_TYPES[self.piece_type][0]
    
    def getPieceType(self):
        if self.orientation == False:
            for i in range(len(self.PIECES_TYPES)):
                if self.x == self.PIECES_TYPES[i][0] and self.y == self.PIECES_TYPES[i][1]:
                    return i
        else:
            for i in range(len(self.PIECES_TYPES)):
                if self.x == self.PIECES_TYPES[i][1] and self.y == self.PIECES_TYPES[i][0]:
                    return i
    
    