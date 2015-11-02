#!/usr/bin/python3

'''
Splits the large protein fasta into multiple smaller fastas (1000 proteins in
length).  Only does this for the protein fasta, as the protein blast takes MUCH
longer than the gene blast and the gene blast finishes in a reasonable amount
of time, even with the full gene fasta.
'''

import argparse


def get_species_list():
    with open('../02_raw_input/species_list.txt', 'r') as f:
        return [item for item in f.read().split('\n') if item]


def make_into_bits(species_list):
    for s in species_list:
        try:
            with open('../02_raw_input/{}_all_prot.fasta'.format(s), 'r') as f:
                line_list = [line for line in f.read().split('\n') if line]
                type = 'prot'
        except IOError:
            with open('../02_raw_input/{}_all_CDS.fasta'.format(s), 'r') as f:
                line_list = [line for line in f.read().split('\n') if line]
                type = 'CDS'
        count, start, bit_number = -1, 0, 1
        for i, line in enumerate(line_list):
            if line.startswith('>'):
                count += 1
            if count == 1000:
                ident_bit = '{0:02d}'.format(bit_number)
                with open('../02_raw_input/{}_{}_{}bit.fasta'
                          .format(s, ident_bit, type), 'w') as f:
                    f.write('\n'.join(line_list[start:i]))
                count, start = 0, i
                bit_number += 1
        else:
            with open('../02_raw_input/{}_{}_{}bit.fasta'.format(s, bit_number, type), 'w') as f:
                f.write('\n'.join(line_list[start:]))


def main(arg):
    species_list = get_species_list()
    make_into_bits(species_list)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Parse big fasta into multiple fastas, 1000 gene in length')
    arg = parser.parse_args()
    main(arg)
