#!/usr/bin/python

import argparse
from typing import TextIO
import bioinfo
import os
import gzip
# import matplotlib.pyplot as plt

def get_args():
    parser = argparse.ArgumentParser(description="Demultiplexer")
    parser.add_argument("-r1", help="R1 file", type=str, required=True)
    parser.add_argument("-r2", help="R2 file", type=str, required=True)
    parser.add_argument("-r3", help="R3 file", type=str, required=True)
    parser.add_argument("-r4", help="R4 file", type=str, required=True)
    parser.add_argument("-q", help="Quality score cutoff", type=int, default=30)
    parser.add_argument("-i", help="valid index file", type=str, required=True)
    parser.add_argument("-o", help="output directory", type=str, required=True)
    return parser.parse_args()

def getIndexes(file : str) -> dict:
	'''Takes in file name, returns a dictionary of indexes'''
	tempDict = {}
	with open(file,"r") as fh:
		for line in fh:
			if "sample" in line:
				continue
			index = line.strip('\n').split('\t')
			tempDict[index[4]] = [index[0],index[1],int(0)]
	return tempDict

def getReverseComplement(sequence : str) -> str:
	'''Takes in a sequence, returns the reverse complement of input sequence'''
	tempString = ""
	for base in sequence:
		if base == "A":
			tempString = tempString + "T"
		elif base == "C":
			tempString = tempString + "G"
		elif base == "G":
			tempString = tempString + "C"
		elif base == "T":
			tempString = tempString + "A"
		elif base == "N":
			tempString = tempString + "N"
	return tempString[::-1]

def outputLocationExists(location : str) -> bool:
	'''Takes in an output directory location, return True if directory exists.
		Return False if the directory does not exist'''
	if os.path.exists(location):
		return True
	else:
		return False

def handleInputs(args : argparse.Namespace) -> None:
	'''Takes in argparse.Namespace object, validates input flags. Throws execptions
		when: files are not found or not readable, output directory exists, Q-score
		cutoff is negative or 0'''

	if outputLocationExists(args.o):
		raise Exception("Output directory already exists!")
	else:
		os.mkdir(args.o)
		
	if args.q <= 0:
		raise Exception("Quality score cutoff cannot be at or below 0!")
	
	if not os.path.isfile(args.r1):
		raise Exception("R1 file cannot be found!")
	
	if not os.path.isfile(args.r2):
		raise Exception("R2 file cannot be found!")
	
	if not os.path.isfile(args.r3):
		raise Exception("R3 file cannot be found!")
	
	if not os.path.isfile(args.r4):
		raise Exception("R4 file cannot be found!")
	
	return

def writeToFile(fh : TextIO, header : str, sequence : str, score : str) -> None:
	fh.write(header + "\n" + sequence + "\n+\n" + score + "\n")
	return

def incrementSampleRecordCount(valueList : list) -> list:
	valueList[2] += 1
	return valueList

# Take in command line arguements 
args = get_args()
handleInputs(args)

# Declare global variables for stat reporting 

matchedRecordCount = 0
matchedAverageQualityScore = 0.0
matchedPercentage = 0.0
matchedGcContent = 0.0

hoppedRecordCount = 0
hoppedAverageQualityScore = 0.0
hoppedPercentage = 0.0
hoppedGcContent = 0.0
hoppedForwardFh = open(args.o + "hopped_R1.fq", "a")
hoppedReverseFh = open(args.o + "hopped_R2.fq", "a")

unknownRecordCount = 0
unknownAverageQualityScore = 0.0
unknownPercentage = 0.0
unknownGcContent = 0.0
unknownForwardFh = open(args.o + "unknown_R1.fq", "a")
unknownReverseFh = open(args.o + "unknown_R2.fq", "a")

lowQualityRecordCount = 0
lowQualityAverageQualityScore = 0.0
lowQualityPercentage = 0.0
lowQualityGcContent = 0.0
lowQualityForwardFh = open(args.o + "lowQ_R1.fq", "a")
lowQualityReverseFh = open(args.o + "lowQ_R2.fq", "a")

