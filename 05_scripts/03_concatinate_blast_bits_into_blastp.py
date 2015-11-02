#!/usr/bin/python2.7

import os
import subprocess


def get_species_list():
    with open('../02_raw_input/species_list.txt', 'r') as f:
        return [item for item in f.read().split('\n') if item]


def concatinate_blast_bits(list_):
    p = subprocess.Popen(['ls', '../03_processed_input'],
                         stdout=subprocess.PIPE)
    file_list = [item for item in p.communicate()[0].split('\n')]
    for spec in list_:
        prot_bit_files = [file for file in file_list
                          if spec in file and 'fasta_blasted' in file]
        for file in prot_bit_files:
            os.system('cat ../03_processed_input/{} >> \
                      ../03_processed_input/{}_blastp.tsv'.format(file, spec))
            os.system('rm ../03_processed_input/{}'.format(file))


def remove_prot_bits_from_raw_input():
    os.system('rm ../02_raw_input/*protbit.fasta')


def main():
    spec_list = get_species_list()
    concatinate_blast_bits(spec_list)
    remove_prot_bits_from_raw_input()

main()
