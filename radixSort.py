# Jessica Oh Hui Yu
############################ Task 1 ###############################

# counting sort
def countingSort(inputList):                                    # inputList = [[ascii, (WORD, ID)],[ascii,(WORD,ID)]]
    """
    This function sorts the digit in increasing order using counting sort.
    :param inputList:
    :returnn outputList:
    :complexity best case, worst case = O(T)
    """
    #print("input list for countingSort (inputList) = ", inputList)
    # find the maximum key for the length of countList
    maxKey = 0
    for i in range(len(inputList)):                                 # for every [ascii, (WORD, ID)]
        if inputList[i][0] > maxKey:                                # if another num is larger than maxKey
            maxKey = inputList[i][0]
    maxKey += 1

    # construct and increment COUNT LIST
    countList = [0] * maxKey  # [0,0,0]
    for i in range(len(inputList)):                                 # for every (key, value)
        countListIndex = inputList[i][0]                            # index in countList = key
        countList[countListIndex] += 1
    # print("countList = ", countList)

    # construct and set POSITION LIST
    positionList = [0] * len(countList)
    positionList[0] = 1                                             # initialise first position as a 1
    for i in range(1, len(countList)):
        positionList[i] = positionList[i - 1] + countList[i - 1]    # subsequent positions
    # print("positionList = ", positionList)

    # construct and set OUTPUT LIST
    outputList = [0] * len(inputList)
    for i in range(len(inputList)):
        positionListIndex = inputList[i][0]                         # index in positionList = key
        outputListIndex = positionList[positionListIndex] - 1       # index in output list
        outputList[outputListIndex] = inputList[i]                  # (key, value) into output index
        positionList[positionListIndex] += 1                        # increment value in position list
    # print("outputList = ", outputList)
    # print("-----------------------------------------------")
    return outputList

def radixSort(unsortedList):                                            # unsortedList = [(WORD, ID), (WORD, ID)]
    """
    This function sorts the ID and convert every letter in a word to ascii value to pass them into counting sort.
    :param unsortedList:
    :return unsortedList:
    :complexity best case, worst case = O(TM)
    """
    #print("input list in radix sort (unsortedList) = ", unsortedList)

    # SORT ID ###################################

    unsortedIDList = []

    for i in range(len(unsortedList)):                                  # for every (word, ID)
        unsortedIDList.append([unsortedList[i][1], unsortedList[i]])    # unsortedLIst = [[ID, (word, ID)]]
    #print(unsortedIDList)

    sortedList = countingSort(unsortedIDList)                           # COUNTING SORT
    # sortedList = [[ID, (WORD, ID)],[ID,(WORD,ID)]]

    unsortedList = []
    for j in range(len(sortedList)):
        unsortedList.append(sortedList[j][1])

    # SORTING WORDS ######################

    # find the maximum number of letters
    maxNLetters = 0
    for i in range(len(unsortedList)):                                  # for every word
        if len(unsortedList[i][0]) > maxNLetters:                       # if word is longer than maxNLetters
            maxNLetters = len(unsortedList[i][0])

    # fill up shorter words with ' at the back
    for i in range(len(unsortedList)):
        fillUp = maxNLetters - len(unsortedList[i][0])
        newWord = unsortedList[i][0] + fillUp*"`"                       # fill up with "`" ascii = 96
        unsortedList[i] = (newWord, unsortedList[i][1])
    # print("WORD UNSORTED LIST = ", unsortedList)

    n = maxNLetters - 1                                                 # index of last position
    while n >= 0:                                                       # for every letter starting from the right
        unsortedWordList = []

        for i in range(len(unsortedList)):                              # for every word
            letterAscii = ord(unsortedList[i][0][n]) - 96               # key will be 1-26
            unsortedWordList.append([letterAscii, unsortedList[i]])

        sortedList = countingSort(unsortedWordList)                     # COUNTING SORT
        # sortedList = [[ascii, (WORD, ID)],[ascii,(WORD,ID)]]

        unsortedList = []
        for j in range(len(sortedList)):
            unsortedList.append(sortedList[j][1])
        n -= 1                                                          # move to the left

    # REMOVE "`" using Linear Search
    for i in range(len(unsortedList)):                                  # for every word
        startRemoveIndex = 0

        for j in range(len(unsortedList[i][0])):                        # for every letter
            if unsortedList[i][0][j] == "`":
                startRemoveIndex = j                                    # found starting index of "`"
                oldWord = unsortedList[i][0][0:startRemoveIndex]        # only take the starting, without "`"
                # print(oldWord)
                ID = unsortedList[i][1]
                unsortedList[i] = (oldWord, ID)                         # replace with new tuple
                break                                                   # stop finding other letters

    # print("FINAL sorted list = ", unsortedList)
    return unsortedList

