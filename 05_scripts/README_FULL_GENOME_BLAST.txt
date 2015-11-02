###############################################################################

                        FULL GENE BLAST INSTRUCTIONS
 
 Usage:  The purpose of the 'full gene blast' scripts is to assign a Dmel 
         ortholog for every gene of a related Drosophila species.  This 
         pipeline gives a rough ortholog assignment based on gene and protein
         blasts, but does not take synteny into account, differentiating it
         from the ortholog pipeline.  The output of 'FULL GENE BLAST' can be
         used in conjunction with the ortholog pipeline for gene duplication
         assignment.


 Requirements: mel_all_gene.fasta - fasta of all Dmel genes
               mel_all_prot.fasta - fasta of all Dmel proteins
               spec_all_gene.fasta - fasta of all specie of choice genes
               spec_all_prot.fasta - fasta of all specie of choice proteins
               species_list.txt - list of all species for which the scripts
                                  are run 
               fbgn_fbtr_fbpp.... - list of all fbgn# and corresponding fbpp#
               
        These file must be named accordingly to work.  For the spec_all_(gene
        or prot).fasta, spec would be replaced with the three-letter name
        abbreviation (eg: ana, ere, sec).  The species_list.txt has to have 
        each specie three-letter abbreviation on its own line.  See an example
        in the 06_test folder.


 Directions: Run the numbered commands below, waiting for jobs to finish
             before continuing onward.

  Load modules
   1. module load python/2.7.6
   2. module load blast

  Blast genes and proteins against Dmel database
   3. bsub -o ../00_logs/make_blast_db.%J.out python 00_mk_db_N_sp_list.py
   4. bsub python 01_parse_prot_fasta.py
   5. bsub python 02_spec_blast_to_mel.py
   6. bsub python 03_concatinate_blast_bits_into_blastp.py

  Assign orthologs based on blast results
   7. bsub -o ../00_logs/ortho_assign.%J.out bash ALL_ORTHO_ASSIGNMENT.sh 
         -this script wraps the 04-10 python scripts for all species on list
