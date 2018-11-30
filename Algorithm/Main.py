import os.path
from FileOperations import importData

if __name__ == '__main__':
    input_pieces = importData(os.path.join(os.path.dirname(os.path.realpath(__file__)),'input.csv'))
    print(input_pieces)