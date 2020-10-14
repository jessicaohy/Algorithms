# Jessica Oh Hui Yu

def lookup(data_file, query_file):
    """
    This function finds out which songs contain the words in the query file.
    :param data_file:
    :param query_file:
    :complexity: O(CI + CQ + CP)
    """

    # reading a file and putting the words into a list
    dataFile = open(data_file, "r")
    dataFileList = []
    for line in dataFile:
        line = line.strip("\n").split(":")                          # remove breakline at end and separate ID and lyrics
        line[1] = line[1].split(" ")                                # split lyrics according to spaces
        dataFileList.append(line)
    # [[ID, [lyrics], [ID, [lyrics]]

    dataFile.close()                                                # close file

    # CONSTRUCTING TRIE
    nodeArray = [None] * 27                                         # 26 alphabets (a-z) + $
    trie = []
    trie.append(nodeArray)                                          # Empty node at the start

    maxNodeIndex = 0                                                # number of nodes the trie currently have
    currNodeIndex = 0                                               # pointer

    for i in range(len(dataFileList)):                              # for every line in data_file
        for j in range(len(dataFileList[i][1])):                    # for every word (lyrics) in date_file

            currNodeIndex = 0                                       # reset and start from first node again

            for k in range(len(dataFileList[i][1][j])):             # for every letter of the word in data_file

                # convert letter to ascii
                letter = dataFileList[i][1][j][k]
                letterIndex = ord(letter) - 97                      # letter will be 0-25 (index)

                # INSERTING IT INTO THE TRIE

                # check if there is a present letter in the node
                # if the letter is not in the node
                if trie[currNodeIndex][letterIndex] == None:
                    nodeArray = [None] * 27                                 # 26 alphabets (a-z) + $
                    trie.append(nodeArray)                                  # add in new node
                    maxNodeIndex += 1                                       # update max index
                    trie[currNodeIndex][letterIndex] = maxNodeIndex         # point to next node
                    currNodeIndex = maxNodeIndex                            # update to next index of node

                # if there is already the letter in the node
                else:
                    currNodeIndex = trie[currNodeIndex][letterIndex]        # go to the next node

                # if is the last letter
                if k == len(dataFileList[i][1][j]) - 1:

                    # if word is not in the trie yet
                    if trie[currNodeIndex][-1] == None:
                        IDArray = []
                        IDArray.append(dataFileList[i][0])                  # add ID
                        trie.append(IDArray)                                # add into trie as a node
                        maxNodeIndex += 1                                   # increase no. of nodes in the trie
                        trie[currNodeIndex][-1] = maxNodeIndex              # "$" pointing to array containing ID

                    # if word is in the trie alr, check if it is a different ID to existing ID
                    else:
                        currNodeIndex = trie[currNodeIndex][-1]                 # go to the node with ID

                        # check thru if existing ID is already inside
                        for l in range(len(trie[currNodeIndex])):
                            if trie[currNodeIndex][l] == dataFileList[i][0]:    # if ID is already inside
                                break
                            elif l == len(trie[currNodeIndex]) -1:              # if ID is not inside and checked thru
                                trie[currNodeIndex].append(dataFileList[i][0])  # add in another ID

                # print("TRIE = ", trie)

    # FINDING WORD
    # reading file and putting word into list
    queryFile = open(query_file, "r")
    queryFileList = []
    for line in queryFile:
        line = line.strip("\n")                                                 # remove backline at end of line
        queryFileList.append(line)

    queryFile.close()                                                           # close file

    outputFile = open("song_ids.txt", "w+")                                     # TO WRITE INTO OUTPUT FILE

    for w in range(len(queryFileList)):                                         # for every word
        currNodeIndex = 0                                                       # reset to start of node

        for x in range(len(queryFileList[w])):                                  # for every letter

            letter = queryFileList[w][x]

            # convert letter to ascii
            letterIndex = ord(letter) - 97                                      # letter will be 0-25 (index)

            # check if letter is in trie
            # if it does not contain letter
            if trie[currNodeIndex][letterIndex] == None:
                outputFile.write("Not found \n")
                break                                                           # stop searching for next letter
                                                                                # go next word
            # if it contains letter
            else:
                currNodeIndex = trie[currNodeIndex][letterIndex]                # go to next node

            # check if it is the last letter
            if x == len(queryFileList[w])-1 and trie[currNodeIndex][-1] != None:

                currNodeIndex = trie[currNodeIndex][-1]             # go to node with ID
                IDArray = trie[currNodeIndex]

                for n in range(len(IDArray)):                       # for every ID
                    if n!=0:
                        outputFile.write(" ")
                    outputFile.write(IDArray[n])

        outputFile.write("\n")
    outputFile.close()


