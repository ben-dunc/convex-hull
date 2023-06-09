#!/usr/bin/python3
from PriorityQueue import PriorityQueue, PriorityQueueHeap, PriorityQueueArray
from CS312Graph import *
import time
import array

array.array('i')


class NetworkRoutingSolver:
    prev = None
    dist = None

    def __init__(self):
        pass

    def initializeNetwork(self, network):
        assert (type(network) == CS312Graph)
        self.network = network

    def getShortestPath(self, destIndex):
        self.dest = destIndex
        path_edges = []
        total_length = 0
        nodeId = destIndex
        prevNodeId = self.prev[nodeId]
        while prevNodeId != -1:
            prevNode = self.network.nodes[prevNodeId]

            edge = None
            for e in prevNode.neighbors:
                if e.dest.node_id == nodeId:
                    edge = e
                    break

            if edge is None:
                print("Error: no edge found.")
                break

            path_edges.append((edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)))
            total_length += edge.length

            nodeId = prevNodeId
            prevNodeId = self.prev[nodeId]
        return {'cost': total_length, 'path': path_edges}

    # Time & space complexity same as dijkstras()
    def computeShortestPaths(self, srcIndex, use_heap=False):
        self.source = srcIndex
        t1 = time.time()

        (self.prev, self.dist) = self.dijkstras(srcIndex, self.network.nodes, PriorityQueueHeap() if use_heap else PriorityQueueArray())

        t2 = time.time()
        return t2 - t1

    # Time: O(|V| * max(Dm, Dk) + |E|)
    # Space: O(|V| * max(Dm, Dk) + |E|)
    def dijkstras(self, srcIndex, nodes, q: PriorityQueue) -> (array.array, array.array):
        numNodes = len(self.network.nodes)
        prev = array.array('i', (-1 for i in range(0, numNodes)))

        q.makeQueue(nodes)
        q.decreaseKey(srcIndex, 0)

        while not q.isEmpty():
            nodeId = q.deleteMin()
            node = nodes[nodeId]
            curDist = q.getDist(nodeId)
            for edge in node.neighbors:
                if q.getDist(edge.dest.node_id) > curDist + edge.length or q.getDist(edge.dest.node_id) == q.INF:
                    q.decreaseKey(edge.dest.node_id, curDist + edge.length)
                    prev[edge.dest.node_id] = nodeId

        dist = q.getKeys()
        return prev, dist

    def testQueue(self, nodes):
        q = PriorityQueueHeap()
        q.makeQueue(nodes)

        print("STARTING TEST")

        for i in range(len(nodes)):
            q.decreaseKey(i, len(nodes) - i)
            print("decreased node " + str(i) + " to " + str(len(nodes) - i) + "\n")
            q.print()

        print("==============")

        while not q.isEmpty():
            min = q.deleteMin()
            print("min is " + str(min) + "\n")
            q.print()

        print("FINISHED TEST")
