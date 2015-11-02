#!/usr/bin/python2.7

import sys


def source_file_LoL():
    '''takes file and turns it into a list of lists (LoL)'''
    with open('../02_raw_input/mel_all_gene.fasta', 'r') as source_file:
        header = ['#genes', 'FBgn_number']
        list_ = [line for line in source_file.read().split('\n')
                     if line.startswith('>')]
    return list_, header


def parse_needed_info(list_):
    return [[line[line.index('name=')+5:line.index('; dbxref=')],
             line[1:line.index(' type')]] for line in list_]


def write_output_file(list_, header):
    '''Write an output file of given name'''
    output_name = '../03_processed_input/mel_genes.tsv'
    print 'Output saved as: {}\n'.format(output_name)
    with open(output_name, 'w+') as output_file:
        list_.insert(0, header)
        for line in list_:
            output_line = '{}\n'.format('\t'.join(line))
            output_file.write(output_line)


print 'Running script {}'.format(sys.argv[0])
genes_list, header = source_file_LoL()
parsed_list = parse_needed_info(genes_list)
write_output_file(parsed_list, header)