def most_common(data_file, query_file):
    """
    This function determine which word is present in the most songs and begins with the given prefix.
    :param data_file:
    :param query_file:
    :complexity: O(CI + CQ + CM)
    """

    # reading a file and putting the words into a list
    dataFile = open(data_file, "r")
    dataFileList = []
    for line in dataFile:
        line = line.strip("\n").split(":")                          # remove breakline at end and separate ID and lyrics
        line[1] = line[1].split(" ")                                # split lyrics according to spaces
        dataFileList.append(line)
    # [[ID, [lyrics], [ID, [lyrics]]

    dataFile.close()                                                # close file

    # CONSTRUCTING TRIE
    nodeArray = [None] * 27                                         # 26 alphabets (a-z) + $
    trie = []
    trie.append(nodeArray)                                          # Empty node at the start

    maxNodeIndex = 0                                                # number of nodes the trie currently have
    currNodeIndex = 0                                               # pointer

    for i in range(len(dataFileList)):                              # for every line in data_file

        currID = dataFileList[i][0]

        for j in range(len(dataFileList[i][1])):                    # for every word (lyrics) in date_file
            currNodeIndex = 0                                       # reset and start from first node again

            for k in range(len(dataFileList[i][1][j])):             # for every letter of the word in data_file

                # convert letter to ascii
                letter = dataFileList[i][1][j][k]
                letterIndex = ord(letter) - 97                      # letter will be 0-25 (index)

                # INSERTING IT INTO THE TRIE

                # check if there is a present letter in the node
                # if the letter is NOT in the node
                if trie[currNodeIndex][letterIndex] == None:
                    nodeArray = [None] * 27                                 # 26 alphabets (a-z) + $
                    trie.append(nodeArray)                                  # add in new node
                    maxNodeIndex += 1                                       # update max index

                    checkedIDList = []
                    checkedIDList.append(currID)
                    trie[currNodeIndex][letterIndex] = (maxNodeIndex, checkedIDList)   # (point next node, [current ID])
                    currNodeIndex = maxNodeIndex                            # update to next index of node


                # if there is already the letter in the node
                else:
                    # if is from the same ID and same word, dont increment

                    # different id, same letter
                    # if song ID has not been added
                    if currID != trie[currNodeIndex][letterIndex][1][-1]:       # check last checked ID

                        nextNodeIndex = trie[currNodeIndex][letterIndex][0]

                        checkedIDList = trie[currNodeIndex][letterIndex][1]
                        checkedIDList.append(currID)                            # add checked ID

                        trie[currNodeIndex][letterIndex] = (nextNodeIndex, checkedIDList)   # put in new tuple

                    currNodeIndex = trie[currNodeIndex][letterIndex][0]         # go to the next node


                # if is the last letter
                if k == len(dataFileList[i][1][j]) - 1:

                    # if word is not in the trie yet
                    if trie[currNodeIndex][-1] == None:
                        wordArray = []
                        wordArray.append(dataFileList[i][1][j])             # add word
                        trie.append(wordArray)                              # add into trie as a node
                        maxNodeIndex += 1                                   # increase no. of nodes in the trie

                        checkedIDList = []
                        checkedIDList.append(currID)                        # add ID
                        trie[currNodeIndex][-1] = (maxNodeIndex, checkedIDList)  # (point next node, [current ID])

                    # if word is in the trie alr, check if it is a different ID to existing ID
                    else:
                        if currID != trie[currNodeIndex][-1][1][-1]:                    # check last checked ID

                            nextNodeIndex = trie[currNodeIndex][-1][0]
                            checkedIDList = trie[currNodeIndex][-1][1]

                            checkedIDList.append(currID)                                # add checked ID

                            trie[currNodeIndex][-1] = (nextNodeIndex, checkedIDList)    # put in new tuple

                # print("TRIE = ", trie)


    # FINDING WORD
    # reading file and putting word into list
    queryFile = open(query_file, "r")
    queryFileList = []
    for line in queryFile:
        line = line.strip("\n")                                                 # remove backline at end of line
        queryFileList.append(line)

    queryFile.close()                                                           # close file

    outputFile = open("most_common_lyrics.txt", "w+")                           # TO WRITE INTO OUTPUT FILE

    for w in range(len(queryFileList)):                                         # for every word
        currNodeIndex = 0                                                       # reset to start of node

        for x in range(len(queryFileList[w])):                                  # for every letter

            letter = queryFileList[w][x]

            # convert letter to ascii
            letterIndex = ord(letter) - 97                                      # letter will be 0-25 (index)

            # check if letter is in trie
            # if it does not contain letter

            if trie[currNodeIndex][letterIndex] == None:
                outputFile.write("Not found \n")
                break                                                           # stop searching for next letter
                                                                                # go next word
            # if it contains letter
            else:
                currNodeIndex = trie[currNodeIndex][letterIndex][0]             # go to next node

            # FINISHED CHECKING PREFIX
            # check if it is the last letter of target prefix
            if x == len(queryFileList[w])-1:

                while len(trie[currNodeIndex]) != 1:
                    # run through node array to check for max number of songs word appeared
                    maxNumSongs = 0
                    maxSongsNodeIndex = 0

                    for i in range(len(trie[currNodeIndex])):

                        # if has a bigger num of songs
                        if trie[currNodeIndex][i] != None and len(trie[currNodeIndex][i][1]) >= maxNumSongs:

                            maxNumSongs = len(trie[currNodeIndex][i][1])        # replace with bigger num of songs
                            maxSongsNodeIndex = trie[currNodeIndex][i][0]       # replace next index to go next


                    currNodeIndex = maxSongsNodeIndex                           # go to next node


                # ALREADY REACH LIST OF THE WORD
                wordArray = trie[currNodeIndex]

                for n in range(len(wordArray)):                                 # for every word
                    outputFile.write(wordArray[n])
        outputFile.write("\n")
    outputFile.close()


