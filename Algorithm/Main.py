import os.path
from file_operations import import_data

if __name__ == '__main__':
    input_pieces = import_data(os.path.join(os.path.dirname(os.path.realpath(__file__)),'input.csv'))
    print(input_pieces)