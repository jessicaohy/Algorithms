# Jessica Oh Hui Yu

import sys

from suffixTree import *


def LCPtraverseEdge(txt, pat, index, start, end, matchCount):
    """
    This function checks through all the characters on one edge and counts the number of matches between txt and pat.
    :param txt:
    :param pat:
    :param index:
    :param start:
    :param end:
    :param matchCount:
    :return: -1, 0 or 1
    complexity: worst case = O(N), where N is the number of characters in txt
    """

    i = start

    while i <= end and index != len(pat):       # while there is character on the edge
        # if they are not matching
        if txt[i] != pat[index]:
            return -1, matchCount               # mismatch

        matchCount += 1                         # increase number of match counts by 1
        # check next character on the edge
        i += 1
        index += 1

    # if checked all char on pat, the whole thing matches
    if index == len(pat):
        return 1, matchCount                    # match

    return 0, matchCount                        # continue to match other edges



def LCPtraverseDown(node, txt, pat, index, matchCount):
    """
    This function traverses the tree and check whether there is a match between txt and pat using other recursion function.
    :param node:
    :param txt:
    :param pat:
    :param index:
    :param matchCount:
    :return:-1 or 1, matchCount
    complexity: worst case = O(N), where N is the number of characters in txt
    """

    # if node does not exist
    if node == None:
        return -1, matchCount               # mismatch

    checkMatch = -1

    # if is not root
    if node.startIndex != -1:

        # check characters on edge
        checkMatch, matchCount = LCPtraverseEdge(txt, pat, index, node.startIndex, node.endIndex, matchCount)

        # if mismatch
        if checkMatch == -1:                # mismatch
            return -1, matchCount

        # if whole thing match
        if checkMatch == 1:                 # match
            return 1, matchCount

    # if is not root
    if node.startIndex != -1:
        index = index + (node.endIndex - node.startIndex + 1)

    patLetter = pat[index]
    patLetterIndex = ord(patLetter)
    # if there is edge, traverse to next edge
    if node.edgeList[patLetterIndex] != None:
        # matchCount += 1
        return LCPtraverseDown(node.edgeList[patLetterIndex], txt, pat, index, matchCount)  # recursion to next edge
    # no existing edge, mismatch
    else:
        return -1, matchCount               # mismatch


def readFile(fileName):
    """
    This function reads a file and makes the content in the file into a string.
    :param fileName:
    :return text:
    :complexity O(N),
    where N is the length of the content in the file.
    """
    file = open(fileName, "r")              # open file
    text = ""
    for character in file:                  # for every character in file
        text += character.strip()           # removes break lines and spaces
    # print("text = ", text)
    file.close()                            # close file
    return text

def readPairsFile(fileName):
    """
    This function reads a file and makes the content in the file into a list of lists containing the start and end of every line in the file.
    :param fileName:
    :return: pairsList
    complexity: O(M), where M is the number characters in fileName
    """

    file = open(fileName, "r")              # open file
    pairsList = []                          # [[i,j],[i,j]...]
    for line in file:                       # for every line in the file
        line = line.split()                 # split by spaces and put into a list
        for i in range(len(line)):          # for every number in each line
            line[i] = int(line[i])          # convert to integer
        pairsList.append(line)
    # print(pairsList)
    return pairsList



def findLCP(txtFile, pairsFile):
    """
    This function finds the longest prefix that is common to the suffixes starting at indexes i and j in str.
    :param txtFile:
    :param pairsFile:
    :return:
    complexity: O(NM), where N is the number of characters in txtFile and M is the number of lines in pairsFile
    """
    # reading file to get the txt
    txt = readFile(txtFile)

    # reading file to get i and j
    pairsList = readPairsFile(pairsFile)

    # output into file
    # creating output file
    outputFile = open("output_lcps.txt", "w")

    # for every i and j on every line
    for x in range(len(pairsList)):
        i = int(pairsList[x][0]) - 1            # subtract 1 to get position
        j = int(pairsList[x][1]) - 1            # subtract 1 to get position

        matchCount = 0                          # number of matches
        if j < len(txt):                        # make sure j is not out of range
            # get 2 strings based on i and j
            firstString = txt[i:]
            secondString = txt[j:]
            # print("j", j)
            # build suffix tree for second string j..n
            suffixTree = SuffixTree()
            suffixTree.buildTree(secondString)

            # traverse the tree to find matches
            checkMatch, matchCount = LCPtraverseDown(suffixTree.tree, firstString, secondString, 0, 0)

        # print("MATCHCOUNT = ", matchCount)

        # write into output file
        outputFile.write(str(i+1) + " " + str(j+1) + " " + str(matchCount))
        outputFile.write("\n")



################# M A I N #################

if __name__== "__main__":
    textFileName = sys.argv[1]                      # 2nd argument in terminal

    pairsFileName = sys.argv[2]                     # 3rd argument in terminal

    findLCP(textFileName, pairsFileName)            # call main function
