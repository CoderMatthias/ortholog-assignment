#!/usr/bin/python

import sys
import subprocess


def open_fbgn_fbtr_fbpp_file():
    p = subprocess.Popen(['ls', '../02_raw_input'], stdout=subprocess.PIPE)
    with open('../02_raw_input/{}'
              .format([file for file in p.communicate()[0].split('\n')
                       if file.startswith('fbgn_fbtr_fbpp')][0]), 'r') as f:
        return [line.split('\t') for line in f.read().split('\n')
                if not line.startswith('#') and line]


def make_list_for_dict(list_):
    return [[line[2], line[0]] for line in list_ if len(line) == 3]


def write_output_file(list_):
    with open('../03_processed_input/02_{}_mel_dict.tsv'
              .format(sys.argv[1]), 'w') as f:
        for line in list_:
            f.write('{}\n'.format('\t'.join(line)))
        print 'Output saved as: {}\n'.format(f.name)

print 'Running script {}'.format(sys.argv[0]) 
line_list = open_fbgn_fbtr_fbpp_file()
output_list = make_list_for_dict(line_list)
write_output_file(output_list)
