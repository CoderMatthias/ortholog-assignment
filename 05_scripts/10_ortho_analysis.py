#!/usr/bin/python3

import sys
import argparse
import re


def logs():
    print 'Running script {}'.format(sys.argv[0])
    print 'Check 00_logs folder to see output for this script\n\n'
    sys.stdout = open('../00_logs/10_{}_analyzed.out'.format(sys.argv[1]), 'w')
    print 'Input file was:', sys.argv[1]
    print


def source_file_list(input_, header='null'):
    '''takes file and turns it into a list of lists (LoL)'''
    with open(input_, 'r') as f:
        header = f.readline().strip().split('\t')
        return [line.split('\t') for line in f.read().split('\n')
                if line.strip() and not line.startswith('#')], header


def add_ortho_column(list_, header):
    '''Adds a column for the species ortholog to be recorded'''
    print '\n{}'.format('-' * 25)
    print 'Total OR genes= {}\n'.format(len(list_))
    header.insert(header.index('FBgn_number') + 1, 'ortholog')
    for line in list_:
        line.insert(header.index('ortholog'), 'null')
    return list_, header


def parse_ambig_and_unambig(ortho_list, header):
    unambig, ambig = [], []
    header.append('blastn_match')
    ortho_list, unambig = one_matching_nucl_blast(ortho_list,
                                                  unambig,
                                                  header.index('blastn'))
    ortho_list, unambig, ambig = one_main_blastn_match(ortho_list,
                                                       unambig,
                                                       ambig,
                                                       header.index('blastn'))
    header.append('blastp_match')
    unambig, ambig = one_main_blastp_match(ortho_list + ambig,
                                           unambig,
                                           header.index('blastp'))
    return unambig, ambig, header


def one_matching_nucl_blast(ortholog_list, unambig_list, index):
    trim_ortho_list = []
    for line in ortholog_list:
        if line[index].strip() and not line[index + 1].strip() \
                and float(line[index].split(',')[1]) > 200:
            line[line.index('null')] = line[index].split(',')[0]
            unambig_list.append(line)
        else:
            trim_ortho_list.append(line)
    print
    print 'Only one blastn match assessment'
    print 'unambiguous= {}'.format(len(unambig_list))
    print 'remain orthos= {}'.format(len(trim_ortho_list))
    return trim_ortho_list, unambig_list


def one_main_blastn_match(ortholog_list, unambig_list, ambig_list, index):
    trim_ortho_list = []
    for line in ortholog_list:
        try:
            top_hit = line[index].split(',')[1]
            compare = line[index + 1].split(',')[1]
            if float(compare) < float(top_hit) * 0.6 and float(top_hit) > 200:
                line[line.index('null')] = line[index].split(',')[0]
                unambig_list.append(line)
            else:
                ambig_list.append(line)
        except IndexError:
            trim_ortho_list.append(line)
    print
    print 'Only one major blastn match assessment'
    print 'unambiguous= {}'.format(len(unambig_list))
    print 'ambiguous= {}'.format(len(ambig_list))
    print 'remain orthos= {}'.format(len(trim_ortho_list))
    return trim_ortho_list, unambig_list, ambig_list


def one_main_blastp_match(ortholog_list, unambig_list, index):
    ambig = []
    for line in ortholog_list:
        try:
            top_hit = line[index].split(',')[1]
            compare = line[index + 1].split(',')[1]
            if float(compare) < float(top_hit) * 0.6 and float(top_hit) > 200:
                line[line.index('null')] = line[index].split(',')[0]
                unambig_list.append(line)
            else:
                ambig.append(line)
        except:
            ambig.append(line)
    print
    print 'Only one major blastp match assessment'
    print 'unambiguous= {}'.format(len(unambig_list))
    print 'ambiguous= {}'.format(len(ambig))
    return unambig_list, ambig


def no_same_orthos(list_, header):
    index = header.index('ortholog')
    dict_ = {line[1]: line for line in list_}
    list_ = sorted(list_, key=lambda x: x[index])
    assigned_orthos = [line[index] for line in list_]
    for i, line in enumerate(list_):
        if i == 0:
            pass
        elif list_[i][index] == list_[i-1][index] and line[index] != 'null':
            count, gene, same_orthos = -1, list_[i][index], []
            while list_[i + count][index] == gene:
                same_orthos.append(list_[i + count])
                count += 1
            same_orthos = sort_same_orthos_list(same_orthos, header)
            for line in same_orthos[1:]:
                possibles = [item for item in line[index + 1:] if item != ''
                             and item != 'yes' and item != 'no']
                for item in possibles:
                    if item.split(',')[0] not in assigned_orthos:
                        line[index] = item.split(',')[0]
                        dict_[line[0]] = line
                        assigned_orthos.append(item.split(',')[0])
                        break
                else:
                    line[index] = 'null'
                    dict_[line[0]] = line
    return [dict_[key] for key in dict_.keys()]


