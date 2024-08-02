## Problem

Lane of sequencing run files, hot off the sequencer. The files are disorganized and not currently interpretable 
by humans nor bioinformatic software. We must determine levels of index-swapping and unknown index-pairs, 
before and after quality filtration. The files must be demultiplexed to accomplish this. 

## Inputs

1. R1 fastQ file, containing read sequences 
2. R2 fastQ file, containing indexes that correspond to the R1 file
3. R3 fastQ file, containing indexes that correspond to the R4 file
4. R4 fastQ file, containing read sequences 
5. Valid index text file

## Outputs 

#### Required Statistics 

1. Number of read-pairs with properly matched indexes (per index-pair)
2. Number of read pairs with index-hopping observed
3. Number of read-pairs with unknown index(es)

#### Files

1. R1/R2 fastQ files, one file per matching index pair
2. R1/R2 fastQ files, for non-matching index-pairs
3. R1/R2 fastQ files, for instances where one or both index reads are unknown or are low quality

#### Optional Statistics

1. Average sequence quality for each output file
2. Total size of each output file (NT count)
3. Number of input reads
4. Average sequence length for each output file
5. GC Content for matching read files
6. Percentage of matched read-pairs
7. Percentage of index-hopped read-pairs
8. Percentage of unknown/low quality read-pairs

### Potential Functions

```python
def getIndexes(fileName : str) -> dict:
	'''Takes in file name, returns a dictionary of indexes'''

	return tempDict
Input: "./indexes.txt"
Expected output: indexes
```

```python
def getReverseComplement(sequence : str) -> str:
	'''Takes in a sequence, returns the reverse complement of input sequence'''

	return tempSeq
Input: "AC"
Expected output: "TG"
```

```python
def averageQuality(sequence : str) -> float:
	'''Takes in sequence, returns average quality score'''

	return tempScore
Input: "I"
Expected output: 40.0
```

```python
def outputLocationExists(location : str) -> boolean:
	'''Takes in an output directory location, return True if directory exists.
		Return False if the directory does not exist'''

	return tempFlag
Input: "/output"
Expected output: "False"
```

```python
def handleInputs(args : object) -> None:
	'''Takes in argparse.Namespace object, validates input flags. Throws execptions
		when: files are not found or not readable, output directory exists, Q-score
		cutoff is negative or 0'''

	return
Input: args
Expected output: None or Exception
```
## Additional Needs

1. An input flag for users to specify a sequence quality score cutoff
2. A default value for sequence quality score cutoff
3. Input flags for fastQ files (R1,R2,R3,R4)
4. An input flag for valid index file
5. Indexes from the R3 file will need to be reverse complemented
6. Output records MUST contain concatenated index-pair string in the header line
7. Input flag for output directory

## Good To Know

- Quality filtering applies to index and read sequences
- Input fastQ files are ordered identically, meaning we can iterate over all 4 simultaneously 
- Valid index file contains 24 records, meaning 48 matched index pair files will be output
- May need to create output directory

## Pseudocode

```python

Take in command line arguements 

Process arguements {

	if output directory exists{
		# throw exception
	}
	else { 
		# create output directory
	}
		
	if input files not readable or dont exist {
		# throw exception
	}
}


Declare global variables for stat reporting 

# Matched index record count
# Matched index average quality score
# Matched index percentage
# GC content

# Index-hopping record count
# Index-hopping average quality score
# Index-hopping percentage

# Unknown index record count
# Unknown index average quality score
# Unknown index percentage

# Low quality record count
# Low quality average quality score
# Low quality percentage

# Total record count 

Get indexes from valid index file

Loop over R1, R2, R3, R4 {

	if R2 index or R3 index contain "N" {

		# Concat index-pair to header lines
		
		# Write R1 and R4 records to low-quality/unknown output file
	}
	else {

		# get reverse complement of R3 index sequence
		
		if R2 and R3-RC index sequences match {

			if matched sequence is a valid index (contained in valid index file) {

				if R1 and R4 sequences pass Q-score cutoff {

					# Concat index-pair to header lines
					
					# Write R1 and R4 records to valid output file
				}
				else {

					# Concat index-pair to header lines
					
					# Write R1 and R4 records to low-quality/unknown output file
				}
			}		
			else {

				# Concat index-pair to header lines
				
				# Write R1 and R4 records to low-quality/unknown output file
			}	
		}
		else {

			# Concat index-pair to header lines
			
			# Write R1 and R4 records to index-hopping file
		}
	}
}

```
