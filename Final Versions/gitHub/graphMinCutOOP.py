#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 19:34:35 2018

@author: Andrew Shillito

Current issues:
    no testing for node membership when adding edges
    
    Node.nodeList as class wide var doesn't allow for multiple graph
    constructions in single run unless it is cleared before each
    which could be done
    
    the checking for duplicate edges is incorrect in graph builder
    (and unfinished)
    
    currently the graph keys are node objects which is creating problems
    when trying to index into the graph while adding edges in constructor
    
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
    #appends the same edge referenced all three places
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
    
    nodeList = []
    
    def __init__(self, name): #edges a list of edges??
        self.name = name
        Node.nodeList.append(name)
    
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
    print(testFiles)
    outputFiles = [j for j in os.listdir(directory) if "Output" in j]
    print(outputFiles)
    for x in range(len(testFiles)):
        graph = Graph()
        testFileRead(directory+"\\"+testFiles[x], graph)
        outputs.append(outputFileRead(directory+"\\"+outputFiles[x]))
        graphs.append(graph)
        Node.nodeList = []
    return graphs, outputs

def testFileRead(fileName, graph):
    file = open(fileName)
#    pdb.set_trace()
    for line in file:
        temp = re.split(r"\D", line)
        while "" in temp:
            temp.remove('')
        if temp[0] not in Node.nodeList:    
            node = Node(temp[0])
            graph.addNode(node)
        else:
            for i in list(graph.graph.keys()):
                if i.name==temp[0]:
                    node = i
                    break
        for destNode in temp[1:]:
            if destNode not in Node.nodeList:
                otherNode = Node(destNode)
                graph.addNode(otherNode)
                graph.addEdge(node, otherNode)
            else:
                for j in list(graph.graph.keys()):
                    if j.name==destNode:
                        otherNode=j
                        break
#                if 
    file.close()
    return None
    
def outputFileRead(fileName):
    file = open(fileName)
    for line in file:
        ans = line[0]
    file.close()
    return ans
    