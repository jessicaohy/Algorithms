# Jessica Oh Hui Yu

from suffixTree import *

import sys


def traverseEdge(txt, pat, index, start, end):
    """
    This function checks through all the characters on one edge to see if it matches with pat.
    :param txt:
    :param pat:
    :param index:
    :param start:
    :param end:
    :return: -1, 0 or 1
    complexity: worst case = O(N), where N is the number of characters in txt
    """
    i = start
    while i <= end and index != len(pat):       # while there is character on the edge

        # if they are not matching
        if txt[i] != pat[index]:
            # print("returned -1")
            return -1                           # mismatch
        # check next character on the edge
        i += 1
        index += 1
    # if checked all char on pat, the whole thing matches
    if index == len(pat):
        return 1                                # match
    return 0                                    # continue to match for other edges


def traverseToLeaf(node, foundList):
    """
    This function traverses the tree until the leaf using recursion.
    :param node:
    :param foundList:
    :return: 0 or 1
    complexity: worst case = O(N) where N is the number of characters in txt
    """
    if node == None:                            # does not exist
        return 0                                # mismatch

    if node.suffixIndex > -1:                   # if is leaf
        # print("FOUND", node.suffixIndex)
        foundList.append(node.suffixIndex)
        return 1                                # match whole thing

    # if is internal node, recursion to the leaf
    for i in range(256):
        if node.edgeList[i] != None:            # if edge exist
            traverseToLeaf(node.edgeList[i], foundList)


def traverseDown(node, txt, pat, index, foundList):
    """
    This function traverses down the tree and check whether there is a match using other recursive traverse functions.
    :param node:
    :param txt:
    :param pat:
    :param index:
    :param foundList:
    :return: -1 or 1
    complexity: worst case = O(N), where N is the number of characters in txt
    """
    if node == None:                                        # does not exist
        return -1                                           # mismatch

    checkMatch = -1

    # if is not root
    if node.startIndex != -1:
        checkMatch = traverseEdge(txt, pat, index, node.startIndex, node.endIndex)  # check through all chars on edge

        # if mismatch
        if checkMatch == -1:                                # mismatch
            return -1

        # if match
        if checkMatch == 1:                                 # match
            # if is leaf
            if node.suffixIndex > -1:
                # print("FOUND = ", node.suffixIndex)
                foundList.append(node.suffixIndex)

            # if is internal node
            else:
                # print("substring count", traverseToLeaf(node))
                traverseToLeaf(node, foundList)             # traverse to leaf

            return 1

    # if is not root
    if node.startIndex != -1:
        index = index + (node.endIndex - node.startIndex + 1)

    # move to next
    patLetter = pat[index]
    patLetterIndex = ord(patLetter)                         # find position in edgeList
    # if there is existing edge
    if node.edgeList[patLetterIndex] != None:
        return traverseDown(node.edgeList[patLetterIndex], txt, pat, index, foundList)
    # no existing edge, mismatch
    else:
        return -1                                           # mismatch


def findMatch(txt, pat):
    """
    This function finds the matches of pat in txt and returns the starting index of the occurrences of pat in txt.
    :param txt:
    :param pat:
    :return: foundList
    complexity: worst case = O(N), where N is the number of characters in txt
    """
    foundList = []                                          # occurrences of pat in txt
    # build suffix tree
    suffixTree = SuffixTree()
    suffixTree.buildTree(txt)

    # traverse the suffix tree to find occurrences of pat in txt
    traverseDown(suffixTree.tree, txt, pat, 0, foundList)

    return foundList


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


def wildCardMatching(txtFile, patFile):
    """
    This function finds all the occurrences of pat in txt and allow wild card matching.
    :param txtFile:
    :param patFile:
    :return:
    complexity worst case = O(N+M),
        where N is the length of txt,
        where M is the length of pat.
    """

    # reading files and getting string in file
    txt = readFile(txtFile)
    pat = readFile(patFile)


    n = len(txt)
    m = len(pat)

    # break pat into substrings without "?"
    substringList = []

    substring = ""
    wildCount = 0                                           # number of "?"
    lastSubLength = 0
    prevLastSubLength = 0

    for j in range(m):

        if pat[j] != "?":                                   # if is letter

            if wildCount != 0:                              # if prev is "?", add into the list
                substringList.append(wildCount)
                wildCount = 0                               # reset number of "?"

            substring += pat[j]
            lastSubLength += 1                              # increase substring length

        else:                                               # if is "?"

            if substring != "":                             # if prev is substring, add it into the list
                substringList.append(substring)
                substring = ""                              # reset substring
                prevLastSubLength = lastSubLength           # update length of prev substring
                lastSubLength = 0                           # reset length of substring

            wildCount += 1                                  # increase number of "?"

        if j == m - 1:                                      # last character in pat
            # check one last time if still got prev saved substring/wildCount not added to the list yet
            if substring != "":
                substringList.append(substring)
            if wildCount != 0:
                substringList.append(wildCount)

    # print("substringList = ", substringList)

    # find positions of substrings in pat
    subPositionList = []
    for i in range(len(substringList)):                         # for every substring

        if type(substringList[i]) == str:                       # if is a substring
            positionList = findMatch(txt, substringList[i])     # find the position of substring using BM
            subPositionList.append(positionList)                # add possible positions into subPositionList

        else:                                                   # if is number
            subPositionList.append(substringList[i])            # add number into subPositionList

    # print("subPositionList = ", subPositionList)

    nextSubPositionList = []
    matchedPositionList = []

    for i in range(len(subPositionList)):                       # for every character in subPositionList

        # if is list of positions, add to the next integer
        if type(subPositionList[i]) != int:

            # if is not the last list
            if i != len(subPositionList) - 1:

                # add number of questions marks to see if tally with next substring position
                for j in range(len(subPositionList[i])):
                    nextSubPosition = subPositionList[i][j] + len(substringList[i]) + subPositionList[i + 1]
                    nextSubPositionList.append(nextSubPosition)

            # compare expected next position and next substring position
            prevMatchedPositionList = []
            if matchedPositionList != []:
                prevMatchedPositionList = matchedPositionList
                matchedPositionList = []
            else:
                prevMatchedPositionList = nextSubPositionList

            for j in range(len(prevMatchedPositionList)):
                # linear search
                for k in range(len(nextSubPositionList)):
                    if prevMatchedPositionList[j] == nextSubPositionList[k]:
                        matchedPositionList.append(prevMatchedPositionList[j])

    # add in last substring length
    for i in range(len(matchedPositionList)):
        matchedPositionList[i] += prevLastSubLength

    # if last position is a number, need to add to length, to minus total length, to find starting position
    if type(subPositionList[-1]) == int:
        for i in range(len(matchedPositionList)):
            matchedPositionList[i] += subPositionList[-1]

    # minus total length to find starting position
    for i in range(len(matchedPositionList)):
        matchedPositionList[i] -= len(pat)

    # add 1 to all position when output
    for i in range(len(matchedPositionList)):
        matchedPositionList[i] += 1


    # print("matchedPositionList = ", matchedPositionList)
    # output into file
    # creating output file
    outputFile = open("output_wildcard_matching.txt", "w")

    # if no occurrences of pat in txt
    if len(matchedPositionList) == 0:
        outputFile.write("Not found")
    # have occurrences of pat in txt
    else:
        # write every positions in output file
        for i in range(len(matchedPositionList)):
            outputFile.write(str(matchedPositionList[i]))
            outputFile.write("\n")
    outputFile.close()                              # close output file


################# M A I N #################

if __name__== "__main__":
    textFileName = sys.argv[1]                      # 2nd argument in terminal

    patFileName = sys.argv[2]                       # 3rd argument in terminal

    wildCardMatching(textFileName, patFileName)     # call main function



