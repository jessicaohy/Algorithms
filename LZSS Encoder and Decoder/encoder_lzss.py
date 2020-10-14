# Jessica Oh Hui Yu

import sys
import heapq
from bitarray import bitarray

###################### H U F F M A N ##############################
class HeapNode:
    def __init__(self, letter, freq):
        """
        This function initialises the attributes in HeapNode class.
        :param letter:
        :param freq:
        :complexity O(1)
        """
        self.letter = letter
        self.freq = freq                        # number of times the letter appears

        self.leftChild = None
        self.rightChild = None

    def __lt__(self, other):                    # compare frequency only so that it can be compared in heapq
        """
        This function allows the less than operator to be used between 2 objects by comparing the freq attribute.
        :param other:
        :return: True or False
        :complexity 0(1)
        """
        # if frequency is lesser than the other frequency
        if self.freq < other.freq:
            return True
        return False


class Huffman:
    def __init__(self):
        """
        This function initialises the attributes in Huffman class.
        :complexity O(1)
        """
        self.freqHeap = []                      # binary tree
        self.codes = [None] * 128               # position = ascii of letter, content = code

    # counts the frequency of every word
    # FreqList position is ascii
    def count_freq(self, txt):
        """
        This function counts the number of times each unique letter appears in txt.
        :param txt:
        :return: freqList
        :complexity worse case = O(N)
        where N is the number of letters in txt
        """
        # list to hold the number of times each letter appears
        freqList = []
        for i in range(128):
            freqList.append(0)                          # put as 0 and increase later

        for i in range(len(txt)):
            letterPosition = ord(txt[i])                # position = ascii letter
            freqList[letterPosition] += 1               # increase freq

        # print("freqList = ", freqList)
        return freqList

    # create min heap of frequencies, increasing
    def createFreqMinHeap(self, freqList):
        """
        This function creates the minimum heap.
        :param freqList:
        :return:
        :complexity O(N)
        where N is the number of nodes in the heap
        """
        # create node
        for i in range(len(freqList)):
            # if there is an occurrence of the letter
            if freqList[i] != 0:
                letter = chr(i)                                 # find letter base on position

                node = HeapNode(letter, freqList[i])            # letter, frequency
                heapq.heappush(self.freqHeap, node)             # push node into min heap

    # imagine each char is leaf node in binary tree and repeatedly joining
    def mergeNodes(self):
        """
        This function merge 2 least frequency nodes until there is only 1 node left.
        :return:
        :complexity O(Nlog(N))
        where N is the number of nodes on the heap
        """
        while len(self.freqHeap)>1:                             # until merged into single node
            firstNode = heapq.heappop(self.freqHeap)            # 1st node taken is 1st smallest
            secNode = heapq.heappop(self.freqHeap)              # 2nd node taken is 2nd smallest

            # new node with sum of freq
            mergedNode = HeapNode(firstNode.letter + secNode.letter, firstNode.freq + secNode.freq)

            # smaller go left, larger go right
            # 1st node is smaller than 2nd node
            mergedNode.leftChild = firstNode
            mergedNode.rightChild = secNode

            # put merged node back into minheap
            heapq.heappush(self.freqHeap, mergedNode)

        # print(self.freqHeap[0].letter)

    def traverse(self, root, code):
        """
        This function traverses to the end of each leaf of the tree using recursion.
        Moving to the left adds 0 to the binary and moving to the right adds 1 to the binary.
        :param root:
        :param code:
        :return:
        :complexity O(N)
        where N is the number of nodes in the tree
        """
        # print(code)

        if root == None:
            return

        if len(root.letter) == 1:
            letterPosition = ord(root.letter)           # find position to insert into self.codes
            self.codes[letterPosition] = code           # record code corresponding to letter
            return

        # recursion.
        self.traverse(root.leftChild, code + "0")       # go left, add 0
        self.traverse(root.rightChild, code + "1")      # go right, add 1


    def createCode(self):
        """
        This function creates the code by calling the recursion function to traverse the tree.
        :return: self.codes
        :complexity O(N)
        where N is the number of nodes in the tree
        """
        root = heapq.heappop(self.freqHeap)             # remove from tree
        code = bitarray()
        self.traverse(root, code)                       # recursion to leaf, adding 0s and 1s
        # print("SELF.CODES = ", self.codes)
        return self.codes


###################### E L I A S ##############################

def dec2binbits(dec):
    """
    This function converts an integer with base 10 (dec) to binary.
    :param dec:
    :return: binaryList
    :complexity worse case = O(log(N))
    where N is the number of digits
    """
    binaryList=[]

    while dec>0:
        binaryList.append(dec%2)                            # remainder either 0 or 1
        dec=dec//2                                          # integer division

    binaryList.reverse()                                    # to get list of binary
    # print("converted = ", binaryList)
    return binaryList

