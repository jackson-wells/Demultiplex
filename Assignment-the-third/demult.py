#!/usr/bin/python

import argparse
# import bioinfo

class Statistics:
    recordCount = 0
    averageQualityScore = 0.0
    percentage = 0.0
    gcContent = 0.0

def get_args():
    parser = argparse.ArgumentParser(description="Demultiplexer")
    parser.add_argument("-1", help="R1 file", type=str, required=True)
    parser.add_argument("-2", help="R2 file", type=str, required=True)
    parser.add_argument("-3", help="R3 file", type=str, required=True)
    parser.add_argument("-4", help="R4 file", type=str, required=True)
    parser.add_argument("-q", help="Quality score cutoff", type=int, default=30)
    parser.add_argument("-i", help="valid index file", type=str, required=True)
    return parser.parse_args()

def getIndexes(fileName : str) -> dict:
	'''Takes in file name, returns a dictionary of indexes'''
    
	return {}

def getReverseComplement(sequence : str) -> str:
	'''Takes in a sequence, returns the reverse complement of input sequence'''

	return ""

def averageQuality(sequence : str) -> float:
	'''Takes in sequence, returns average quality score'''

	return 0.0

def outputLocationExists(location : str) -> bool:
	'''Takes in an output directory location, return True if directory exists.
		Return False if the directory does not exist'''

	return True

def handleInputs(args : object) -> None:
	'''Takes in argparse.Namespace object, validates input flags. Throws execptions
		when: files are not found or not readable, output directory exists, Q-score
		cutoff is negative or 0'''
    # Process arguements {

# 	if output directory exists{
# 		# throw exception
# 	}
# 	else { 
# 		# create output directory
# 	}
		
# 	if input files not readable or dont exist {
# 		# throw exception
# 	}
# }
	return

# Take in command line arguements 
args = get_args()
handleInputs(args)

# Declare global variables for stat reporting 

matched = Statistics
hopped = Statistics
unknown = Statistics
lowQuality = Statistics
totalReadCount = 0

# Get indexes from valid index file
validIndex = getIndexes(args.i)


# Loop over R1, R2, R3, R4 {
# Concat index-pair to header lines

# 	if R2 index or R3 index contain "N":
		# Write R1 and R4 records to low-quality/unknown output file
	# else:
		# get reverse complement of R3 index sequence
		
		# if R2 and R3-RC index sequences match:
		# 	if matched sequence is a valid index:
		# 		if R1 and R4 sequences pass Q-score cutoff:			
					# Write R1 and R4 records to valid output file
				# else:
					# Write R1 and R4 records to low-quality/unknown output file
			# else:
				# Write R1 and R4 records to low-quality/unknown output file
		# else:
			# Write R1 and R4 records to index-hopping file