totalReadCount = 0

# Get indexes from valid index file
validIndexes = getIndexes(args.i)

recordCount = 0

matchedForwardFileHandles = {}
matchedReverseFileHandles = {}


for value in validIndexes:
	valueList = validIndexes[value]
	fileName1 = args.o + valueList[1] + "_" + valueList[0] + "_R1.fq"
	fileName2 = args.o + valueList[1] + "_" + valueList[0] + "_R2.fq"
	fh1 = open(fileName1,"a")
	fh2 = open(fileName2,"a")
	matchedForwardFileHandles[value] = fh1
	matchedReverseFileHandles[value] = fh2

nIndexCount = 0

with gzip.open(args.r1,"rt") as fh1, gzip.open(args.r2,"rt") as fh2, gzip.open(args.r3,"rt") as fh3, gzip.open(args.r4,"rt") as fh4:
	while True:
		header1 = fh1.readline().strip()

		if header1 == '':
			break

		header1 = str(header1)
		header2 = str(fh2.readline().strip())
		header3 = str(fh3.readline().strip())
		header4 = str(fh4.readline().strip())

		seq1 = str(fh1.readline().strip())
		seq2 = str(fh2.readline().strip())
		seq3 = str(fh3.readline().strip())
		seq4 = str(fh4.readline().strip())

		sep1 = str(fh1.readline().strip())
		sep2 = str(fh2.readline().strip())
		sep3 = str(fh3.readline().strip())
		sep4 = str(fh4.readline().strip())

		score1 = str(fh1.readline().strip())
		score2 = str(fh2.readline().strip())
		score3 = str(fh3.readline().strip())
		score4 = str(fh4.readline().strip())
	
		
		header1 = header1 + " " + seq2 + "-" + seq3 
		header4 = header4 + " " + seq2 + "-" + seq3 
		recordCount += 1
		q1 = bioinfo.qual_score(seq1)
		q2 = bioinfo.qual_score(seq4)

		if 'N' in seq2 or 'N' in seq3:
			nIndexCount += 1
			lowQualityRecordCount += 1
			lowQualityGcContent += bioinfo.gc_content(seq1) + bioinfo.gc_content(seq4)
			lowQualityAverageQualityScore += q1 + q2
			writeToFile(lowQualityForwardFh, header1, seq1, score1)
			writeToFile(lowQualityReverseFh, header4, seq4, score4)
		else:
			if seq2 == getReverseComplement(seq3):
				if seq2 in validIndexes:			
					if q1 >= args.q and q2 >= args.q:
						matchedRecordCount += 1
						matchedGcContent += bioinfo.gc_content(seq1) + bioinfo.gc_content(seq4)
						matchedAverageQualityScore += q1 + q2
						validIndexes[seq2] = incrementSampleRecordCount(validIndexes[seq2])
						writeToFile(matchedForwardFileHandles[seq2], header1, seq1, score1)
						writeToFile(matchedReverseFileHandles[seq2], header4, seq4, score4)
					else:
						lowQualityRecordCount += 1
						lowQualityGcContent += bioinfo.gc_content(seq1) + bioinfo.gc_content(seq4)
						lowQualityAverageQualityScore += q1 + q2
						writeToFile(lowQualityForwardFh, header1, seq1, score1)
						writeToFile(lowQualityReverseFh, header4, seq4, score4)
				else:
					unknownRecordCount += 1
					unknownGcContent += bioinfo.gc_content(seq1) + bioinfo.gc_content(seq4)
					unknownAverageQualityScore += q1 + q2
					writeToFile(unknownForwardFh, header1, seq1, score1)
					writeToFile(unknownReverseFh, header4, seq4, score4)
			else:
				hoppedRecordCount += 1
				hoppedGcContent += bioinfo.gc_content(seq1) + bioinfo.gc_content(seq4)
				hoppedAverageQualityScore += q1 + q2
				writeToFile(hoppedForwardFh, header1, seq1, score1)
				writeToFile(hoppedReverseFh, header4, seq4, score4)

		
