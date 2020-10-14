# Jessica Oh Hui Yu


class Node:

    leafEnd = -1                                            # applies to all nodes
    def __init__(self, startIndex, endIndex, checkLeaf):
        """
        This function initialises the variables.
        :param startIndex:
        :param endIndex:
        :param checkLeaf:
        :complexity: O(1)
        """
        self.edgeList = [None] * 256                        # contains the nodes it is connected to, 256 chars in ascii

        # Trick 1 (startIndex, endIndex)
        self.startIndex = startIndex
        self.endIndex = endIndex

        self.checkLeaf = checkLeaf                          # True/False, 2 types of nodes: internal, leaf

        self.suffixLink = None

        self.suffixIndex = -1                               # on leaves, shows start index of suffix on txt


    def __getattribute__(self, item):                       # if node.endIndex == None, node.leafEnd will be used instead
        """
        This function gets the leaf end if node end index has not been assigned yet.
        :param item:
        :return: Node.leafEnd
        complexity: worst case = O(N), where N is the number of leaves in the path
        """
        if item == 'endIndex':                              # for endIndex
            if self.checkLeaf == True:                      # base case = reached leafEnd
                return Node.leafEnd                         # get leafEnd
        return super(Node, self).__getattribute__(item)     # default


class SuffixTree:

    def __init__(self):
        """
        This function initialises the variables.
        complexity: O(1)
        """
        self.size = -1                          # length of txt
        self.tree = Node(-1, -1, False)         # root
        self.tree.suffixLink = self.tree        # link to root
        self.suffixIndexCount = -1              # position of starting index of suffix in txt


    def buildTree(self, txt):
        """
        This function builds the suffix tree using Ukkonen's algorithm.
        :param txt:
        complexity: worst case = O(N), where N is the number of characters in txt
        """

        # Construct implicitST1
        letter = txt[0]                         # 1st letter
        letterIndex = ord(letter)               # position of letter in edgeList
        # self.tree.startIndex = 0
        # self.tree.endIndex = 0

        # Phases
        activeNode = self.tree                  # root
        activeEdge = None                       # containing letter
        activeEdgeIndex = -1                    # letter index in txt
        activeLength = 0
        remainder = 0                           # no. of suffixes to be added

        lastNewNode = None

        n = len(txt)
        for i in range(n):                      # for every letter

            # Rule 1
            Node.leafEnd = i                    # extend all leaves

            lastNewNode = None                  # no internal node waiting for suffix link to reset

            remainder += 1                      # new suffix added
            # add all suffixes to be added
            while remainder > 0:

                # not pointing to any letter on edge
                if activeLength == 0:
                    activeEdgeIndex = i
                    activeEdge = txt[i]

                activeEdgeletter = txt[activeEdgeIndex]
                activeEdgeletterIndex = ord(activeEdgeletter)      # find position in edgeList using ascii

                # no existing edge
                if activeNode.edgeList[activeEdgeletterIndex] == None:

                    # Rule 2
                    activeNode.edgeList[activeEdgeletterIndex] = Node(i, None, True)                # new leaf edge
                    activeNode.edgeList[activeEdgeletterIndex].suffixLink = self.tree               # link to root
                    self.suffixIndexCount += 1
                    activeNode.edgeList[activeEdgeletterIndex].suffixIndex = self.suffixIndexCount  # add suffix index to leaf
                    # print("RULE 2 self.tree.edgeList", self.tree.edgeList)


                    # if have internal node waiting for suffix link
                    if lastNewNode != None:
                        lastNewNode.suffixLink = activeNode     # pt suffix link frm last internal node to current activeNode
                        lastNewNode = None                      # no more mode waiting


                # there is existing edge from activeNode
                else:
                    # next node at end of edge from activeEdgeIndex
                    next = activeNode.edgeList[activeEdgeletterIndex]

                    # print("next.endIndex", next.endIndex)
                    # print("next.startIndex", next.startIndex)

                    # Trick 2
                    # if next.endIndex == None:
                    #   nextLength = next.leafEnd - next.startIndex + 1
                    # need __getattribute__ function so that endIndex will return leafEnd if is None
                    nextLength = next.endIndex - next.startIndex + 1

                    if activeLength >= nextLength:
                        # print("MOVED TO INTERNAL NODE")
                        activeEdgeIndex += nextLength
                        # prevActiveEdgeIndex = ord(activeEdge)
                        # activeEdge = txt[prevActiveEdgeIndex+nextLength]
                        activeLength -= nextLength
                        activeNode = next
                        continue

                    # Rule 3
                    # if char alr on edge
                    # no further action required
                    if txt[next.startIndex + activeLength] == txt[i]:
                        activeLength += 1
                        # print("RULE 3 self.tree.edgeList", self.tree.edgeList)

                        # if have node waiting
                        if lastNewNode != None and activeNode != self.tree:
                            lastNewNode.suffixLink = activeNode     # pt suffix link frm last internal node to current activeNode
                            lastNewNode = None                      # no more node waiting
                        break                                       # move to next phase


                    # Rule 2 (continued)
                    # active pt in the middle of edge and cur char not on edge

                    # add new internal node and new leaf
                    intNodeStartIndex = next.startIndex
                    intNodeEndIndex = next.startIndex + activeLength - 1
                    intNode = Node(intNodeStartIndex, intNodeEndIndex, False)   # new internal node
                    intNode.suffixLink = self.tree                              # link to root

                    activeEdgeletter = txt[activeEdgeIndex]                     # char on activeEdge
                    activeEdgeletterIndex = ord(activeEdgeletter)               # find position in edgeList
                    activeNode.edgeList[activeEdgeletterIndex] = intNode        # add new internal node to connect

                    # new leaf from internal node
                    curLetter = txt[i]                                          # current char
                    curLetterIndex = ord(curLetter)                             # find position in edgeList
                    intNode.edgeList[curLetterIndex] = Node(i, None, True)      # add leaf to internal node
                    intNode.edgeList[curLetterIndex].suffixLink = self.tree     # link to root
                    # intNode.edgeList[curLetterIndex].suffixIndex = i

                    self.suffixIndexCount += 1                                  # move to next position of suffix in txt
                    intNode.edgeList[curLetterIndex].suffixIndex = self.suffixIndexCount

                    next.startIndex += activeLength                             # next start index move to activeLength

                    nextLetter = txt[next.startIndex]                           # next index in txt
                    nextLetterIndex = ord(nextLetter)
                    intNode.edgeList[nextLetterIndex] = next                    # update internal node edge list


                    # print("RULE 2 CONTINUED self.tree.edgeList", self.tree.edgeList)

                    # if internal node waiting for suffix link
                    if lastNewNode != None:
                        lastNewNode.suffixLink = intNode                        # suffix link point to internal node
                    lastNewNode = intNode

                remainder -= 1                                                  # move to next suffix

                # get activeNode start and end indexes
                actStart = activeNode.startIndex
                actEnd = activeNode.endIndex
                # get root start and end indexes
                rootStart = self.tree.startIndex
                rootEnd = self.tree.endIndex

                # if is same as root
                if actStart == rootStart and actEnd == rootEnd:
                    # if more than 0
                    if activeLength > 0:
                        activeLength -= 1                                       # decrease by 1
                        activeEdgeIndex = i - remainder + 1
                # if is not same as root
                else:
                    activeNode = activeNode.suffixLink


