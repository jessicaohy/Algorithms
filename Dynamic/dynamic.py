# Jessica Oh Hui Yu

def best_score(pile1, pile2):
    """
    This function determine the optimal play, highest score and sequence, for the coin taking time.
    :param pile1:
    :param pile2:
    :return: (highestScore, choicesList):
    :complexity: O(NM)
    """

    # create table
    nCol = len(pile1)+1                                         # add one for empty
    nRow = len(pile2)+1                                         # add one for empty
    table = [None] * nRow
    for i in range(nRow):                                       #           pile1, pile1, pile1
        table[i] = [None] * nCol                                # pile2
    # printPretty(table)                                        # pile2
    # print("#####")

    # BASE CASES
    table[0][0] = 0
    if pile1 != []:
        table[0][1] = pile1[0]
    if pile2 != []:
        table[1][0] = pile2[0]

    # print("#####")
    # printPretty(table)

    for col in range(2, nCol):
        table[0][col] = table[0][col-2] + pile1[col-1]          # look at 2 positions before coz next player turn

    for row in range(2, nRow):
        table[row][0] = table[row-2][0] + pile2[row-1]

    # print("#####")
    # printPretty(table)

    # CHOOSING WHICH PILE TO TAKE
    for row in range(1, nRow):
        for col in range(1, nCol):

            if (col > 1):                                       # if there is left left
                leftLeft = table[row][col-2]
            else:                                               # no left left
                leftLeft = None

            leftUp = table[row-1][col-1]                        # definitely will have leftUp

            if (row >  1):                                      # if there is up up
                upUp = table[row-2][col]
            else:
                upUp = None                                     # no up up

            # put it the same as leftUp so is like saying there is only leftUp
            if leftLeft == None:
                leftLeft = leftUp
            if upUp == None:
                upUp = leftUp

            table[row][col] = max(pile1[col-1]+min(leftLeft,leftUp), pile2[row-1]+min(leftUp, upUp))
            # print("#######################################")
            # printPretty(table)

    highestScore = table[nRow-1][nCol-1]                    # bottom right
    #print(highestScore)

    # GETTING SEQUENCE
    choicesList = []
    row = nRow - 1
    col = nCol - 1
    # start from bottom right
    while row > 0 or col > 0:

        left = table[row][col-1]
        up = table[row-1][col]
        if left < up:                                       # if left is smaller than up
            choicesList.append(1)                           # move left, take from pile1
            col -= 1
        else:                                               # if up is smaller than up
            choicesList.append(2)                           # move up, take from pile2
            row -= 1
    # print("#######")
    # printPretty(table)
    return (highestScore, choicesList)


def is_in(grid, word):
    """
    This function find a word in a given Snake-words grid and returns the a list of tuples of the sequence.
    :param grid:
    :param word:
    :return: False or DPGrid[i][j]
    :complexity: O(KN^2)
    """

    # assigning numbers according to words that appear
    letterIndex = 0
    prevDPGrid = []

    while letterIndex < len(word):                                      # for every letter in word
        # print("###############################################")
        # print("start letterIndex  = ",letterIndex)
        # print("start letter = ", word[letterIndex])
        # print("start prevDPGrid = ", prevDPGrid)

        # creating a NEW dynamic grid                                   # new DPGrid for every letter
        DPGrid = []
        for i in range(len(grid)):
            DPGrid.append([])
            for j in range(len(grid)):
                DPGrid[i].append([])
        # print("EMPTY DPGrid = ", DPGrid)
        # print("previousGrid", prevDPGrid)

        # check through grid for similar letter
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] == word[letterIndex]:                         # if letter in grid is the target

                    if letterIndex == 0:
                        DPGrid[row][col].append((row, col))  # add current tuple

                    elif letterIndex > 0:
                        #print("-------CHECKING ADJACENT---------")

                        # CHECK ADJACENT FOR PREVIOUS VALID TUPLES #

                        # check up, upLeft, upRight
                        if row > 0:
                            if prevDPGrid[row-1][col] != []:
                                DPGrid[row][col]+=prevDPGrid[row-1][col]            # add in previous tuples
                            if col > 0 and prevDPGrid[row-1][col-1] != []:
                                DPGrid[row][col]+=prevDPGrid[row - 1][col-1]        # add in previous tuples
                            if col < len(grid)-1 and prevDPGrid[row-1][col+1] != []:
                                DPGrid[row][col]+=prevDPGrid[row - 1][col+1]        # add in previous tuples

                        # check left
                        if col > 0:
                            if prevDPGrid[row][col-1] != []:
                                DPGrid[row][col]+=prevDPGrid[row][col-1]            # add in previous tuples

                        # check right
                        if col < len(grid)-1:
                            if prevDPGrid[row][col+1] != []:
                                DPGrid[row][col]+=prevDPGrid[row][col+1]            # add in previous tuples

                        # check down, downLeft, downRight
                        if row < len(grid)-1:
                            if prevDPGrid[row+1][col] != []:
                                DPGrid[row][col]+=prevDPGrid[row+1][col]            # add in previous tuples
                            if col > 0  and prevDPGrid[row+1][col-1] != []:
                                DPGrid[row][col]+=prevDPGrid[row+1][col-1]          # add in previous tuples
                            if col < len(grid)-1 and prevDPGrid[row+1][col+1] != []:
                                DPGrid[row][col]+=prevDPGrid[row+1][col+1]          # add in previous tuples

                        # print("DPGrid[row][col] = ", DPGrid[row][col])
                        if DPGrid[row][col] !=  []:                                 # if is valid (has prev seq)
                            DPGrid[row][col].append((row, col))                     # add current tuple
                        # print("FINAL GRID", DPGrid)

        # add current grid to allDPGrid for comparison ltr
        prevDPGrid = []
        for i in range(len(grid)):
            prevDPGrid.append([])
            for j in range(len(grid)):
                prevDPGrid[i].append(DPGrid[i][j])

        # print("FINAL prevGrid = ", prevDPGrid)
        letterIndex += 1                                                    # go to next letter in the word
    # printPretty(DPGrid)

    # returning sequence
    for i in range(len(DPGrid)):
        for j in range(len(DPGrid[i])):
            if len(DPGrid[i][j]) == len(word):
                return DPGrid[i][j]
    return False                                                            # word not found

###################### M A I N ######################
if __name__=="__main__":

    print(best_score([20,5], [1]))
    print(best_score([1,2,3] , [1]))
    print(best_score([5,8,2,4,1,10,2], [6,2,4,5,6,9,8]))

    grid = [['a', 'b', 'c', 'd'],
            ['e', 'a', 'p', 'f'],
            ['e', 'p', 'g', 'h'],
            ['l', 'i', 'j', 'k']]
    word1 = 'apple'
    word2 = 'xylophone'
    print(is_in(grid, word1))
    print(is_in(grid, word2))