def elias(n):
    """
    This function encodes an integer using Elias Omega algorithm.
    :param n:
    :return: finalCode
    :complexity O(N^2)
    where N is the number of bits
    """
    finalBinaryList = []

    minBinaryList = dec2binbits(n)                          # convert to binary

    # combine to bit array
    codePart = bitarray()
    for i in range(len(minBinaryList)):
        codePart = codePart + str(minBinaryList[i])

    # codePart = int(codePart)  # convert to integer
    finalBinaryList.append(codePart)


    # Encoding Length
    # continue until left 1 digit in binary
    while len(codePart) != 1:

        encodeLength = len(minBinaryList) - 1               # decrease by 1 each loop

        minBinaryList = dec2binbits(encodeLength)           # convert to binary

        # if most significant is 1
        if minBinaryList[0] == 1:
            minBinaryList[0] = 0                            # change it to 0

        # combine to bitarray
        codePart = bitarray()
        for i in range(len(minBinaryList)):
            codePart = codePart + str(minBinaryList[i])

        #codePart = int(codePart)  # convert to integer

        finalBinaryList.append(codePart)
    # print("\n")
    # print(finalBinaryList)
    finalBinaryList.reverse()                               # cause appended, length at the back but shld be front
    # print("reversed = ", finalBinaryList)
    # combine to bit array
    finalCode = bitarray()
    for i in range(len(finalBinaryList)):
        finalCode = finalCode + finalBinaryList[i]

    # print("finalCode", finalCode)
    return finalCode


def countDiffLetters(txt):
    """
    This function counts the different letters in a text.
    :param txt:
    :return: len(diffLetterList)
    :complexity worse case = O(N^2)
    where N is the number of letters in txt
    """
    diffLetterList = []

    i = 0
    # go through all the letters in txt
    while i < (len(txt)):
        # at the start, nothing inside
        if len(diffLetterList) == 0:
            diffLetterList.append(txt[i])                   # insert first letter inside

        # check through all letters that exist in diffLetterList
        for j in range(len(diffLetterList)):
            # if it exist
            if diffLetterList[j] == txt[i]:
                break                                       # move to next letter
            # searched through whole list and letter does not exist
            elif diffLetterList[j] != txt[i] and j == len(diffLetterList) - 1:
                diffLetterList.append(txt[i])               # add in to note that it now exists
        i += 1                                              # move to next letter

    # print("Number of different letters = ", diffLetterList)
    return len(diffLetterList)                              # number of different letters


###########################################

def encodeHeader(txt):
    """
    This function encodes the header by calling functions to encode using Elias and Huffman algorithms.
    :param txt:
    :return: finalHeadList, huffman
    :complexity worse case = O(N^2)
    where N is the number of letters in txt
    """
    # number of different letters #
    finalHeadList = []

    nDiffLetters = countDiffLetters(txt)                    # number of different letters
    # encode using elias
    nDiffLettersCode = elias(nDiffLetters)                  # get elias code
    finalHeadList.append(nDiffLettersCode)

    # codes for each letter in txt
    # encode using huffman
    huffman = Huffman()
    freqList = huffman.count_freq(txt)
    huffman.createFreqMinHeap(freqList)
    huffman.mergeNodes()
    codeList = huffman.createCode()                         # code for each letter

    for i in range(len(codeList)):
        finalCode = bitarray()

        # if position contain code
        if codeList[i] != None:

            # get letter based on position
            letter = chr(i)                                 # get letter
            letterASCII = ord(letter)                       # get ascii of letter

            # get binary
            binLetterASCIIList = dec2binbits(letterASCII)   # convert to binary

            # combine bits
            binLetterASCII = bitarray()
            for j in range(len(binLetterASCIIList)):
                binLetterASCII = binLetterASCII + str(binLetterASCIIList[j])

            finalCode = finalCode + binLetterASCII

            # huffman of length #
            codeLength = len(codeList[i])
            codeLengthCode = elias(codeLength)              # using elias

            finalCode = finalCode + codeLengthCode

            # huffman code of letter #
            finalCode = finalCode + codeList[i]

            finalHeadList.append(finalCode)
    # print("FINAL = ", finalHeadList)
    return finalHeadList, huffman




########### ENCODING DATA ################

