import array
import math

array.array('i')


class PriorityQueue:
    INF = 1000000000
    DNE = -1
    keys: array = None

    def makeQueue(self, nodes):
        pass

    def decreaseKey(self, index, value):
        pass

    def deleteMin(self) -> int:
        pass

    def isEmpty(self) -> bool:
        pass

    def getKeys(self) -> array.array:
        pass

    def getDist(self, nodeId) -> float:
        pass


class PriorityQueueHeap(PriorityQueue):
    heap: array = None
    point: array = None
    keys: array = None
    finalkeys: array = None

    def __init__(self):
        pass

    # Time: O(n)
    # Space: O(n)
    def makeQueue(self, nodes):
        self.heap = array.array('i', (node.node_id for node in nodes))
        self.point = array.array('i', (node.node_id for node in nodes))
        self.keys = array.array('f', (self.INF for i in range(0, len(nodes))))
        self.finalkeys = array.array('f', (self.INF for i in range(0, len(nodes))))

    # Time: O(log n)
    # Space: O(log n)
    def decreaseKey(self, nodeId: int, value: float):
        self.keys[nodeId] = value
        self.finalkeys[nodeId] = value
        self.bubbleUp(self.getHeapIndex(nodeId))

    # Time: O(log n)
    # Space: O(log n)
    def deleteMin(self) -> int:
        minIndex = 0
        minNodeId = self.heap[minIndex]
        self.finalkeys[self.getNodeId(minIndex)] = self.keys[self.getNodeId(minIndex)]
        self.keys[self.getNodeId(minIndex)] = self.DNE
        self.bubbleDown(minIndex)
        return minNodeId

    # Time: O(log n)
    # Space: O(log n)
    def bubbleUp(self, heapIndex):
        hi = heapIndex
        if hi == 0:
            return
        pi = self.getParentIndex(hi)
        if self.doSwapNodes(pi, hi):
            self.swapNodes(pi, hi)
            self.bubbleUp(pi)

    # Time: O(log n)
    # Space: O(log n)
    def bubbleDown(self, heapIndex):
        pi = heapIndex
        fi = math.floor(self.getChildIndex(pi))  # first child index

        if fi >= len(self.heap):
            pass
        elif fi + 1 >= len(self.heap) and self.doSwapNodes(pi, fi):
            self.swapNodes(pi, fi)
        elif fi + 1 >= len(self.heap):
            pass
        elif self.getNodeWeightByHI(fi) < self.getNodeWeightByHI(fi + 1) and self.doSwapNodes(pi, fi):
            self.swapNodes(pi, fi)
            self.bubbleDown(fi)
        elif self.doSwapNodes(pi, fi + 1) and not (self.getNodeWeightByHI(fi) >= 0 > self.getNodeWeightByHI(fi + 1)):
            self.swapNodes(pi, fi + 1)
            self.bubbleDown(fi + 1)
        elif self.doSwapNodes(pi, fi):
            self.swapNodes(pi, fi)
            self.bubbleDown(fi)

    # Time: O(1)
    # Space: O(1)
    def doSwapNodes(self, parentHeapIndex, childHeapIndex) -> bool:
        if parentHeapIndex >= len(self.keys) or childHeapIndex >= len(self.keys):
            return False

        pw = self.getNodeWeightByHI(parentHeapIndex)
        cw = self.getNodeWeightByHI(childHeapIndex)
        return (pw > cw or (pw < 0 <= cw)) and not (pw >= 0 > cw)

    # Time: O(1)
    # Space: O(1)
    def swapNodes(self, heapI1, heapI2):
        nodeId1 = self.getNodeId(heapI1)
        nodeId2 = self.getNodeId(heapI2)

        (self.heap[heapI1], self.heap[heapI2]) = (self.heap[heapI2], self.heap[heapI1])
        (self.point[nodeId1], self.point[nodeId2]) = (self.point[nodeId2], self.point[nodeId1])

    # Time: O(1)
    # Space: O(1)
    def getNodeWeight(self, nodeId):
        return self.keys[nodeId]

    # Time: O(1)
    # Space: O(1)
    def getNodeWeightByHI(self, heapIndex):
        return self.getNodeWeight(self.getNodeId(heapIndex))

    # Time: O(1)
    # Space: O(1)
    def getHeapIndex(self, nodeId):
        return self.point[nodeId]

    # Time: O(1)
    # Space: O(1)
    def getNodeId(self, heapIndex):
        return self.heap[heapIndex]

    # Time: O(1)
    # Space: O(1)
    def getChildIndex(self, index) -> int:
        return index * 2 + 1

    # Time: O(1)
    # Space: O(1)
    def getParentIndex(self, index) -> int:
        return math.floor((index - 1) / 2)

    # Time: O(1)
    # Space: O(1)
    def isEmpty(self) -> bool:
        return self.getNodeWeightByHI(0) < 0

    # Time: O(1)
    # Space: O(1)
    def getKeys(self) -> array.array:
        return self.finalkeys

    # Time: O(1)
    # Space: O(1)
    def getDist(self, nodeId) -> float:
        return self.finalkeys[nodeId]

    # I didn't calculate the complexity of this method because I only used it for debugging
    def print(self):
        index = "index: "
        for i in range(0, len(self.keys)):
            index += str(i) + " "
        points = "point:  "

        heap = "heap:   \n\t "
        for k in range(0, math.floor(math.log(len(self.heap), 2) - 1)):
            heap += " "
        heap += str(self.heap[0]) + "\n\t"
        i = 0
        j = 0
        for nodeId in self.heap:
            if j == 0:
                j = 1
                continue
            for k in range(0, math.floor(math.log(len(self.heap), 2) - j)):
                heap += " "
            heap += str(nodeId)
            if i == j * 2 - 1:
                i = 0
                j += 1
                heap += "\n\t"
            else:
                heap += " "
                i += 1

        keys = "keys:   "
        for dist in self.keys:
            keys += (str(dist) if dist >= 0 else ('DNE' if dist == -1 else 'INF')) + " "
        for point in self.point:
            points += str(point) + "   "
        print(index)
        print(keys)
        print(points)
        print(heap)


