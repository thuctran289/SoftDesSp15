# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:24:42 2014

@author: Thuc Tran

"""

# you may find it useful to import these variables (although you are not required to use them)
from amino_acids import aa, codons, aa_table
import random
from load import load_seq

def shuffle_string(s):
    """ Shuffles the characters in the input string
        NOTE: this is a helper function, you do not have to modify this in any way """
    return ''.join(random.sample(s,len(s)))

### YOU WILL START YOUR IMPLEMENTATION FROM HERE DOWN ###


def get_complement(nucleotide):
    """ Returns the complementary nucleotide

        nucleotide: a nucleotide (A, C, G, or T) represented as a string
        returns: the complementary nucleotide
    >>> get_complement('A')
    'T'
    >>> get_complement('C')
    'G'
    >>> get_complement('G')
    'C'
    >>> get_complement('T')
    'A'
    >>> get_complement(' ')
    ''

    The goal of the above is to cover all/most of the major cases for getting 
    the complement nucleotide.
    """
    if nucleotide=='A': #don't need these parens
        return 'T'
    elif (nucleotide =='T'): #ditto
        return 'A'
    elif (nucleotide =='G'):
        return 'C'
    elif (nucleotide =='C'):
        return 'G'
    else:
        return 'Nucleotide not found'   #nice error checking, but you want to have a descriptive error message

def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
        sequence
    
        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    >>> get_reverse_complement("ATGCCCGCTTT")
    'AAAGCGGGCAT'
    >>> get_reverse_complement("CCGCGTTCA")
    'TGAACGCGG'
    >>> get_reverse_complement("AAATTTGGGCCC")
    'GGGCCCAAATTT'
    >>> get_reverse_complement("")
    ''
    >>> get_reverse_complement("1231")
    ''
    
    The above ought to cover most of the cases for the reverse complement
    Added another case to have a little bit more isolated case.
    Another for if it gets an input with nothing in it
    And another for bad input. Assumption is that bad input will be ignored.
    
    ^Nicely done, I appreciate the additional information. Your comments are also very nice
    """
    #Reverses the DNA
    reverse_DNA = dna[::-1]
    #Creates a reverse_dna Complement string
    reverse_DNA_complement = ''
    #Iterates through each character in reverseDNA and adds the complement to reverse complement
    for char in reverse_DNA:
        reverse_DNA_complement += get_complement(char)
    #returns reverse_dna_complement
    return reverse_DNA_complement

def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start codon and returns
        the sequence up to but not including the first in frame stop codon.  If there
        is no in frame stop codon, returns the whole string.
        
        T.Tran's Note: regarding this structure, my understanding is that it will require that the first three nucleotides to be ATG, if not it
        should return nothing. If the assumption is correct for the first three characters being ATG, it will stop at either the first stop codon
        on an element of three, or otherwise return all of it. 

        dna: a DNA sequence
        returns: the open reading frame represented as a string
    >>> rest_of_ORF("ATGTGAA")
    'ATG'
    >>> rest_of_ORF("ATGAGATAGG")
    'ATGAGA'

    This simulates the simplest case of start and stop with whatever codons inbetween

    >>> rest_of_ORF("ATGATGA")
    'ATGATGA'

    >>> rest_of_ORF("ATGAGA")
    'ATGAGA'

    This emulates the case where a stop codon is off base

    >>> rest_of_ORF("ATGCATGAATGTAGATAGATGTGCCC")
    'ATGCATGAATGTAGA'
    >>> rest_of_ORF("ATGTGATGA")
    'ATG'
    >>> rest_of_ORF("ATGAGATGATGA")
    'ATGAGA'

    This describes the cases where there are multiple end codons in the same codon.

    """
    #checks to find first stop codon.
    for index in range(0, len(dna), 3):
        if(dna[index:index+3] == "TAG" or dna[index:index+3] == "TAA" or dna[index:index+3] == "TGA"):
            return dna[0:index]
    return dna


def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence and returns
        them as a list.  This function should only find ORFs that are in the default
        frame of the sequence (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_oneframe("ATGCATGAATGTAGATAGATGTGCCC")
    ['ATGCATGAATGTAGA', 'ATGTGCCC']
    >>> find_all_ORFs_oneframe("ATGCATGAATGTAG")
    ['ATGCATGAATGTAG']"""
    
    ORFList = []
    #Start positions on valid parts of the dna code (i.e. mod3==0)
    index = 0
    while(index<len(dna)): #while loops are cool, but for loops avoids infinite looping.
        if(dna[index:index+3]=="ATG"):
            new_ORF = rest_of_ORF(dna[index:])
            index += len(new_ORF)
            ORFList.append(new_ORF)
        index+=3
    return ORFList