###################### L Z S S ##############################
class LZSS: # easier to create class so that can use information everywhere instead of returning

    def __init__(self, txt, W, L):
        """
        This function initialises the attributes in LZSS class.
        :param txt:
        :param W:
        :param L:
        :complexity O(1)
        """
        self.txt = txt
        self.windowSize = W                     # search window size
        self.bufferSize = L                     # lookahead buffer size

        self.bufferStart = 0
        self.move = 0


    def findWord(self, dictionary, window):
        """
        This function finds the position of window in dictionary and return -1 if it is not found.
        :param dictionary:
        :param window:
        :return: i or -1
        complexity: O(MN)
        where M is the number of letters in window
        where N is the number of letters in dictionary
        """
        # print(dictionary, window)
        # if length of dictionary shorter than length of window
        if len(dictionary) < len(window):
            # print("return -1")
            return -1                               # window not in dictionary

        # go through every position in dictionary
        for i in range(len(dictionary)):

            j = 0
            # go through every letter in window
            while j < len(window):

                # to make sure that it does not go beyond dictionary
                # avoid out of range
                if i+j >= len(dictionary):
                    return -1                       # not found

                if dictionary[i+j] != window[j]:
                    break                           # go to next position in dictionary
                elif j == len(window) - 1:          # matched all the way to the end
                    # print("FOUND", i )
                    return i
                j += 1                              # go to next position in dictionary
        # print("return -1")
        return -1                                   # not found




    # search dictionary
    def findBufferOffset(self, index):
        """
        This function calculates the offset by calling another function to find the position where a word is found in another word.
        :param index:
        :return: len(dictionary) - foundPos
        :complexity O(MN)
        where M is the number of letters in window
        where N is the number of letters in dictionary
        """
        start = self.bufferStart - self.windowSize
        end = self.bufferStart

        # print("\n")
        # print("start", start)
        # print("self.bufferStart", self.bufferStart)
        # at the start
        if end < 1:
            return -1
        # if start is negative, put it as the first letter
        if start < 0:
            start = 0
            # if end is at the start, move to the 2nd position so that comparison can take place
            if end == 0:
                end = 1

        dictionary = self.txt[start:end]                # set dictionary

        window = self.txt[self.bufferStart: index]      # set window

        # find window position in dictionary
        # print("Dictionary = ", dictionary)
        # print("Window = ", window)
        foundPos = self.findWord(dictionary, window)    # find position of window in dictionary

        # if not found
        if foundPos == -1:
            return -1
        return len(dictionary) - foundPos               # to find offset


    def findMatch(self):
        """
        This function finds the offset and number of matches in a dictionary and window.
        :return: (offset, nMatched)
        :complexity worse case = O(MN)
        where M is the number of letters in window
        where N is the number of letters in dictionary
        """
        nMatched = 0
        offset = 0

        # if beyond the end of txt
        if self.bufferStart+self.bufferSize > len(self.txt)-1:
            minEdge = len(self.txt)                     # set as end of txt
        # if havent reach beyond end of txt
        else:
            minEdge = self.bufferStart+self.bufferSize+1

        # finding substring that matches
        for i in range(self.bufferStart+1, minEdge):
            offsetTemp = self.findBufferOffset(i)       # different i for window end index

            # if not found
            if offsetTemp == -1:
                return (offset, nMatched)               # no match

            offset = offsetTemp                         # replace
            nMatched += 1                               # increase number of matched counts
        return (offset, nMatched)



    def format(self):
        """
        This function creates the format-0/1 fields.
        :return:
        :complexity O(MN)
        where M is the number of letters in window
        where N is the number of letters in dictionary
        """
        offsetMatchedList = []

        # while it is not the end of the txt
        while self.bufferStart + self.move <= len(self.txt) - 1:    # until reach end of the txt
            # window
            self.bufferStart += self.move                           # shift

            # get offset and length of largest matching string
            (offset, nMatched) = self.findMatch()

            # set next window
            # if no matches
            if nMatched == 0:
                self.move = 1                                       # move 1 step
                offsetMatchedList.append((0,0))                     # offset = 0, length = 0

            # if have matches
            else:
                self.move = nMatched
                # print("self.move", self.move)
                offsetMatchedList.append((offset, nMatched))

        # print(offsetMatchedList)

        # to allow searches to go into lookahead buffer
        finalOffsetMatchedList = []
        i = 0
        # go through every item in the list
        while i < (len(offsetMatchedList)-1):
            # if current and next have matches, combine them
            # can search beyond dictionary and into window so combine them
            if offsetMatchedList[i][1] != 0 and offsetMatchedList[i+1][1] != 0:
                finalOffsetMatchedList.append((offsetMatchedList[i][0], offsetMatchedList[i][1]+offsetMatchedList[i+1][1]))
                i += 1
            # seached until the 2nd last and cannot combine so just add them individually
            elif i == len(offsetMatchedList) - 2:
                finalOffsetMatchedList.append(offsetMatchedList[i])
                finalOffsetMatchedList.append(offsetMatchedList[i+1])
            # cannot combine
            else:
                finalOffsetMatchedList.append(offsetMatchedList[i])
            i += 1                                                                      # next position

        # print("finalOffsetMatchedList = ", finalOffsetMatchedList)

        # put into formats 0 or 1
        formatList = []
        letterPos = 0
        for i in range(len(finalOffsetMatchedList)):

            # if length is less than 3
            # format 1
            if finalOffsetMatchedList[i][1] < 3:
                letter = self.txt[letterPos]
                formatList.append((1, letter))                                                      # format 1

                # if length == 0 (no match) or 1
                if finalOffsetMatchedList[i][1] <= 1:
                    letterPos += 1
                else:
                    letterPos += finalOffsetMatchedList[i][1]

            # if length is more than or equals to 3
            # format 0
            else:
                formatList.append((0, finalOffsetMatchedList[i][0], finalOffsetMatchedList[i][1]))  # format 0

                # if length == 0 (no match) or 1
                if finalOffsetMatchedList[i][1] <= 1:
                    letterPos += 1
                else:
                    letterPos += finalOffsetMatchedList[i][1]

        # print("formatList = ", formatList)
        return formatList


