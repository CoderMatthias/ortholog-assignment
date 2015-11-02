#!/usr/bin/python2.7

import os
import subprocess


def get_species_list():
    with open('../02_raw_input/species_list.txt', 'r') as f:
        return [item for item in f.read().split('\n') if item and item != 'mel']


def run_blastn_for_all_species(list_):
    for spec in list_:
        os.system('bsub \
                  -J {0}_blastn blastn \
                  -db ../02_raw_input/mel_all_gene.fasta \
                  -query ../02_raw_input/{0}_all_gene.fasta \
                  -out ../03_processed_input/{0}_blastn.tsv \
                  -outfmt 6'.format(spec))


def run_blastp_for_all_species(list_):
    p = subprocess.Popen(['ls', '../02_raw_input'], stdout=subprocess.PIPE)
    file_list = [item for item in p.communicate()[0].split('\n')]
    for spec in list_:
        prot_bit_list = [prot_bit for prot_bit in file_list if spec in prot_bit
                         and 'protbit' in prot_bit]
        for prot_bit in prot_bit_list:
            os.system('bsub \
                      -J {0}_blastp blastp \
                      -db ../02_raw_input/mel_all_prot.fasta \
                      -query ../02_raw_input/{1} \
                      -out ../03_processed_input/{1}_blasted \
                      -outfmt 6'.format(spec, prot_bit))


def run_blastx_for_all_species(list_):
    p = subprocess.Popen(['ls', '../02_raw_input'], stdout=subprocess.PIPE)
    file_list = [item for item in p.communicate()[0].split('\n')]
    for spec in list_:
        cds_bit_list = [cds_bit for cds_bit in file_list if spec in cds_bit
                         and 'cdsbit' in cds_bit]
        for prot_bit in prot_bit_list:
            os.system('bsub \
                      -J {0}_blastp blastp \
                      -db ../02_raw_input/mel_all_prot.fasta \
                      -query ../02_raw_input/{1} \
                      -out ../03_processed_input/{1}_blasted \
                      -outfmt 6'.format(spec, prot_bit))


def main():
    spec_list = get_species_list()
    run_blastn_for_all_species(spec_list)
    run_blastp_for_all_species(spec_list)

main()
