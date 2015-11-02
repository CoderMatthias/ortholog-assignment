#!/bin/usr/python2

###############################################################################
#
# This wraps the second part of the full geneome blast scripts into one 
# pipeline. The first four scripts (through 03_concat...) will still need to be
# run alone, waiting until each script is completed before continuing on.
#
# Required files in 02_raw_input:  mel_all_genes.fasta
#                                  mel_all_prots.fasta
#                                  spec_all_gene.fasta
#                                  spec_all_prot.fasta
#                                  fbgn_fbtr_fbpp(...).tsv (get from flybase
#                                  species_list.txt (more below)
#
# The species_list.txt should include the three letter abbreviation for the
# Drosophila species for each species to be run through the pipeline. Each
# species should be on its own line. For example:     ana
#                                                     ere
#                                                     sec
#
#
###############################################################################

for spec in $(cat ../02_raw_input/species_list.txt); do
  python 04_BO_parser_nuc.py $spec
  python 05_make_mel_dict.py $spec
  python 06_make_dict.py $spec
  python 07_BO_parser_prot.py $spec
  python 08_make_mel_gene_file.py
  python 09_ortho_list_w_blast_results.py $spec
  python 10_ortho_analysis.py $spec
done