class PriorityQueueArray(PriorityQueue):
    queue: array = None
    keys: array = None

    def __init__(self):
        pass

    # Time: O(n)
    # Space: O(n)
    def makeQueue(self, nodes):
        self.queue = array.array('i', (node.node_id for node in nodes))
        self.keys = array.array('f', (self.INF for i in range(0, len(nodes))))

    # Time: O(1)
    # Space: O(1)
    def decreaseKey(self, nodeId: int, value: float):
        self.keys[nodeId] = value

    # Time: O(n)
    # Space: O(1)
    def deleteMin(self) -> int:
        minIndex = 0
        minWeight: int = self.keys[self.queue[0]]
        for i in range(0, len(self.queue)):
            if (self.keys[self.queue[i]] < minWeight and self.keys[self.queue[i]] != self.INF) or minWeight < 0:
                minIndex = i
                minWeight = self.keys[self.queue[i]]
        return self.queue.pop(minIndex)

    # Time: O(1)
    # Space: O(1)
    def isEmpty(self) -> bool:
        return len(self.queue) == 0

    # Time: O(1)
    # Space: O(1)
    def getKeys(self) -> array.array:
        return self.keys

    # I didn't calculate the complexity of this method because I only used it for debugging
    def print(self):
        print("\n\n")
        index = "index: "
        queue = "queue: "
        keys = "keys:  "
        for i in range(0, len(self.keys)):
            index += str(i) + " "
        for nodeId in self.queue:
            queue += str(nodeId) + " "
        for dist in self.keys:
            keys += str(dist) + " "
        print(index)
        print(queue)
        print(keys)

    # Time: O(1)
    # Space: O(1)
    def getDist(self, nodeId) -> float:
        return self.keys[nodeId]