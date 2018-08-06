#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 19:34:35 2018

@author: Andrew Shillito

Current issues:    
    Finally fixed edge issue when constructing new graphs
"""

import random, copy, os, re, pdb

class Graph(object):
    def __init__(self): 
        self.edges = []
        self.graph = {}
        
    def getNodes(self):
        return list(self.graph.keys())
    
    def getEdges(self):
        return self.edges[:]

    def combineNodes(self, node, otherNode):
        return None
    
    def contractNodes(self, edge):
        return None
    
    def selectEdge(self):
        randEdge = random.sample(self.edges, 1)[0]
        return randEdge
    
    def removeSelfLoops(self, node, otherNode):
        return None
    
    def addNode(self, node):
        self.graph[node]=[]
        return None
    
    def removeNode(self, node):
        del self.graph[node]
        try:
            del self.graph[node]
        except KeyError:
            print("No such node in Graph")
        return None
    
    def addEdge(self, node, otherNode):
        newEdge = Edge(node, otherNode)
#        revEdge = Edge(otherNode, node)
        self.graph[node].append(newEdge)
#        self.graph[otherNode].append(revEdge)
        self.edges.append(newEdge)
#        self.edges.append(revEdge)
        return None
    
    def removeEdge(self, edge):
        try:
            self.edges.remove(edge)
            self.graph[edge.getSrc()].remove(edge)
            self.graph[edge.getDest()].remove(edge)
        except ValueError:
            print("Edge not present")
            pass
        return None
    
    def __str__(self):
        ansString = ''
        for node in list(self.graph.keys()):
            ansString+= node.getName()+" --> "
            for edge in self.graph[node]:
                temp = edge.getNodes()
                for i in temp:
                    if i!=node:
                        ansString+= i.getName()+', '
                        break
            ansString = ansString[:-2]+'\n'
        return ansString[:-1]
    

class Node(object):
    
    nodeDict = {} #purely for building graphs from the files given
    
    def __init__(self, name): #edges a list of edges??
        if name in Node.nodeDict:
            print("KeyError: A Node with that name already exists")
            raise KeyError
        else:
            self.name = name
            Node.nodeDict[name]=self
    
    def getName(self):
        return self.name
    
    def getNodeByName(name):
        try:
            return Node.nodeDict[name]
        except KeyError:
            return False
    
class Edge(object):
    
    edgeIdDict = {}
    edgeId = 0
    
    def __init__(self, tail, head):
        self.tail = tail
        self.head = head
        self.id = Edge.edgeId
        Edge.edgeIdDict[self.id]=self
        Edge.edgeId+=1

    def getNodes(self):
        return (self.tail, self.head)
    
    def getSrc(self):
        return self.tail
    
    def getDest(self):
        return self.head
    
    def getEdgeById(ID):
        return Edge.edgeIdDict[ID]
    
#n1 = Node('1')
#n2 = Node('2')
#n3 = Node('3')
#graph = Graph()
#graph.addNode(n1)
#graph.addNode(n2)
#graph.addNode(n3)
#graph.addEdge(n1, n2)
#graph.addEdge(n1, n3)
#graph.addEdge(n3, n2)
#graph.addEdge(n3, n1)
#graph.removeEdge(graph.getEdges()[0])

def constructGraph():
    directory = os.path.abspath("..")+"\\testCases"
    graphs = []
    outputs = []
    testFiles = [i for i in os.listdir(directory) if "Output" not in i and ".rtf" not in i]
#    print(testFiles)
    outputFiles = [j for j in os.listdir(directory) if "Output" in j]
#    print(outputFiles)
    for x in range(len(testFiles)):
        graph = Graph()
        testFileRead(directory+"\\"+testFiles[x], graph)
        outputs.append(outputFileRead(directory+"\\"+outputFiles[x]))
        graphs.append(graph)
        Node.nodeDict = {}
    return graphs, outputs

def testFileRead(fileName, graph):
    file = open(fileName)
#    pdb.set_trace()
    for line in file:
        flag = 0 #keeps track of if temp[0] already exists as a Node.nodeDict key
        temp = re.split(r"\D", line)
        while "" in temp:
            temp.remove('')
#        node = (Node.getNodeByName(temp[0]) or Node(temp[0]))
        if temp[0] not in Node.nodeDict:    
            #node by that name does not exist
            node = Node(temp[0])
            graph.addNode(node)
        else:
            #node by that name already exists
            node = Node.getNodeByName(temp[0])
            flag+=1
        for destNode in temp[1:]:
            existingNode = Node.getNodeByName(destNode)
            if existingNode:
                graph.addEdge(node, existingNode)
            else:
                #key(node) does not exist
                newNode = Node(destNode)
                graph.addNode(newNode)
                graph.addEdge(node, newNode)
    file.close()
    return None
    
def outputFileRead(fileName):
    file = open(fileName)
    for line in file:
        ans = line[0]
    file.close()
    return ans
    