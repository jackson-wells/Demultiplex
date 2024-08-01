
#!/usr/bin/env python

# Author: Jackson Wells <jwel@uoregon.edu>

# Check out some Python module resources:
#   - https://docs.python.org/3/tutorial/modules.html
#   - https://python101.pythonlibrary.org/chapter36_creating_modules_and_packages.html
#   - and many more: https://www.google.com/search?q=how+to+write+a+python+module

'''This module is a collection of useful bioinformatics functions
written during the Bioinformatics and Genomics Program coursework.
You should update this docstring to reflect what you would like it to say'''

__version__ = "0.3"         # Read way more about versioning here:
                            # https://en.wikipedia.org/wiki/Software_versioning

DNA_bases = {"A","T","C","G","N"}
RNA_bases = {"A","U","C","G","N"}

def convert_phred(letter: str) -> int:
    """Converts a single character into a phred score"""
    return (ord(letter)-33)

def qual_score(phred_score: str) -> float:
    """Computes the average quality score for a string"""
    sum = 0
    for letter in list(phred_score):
        sum += convert_phred(letter)
    return (sum/len(phred_score))

def validate_base_seq(seq: str, RNAflag=False) -> bool:
    '''This function takes a string. Returns True if string is composed
    of only As, Ts (or Us if RNAflag), Gs, Cs. False otherwise. Case insensitive.'''
    seqUpper = seq.upper()
    temp = set(seqUpper.split())
    if (DNA_bases.intersection(temp) and not RNAflag) or (RNA_bases.intersection(temp) and RNAflag):
        return True
    else:
        return False

def gc_content(DNA: str) -> float:
    '''Returns GC content of a DNA or RNA sequence as a decimal between 0 and 1.'''
    DNA = DNA.upper()
    if not validate_base_seq(DNA):
        raise Exception("Invalid sequence supplied")
    else:
        return (DNA.count("G")+DNA.count("C"))/len(DNA)

def calc_median(lst: list) -> float:
    '''Given a sorted list, returns the median value of the list'''
    if len(lst) % 2 == 0:
        return ((lst[(len(lst)//2)]-lst[(len(lst)//2)-1])/2)+lst[(len(lst)//2)-1]
    else:
        return lst[(len(lst)//2)]

def oneline_fasta(file,outFile):
    '''takes in an input fasta, writes to output to file name passed in as second parameter, concatenates all sequences onto one line'''
    with open(file,"r") as fh:
        with open(outFile,"w") as oFh:
            first = True                    #boolean to capture base case (first sequence in fasta)
            for line in fh:
                if first:       #Don't add additional new line 
                    header = line.strip('\n')
                    oFh.write(header + "\n")
                    first = False
                elif not line.find(">"):        #do add additional new line 
                    header = line.strip('\n')
                    oFh.write("\n" + header + "\n")
                else:                           #concatenate sequence lines
                    oFh.write(line.strip('\n'))

if __name__ == "__main__":
    # write tests for functions above, Leslie has already populated some tests for convert_phred
    # These tests are run when you execute this file directly (instead of importing it)
    assert convert_phred("I") == 40, "wrong phred score for 'I'"
    assert convert_phred("C") == 34, "wrong phred score for 'C'"
    assert convert_phred("2") == 17, "wrong phred score for '2'"
    assert convert_phred("@") == 31, "wrong phred score for '@'"
    assert convert_phred("$") == 3, "wrong phred score for '$'"
    assert qual_score("CATCGATACGACTACTG") == 38.11764705882353, "Incorrect average quality score"
    assert qual_score("BBBBBBBBBB>>&>>0002/BBB?BABBBB##############################") == 15.216666666666667, "Incorrect average quality score"
    assert qual_score("1") == 16.0, "Incorrect average quality score"
    assert qual_score("******") == 9.0, "Incorrect average quality score"
    assert qual_score("unitTest") == 75.0, "Incorrect average quality score"
    assert validate_base_seq("ACGTGACGTACGACTTACTGNNACT") == True, "Invalid sequence supplied"
    assert validate_base_seq("CATCGATACGACTACTG") == True, "Invalid sequence supplied"
    assert validate_base_seq("CAGUCGAUCGAUCGttttUnnn") == True, "Invalid sequence supplied"
    assert validate_base_seq("12345") == False, "Invalid sequence supplied"
    assert validate_base_seq("fajsdhfl") == False, "Invalid sequence supplied"
    assert gc_content("ACCGACTACGACTACTACG") == 0.5263157894736842, "Incorrect GC content value returned"
    assert gc_content("UGACTACGTACGACTACGCAGGTTGACGCAT") == 0.5161290322580645, "Incorrect GC content value returned"
    assert gc_content("#!$@#%") == 0.0, "Incorrect GC content value returned"
    assert gc_content("123") == 0.0, "Incorrect GC content value returned"
    assert gc_content("GCGCGCGCGCGCGCGCGCGCGCG") == 1.0, "Incorrect GC content value returned"
    assert calc_median([1,2,3,4,5]) == 3, "Incorrect median for list"
    assert calc_median([2,6,7]) == 6, "Incorrect median for list"
    assert calc_median([2,2,2,2,2,2,2,2]) == 2, "Incorrect median for list"
    assert calc_median([1,4,101,1000]) == 52.5, "Incorrect median for list"
    assert calc_median([1,2,3,4,5,6,7,8]) == 4.5, "Incorrect median for list"
    
    print("Your convert_phred function is working! Nice job")
