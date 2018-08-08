#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 19:34:35 2018

@author: Andrew Shillito

Current Status:
    Creation of newNode edges now works using set XOR
    need to modify other existing node lists - look into more set operations
    
    maybe should use sets instead of lists for graph[node]-edges
    
    the updateEdges func now works and also removes self-loops
    however, it would be most efficient to also change the edges
    of self.graph at the same time and to avoid creating new edges
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
  
    def contractNodes(self):
        """Karger's algorithm for random node contraction"""
        edge = self.selectEdge() #select random edge
        print("Selected", edge)
        source = edge.getSrc() #find source node
        dest = edge.getDest() #find destination node
        newNodeName = source.getName()+', '+dest.getName()
        
        #create new superNode
        newNode = Node(newNodeName)
        self.addNode(newNode) #just leave as is - broke program somehow when I changed addNode function
        
        #show edgeList components that are from self.graph[source] or self.graph[dest] - seems to work
#        testString = []
#        for i in self.edges:
#            if i in self.graph[source] or i in self.graph[dest]:
#                testString.append(str(i)[6:])
#        print("Relevant Self Edges: "+', '.join(testString))# - seems to work correctly
        
        #removes all edges from self.edges that are in self.graph[source] or self.graph[dest]
#        pdb.set_trace()
#        self.removeFromSelfEdges(source, dest)
        
        #show modified edgeList - seems to be modifying correctly
#        testString = []
#        for j in self.edges:
#            if j in self.graph[source] or j in self.graph[dest]:
#                testString.append(str(j)[6:])
#        print("Self Edges: "+', '.join(testString))
#         
         #show set operation result
#        print("set: ", set(self.graph[source]+self.graph[dest]))
#        testString = []
#        for z in set(self.graph[source])^set(self.graph[dest]): #I think this works
#            testString.append(str(z)[6:])
#        print("Set: "+', '.join(testString))
        
        self.graph[newNode]=list(set(self.graph[source])^set(self.graph[dest]))
        
        #possible way to update self.graph and self.edges
#        pdb.set_trace()
        print([str(i)[6:] for i in self.edges])
        self.updateEdges(source, dest, newNode)
        print([str(i)[6:] for i in self.edges])
        self.updateGraph(source, dest, newNode)
        
        del self.graph[source]
        del self.graph[dest]
        #associate edges in self.graph with new Node
        #make sure no self-loops in self.graph or self.edges
        #delete old nodes and related edges from self.graph and self.edges
        print(self)
        return None
    
    def updateEdges(self, source, dest, newNode):
        """Change source nodes/dest nodes of self.edges to newNode if necessary
        also removes self-loops - doesn't work - also would be preferable to use setters"""
        self.edges[:] = [edge if (edge.getSrc()!=source and edge.getDest()!=dest) and (edge.getSrc()!=dest and edge.getDest()!=source)\
                  else Edge(newNode, edge.head) if (edge.getSrc()==source or edge.getDest()==dest)\
                  else Edge(edge.tail, newNode) if (edge.getDest()==source or edge.getDest()==dest) else edge for edge in self.edges]        
        return None
    
    def updateGraph(self, source, dest, newNode):
        """computationally expensive"""
        self.graph = {node:[Edge(newNode, edge.head) if (edge.getSrc()==source or edge.getSrc()==dest) else Edge(edge.tail, newNode) if (edge.getDest()==source or edge.getDest()==dest) else edge for edge in self.graph[node]] for node in self.graph}
        for i in self.graph:
            for j in self.graph[i]:
                if j.getSrc()==source or j.getSrc()==dest:
                    j.setSrc(newNode)
                elif j.getDest()==source or j.getDest()==dest:
                    j.setDest(newNode)
        return None
    
    def selectEdge(self):
        randEdge = random.sample(self.edges, 1)[0]
        return randEdge
    
    def removeSelfLoops(self, node, otherNode, edge):
        return None
    
    def contract(self, node, otherNode):
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
        for node in self.graph:
            ansString+= node.getName()+" --> "
            for edge in self.graph[node]:
                temp = edge.getNodes()
                ansString+='('+temp[0].getName()+ "->" +temp[1].getName()+')'+', '
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
        
    def __str__(self):
        return "Node: "+self.name
    
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
    
    def setSrc(self, source):
        self.tail = source
        return None
    
    def setDest(self, dest):
        self.head = dest
        return None
    
    def __str__(self):
        ansString = "Edge: "+self.tail.name+" --> "+self.head.name
        return ansString

def constructGraph():
    directory = os.getcwd()+"\\testCases\\"
    graphs = []
    outputs = []
    testFiles = [i for i in os.listdir(directory) if "Output" not in i and ".rtf" not in i and "karger" not in i]
#    print(testFiles)
    outputFiles = [j for j in os.listdir(directory) if "Output" in j]
#    print(outputFiles)
    for x in range(len(testFiles)):
        graph = Graph()
        testFileRead(directory+testFiles[x], graph)
        outputs.append(outputFileRead(directory+outputFiles[x]))
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

def graphMinCut(graph, numTests):
    """graphMinCut takes graph of nodes/edges, duplicates it using copy.deepcopy() 
    and run's karger's contraction algorithm numTests times.
    graph.contractNodes() is the actual algorithm
    returns best (shortest length) min cut num"""
    best = 100000 #arbitrarily large num
    for i in range(numTests):
        testGraph = copy.deepCopy(graph)
        while len(testGraph)>2:
            testGraph.contractNodes() #this is the hub for the entire algorithm
        for node in testGraph: #exactly 2 tests but each should be the same length
            if len(testGraph[node])<best:
                best = len(testGraph[node])
                minCutGraph = copy.deepCopy(testGraph)
    return best, minCutGraph

def testProgram():
    graphList, outputs = constructGraph()
#    print(outputs)
    ans = graphList[0]
    print(ans, "\n")
#    ans.contractNodes()
    return ans #for now - graphList later
    