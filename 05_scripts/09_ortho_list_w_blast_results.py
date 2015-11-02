#!/usr/bin/python3

import sys
import argparse


def logs(name):
    print 'Running script {}'.format(sys.argv[0])
    print 'Specie: {}'.format(name)


def source_file_dict(file_input):
    '''takes file and turns it into a list of lists (LoL)'''
    with open(file_input, 'r') as f:
        header = f.readline().strip().split('\t')
        return {line.split('\t')[1]: line.split('\t')
                for line in f.read().split('\n')
                if not line.startswith('#') and line.strip()}, header


def source_file_LoL(file_input):
    '''takes file and turns it into a list of lists (LoL)'''
    with open(file_input, 'r') as f:
        return [line.split('\t') for line in f.read().split('\n')
                if not line.startswith('#') and line.strip()]


def try_blast_files(blastn, blastp, numhits, list_, header):
    '''Check the blast input opts before passing to next function'''
    blasts = [blastn, blastp]
    for blast in blasts:
        list_, header = open_blast(list_, blast, numhits, header)
    return sorted(list_.values(), key=lambda x: x[1]), header


def open_blast(formatted_gene_dict, blast, num_of_hits_included, header):
    '''opens the blast parsed data and combines it with formatted data'''
    blast_LoL = source_file_LoL(blast)
    blast_LoL = [[item[:item.index('-')]
                  if '-' in item else item for item in line]
                 for line in blast_LoL]
    file_name = blast.split('/')[-1]
    blast_name = file_name.split('_')[2]
    header += [blast_name] * num_of_hits_included
    blast_dict = {}
    for line in blast_LoL:
        try:
            blast_dict[line[0]].append([line[1], float(line[2])])
        except KeyError:
            blast_dict[line[0]] = [[line[1], float(line[2])]]
    for key, value in formatted_gene_dict.iteritems():
        try:
            if len(blast_dict[key]) > num_of_hits_included:
                formatted_gene_dict[key] += sorted(blast_dict[key],
                                                   key=lambda x: -x[1])[
                                                       :num_of_hits_included]
            elif len(blast_dict[key]) == num_of_hits_included:
                formatted_gene_dict[key] += sorted(blast_dict[key],
                                                   key=lambda x: -x[1])
            else:
                value = sorted(blast_dict[key],
                               key=lambda x: -x[1]) + [''] * \
                    (num_of_hits_included - len(blast_dict[key]))
                formatted_gene_dict[key] += value
        except KeyError:
            value = [''] * num_of_hits_included
            formatted_gene_dict[key] += value
    return formatted_gene_dict, header


def write_output_file(list_to_write, name, header):
    with open('../03_processed_input/05_{}_blast_analyzed.tsv'
              .format(name), 'w+') as f:
        print 'Output saved as: {}\n'.format(f.name)
        f.write('{}\n'.format('\t'.join(header)))
        for line in list_to_write:
            output_line = [','.join(map(str, item)) if isinstance(item, list)
                           else item for item in line]
            output_line = "{}\n".format('\t'.join(output_line))
            f.write(output_line)


def main(arg):
    species_name = arg.species_name
    logs(species_name)
    mel_ORs, header = source_file_dict(
        '../03_processed_input/mel_genes.tsv')
    mel_ORs, header = try_blast_files(
        '../03_processed_input/01_{}_blastn_parsed.tsv'.format(species_name),
        '../03_processed_input/04_{}_blastp_parsed.tsv'.format(species_name),
        arg.numhits,
        mel_ORs,
        header
        )
    write_output_file(mel_ORs, species_name, header)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Combine the melanogaster blast results')
    parser.add_argument(
        'species_name',
        action='store',
        help='species_name'
        )
    parser.add_argument(
        '-nh',
        action='store',
        dest='numhits',
        default=5,
        type=int,
        help='top # of hits included in output file from each blast input'
        )
    arg = parser.parse_args()
    main(arg)
