import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Script to encrypt text using the rc4 cipher.')

    parser.add_argument('input_file', metavar='input_file', type=str, nargs='+',
                        help='input file')
    parser.add_argument('output_file', metavar='output_file', type=str, nargs='+',
                        help='output file')
    args = parser.parse_args()
    args_dict = dict()
    args_dict['input_file'] = args.input_file[0]
    args_dict['output_file'] = args.output_file[0]
    return args_dict


def get_key(p):
    passphrase_len = len(p)
    S = []
    for i in range(256):
        S.append(i)

    j = 0
    for i in range(256):
        j = (j + S[i] + p[i % passphrase_len]) % 256
        S[i], S[j] = S[j], S[i]

    return S


def get_stream(pasp):
    S = get_key(pasp)
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256

        S[i], S[j] = S[j], S[i]
        W = S[(S[i] + S[j]) % 256]
        yield W


def main():
    args = parse_args()
    input_file = args['input_file']
    output_file = args['output_file']

    f = open(input_file, "r")
    input_txt = [ord(k) for k in f.read()]
    f.close()

    passphrase = [ord(k) for k in input("Enter passphrase: ")]

    stream = get_stream(passphrase)

    res = []
    for k in input_txt:
        x = (k ^ next(stream))
        res.append(x)

    res_str = ''.join([chr(i) for i in res])

    f = open(output_file, "w")
    f.write(res_str)
    f.close()
    print("Encoding complete!")


if __name__ == '__main__':
    main()
