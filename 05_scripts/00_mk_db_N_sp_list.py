#!/usr/bin/python2

'''
Makes list of all Drosophila species out of list of files, submits makeblastdb
for the .fasta files
'''

import subprocess
import os


def get_list_of_all_files():
    '''Puts filenames of files in 02_raw_input into a list'''
    p = subprocess.Popen(['ls', '../02_raw_input'], stdout=subprocess.PIPE)
    return [item for item in p.communicate()[0].split('\n')]


def submit_makeblastdbs(list_):
    '''Makes a blast db from mel_all_gene and mel_all_prot to blast to'''
    for file_ in list_:
        if 'all_gene' in file_ and file_.endswith('.fasta') and 'mel' in file_:
            os.system('makeblastdb -in ../02_raw_input/{} \
                      -dbtype nucl -parse_seqids'.format(file_))
        elif 'all_prot' in file_ and file_.endswith('.fasta') and 'mel' in file_:
            os.system('makeblastdb -in ../02_raw_input/{} \
                      -dbtype prot -parse_seqids'.format(file_))


def make_species_list(list_):
    '''makes list of all species whose files are in 02_raw_input & puts in list'''
    with open('../02_raw_input/species_list.txt', 'w') as f:
        species_list = list(set([file_.split('_')[0]
                                 for file_ in list_ if file_]))
        species_list = [spec for spec in species_list
                        if spec != 'mel' and spec != 'fbgn' and spec != 'species']
        f.write('\n'.join(species_list))
        print
        print
        print 'Species in species_list.txt:'
        print '\n'.join(species_list)

list_ = get_list_of_all_files()
submit_makeblastdbs(list_)
make_species_list(list_)
