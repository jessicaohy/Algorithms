# Jessica Oh Hui Yu

class Edge:
    def __init__(self, targetVertex, weight):
        """
        This function initialise variables.
        :param targetVertex:
        :param weight:
        :complexity: O(1)
        """
        self.targetVertex = targetVertex                    # what it is connected to
        self.weight = weight

    def updateWeight(self, weight):
        """
        This function updates the weight of the edge.
        :param weight:
        :complexity: O(1)
        """
        self.weight = weight

class Vertex:
    def __init__(self, ID, word):
        """
        This function initialises the variables.
        :param ID:
        :param word:
        :complexity: O(1)
        """
        self.ID = ID
        self.word = word
        self.connectedVList = []                            # edges it is connected to

    def addEdge(self, targetVertex, weight):
        """
        This function creates an edge from Edge class and add it to connectedVList.
        :param targetVertex:
        :param weight:
        :complexity: O(1)
        """
        edge = Edge(targetVertex, weight)                   # create new edge
        self.connectedVList.append(edge)                    # add to list of connections

        # print("self.connectedVList = ", self.connectedVList)

class Graph:


    def __init__(self, vertices_filename, edges_filename):
        """
        This function reads the files and initialises the variables.
        :param vertices_filename:
        :param edges_filename:
        :complexity: O(V+E)
        """
        # reading vertices file into a list
        verticesFileData = open(vertices_filename, "r")
        verticesList = []
        for line in verticesFileData:
            line = line.strip("\n").split(" ")              # remove break line then split according to spaces
            verticesList.append(line)
        verticesFileData.close()                            # close file
        # print("verticesList = ", verticesList)

        # reading edges file into a list
        edgesFileData = open(edges_filename, "r")
        edgesList = []
        for line in edgesFileData:
            line = line.strip("\n").split(" ")              # remove break line then split according to spaces
            edgesList.append(line)
        edgesFileData.close()                               # close file
        # print("edgesList = ", edgesList)


        # CREATING A GRAPH                                      # [[None, None, None],[None, None..][None,..]]
                                                                # from (row), to (col)
        nVertices = int(verticesList[0][0])                     # total number of vertices

        # ADDING WORDS AND NODES
        self.graph = []
        for i in range(nVertices):
            self.graph.append(None)
        # print(self.graph)

        # adding new nodes
        for i in range(nVertices):
            vertex = Vertex(verticesList[i+1][0], verticesList[i+1][1])         # ADDED ID AND WORD
            self.graph[int(verticesList[i+1][0])] = vertex                      # position in self.graph = ID

        # print("AFTER PUTTING IN VALUES GRAPH = ")
        # self.printAllVertexes()

        # ADD CONNECTIONS
        for i in range(len(edgesList)):
            startVertex = int(edgesList[i][0])                                  # position in self.graph
            targetVertex = int(edgesList[i][1])



            # find cost (WEIGHTS)
            startVertexWord = self.graph[startVertex].word
            targetVertexWord = self.graph[targetVertex].word
            # print(startVertexWord)
            # print(targetVertexWord)

            for j in range(len(startVertexWord)):
                if startVertexWord[j] != targetVertexWord[j]:
                    startVertexLetter = startVertexWord[j]
                    startVertexAscii = ord(startVertexLetter) -96               # 1-26

                    targetVertexLetter = targetVertexWord[j]
                    targetVertexAscii = ord(targetVertexLetter) -96             # 1-26

                    # print("startVertexLetter", startVertexLetter, "targetVertexLetter", targetVertexLetter)
                    # print("startVertexAscii", startVertexAscii, "targetVertexAscii", targetVertexAscii)

                    cost = (startVertexAscii - targetVertexAscii)*(startVertexAscii - targetVertexAscii)
                    #print("cost",cost)


            self.graph[startVertex].addEdge(targetVertex, cost)                    # add connections from (position)



        # subgraph that contains the letter
        self.validGraph = []
        for i in range(len(self.graph)):
            self.validGraph.append(None)

        # TO SEE GRAPH
        #print("AFTER PUTTING IN VALUES GRAPH = ")
        #self.printAllVertexes()


    # Solving a ladder (finding shortest list of intermediate words)
    # BREADTH FIRST SEARCH
    def solve_ladder(self, start_vertex, target_vertex):
        """
        This function finds the shortest list of intermediate words which solves it.
        :param start_vertex:
        :param target_vertex:
        :return: (cheapestValidCost, cheapestValidList)
        :complexity: O(V+E)
        """
        nVertices = len(self.graph)

        # creating distance
        dist = []
        for i in range(nVertices):
            dist.append(float('inf'))
        # print("dist = ", dist)

        # creating visited
        pred = []
        for i in range(nVertices):
            pred.append(None)
        # print("pred = ", pred)

        # creating queue
        queue = []

        queue.append(start_vertex)
        dist[start_vertex] = 0

        # finding pred
        while queue != []:

            u = queue[0]                                            # similar to popping
            queue.remove(u)

            neighbourList = self.graph[u].connectedVList            # each item in list is an edge object

            for i in range(len(neighbourList)):

                v = neighbourList[i].targetVertex

                if dist[v] == float('inf'):
                    dist[v] = dist[u] + 1
                    pred[v] = u                                     # update where it came from
                    queue.append(v)                                 # add it into the queue
                # print("---------------------")
                # print("dist = ", dist)
                # print("queue = ", queue)
                # print("pred = ", pred)

        # FINDING SHORTEST PATH IN PRED
        shortestList = []
        shortestList.append(self.graph[target_vertex].word)
        fromVertex = pred[target_vertex]                            # update to where it came from

        while fromVertex != None:                                   # not the start yet
            shortestList.append(self.graph[fromVertex].word)
            fromVertex = pred[fromVertex]                           # update to where it came from
        # print(shortestList)
        if shortestList == []:
            return False
        return shortestList


    # Restricted word ladder (find cheapest word ladder)
    def cheapest_ladder(self, start_vertex, target_vertex, req_char):
        """
        This function find the cheapest word ladder.
        :param start_vertex:
        :param target_vertex:
        :param req_char:
        :return: (cheapestValidCost, cheapestValidList)
        :complexity: O(Elog(V))
        """
        nVertices = len(self.graph)

        # CHECK IF THERE IS THE REQUIRED WORD
        requiredVertexList = []

        for i in range(nVertices):

            # finding if the word contains the letter
            # for j in range(len(self.graph[i].word)):

            if self.graph[i].word[0] == req_char:                   # if first letter of the word is the req_char

                requiredVertexList.append(i)                        # add in the required vertex
        # print("requiredVertexList = ", requiredVertexList)

        # if does not have the required vertex
        if requiredVertexList == []:                                # if it does not have req_char
            # print("False")
            return False

        ############
        # finding subgraph that contains connections to required characters

        # START TO LETTER (going backwards)
        pred = self.dijkstra(start_vertex)                          # DIJKSTRA

        cheapestVertexList = []

        for i in range(len(requiredVertexList)):
            self.findCheapestPath(start_vertex, requiredVertexList[i], pred, cheapestVertexList)

        for i in range(len(cheapestVertexList)):
            self.validGraph[cheapestVertexList[i]] = self.graph[cheapestVertexList[i]]      # copy over the vertex

        # print(self.validGraph)

        # LETTER TO TARGET (going forward)
        for i in range(len(requiredVertexList)):
            edgeList = self.graph[requiredVertexList[i]].connectedVList
            for j in range(len(edgeList)):
                self.validGraph[edgeList[j].targetVertex] = self.graph[edgeList[j].targetVertex]

        # print(self.validGraph)

        cheapestValidCostPred = self.dijkstraValid(start_vertex, target_vertex)
        cheapestValidCost = cheapestValidCostPred[0]                            # CHEAPEST VALID COST
        validPred = cheapestValidCostPred[1]
        # print(validPred)
        # print("FINAL VALID CHEAPEST COST = ", cheapestValidCost)

        cheapestValidList = []
        self.findCheapestValidPath(start_vertex, target_vertex, validPred, cheapestValidList)
        # print("FINAL VALID CHEAPEST LIST = ", cheapestValidList)

        # print((cheapestValidCost, cheapestValidList))
        return (cheapestValidCost, cheapestValidList)


    def dijkstra(self, start_vertex):
        """
        This function finds uses Dijkstra algorithm on self.graph to get the pred
        which states which vertex each vertex should go to for the shortest cost path.
        :param start_vertex:
        :return: pred
        :complexity: O(Elog(V))
        """

        nVertices = len(self.graph)

        # DIJKSTRA'S ALGORITHM
        dist = []
        for i in range(nVertices):
            dist.append(float('inf'))
        # print("dist = ", dist)

        pred = []
        for i in range(nVertices):
            pred.append(0)
        # print("pred = ", pred)

        # priority queue
        queueHeap = []
        for i in range(nVertices):
            self.insertHeap(queueHeap, [i, float('inf')])
        # print("queueHeap = ", queueHeap)

        # u = self.removeMin(queueHeap)
        # u = u[0]
        dist[start_vertex] = 0

        while queueHeap != []:
            u = self.removeMin(queueHeap)
            u = u[0]
            # print("=====================================")
            # print("u = ", u)

            neighbourList = self.graph[u].connectedVList                        # each item in list is an edge object

            for i in range(len(neighbourList)):
                v = neighbourList[i].targetVertex
                currWeight = neighbourList[i].weight                            # cost

                # print("v = ", v, "currWeight = ", currWeight)

                #RELAX
                if dist[u] + currWeight < dist[v]:                              # if found a cheaper path

                    dist[v] = dist[u] + currWeight
                    pred[v] = u                                                 # update where it came from

                    #priority queue must be updated
                    self.updateHeap(queueHeap, v, dist[u] + currWeight)         # check from where it is updated

        # print("PRED = ", pred)
        return pred

    def dijkstraValid(self, start_vertex, target_vertex):
        """
        This function finds uses Dijkstra algorithm on self.validGraph to get the pred
        which states which vertex each vertex should go to for the shortest cost path.
        :param start_vertex:
        :param target_vertex:
        :return: pred
        :complexity: O(Elog(V))
        """

        nVertices = len(self.validGraph)

        # DIJKSTRA'S ALGORITHM
        dist = []
        for i in range(nVertices):
            dist.append(float('inf'))
        # print("dist = ", dist)

        pred = []
        for i in range(nVertices):
            pred.append(0)
        # print("pred = ", pred)

        # priority queue
        queueHeap = []
        for i in range(nVertices):
            self.insertHeap(queueHeap, [i, float('inf')])
        # print("queueHeap = ", queueHeap)

        # u = self.removeMin(queueHeap)
        # u = u[0]
        dist[start_vertex] = 0

        while queueHeap != []:
            u = self.removeMin(queueHeap)
            u = u[0]
            # print("=====================================")
            # print("u = ", u)

            if self.validGraph[u] != None:                              # only for vertices that exist
                neighbourList = self.validGraph[u].connectedVList  # each item in list is an edge object

                for i in range(len(neighbourList)):
                    v = neighbourList[i].targetVertex
                    currWeight = neighbourList[i].weight

                    # print("v = ", v, "currWeight = ", currWeight)

                    #RELAX
                    if dist[u] + currWeight < dist[v]:                  # found a cheaper path

                        dist[v] = dist[u] + currWeight
                        pred[v] = u                                     # update where it came from

                        #priority queue must be updated
                        self.updateHeap(queueHeap, v, dist[u] + currWeight)         # check from where it was updated

        cheapestCost = dist[target_vertex]

        # print("PRED = ", pred)
        return (cheapestCost, pred)



    def findCheapestPath(self, start_vertex, target_vertex, pred, cheapestList):
        """
        This function finds the cheapest path in self.graph using pred.
        :param start_vertex:
        :param target_vertex:
        :param pred:
        :param cheapestList:
        :return: cheapestList
        :complexity: O(V)
        """

        cheapestList.append(target_vertex)                      # add in word of the target vertex
        fromVertex = pred[target_vertex]                        # go to vertex where it is from


        while fromVertex != start_vertex:
            # print("cheapL = ", cheapestList)
            cheapestList.append(fromVertex)                     # add in the word of vertex where it is from
            fromVertex = pred[fromVertex]                       # update the vertex where it is from

        cheapestList.append(start_vertex)                       # add in word of start vertex

        return cheapestList

    def findCheapestValidPath(self, start_vertex, target_vertex, pred, cheapestValidList):
        """
        This function finds the cheapest path in self.validGraph using pred.
        :param start_vertex:
        :param target_vertex:
        :param pred:
        :param cheapestValidList:
        :return: cheapestValidList
        :complexity: O(V)
        """

        # FINDING SHORTEST PATH IN PRED

        cheapestValidList.append(self.graph[target_vertex].word)        # add in word of the target vertex
        fromVertex = pred[target_vertex]                                # go to vertex where it is from

        while fromVertex != 0:
            cheapestValidList.append(self.graph[fromVertex].word)       # add in the word of vertex where it is from
            fromVertex = pred[fromVertex]                               # update the vertex where it is from
        cheapestValidList.append(self.graph[0].word)                    # add in word of start vertex
        return cheapestValidList

    ############################## HEAP #################################
    # update with smaller weight
    def updateHeap(self, heap, vertex, newWeight):
        """
        This function updates the heap, swapping the parent and child if the parent is larger than the child.
        :param heap:
        :param vertex:
        :param newWeight:
        :complexity: O(log(V))
        """

        # child = vertex

        for i in range(len(heap)):
            if heap[i][0] == vertex:
                heap[i][1] = newWeight                          # update weight
                child = i
        # print(child)
        # print(heap)

        parent = (child - 1) // 2                               # halving the list to get to the parent position
        # swap upwards
        # check if child is smaller than parent until root
        while parent>=0 and heap[parent][1] > heap[child][1]:

            # swap
            tmp = heap[child]
            heap[child] = heap[parent]
            heap[parent] = tmp

            # move to next
            child = parent
            parent = (parent-1)//2                              # halving the list to get to the parent position

            #print("updatedHeap = ", heap)
            #print("child = ", child)
            #print("parent = ", parent)


    def insertHeap(self, heap, item):
        """
        This function insert the item into the heap,
        swapping the parent and child if the parent is larger than the child.
        :param heap:
        :param item:
        :complexity: O(log(V))
        """

        heap.append(item)
        child = len(heap) - 1
        parent = (child-1)//2                                   # halving the list to get to the parent position

        # swap upwards
        # check if child is smaller than parent until root
        while child>0 and heap[parent][1] > heap[child][1]:
            # swap
            tmp = heap[child]
            heap[child] = heap[parent]
            heap[parent] = tmp

            # move to next
            child = parent
            parent = (parent-1)//2

    def removeMin(self, heap):
        """
        This function remove the item in the heap,
        move last item to first item in the heap,
        swapping the parent and child if the parent is larger than the child.
        :param heap:
        :return minItem:
        :complexity: O(log(V))
        """

        # store minimum which is the first item in heap
        minItem = heap[0]

        # move the last item to the front
        heap[0] = heap[len(heap)-1]                             # put the last item to the front
        heap.pop()                                              # remove last item

        #print("popped Heap = ", heap)

        # if nothing in queue anymore
        if heap == []:
            return minItem

        # swap downwards if larger than child

        parent = 0
        leftChild = (parent*2)+1                                # move to next half of the array
        rightChild = (parent*2)+2                               # move to next half of the array


        # while there is child
        while leftChild < len(heap) or rightChild < len(heap):

            # got both child
            if leftChild < len(heap) and rightChild < len(heap):

                if heap[leftChild][1] < heap[rightChild][1]:
                    minChild = leftChild
                else:
                    minChild = rightChild

            # has only left child
            elif leftChild < len(heap):
                minChild = leftChild
            # cannot have right without left

            # check if need swap with min child
            if heap[minChild][1] < heap[parent][1]:

                tmp = heap[parent]
                heap[parent] = heap[minChild]
                heap[minChild] = tmp

                # update parent and child to move
                parent = minChild
                leftChild = (parent * 2) + 1                    # move to next half of the array
                rightChild = (parent * 2) + 2                   # move to next half of the array
            # at the correct position
            else:
                break
        #print("finishedPopHeap = ", heap)
        return minItem


################## M A I N #######################
if __name__=="__main__":
    my_graph = Graph("vertices.txt", "edges.txt")
    my_graph.solve_ladder(0,6)

    # my_graph.cheapest_ladder(0, 6, 'a')
    # my_graph.cheapest_ladder(0, 6, 'z')
    my_graph.cheapest_ladder(0, 6, 'c')               