for value in validIndexes:
	matchedForwardFileHandles[value].close()
	matchedReverseFileHandles[value].close()

hoppedForwardFh.close()
hoppedReverseFh.close()

unknownForwardFh.close()
unknownReverseFh.close()

lowQualityForwardFh.close()
lowQualityReverseFh.close()

print("Total Reads:\t\t\t\t\t\t\t\t\t" + str(recordCount))

print("\nMatched Reads:\t\t\t\t\t\t\t\t\t" + str(matchedRecordCount))
matchedAverageQualityScore = "{:.2f}".format(matchedAverageQualityScore/(matchedRecordCount*2))
print("Average quality score of matched reads:\t\t\t" + str(matchedAverageQualityScore))
matchedPercentage = "{:.2f}".format((matchedRecordCount/recordCount)*100)
print("Percentage of matched reads:\t\t\t\t\t" + str(matchedPercentage) + "%")
matchedGcContent = "{:.2f}".format((matchedGcContent/(matchedRecordCount*2))*100)
print("Average GC content of matched reads:\t\t\t" + str(matchedGcContent) + "%")

print("\nIndex-hopped Reads:\t\t\t\t\t\t\t\t" + str(hoppedRecordCount))
hoppedAverageQualityScore = "{:.2f}".format(hoppedAverageQualityScore/(hoppedRecordCount*2))
print("Average quality score of index-hopped reads:\t" + str(matchedAverageQualityScore))
hoppedPercentage = "{:.2f}".format((hoppedRecordCount/recordCount)*100)
print("Percentage of index-hopped reads:\t\t\t\t" + str(hoppedPercentage) + "%")
hoppedGcContent = "{:.2f}".format((hoppedGcContent/(hoppedRecordCount*2))*100)
print("Average GC content of index-hopped reads:\t\t" + str(hoppedGcContent) + "%")

print("\nUnknown index Reads:\t\t\t\t\t\t\t" + str(unknownRecordCount))
unknownAverageQualityScore = "{:.2f}".format(unknownAverageQualityScore/(unknownRecordCount*2))
print("Average quality score of unknown index reads:\t" + str(matchedAverageQualityScore))
unknownPercentage = "{:.2f}".format((unknownRecordCount/recordCount)*100)
print("Percentage of unknown index reads:\t\t\t\t" + str(unknownPercentage) + "%")
unknownGcContent = "{:.2f}".format((unknownGcContent/(unknownRecordCount*2))*100)
print("Average GC content of unknown index reads:\t\t" + str(unknownGcContent) + "%")

print("\nLow quality Reads:\t\t\t\t\t\t\t\t" + str((lowQualityRecordCount-nIndexCount)))
print("Reads with 'N' in their index:\t\t\t\t\t" + str(nIndexCount))
lowQualityAverageQualityScore = "{:.2f}".format(lowQualityAverageQualityScore/(lowQualityRecordCount*2))
print("Average quality score of low quality reads:\t\t" + str(matchedAverageQualityScore))
lowQualityPercentage = "{:.2f}".format((lowQualityRecordCount/recordCount)*100)
print("Percentage of loq quality reads:\t\t\t\t" + str(lowQualityPercentage) + "%")
lowQualityGcContent = "{:.2f}".format((lowQualityGcContent/(lowQualityRecordCount*2))*100)
print("Average GC content of low quality reads:\t\t" + str(lowQualityGcContent) + "%\n")

print("Group\tSample\tMatched Read %")
for value in validIndexes:
	valueList = validIndexes[value]
	tempPercent = "{:.2f}".format((int(valueList[2])/recordCount)*100)
	print(valueList[0] + "\t" + valueList[1] + "\t" + tempPercent + "%")

print("\n\n\n")