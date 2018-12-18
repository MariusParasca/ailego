from sys import argv


if (len(argv) <= 1):
    print("usage: 'python input_interface_to_input_alg.py <file_path>")
    raise SystemExit


with open('input.csv', 'w') as f:
    with open(argv[1]) as fd:
        for line in fd.readlines():
            data = line.split(',')
            f.write(data[1] + ',' + data[2] + ',' +
                    data[3] + ',' + data[4] + '\n')

                    
print("Result written in input.csv")
