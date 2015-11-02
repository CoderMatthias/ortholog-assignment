#!/usr/bin/python

import sys


def source_file_gene_list():
    in_file = '../02_raw_input/{}_all_prot.fasta'.format(sys.argv[1])
    with open(in_file, 'r') as source_file:
        return [line[1:] for line in source_file.read().strip().split('\n')
                if line.startswith('>')]


def make_dict(list_):
    out_list = []
    for line in list_:
        try:
            FBpp = line[:line.index(' type=')]
            FBgn = line[line.index('parent=')+7:line.index('parent=')+18]
            out_list.append([FBpp, FBgn])
        except ValueError:
            out_list.append([line, line])
    return ['\t'.join(line) for line in out_list]


def write_output_file(list_):
    out_file = '../03_processed_input/03_{}_dict.tsv'.format(sys.argv[1])
    with open(out_file, 'w+') as f:
        print 'Output saved as: {}\n'.format(out_file)
        f.write('\n'.join(list_))


def main():
    print 'Running script {}'.format(sys.argv[0])
    gene_name_list = source_file_gene_list()
    out_list = make_dict(gene_name_list)
    write_output_file(out_list)

if __name__ == '__main__':
    main()
