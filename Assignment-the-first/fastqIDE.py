#!/usr/bin/python

import argparse
import bioinfo
import gzip
import os
import matplotlib.pyplot as plt

def get_args():
    parser = argparse.ArgumentParser(description="IDE")
    parser.add_argument("-f", help="Name of input file", type=str, required=True)
    parser.add_argument("-r", help="R#", type=str, required=True)
    return parser.parse_args()

args = get_args()
file = str(args.f)
r = str(args.r)
file = os.path.realpath(file)

if r == "1" or r == "4":
    all_qscores = [0] * 101
    avg_qscores = [0.0] * 101
    bins = 101
else:
    all_qscores = [0] * 8
    avg_qscores = [0.0] * 8
    bins=8

lineCount = 0
recordCount = 0
with gzip.open(file,"rt") as fh:
    for lineCount,line in enumerate(fh):
        line = line.strip('\n')
        if lineCount % 4 == 3: #if qscore line
            i = 0
            recordCount += 1
            for letter in line:
                all_qscores[i] += bioinfo.convert_phred(str(letter))
                i += 1


for i in range(len(all_qscores)):
    avg_qscores[i] = all_qscores[i]/recordCount

plt.bar(range(bins),avg_qscores)
plt.ylabel("Q Score")
plt.xlabel("Position in Read (0-based)")
plt.xlim(0,bins-1)
plt.ylim(0,41)
plt.title("Distribution of Average Q-score per base in R" + r + " file")
plt.savefig("R" + r + "_hist.png")