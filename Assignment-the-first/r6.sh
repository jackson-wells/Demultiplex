#!/bin/bash
#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --cpus-per-task=8
#SBATCH --job-name=bash
#SBATCH --nodes=1
#SBATCH --time=5-00:00:00
#SBATCH --error=logs/r6_%j.txt
#SBATCH --output=logs/r6_%j.txt 


/usr/bin/time -v zcat /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz | sed -n '2~4p' | grep -c "N" 