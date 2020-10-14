# Jessica Oh Hui Yu
import sys
from bitarray import bitarray


def bitArrayToDec(bitarray):
    """
    This function converts bit array to decimal.
    :param bitarray:
    :return: dec
    :complexity O(log(N))
    where N is the number of bits
    """
    # print("bitarray to dec", bitarray)
    # converting bit array to decimal
    dec = 0
    # for every bit
    for bit in bitarray:
        dec = dec << 1 | bit
    # print(dec)
    return dec

def decodeElias(codeword):
    """
    This function decodes the codeword that was encoded using elias omega algorithm.
    :param codeword:
    :return: n, codeword
    :complexity O(Nlog(N))
    where N is the number of bits in codeword
    """

    readlen = int("1", 2)   # convert to dec
    component = ""
    pos = 0

    component = codeword[pos:pos+readlen]           # get part of codeword

    # remove from codeword
    nToRemove = 1

    # while most significant is 0
    while component[0] == False:

        # flip 0 to 1
        component[0] = True
        pos += readlen                              # increase pos
        readlen = bitArrayToDec(component) + 1      # increase readlen
        component = codeword[pos:pos+readlen]       # get part of codeword

        # remove from codeword
        nToRemove = pos+readlen

    n = bitArrayToDec(component)                    # convert bit array to integer base 10 (dec)

    # remove from codeword
    codeword = codeword[nToRemove:]

    return n, codeword                              # return the elias number and remaining codewords




def decodeHeader(codeword):
    """
    This function decode the header part.
    :param codeword:
    :return: codeword, huffmanCodeList
    :complexity O(Nlog(N))
    where N is the number of bits
    """
    # number of letters
    n, codeword = decodeElias(codeword)

    huffmanCodeList = [None] * 128                  # to hold codes of letters
    for i in range(n):

        # decode ascii letter
        asciiLetter = codeword[0:7]                 # first 7 numbers


        decLetter = bitArrayToDec(asciiLetter)      # convert bit to integer base 10 (dec)
        letter = chr(decLetter)


        # removes first 7 bits
        codeword = codeword[7:]

        # decode huffman
        # number of huffman chars
        # decoding using elias
        nHuffmanCodes, codeword = decodeElias(codeword)


        # record letter and code for decoding data ltr
        huffmanCodeList[decLetter] = codeword[:nHuffmanCodes]

        # remove code from codeword
        codeword = codeword[nHuffmanCodes:]

    return codeword, huffmanCodeList


def decodeHuffman(codeword, huffmanCodeList):
    """
    This function decode codeword that was encoded using Huffman algorithm.
    :param codeword:
    :param huffmanCodeList:
    :return: j, codeword or -1, codeword
    :complexity O(MN)
    where M is the number of positions in huffmanCodeList that are not None
    where N is the number of letters in codeword
    """
    findCodeword = bitarray()
    # increase codeword if cannot find in huffman code list
    for i in range(len(codeword)):
        findCodeword = codeword[:i+1]               # increase codeword

        # find in huffman code list
        for j in range(len(huffmanCodeList)):

            # found a code that has corresponding letter
            if huffmanCodeList[j] == findCodeword:
                # remove
                codeword = codeword[i+1:]
                return j, codeword                  # return ascii of letter

    return -1, codeword                             # cannot find

def decodeData(codeword, huffmanCodeList):
    """
    This function decodes the data part.
    :param codeword:
    :param huffmanCodeList:
    :return: decoded
    :complexity O(MN)
    where M is the number of positions in huffmanCodeList that are not None
    where N is the number of letters in codeword

    """

    decoded = ""

    n, codeword = decodeElias(codeword)


    # while there is still bits in codeword
    while len(codeword) != 0:
        # print("\n")
        # print("remaining codeword", codeword)

        checkAllZeros = True

        # check whether remaining is 0s only
        # print(len(codeword))
        for i in range(len(codeword)):
            if codeword[i] == True:
                checkAllZeros = False

        # if all 0s only
        if checkAllZeros == True:
            return decoded              # finished decoding everything


        # format 1
        if codeword[0] == True:
            # remove
            codeword = codeword[1:]

            # decode using huffman
            letterASCII, codeword = decodeHuffman(codeword, huffmanCodeList)
            letter = chr(letterASCII)                   # get letter

            decoded = decoded + letter                  # combine


        # format 0
        elif codeword[0] == False:
            # remove
            codeword = codeword[1:]

            # get offset
            offset, codeword = decodeElias(codeword)

            # get length
            length, codeword = decodeElias(codeword)

            nDecoded = len(decoded)
            startDecoded = len(decoded) - offset
            for i in range(length):
                decoded = decoded + decoded[startDecoded+i]

        # print("DECODED = ", decoded)

    return decoded


def readBinFile(binFile):
    file = open(binFile, "rb")
    byte = file.read()
    encodedBit = bitarray()
    encodedBit.frombytes(byte)                                  # get bitarray
    # print(encodedBit)
    return encodedBit


def decode(binFile):
    """
    This function decodes the header and data parts to give the final decoded characters.
    :param codeword:
    :return: decoded
    :complexity O(MNlog(N))
    where M is the number of positions in huffmanCodeList that are not None
    where N is the number of letters in codeword
    """

    codeword = readBinFile(binFile)                             # read bin file into bit array

    codeword, huffmanCodeList = decodeHeader(codeword)          # decode header

    # print("##########################")
    decoded = decodeData(codeword, huffmanCodeList)             # decode data
    # print("DECODED = ", decoded)

    # creating output file
    outputFile = open("output_decoder_lzss.txt", "w")           # open file
    outputFile.write(decoded)                                   # write decoded string
    outputFile.close()                                          # close file
    return decoded


############################## M A I N #############################
if __name__== "__main__":
    binFile = sys.argv[1]     # 2nd argument in terminal

    decode(binFile)





