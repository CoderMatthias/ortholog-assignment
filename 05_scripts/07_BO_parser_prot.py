#!/usr/bin/python3

import sys
import argparse

'''
This python script takes the blastp tab-deliminated data
and parses it to include unique hits and an additive bit score
Requires: blastp output, dict to convert FBpp#s to FBgn#s for both Dmen \
    and other D species
Usage:   python BO_parser_prot.py blastp_output.tsv \
    Dmel_FBpp_to_FBgn.tsv species_FBpp_to_FBgn.tsv
'''


def list_from_input(input_):
    '''Open a file and make a line list with it's contents'''
    with open(input_, 'r') as source_file:
        return [line.split('\t') for line in source_file.read().split('\n')
                if not line.startswith('#') and line.strip() != '']


def FBpp_to_FBgn_dict(dict_sys_argv):
    '''Converts the FBpp <-> FBgn file and to a dictionary'''
    LoL = list_from_input(dict_sys_argv)
    return {line[0]: line[1] for line in LoL}


def replace_FBpp_w_FBgn(pp_to_gn_dict, list_to_switch, column_to_switch):
    '''Replaces protein number (FBpp) with the gene number (FBgn)'''
    for line in list_to_switch:
        try:
            line[column_to_switch] = pp_to_gn_dict[line[column_to_switch]]
        except KeyError:
            print 'Missing Key:', line
    return list_to_switch


def make_blast_dict(blast_list):
    '''make blast results dict where key = gene and value contains bitscore'''
    blast_dict = {}
    for line in blast_list:
        key = ':'.join(line[:2])
        if key not in blast_dict:
            blast_dict[key] = [float(line[-1])]
        else:
            blast_dict[key].append(float(line[-1]))
    return [key.split(':') + [sum(value)]
            for key, value in blast_dict.iteritems()]


def write_output(name, list_to_write):
    '''Write an output file from a list'''
    output_file_name = \
        '../03_processed_input/04_{}_blastp_parsed.tsv'.format(name)
    print 'Output saved as: {}\n'.format(output_file_name)
    with open(output_file_name, 'w') as output_file:
        for line in sorted(list_to_write, key=lambda x: (x[0], -x[2])):
            output_line = '\t'.join(map(str, line))
            output_file.write('{}\n'.format(output_line))


def main(arg):
    print 'Running script {}'.format(sys.argv[0])
    blast_list = list_from_input(
        '../03_processed_input/{}_blastp.tsv'.format(arg.spec))
    blast_list = [line[1::-1] + [line[-1]] for line in blast_list]
    m_dict = FBpp_to_FBgn_dict(
        '../03_processed_input/02_{}_mel_dict.tsv'.format(arg.spec))
    s_dict = FBpp_to_FBgn_dict(
        '../03_processed_input/03_{}_dict.tsv'.format(arg.spec))
    blast_list = replace_FBpp_w_FBgn(m_dict, blast_list, 0)
    blast_list = replace_FBpp_w_FBgn(s_dict, blast_list, 1)
    output_list = make_blast_dict(blast_list)
    write_output(arg.spec, output_list)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Removes un-needed columns & sums bit values for same hits')
    parser.add_argument(
        'spec',
        action='store',
        help='D. specie')
    arg = parser.parse_args()
    main(arg)
