#!/bin/bash
#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --cpus-per-task=16
#SBATCH --job-name=python
#SBATCH --nodes=1
#SBATCH --time=5-00:00:00
#SBATCH --error=logs/r3_%j.txt
#SBATCH --output=logs/r3_%j.txt 

conda activate plots

/usr/bin/time -v python /projects/bgmp/jwel/bioinfo/Demultiplex/Assignment-the-first/fastqIDE.py -r "3" -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz
