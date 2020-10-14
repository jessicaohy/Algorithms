# Jessica Oh Hui Yu

import sys
from suffixTree import *


def traverseToSuffixIndex(node, suffixIndexesList):
    """
    This function traverses down until the leaves to get the suffix indexes and creates the suffix array using recursion.
    :param node:
    :param suffixIndexesList:
    :return:
    complexity: worst case = O(N), where N is the number of characters in txt
    """
    # suffix array created by arranging in alphabetical order
    # smaller chars = comes first in edgeList = will get suffix indexes first

    # node does not exist
    if node == None:
        return

    # if it is an internal node
    if node.suffixIndex == -1:

        for i in range(256):                                                # for every node in edgeList
            # if node exists
            if node.edgeList[i] != None:
                traverseToSuffixIndex(node.edgeList[i], suffixIndexesList)  # traverse down to get suffixIndex
    # if is leaf
    elif node.suffixIndex > -1:
        suffixIndexesList.append(node.suffixIndex)                          # add suffix index into suffix array

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


def findBWT(txtFile):
    """
    This function uses the suffix array to find the Burrows-Wheeler Transform of txt.
    :param txtFile:
    :return:
    complexity: worst case = O(N), where N is the number of characters in txt.
    """

    # reading file and getting string
    txt = readFile(txtFile)
    txt = txt + "$"                         # add $ to end of txt

    # building the tree
    suffixTree = SuffixTree()
    suffixTree.buildTree(txt)
    tree = suffixTree.tree                  # to get node/root

    # print("tree = ", tree)
    suffixIndexesList = []

    # find suffix array
    traverseToSuffixIndex(tree, suffixIndexesList)
    # print('SUFFIXINDEXESLIST = ', suffixIndexesList)

    # to get BWT, every position in suffix array -1 to get the last char in the string
    BWTString = ""
    # for every index in suffix array
    for i in range(len(suffixIndexesList)):
        BWTLetterPosition = suffixIndexesList[i] - 1        # to get last char in string
        BWTString = BWTString + txt[BWTLetterPosition]      # add character

    # print("BWTString = ", BWTString)
    # output into file
    # creating output file
    outputFile = open("output_bwt.txt", "w")                # open file
    outputFile.write(BWTString)                             # write bwt string
    outputFile.close()                                      # close file


################# M A I N #################

if __name__== "__main__":
    textFileName = sys.argv[1]                  # 2nd argument in terminal

    findBWT(textFileName)                       # call main function
