#!/usr/bin/python3

import argparse


def line_list_from_input(input_):
    '''Open a file and make a line list with it's contents'''
    with open('../03_processed_input/{}_blastn.tsv'.format(input_), 'r') as f:
        return [line.split('\t') for line in f.read().split('\n') if line]


def make_blast_dict(blast_list):
    '''make dict of blast results where key=gene and value contains bitscore'''
    blast_dict = {}
    for line in blast_list:
        if line[0] not in blast_dict:
            blast_dict[line[0]] = [float(line[1])]
        else:
            blast_dict[line[0]].append(float(line[1]))
    return blast_dict


def write_output(name, list_to_write):
    '''writes the output file and prints name of the saved output file'''
    out_file_name = '../03_processed_input/01_{}_blastn_parsed.tsv'.format(name)
    with open(out_file_name, 'w+') as output_file:
        print "Output saved as: {}\n".format(output_file.name)
        for line in sorted(list_to_write, key=lambda x: (x[0], -x[2])):
            output_line = '{}\n'.format('\t'.join(map(str, line)))
            output_file.write(output_line)


def main(arg):
    print 'Running script 04_BO_parser_nuc.py'
    blastn_LoL = line_list_from_input(arg.input_)
    blastn_LoL = [[':'.join(line[1::-1])] + [line[-1]] for line in blastn_LoL]
    blast_dict = make_blast_dict(blastn_LoL)
    output_list = [key.split(':') + [sum(value)]
                   for key, value in blast_dict.iteritems()]
    write_output(arg.input_, output_list)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Remove unneeded columns and sums bit values for same hits')
    parser.add_argument(
        'input_',
        action='store',
        help='blastn output file, called (specie)_blastn.tsv'
        )
    arg = parser.parse_args()
    main(arg)
