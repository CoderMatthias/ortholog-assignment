#Ortholog Assignment Pipeline
This script takes a fasta files containing the sequences for all of the genes and proteins of a species and predicts the *Drosophila melanogaster* ortholog.  The assigning of the ortholog is based on both a gene blast and a protein blast, with a higher emphasis on the gene blast.

##Usage
The purpose of the 'full gene blast' scripts is to assign a *Drosophila melanogaster* ortholog for every gene of a related *Drosophila* species.  This pipeline gives a rough ortholog assignment based on gene and protein blasts, but does not take synteny into account, differentiating it from the ortholog pipeline.

##Requirements
###Software
`python v2.7.6`  
`blast v2.2.31`

###Files
`mel_all_gene.fasta` - fasta of all *Drosophila melanogaster* genes  
`mel_all_prot.fasta` - fasta of all *Drosophila melanogaster* proteins  
`spec_all_gene.fasta` - fasta of all 'specie of choice' genes  
`spec_all_prot.fasta` - fasta of all 'specie of choice' proteins  
`fbgn_fbtr_fbpp_....` - list of all fbgn#'s and corresponding fbpp#'s

The `mel_all_gene.fasta, mel_all_prot.fasta, and fbgn_fbtr_fbpp...` can be downloaded from the [geneomes](ftp://ftp.flybase.net/genomes/Drosophila_melanogaster/ "Dmel genes and translations") and [releases](ftp://ftp.flybase.net/releases/ "fbgn_fbtr_fbpp...") ftp section on FlyBase. Go to the appropriate release (likely the most recent) and navigate to the appropriate files.

These file must be named accordingly to work.  For the spec_all_(gene or prot).fasta, spec would be replaced with a name abbreviation (eg: ana, Dere1, sec).  The species_list.txt has to have the corresponding name abbreviation on its own line.  See an example in the 06_test folder.

##Directions
These directions are specifically for running this pipeline on the UNC computing clusters and will likely have to be modified if working in a different computing environment.  

Run the numbered commands below, waiting for jobs to finish before continuing onward.  
Load modules  
1. `module load python/2.7.6`  
2. `module load blast/2.2.31`  

Blast genes and proteins against *Drosophila melanogaster* database  
3. `bsub -o ../00_logs/make_blast_db.%J.out python 00_mk_db_N_sp_list.py`  
4. `bsub python 01_parse_prot_fasta.py`  
5. `bsub python 02_spec_blast_to_mel.py`  
6. `bsub python 03_concatinate_blast_bits_into_blastp.py`  

Assign orthologs based on blast results  
7. `bsub -o ../00_logs/ortho_assign.%J.out bash ALL_ORTHO_ASSIGNMENT.sh`
  + This bash script wraps the 04-10 python scripts to quicken the process.  

##Weaknesses
This program gives a prediction of the orthologs.  However, in its current itteration, this program is unable to identify gene duplication events.  The duplicated gene the deviates most from the *Drosophila melanogaster* sequence will be discarded.

##Detailed description of calling
This work flows combines the results of a blastn and a blastp of a species against a *Drosophila melanogaster* blast databases.  For each gene, the blastn and blastp results are combined and checked against a set of parameters, and if met, is considered an ortholog.  The ortholog parameters are as follows (in order of importance):  
1. There is only one blastn result for the gene, and the blastn bit score is > 200.  
2. There is more than one blastn result, but 60% of the top hit's bit score is greater than the next closest.  
3. There is more than one blastp result, but 60% of the top hit's bit score is greater than the next closest, and the top hit's bit score is greater than 200.  