#################################### T A S K  3 ########################################
def palindromic_substrings(S):
    """
    This function find all palindromic substrings of given S that have a length of at least 2.
    :param S:
    :return: palindromeList
    :complexity: O(N^2)
    """

    # CONSTRUCTING TRIE
    nodeArray = [None] * 27                                         # 26 alphabets (a-z) + $
    trie = []
    trie.append(nodeArray)                                          # Empty node at the start

    maxNodeIndex = 0                                                # number of nodes the trie currently have
    currNodeIndex = 0                                               # pointer

    # creating a list of substrings
    substringsList = []
    for i in range(len(S)):                                         # for every position in S
        suffixWord = S[i:]
        substringsList.append(suffixWord)


    for i in range(len(substringsList)):                                    # for every substring in S

        currNodeIndex = 0

        for j in range(len(substringsList[i])):                             # for every letter in substring

            # convert letter to ascii
            letter = substringsList[i][j]
            letterIndex = ord(letter) - 97                                  # index  = 0-25, index 26 = $

            # INSERTING IT INTO THE TRIE

            # check if there is a present letter in the node
            # if the letter is not in the node
            if trie[currNodeIndex][letterIndex] == None:
                nodeArray = [None] * 27                                 # 26 alphabets (a-z) + $
                trie.append(nodeArray)                                  # add in new node
                maxNodeIndex += 1                                       # update max index

                startEndTuple = (i, i+j)                                # start index, end index
                startEndList = []
                startEndList.append(startEndTuple)
                trie[currNodeIndex][letterIndex] = (maxNodeIndex, startEndList)       # (point next node, startEndList)
                currNodeIndex = maxNodeIndex                            # update to the next index of node

            # if there is already the letter in the node
            else:
                # if is different part of the word, add in new tuple
                trie[currNodeIndex][letterIndex][1].append((i, i+j))        # append new start end tuple

                currNodeIndex = trie[currNodeIndex][letterIndex][0]         # go to the next node

            # if is the last letter
            if j == len(substringsList[i]) - 1:

                # if word is not in the trie yet
                if trie[currNodeIndex][-1] == None:
                    trie[currNodeIndex][-1] = "$"

            # print("TRIE = ", trie)


    # FIND ALL PALINDROME

    # creating list of suffixes of reversed S
    reversedSubstringList = []
    reversedS= S[-1::-1]
    for i in range(len(reversedS)):
        reversedWord = reversedS[i:]
        reversedSubstringList.append(reversedWord)

    palindromeList = []

    # CHECK IF REVERSED IS IN THE NORMAL SUFFIX TRIE
    for w in range(len(reversedSubstringList)):                                 # for every word

        currNodeIndex = 0

        checkStartEnd = None
        checkTrieStartEndList = None
        for x in range(len(reversedSubstringList[w])):                          # for every letter

            letter = reversedSubstringList[w][x]

            # convert letter to ascii
            letterIndex = ord(letter) - 97                                      # letter will be 0-25 (index)


            # check if letter is in trie
            # if it does not contain letter
            if trie[currNodeIndex][letterIndex] == None:

                if checkStartEnd == None:
                    print("Not found")
                    break                                                       # go next word

            # if it contains letter
            else:
                checkTrieStartEndList = trie[currNodeIndex][letterIndex][1]
                checkStartEnd = (len(reversedSubstringList[0]) - 1 - (w+x), len(reversedSubstringList[0])-1 - w)

                # print("checkTrieStartEndList", checkTrieStartEndList)
                # print("checkStartEnd", checkStartEnd)

                for n in range(len(checkTrieStartEndList)):                     # for every start end tuple

                    palindromeTuple = checkTrieStartEndList[n]

                    # if start end of reversed suffix is the same as start end if normal suffix in trie
                    # IT IS PALINDROME
                    if palindromeTuple == checkStartEnd:
                        if checkStartEnd[0] - checkStartEnd[1] != 0:            # word must be atleast length 2
                            palindromeList.append(palindromeTuple)
                            break

                currNodeIndex = trie[currNodeIndex][letterIndex][0]  # go to next node to find next possible palindrome

    return palindromeList



############### M A I N ################
if __name__=="__main__":

    lookup("data_file", "query_file")

    most_common("data_file", "query_file")

    print(palindromic_substrings("ababcbaxx"))