def sort_same_orthos_list(same_orthos, header):
    blast_list = list(sorted(set([item for item in header
                                  if 'blast' in item and 'match' not in item])))
    for i, item in enumerate(blast_list[:]):
        blast_list[i] = sorted([line for line in same_orthos
                                if line[header.index(item)] != ''],
                               key=lambda x: float(x[
                                   header.index(item)].split(',')[1]),
                               reverse=True)
    blast_list = [item for sublist in blast_list for item in sublist]
    sorted_list, remove_redund = [], []
    for line in blast_list:
        if line not in remove_redund:
            sorted_list.append(line)
            remove_redund.append(line)
    return sorted_list


def blast_match_ortholog_check(list_, header):
    print '{}\n'.format('-' * 25)
    match_colm = [item[:item.index('_match')] for item in header
                  if 'match' in item]
    for item in match_colm:
        for line in list_:
            if line[header.index(item)] != '':
                bit = line[header.index(item)].split(',')[0]
                ortho = line[header.index('ortholog')]
                if '.' in bit:
                    bit = bit.split('.')[0]
                if '.' in ortho:
                    ortho = ortho.split('.')[0]
                if bit == ortho: 
                    line.append('yes')
                else:
                    print line[header.index('ortholog')]
                    print bit
                    print '----------------'
                    line.append('no')
            else:
                line.append('no')
    return list_


def fill_in_null_orthos(list_, header):
    blast_colm = list(sorted(set([item for item in header
                                  if 'blast' in item and 'match' not in item])))
    for line in list_:
        if line[header.index('ortholog')] == 'null':
            for item in blast_colm:
                if line[header.index(item)] != '':
                    line[header.index('ortholog')] = \
                        line[header.index(item)].split(',')[0]
                    break
    return list_


def check_blastn_and_blastp_match(unambiguous, header):
    print
    print 'unambig where blastn and blastp top hit don\'t match'
    print '{:20}\t{:15}\t{:15}'.format('', 'blastn', 'blastp')
    count = 0
    assigned_orthos = []
    ibnm, ibn = header.index('blastn_match'), header.index('blastn')
    ibpm, ibp = header.index('blastp_match'), header.index('blastp')
    for line in unambiguous:
        print line[ibnm], line[ibpm]
        print
        if line[ibnm] != line[ibpm] \
                and line[ibn].strip() != '' \
                and line[ibp].strip() != '':
            print '{:20}\t{:15}\t{:15}'.format(line[0], line[ibn], line[ibp])
            count += 1
        elif line[ibnm] == 'yes' and line[ibpm] == 'yes':
            assigned_orthos.append(line)
    print '# of unmatched', count
    return assigned_orthos


def write_output_file(spec_name, list_to_write, header):
    '''writes the output file and prints name of the saved output file'''
    output_file_name = '../04_final_output/{}_full_ortho.tsv'.format(spec_name)
    with open(output_file_name, 'w+') as output_file:
        print "Output saved as: {}".format(output_file.name)
        header = '\t'.join(header)
        output_file.write('{}\n'.format(header))
        for line in list_to_write:
            for item in line:
                if type(item) == list:
                    item = ','.join(map(str, item))
            output_line = '{}\n'.format('\t'.join(map(str, line)))
            output_file.write(output_line)


def main(arg):
    spec_name = sys.argv[1]
    logs()
    OR_orthos, header = source_file_list(
        '../03_processed_input/05_{}_blast_analyzed.tsv'.format(sys.argv[1]))
    OR_orthos, header = add_ortho_column(OR_orthos, header)
    unambiguous, ambiguous, header = parse_ambig_and_unambig(OR_orthos, header)

    analyzed = unambiguous + ambiguous
    analyzed = fill_in_null_orthos(analyzed, header)
    analyzed = no_same_orthos(analyzed, header)
    analyzed = blast_match_ortholog_check(analyzed, header)

    assigned_orthos = check_blastn_and_blastp_match(unambiguous, header)
    assigned_orthos = unambiguous
    write_output_file(spec_name, assigned_orthos, header)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Analyzed the combined blast results')
    parser.add_argument(
        'input_',
        action='store',
        help='File of all the blast results lined up with D.mel ORs')
    arg = parser.parse_args()
    main(arg)
