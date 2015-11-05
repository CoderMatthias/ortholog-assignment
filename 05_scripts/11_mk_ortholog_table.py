#!/usr/bin/python2

import argparse


def open_input(input_):
    '''takes file and turns it into a list of lists (LoL)'''
    with open(input_, 'r') as f:
        header = f.readline().strip().split('\t')
        if '/' in f.name:
            sp_name = f.name.split('/')[-1].split('_')[0]
        else: 
            sp_name = f.name.split('_')[0]
        line_list = [line for line in f.read().split('\n')
                     if line.strip() and not line.startswith('#')]
    return [line.split('\t') for line in line_list], header, sp_name


def only_genes_of_interest(ref_in, goi):
    with open(goi, 'r') as f:
        ls = f.read().split('\n')
        return [line for line in ref_in if line[0] in ls]


def make_FBgn_dict(list_, header):
    return {line[header.index('FBgn_number')]: line for line in list_}


def make_ortho_dicts(orthos_inputs):
    orthos_di = []
    for ortho in orthos_inputs:
        list_, header, name = open_input(ortho)
        orthos_di.append([name, make_ortho_dict(list_, header)])
    return orthos_di


def make_ortho_dict(list_, header):
    return {line[header.index('FBgn_number')]: line[header.index('ortholog')]
            for line in list_}


def mel_w_species_dict(input_dict, ortho_list_dict, input_header):
    for specie in ortho_list_dict:
        input_header.append(specie[0])
        for key, value in input_dict.iteritems():
            try:
                value.append(specie[1][key])
            except KeyError:
                value.append('null')
    return input_dict, input_header


def write_output(output_di, header, output_name):
    '''Write an output file of given name'''
    print 'Output saved as:', output_name
    with open(output_name, 'w+') as output_file:
        output_file.write('{}\n'.format('\t'.join(header)))
        for value in sorted(output_di.values(),
                            key=lambda x: x[header.index('FBgn_number')]):
            output_line = '{}\n'.format('\t'.join(value))
            output_file.write(output_line)


def main(arg):
    input_, header = open_input(arg.temp)[0:2]
    input_ = only_genes_of_interest(input_, arg.goi)
    input_di = make_FBgn_dict(input_, header)
    ortho_list_di = make_ortho_dicts(arg.orth_files)
    final_outs, header = mel_w_species_dict(input_di, ortho_list_di, header)
    write_output(final_outs, header, arg.out_name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='takes outputs from ortholog pipeline script \
        and combines into an ortholog table')
    parser.add_argument(
        'goi',
        action='store',
        help='list of genes of interest, each on own line')
    parser.add_argument(
        '-i',
        action='store',
        dest='temp',
        help='template file containing the mel genes and FBgn#s')
    parser.add_argument(
        '-a',
        nargs='+',
        action='store',
        dest='orth_files',
        help='all of the final outputs from the ortholog pipeline script')
    parser.add_argument(
        '-o',
        action='store',
        dest='out_name',
        default='mel_ortholog_list.tsv',
        help='user defined output name, defaults to mel_ortholog_list.tsv')
    arg = parser.parse_args()
    main(arg)
