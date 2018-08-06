#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 19:34:35 2018

@author: Andrew Shillito

Current Status:
    fixed graph constructor
    edgeId's removed
    edgeIdDict removed
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
        self.graph[node].append(newEdge)
        self.graph[otherNode].append(newEdge)
        self.edges.append(newEdge)
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
        ansString = '\nGraph: Node-->Edges\n'
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
    
    def getNodeByName(name): #only used for graph construction
        try:
            return Node.nodeDict[name]
        except KeyError:
            return False
    
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
    
    def __str__(self):
        ansString = "Edge: "+self.tail.name+" --> "+self.head.name
        return ansString

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
    for line in file: #first build the graph nodes
        temp = re.split(r"\D", line)
        while "" in temp:
            temp.remove('')
        node = Node(temp[0])
        graph.addNode(node)
#    print(graph, "\n")
    file.close()
    file = open(fileName)
    for linePass2 in file: #now add the edges
        temp = re.split(r"\D", linePass2)
        while "" in temp:
            temp.remove('')
        node = Node.getNodeByName(temp[0])
        temp = temp[1:] #isolate edges
        if len(graph.graph[node])==0:
            for i in temp:
                otherNode = Node.getNodeByName(i)
                graph.addEdge(node, otherNode)
        else:
            #this node is a head for an edge
            #find src node of each edge
            #remove src node name from temp if present
            #continue and add all remaining edges as normal
            for edge in graph.graph[node]:
                if edge.getSrc().name in temp:
                    temp.remove(edge.getSrc().name)
            for j in temp:
                otherNode = Node.getNodeByName(j)
                graph.addEdge(node, otherNode)
    file.close()
    return None
    
def outputFileRead(fileName):
    file = open(fileName)
    for line in file:
        temp = re.split(r'\D', line)
        ans = temp[0]
    file.close()
    return ans