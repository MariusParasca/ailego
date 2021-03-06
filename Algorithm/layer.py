from piece import Piece

class Layer:

    def __init__(self, pieces):
        self.pieces = pieces
        self.merged_pieces = []

    def orizontal_piece_match(self, p1, p2):
        if self.pieces[p1].x + self.pieces[p1].size_x != self.pieces[p2].x or\
        self.pieces[p1].color != self.pieces[p2].color or\
        self.pieces[p1].size_y > 2 or self.pieces[p2].size_y > 2:
            return -1

        width = self.pieces[p1].size_x + self.pieces[p2].size_x
        widths = [t[1] for t in Piece.PIECES_TYPES]

        if width in widths and self.pieces[p1].size_y == self.pieces[p1].size_y:
            return (width,self.pieces[p1].size_y)
        return -1

    def vertical_piece_match(self, p1, p2):
        if self.pieces[p1].y + self.pieces[p1].size_y != self.pieces[p2].y or\
        self.pieces[p1].color != self.pieces[p2].color or\
        self.pieces[p1].size_y > 2 or self.pieces[p2].size_y > 2:
            return -1

        height = self.pieces[p1].size_y + self.pieces[p2].size_y
        heights = [t[0] for t in Piece.PIECES_TYPES]

        if height in heights and self.pieces[p1].size_x == self.pieces[p2].size_x:
            return (self.pieces[p1].size_x,height)
        return -1

    def pieces_iteration(self):
        i=0
        self.pieces.sort(key = lambda p: (p.z, p.y, p.x))
        while i < len(self.pieces)-1:
            merged_piece_size = self.orizontal_piece_match(i,i+1)
            if merged_piece_size != -1:
                self.merge_pieces(i,i+1,merged_piece_size)
            else:
                i=i+1

        i=0
        self.pieces.sort(key = lambda p: (p.z, p.x, p.y))
        while i < len(self.pieces)-1:
            merged_piece_size = self.vertical_piece_match(i,i+1)
            if merged_piece_size != -1:
                self.merge_pieces(i,i+1,merged_piece_size)
            else:
                i=i+1

    def print_pieces(self):
        for i in range(len(self.pieces)):
            print(self.pieces[i])


    def orizontal_piece_match_invert(self, p1, p2):
        if self.pieces[p1].x + self.pieces[p1].size_x != self.pieces[p2].x or\
        self.pieces[p1].color != self.pieces[p2].color or\
        self.pieces[p1].size_x > 2 or self.pieces[p2].size_x > 2:
            return -1
        width = self.pieces[p1].size_x + self.pieces[p2].size_x
        widths = [t[0] for t in Piece.PIECES_TYPES]

        if width in widths and self.pieces[p1].size_y == self.pieces[p2].size_y:
            return (width,self.pieces[p1].size_y)
        return -1
        

    def vertical_piece_match_invert(self, p1, p2):
        if self.pieces[p1].y + self.pieces[p1].size_y != self.pieces[p2].y or\
        self.pieces[p1].color != self.pieces[p2].color or\
        self.pieces[p1].size_x > 2 or self.pieces[p2].size_x > 2:
            return -1

        height = self.pieces[p1].size_y + self.pieces[p2].size_y
        heights = [t[1] for t in Piece.PIECES_TYPES]

        if height in heights and self.pieces[p1].size_x == self.pieces[p2].size_x:
            return (self.pieces[p1].size_x,height)
        return -1

    def merge_pieces(self, p1, p2, size):
        self.pieces[p1].set_type_by_size(size[0], size[1])
        self.pieces.pop(p2)

    def pieces_iteration_invert(self):
        i=0
        self.pieces.sort(key = lambda p: (p.z, p.x, p.y))
        while i < len(self.pieces)-1:
            merged_piece_size = self.vertical_piece_match_invert(i,i+1)
            if merged_piece_size != -1:
                self.merge_pieces(i,i+1,merged_piece_size)
            else:
                i=i+1

        i=0
        self.pieces.sort(key = lambda p: (p.z, p.y, p.x))
        while i < len(self.pieces)-1:
            merged_piece_size = self.orizontal_piece_match_invert(i,i+1)
            if merged_piece_size != -1:
                self.merge_pieces(i,i+1,merged_piece_size)
            else:
                i=i+1

    
    def empty_inside_first(self):
        self.pieces.sort(key = lambda p: (p.z, p.y, p.x))
        useless_pieces = []
        i=-1
        while i<len(self.pieces)-1:
            i=i+1
            #for p in layer2.pieces:
            #    if p.x == self.pieces[i].x and p.y == self.pieces[i].y:
            #        continue
            
            if self.pieces[i].x%8 == 0 or\
                self.pieces[i].y%8 == 0 or\
                (self.pieces[i].x+1)%8 == 0 or\
                (self.pieces[i].y+1)%8 == 0:
                    continue
            j=0
            k=0
            while j<len(self.pieces):
                if self.pieces[i].x-2 == self.pieces[j].x and\
                self.pieces[i].y-2 == self.pieces[j].y:
                    k=k+1
                if self.pieces[i].x+2 == self.pieces[j].x and\
                self.pieces[i].y-2 == self.pieces[j].y:
                    k=k+1
                if self.pieces[i].x-2 == self.pieces[j].x and\
                self.pieces[i].y+2 == self.pieces[j].y:
                    k=k+1
                if self.pieces[i].x+2 == self.pieces[j].x and\
                self.pieces[i].y+2 == self.pieces[j].y:
                    k=k+1
                
                if self.pieces[i].x == self.pieces[j].x and\
                self.pieces[i].y+2 == self.pieces[j].y:
                    k=k+1
                
                if self.pieces[i].x+2 == self.pieces[j].x and\
                self.pieces[i].y == self.pieces[j].y:
                    k=k+1
                
                if self.pieces[i].x == self.pieces[j].x and\
                self.pieces[i].y-2 == self.pieces[j].y:
                    k=k+1
                
                if self.pieces[i].x-2 == self.pieces[j].x and\
                self.pieces[i].y == self.pieces[j].y:
                    k=k+1

                if k == 8:
                    useless_pieces.append(i)
                    break
                j=j+1
        
        while len(useless_pieces) > 0:
            del self.pieces[useless_pieces[0]]
            del useless_pieces[0]
            useless_pieces = [x-1 for x in useless_pieces]
        f=5
    
    def empty_inside(self,layer2):
        self.pieces.sort(key = lambda p: (p.z, p.y, p.x))
        useless_pieces = []
        i=-1
        while i<len(self.pieces)-1:
            i=i+1
            for p in layer2.pieces:
                if p.x == self.pieces[i].x and p.y == self.pieces[i].y:
                    continue
            
            if (self.pieces[i].x)%8 == 0 or\
                (self.pieces[i].y)%8 == 0 or\
                (self.pieces[i].x-1)%8 == 0 or\
                (self.pieces[i].y-1)%8 == 0:
                    continue
            j=0
            k=0
            while j<len(self.pieces):
                if self.pieces[i].x-2 == self.pieces[j].x and\
                self.pieces[i].y-2 == self.pieces[j].y:
                    k=k+1
                if self.pieces[i].x+2 == self.pieces[j].x and\
                self.pieces[i].y-2 == self.pieces[j].y:
                    k=k+1
                if self.pieces[i].x-2 == self.pieces[j].x and\
                self.pieces[i].y+2 == self.pieces[j].y:
                    k=k+1
                if self.pieces[i].x+2 == self.pieces[j].x and\
                self.pieces[i].y+2 == self.pieces[j].y:
                    k=k+1
                
                if self.pieces[i].x == self.pieces[j].x and\
                self.pieces[i].y+2 == self.pieces[j].y:
                    k=k+1
                
                if self.pieces[i].x+2 == self.pieces[j].x and\
                self.pieces[i].y == self.pieces[j].y:
                    k=k+1
                
                if self.pieces[i].x == self.pieces[j].x and\
                self.pieces[i].y-2 == self.pieces[j].y:
                    k=k+1
                
                if self.pieces[i].x-2 == self.pieces[j].x and\
                self.pieces[i].y == self.pieces[j].y:
                    k=k+1

                if k == 8:
                    useless_pieces.append(i)
                    break
                j=j+1
        
        while len(useless_pieces) > 0:
            del self.pieces[useless_pieces[0]]
            del useless_pieces[0]
            useless_pieces = [x-1 for x in useless_pieces]
        f=5
