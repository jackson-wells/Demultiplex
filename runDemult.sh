#!/bin/bash
#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --cpus-per-task=16
#SBATCH --job-name=demultiplex
#SBATCH --nodes=1
#SBATCH --time=5-00:00:00
#SBATCH --error=logs/demult_%j.txt
#SBATCH --output=logs/demult_%j.txt

conda activate plots

/usr/bin/time -v python /projects/bgmp/jwel/bioinfo/Demultiplex/Assignment-the-third/demult.py \
    -r1 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz \
    -r2 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz \
    -r3 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz \
    -r4 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz \
    -o /projects/bgmp/jwel/bioinfo/Demultiplex/Assignment-the-third/output/ \
    -i /projects/bgmp/shared/2017_sequencing/indexes.txt \
    -q 30
