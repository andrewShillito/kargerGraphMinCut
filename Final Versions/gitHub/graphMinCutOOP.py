#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 19:34:35 2018

@author: Andrew Shillito

Current issues:
    no testing for node membership when adding edges - will fix
    
    having node.getEdges() makes graph dict redundant
    if I remove getEdges() I can accomplish the same thing
    by indexing into the graph[node] which will make more sense
"""

import random, copy, os, re

class Graph(object):
    def __init__(self): 
#assumes graph is pre-constructed dict (nodes/edges) adjacency list
        self.nodes = []
        self.edges = []
        self.graph = {}
        
    def getNodes(self):
        return self.nodes[:]
    
    def getEdges(self):
        return self.edges[:]
    
#    def getGraphCopy(self):
#        return copy.deepcopy(self.graph)
    
    def combineNodes(self, node, otherNode):
        return None
    
    def contractNodes(self, node, otherNode):
        return None
    
    def selectEdge(self, edges):
        randEdge = random.sample(edges, 1)[0]
        return randEdge
    
    def removeSelfLoops(self, node, otherNode):
        return None
    
    def addNode(self, node):
        self.nodes.append(node)
        return None
    
    def removeNode(self, node):
        self.nodes.remove(node) #this is O(n)
        return None
    
    def addEdge(self, node, otherNode):
        newEdge = Edge(node, otherNode)
        node.edges.append(newEdge)
        otherNode.edges.append(newEdge)
        self.edges.append(newEdge)
    #appends the same edge refernced all three places
        return None
    
    def removeEdge(self, edge):
        try:
            self.edges.remove(edge)
            edge.getSrc().edges.remove(edge)
            edge.getDest().edges.remove(edge)
        except ValueError:
            print("Edge not present")
            pass
        return None
    
    def __str__(self):
        ansString = ''
        for node in self.nodes:
            ansString+= node.getName()+" --> "
            for edge in node.getEdges():
                temp = edge.getNodes()
                for i in temp:
                    if i!=node:
                        ansString+= i.getName()+', '
                        break
            ansString = ansString[:-2]+'\n'
        return ansString[:-1]
    

class Node(object):
    def __init__(self, name): #edges a list of edges??
        self.name = name
#        self.edges = []
        
#    def getEdges(self):
#        return self.edges[:]
    
    def removeEdge(self, edge):
        return None
    
    def getName(self):
        return self.name
    
class Edge(object):
    def __init__(self, tail, head):
        self.tail = tail
        self.head = head

    def getNodes(self):
        return (self.tail, self.head)
    
    def getSrc(self):
        return self.tail
    
    def getDest(self):
        return self.head
    
n1 = Node('1')
n2 = Node('2')
n3 = Node('3')
graph = Graph()
graph.addNode(n1)
graph.addNode(n2)
graph.addNode(n3)
graph.addEdge(n1, n2)
graph.addEdge(n1, n3)
graph.addEdge(n3, n2)
graph.addEdge(n3, n1)
#graph.removeEdge(graph.getEdges()[0])

def constructGraph():
    directory = os.getcwd()+"\\testCases"
    tests = []
    outputs = []
    graphs = []
    y = 0
    testFiles = [i for i in os.listdir(directory) if "Output" not in i]
    testFiles = testFiles[:-1]
    outputFiles = [j for j in os.listdir(directory) if "Output" in j]
    for x in range(len(testFiles)):
        graph = []
        temp = testFileRead(testFiles[x], graph)
        outputs.append(outputFileRead(outputFiles[x]))
    return graphs, outputs

def testFileRead(fileName, graph):
    file = open(fileName)
    for line in file:
        temp = re.split(r"\D", line)
        while "" in temp:
            temp.remove('')
        node = Node(temp[0])
        graph.addNode(node)
        for edge in temp[1:]:
            pass #left off here - fixing node and graph implementation-
            #graph now has self.graph which is a dict node-->edges
            #must change node class, Graph.self.graph, graph.addNode graph.addEdge
            #graph.removeEdge, graph.removeNode, and graph.__str__
    file.close()
    
def outputFileRead(fileName):
    file = open(fileName)
    for line in file:
        ans = line[0]
    file.close()
    return ans
    