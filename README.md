#Ortholog Assignment Pipeline
This script takes a fasta file containing all genes and proteins of a species and determines the *Drosophila melanogaster* ortholog.  The assigning of the ortholog is based on both a gene blast and a protein blast, with a higher emphasis on the gene blast.

##Usage
The purpose of the 'full gene blast' scripts is to assign a *Drosophila melanogaster* ortholog for every gene of a related *Drosophila* species.  This pipeline gives a rough ortholog assignment based on gene and protein blasts, but does not take synteny into account, differentiating it from the ortholog pipeline.  The output of 'FULL GENE BLAST' can be used in conjunction with the ortholog pipeline for gene duplication assignment.

##Requirements
###Software
python v2.7.6
blast v2.2.31

###Files