def process(filename):
    """
    This function sort the words and output the sorted words with its IDs to another file.
    :param filename:
    :return:
    :complexity best case, worst case = O(TM)
    """
    file = open(filename, "r")                                              # read filename into file

    fileList = []
    for line in file:
        line = line.strip().split(":")
        #line[0] = int(line[0])  # convert ID to integers
        line[1] = line[1].split(" ")
        fileList.append(line)
    # print("process fileList = ", fileList)                                # [[ID, [word, word, word]], [ID, [word,..]]

    file.close()                                                            # close file

    wordIDList = []
    for i in range(len(fileList)):                                          # for every line
        for j in range(len(fileList[i][1])):                                # for every word
            wordIDList.append((fileList[i][1][j], int(fileList[i][0])))     # (Word, ID)
    #print("wordIDList = ", wordIDList)

    radixSortedList = radixSort(wordIDList)                                 # RADIX SORT

    # write into another file
    outputFile = open("sorted_words.txt", "w+")
    for i in range(len(radixSortedList)):
        outputFile.write(radixSortedList[i][0]+":"+str(radixSortedList[i][1])+"\n")

    outputFile.close()                                                      # close file


############################# Task 2 ################################

def collate(filename):
    """
    This function collects the song IDs of each word and output the unique words together with their song IDs to another file.
    :param filename:
    :return:
    :complexity best case, worst case = O(TM)
    """
    file = open(filename, "r")

    # reading content in file into fileList
    fileList = []
    for line in file:
        line = line.strip().split(":")
        fileList.append(line)
    # print("collate fileList = ", fileList)                                 # fileList = [[word, ID],[word,ID]]

    file.close()

    # collating and putting into another output file
    outputFile = open("collated_ids.txt", "w+")
    previousWord = ""
    previousID = ""
    for i in range(len(fileList)):
        if fileList[i][0] != previousWord:                                  # not the same word
            if i != 0:                                                      # if it is not the first line
                outputFile.write("\n")
            outputFile.write(fileList[i][0]+":"+fileList[i][1])             # write word:ID
            previousWord = fileList[i][0]
            previousID = fileList[i][1]
        else:                                                               # same word
            if fileList[i][1] != previousID:                                # if the ID number is not in output list
                outputFile.write(" " + fileList[i][1])
                previousID = fileList[i][1]

    outputFile.close()


######################### Task 3 ##################################

def lookup(collated_file, query_file):
    """
    This function finds the songs which contain every word in query_file.
    :param collated_file:
    :param query_file:
    :return:
    :complexity best case, worst case = O(qxMlog(U)+P)
    """

    # reading collated file into fileList
    file = open(collated_file, "r")
    fileList = []
    for line in file:
        line = line.strip().split(":")
        line[1] = line[1].split(" ")
        fileList.append(line)
    # print("lookup fileList = ", fileList)                             # fileList = [[word, [ID, ID],[word,[ID, ID]]]
    file.close()

    # reading query file into queryFileList
    queryFile = open(query_file, "r")
    queryFileList = []
    for line in queryFile:
        line = line.strip()
        queryFileList.append(line)
    # print("lookup queryFileList = ", queryFileList)                   # fileList = [word, word]
    queryFile.close()

    # write into another file
    outputFile = open("songs_id.txt", "w+")
    for i in range(len(queryFileList)):
        if i != 0:
            outputFile.write("\n")
        target = queryFileList[i]

        # BINARY SEARCH on every word in queryFileList
        low = 0
        high = len(fileList)-1
        found = False
        while low <= high:
            mid = (low + high) // 2                                     # find middle position
            if fileList[mid][0] == target:
                #return mid
                for j in range(len(fileList[mid][1])):
                    if j != 0:
                        outputFile.write(" ")                           # if 2nd ID, put space first
                    outputFile.write(fileList[mid][1][j])               # write in ID
                found = True
                break                                                   # stop finding for target
            elif fileList[mid][0] > target:                             # move to left
                high = mid - 1
            else:                                                       # move to right
                low = mid + 1
        if found == False:
            outputFile.write("Not found")                               # item not in the list

    outputFile.close()

############################################ M A I N ###############################################
if __name__=="__main__":
    process("example_songs.txt")                                            # Task 1
    collate("sorted_words.txt")                                             # Task 2
    lookup("collated_ids.txt", "example_queries.txt")                       # Task 3