def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in all 3
        possible frames and returns them as a list.  By non-nested we mean that if an
        ORF occurs entirely within another ORF and they are both in the same frame,
        it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs

    >>> find_all_ORFs("ATGCATGAATGTAG")
    ['ATGCATGAATGTAG', 'ATGAATGTAG', 'ATG']
    >>> find_all_ORFs("AATGCATGAATGTAG")
    ['ATG', 'ATGCATGAATGTAG', 'ATGAATGTAG']
    >>> find_all_ORFs("AAATGCATGAATGTAG")
    ['ATGAATGTAG', 'ATG', 'ATGCATGAATGTAG']
    """
    all_ORFs =[]
    
    #You should make the below a loop. This works, but is clunky
    dnaSet0 = find_all_ORFs_oneframe(dna[0:])
    dnaSet1 = find_all_ORFs_oneframe(dna[1:])
    dnaSet2 = find_all_ORFs_oneframe(dna[2:])
    if len(dnaSet0) != 0: #you don't need to error check this
        all_ORFs.extend(dnaSet0)
    if len(dnaSet1) != 0:
        all_ORFs.extend(dnaSet1)
    if len(dnaSet2) != 0:
        all_ORFs.extend(dnaSet2)

    return all_ORFs

def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG', 'ATGCTACATTCGCAT']
    """
    all_ORFs = []
    forwardStrand = find_all_ORFs(dna)
    if len(forwardStrand) !=0:
        all_ORFs.extend(forwardStrand)
    backwardStrand =find_all_ORFs(get_reverse_complement(dna))
    if len(backwardStrand) !=0:
        all_ORFs.extend(backwardStrand)

    return all_ORFs



def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string
    >>> longest_ORF("ATGCGAATGTAGCATCAAA")
    'ATGCTACATTCGCAT'
    """
    all_ORFs = find_all_ORFs_both_strands(dna)
    if len(all_ORFs) == 0:
        return ""
    maxLength = max(all_ORFs, key = len)
    return maxLength

def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """
    longestFoundORF = ""
    for x in range(num_trials): #range assumes starting from 0
        dna1 = shuffle_string(dna)
        if (len(longest_ORF(dna1))>len(longestFoundORF)):
            longestFoundORF = longest_ORF(dna1)
    return len(longestFoundORF)

def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).
        
        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment

        >>> coding_strand_to_AA("ATGCGA")
        'MR'
        >>> coding_strand_to_AA("ATGCCCGCTTT")
        'MPA'
    """
    totalLength = len(dna)/3*3 #Isn't this literally just len(dna)?
    index = 0
    proteinString  = ''
    while index<totalLength:
        proteinString += aa_table[dna[index:index+3]]
        index+=3
    return proteinString


def gene_finder(dna):
    """ Returns the amino acid sequences that are likely coded by the specified dna
        
        dna: a DNA sequence
        threshold: the minimum length of the ORF for it to be considered a valid
                   gene.
        returns: a list of all amino acid sequences whose ORFs meet the minimum
                 length specified.
    """    
    long_NC_ORF = longest_ORF_noncoding(dna,1500) #this variable should be named 'threshold' or something more
                                                #descriptive. Clarity is important
    long_C_ORF = [x for x in find_all_ORFs_both_strands(dna) if len(x)>long_NC_ORF]
    amino_acid_list = [coding_strand_to_AA(x) for x in long_C_ORF]
    return amino_acid_list



if __name__ == "__main__":
    import doctest
    doctest.testmod()
    dna = load_seq("./data/X73525.fa")

    genes =  gene_finder(dna)
    print genes