def encodeData(txt, W, L, huffmanCodeList):
    """
    This function encodes the data part.
    :param txt:
    :param W:
    :param L:
    :param huffmanCodeList:
    :return: finalDataList
    :complexity worse case = O(MN)
    where M is the number of letters in window
    where N is the number of letters in dictionary
    """

    finalDataList = []

    # encode using lz77
    data = LZSS(txt, W, L)
    formatList = data.format()

    # number of formats #
    nFormats = len(formatList)
    nFormatsCode = elias(nFormats)
    finalDataList.append(nFormatsCode)

    for i in range(len(formatList)):
        # if format = 1
        # use huffman
        if formatList[i][0] == 1:

            letter = formatList[i][1]
            # print("letter = ", letter)

            letterPos = ord(letter)                         # get letter position
            letterHuffmanCode = huffmanCodeList[letterPos]  # get code based on letter position

            # (1, letter) #
            finalDataList.append(bitarray("1"))
            finalDataList.append(letterHuffmanCode)         # add letter code

        # if format = 0
        # use elias
        else:

            # encode using elias
            offsetCode = elias(formatList[i][1])            # get offset code
            lengthCode = elias(formatList[i][2])            # get length code

            # print("offsetCode = ", offsetCode, "lengthCode = ", lengthCode)

            # (0, offset, length) #
            finalDataList.append(bitarray("0"))
            finalDataList.append(offsetCode)                # add offset
            finalDataList.append(lengthCode)                # add length

    # print('FINAL = ', finalDataList)
    return finalDataList


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



def encode(txtFile, W, L):
    """
    This function encodes the header part and data part, and concatenate both of them together.
    The output is printed into a bin file.
    :param txt:
    :param W:
    :param L:
    :return:
    :complexity O(MN)
    where M is the number of letters in window
    where N is the number of letters in dictionary
    """

    txt = readFile(txtFile)

    finalHeadList,huffmanCodes = encodeHeader(txt)                  # encode header

    finalDataList = encodeData(txt, W, L, huffmanCodes.codes)       # encode data


    # convert all items in list to a long sentence
    finalHeadCode = bitarray()
    for i in range(len(finalHeadList)):
        finalHeadCode = finalHeadCode + finalHeadList[i]
    # print("finalHeadCode = ", finalHeadCode)

    # combine to single bitarray
    finalDataCode = bitarray()
    for i in range(len(finalDataList)):
        finalDataCode = finalDataCode + finalDataList[i]
    # print("finalDataCode = ", finalDataCode)

    # combine both
    finalCode = finalHeadCode + finalDataCode

    # pack into bytes
    remainder = len(finalCode) % 8
    fillZero = 8 - remainder
    while fillZero != 0:
        finalCode = finalCode + bitarray("0")
        fillZero -= 1

    # print("FINAL CODE = ", finalCode)

    outputBinFile = open("output_encoder_lzss.bin","wb")    #.bin file
    finalCode = finalCode.tobytes()
    outputBinFile.write(finalCode)
    outputBinFile.close()                                   # close file

    return finalCode


############################## M A I N #############################
if __name__== "__main__":
    txtFile = sys.argv[1]       # 2nd argument in terminal

    W = sys.argv[2]             # 3rd argument in terminal
    W = int(W)                  # convert to int

    L = sys.argv[3]             # 4th argument in terminal
    L = int(L)                  # convert to int

    # Encoding
    encode(txtFile, W, L)         # W = 6, L = 4


