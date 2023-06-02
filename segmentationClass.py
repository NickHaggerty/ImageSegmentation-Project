import numpy as np
import matplotlib.pyplot as plt
import math
from collections import deque

class segmentationClass:

    #set default variables, subject to change
    p0 = 1
    x_a = np.array([0,0])
    x_b = np.array([1,1])
    

    def RGBDist(self, a, b):
        # Calculate the squared difference between the red components of the two colors
        r = (int(a[0]) - int(b[0]))**2
        
        # Calculate the squared difference between the green components of the two colors
        g = (int(a[1]) - int(b[1]))**2
        
        # Calculate the squared difference between the blue components of the two colors
        b = (int(a[2]) - int(b[2]))**2
        
        # Calculate the total distance as the square root of the sum of the squared differences
        total = math.sqrt(r+g+b)
        
        # Return the total distance
        return total



    def euclideanDist(self, a, b):
        # Calculate the squared difference between the x-coordinates of the two points
        x = (a[0] - b[0])**2
        
        # Calculate the squared difference between the y-coordinates of the two points
        y = (a[1] - b[1])**2
        
        # Calculate the total distance as the square root of the sum of the squared differences
        total = math.sqrt(x+y)
        
        # Return the total distance
        return total


    #PROVIDED CODE
    def BFS(self, graph, s, t, parent):
        # Mark all the vertices as not visited
        visited = [False]*len(graph)
 
        # Create a queue for BFS
        queue = []
 
        # Mark the source node as visited and enqueue it
        queue.append(s)
        visited[s] = True
 
         # Standard BFS Loop
        while queue:
            # Dequeue a vertex from queue and print it
            u = queue.pop(0)

            w, h = graph.shape
            # Get all adjacent vertices of the dequeued vertex u
            # If a adjacent has not been visited, then mark it
            # visited and enqueue it
            for ind, val in enumerate(graph[u]):
                if visited[ind] == False and val > 0 :
                    # If we find a connection to the sink node,
                    # then there is no point in BFS anymore
                    # We just have to set its parent and can return true
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u
        
        # We didn't reach sink in BFS starting
        # from source, so return false
        return True if visited[t] else False

    #PROVIDED CODE
    def dfs(self, graph,s,hitNodes):
        hitNodes[s]=True
        for i in range(len(graph)):
            if graph[s][i]>0 and not hitNodes[i]:
                self.dfs(graph,i,hitNodes)
                
                


    def fFolk(self, graph, source, sink, OShape):
        #make a new graph to edit
        res_graph = graph.copy()
        #n is the number of nodes
        n = len(res_graph)
        #get the width and height of our adjjacency matrix
        w, h = res_graph.shape
        #copy sink to be changed later
        s = sink

        #make an empty list of -1 to keep track of node connection trail
        parent = [-1] * n
        #set max flow to 0
        max_flow = 0

       #continute the code while there is a path from source to sink
        while self.BFS(res_graph, source,sink,parent):
            #set the path variable
            path_flow = 9999999
            #reset the sink
            s = sink
            #while we havent reached the source...
            while(s != source):
                #take the minimum value between the path_flow or the weight in the res_graph
                path_flow = min(path_flow, res_graph[parent[s]][s])
                #set the connection
                s = parent[s]

            #add to max_flow
            max_flow += path_flow

            #set another temporary sink value
            secSource = sink
            #while we have yet to reach the source...
            while (secSource != source):
                #follow the path
                u = parent[secSource]
                # Decrease the flow from u to secSource by path_flow
                res_graph[u][secSource] -= path_flow

                # Increase the flow from secSource to u by path_flow
                res_graph[secSource][u] += path_flow

                #iterate along the path and run again until you hit source
                secSource = parent[secSource]
                

        #create an empty array to keep track of nodes hit
        hitNodes=len(res_graph)*[False]
        #run bfs on altered res_graph to recieve the minimum cuts
        self.dfs(res_graph,s,hitNodes)

        #a list to keep track of nodes cut from source
        bgNodes = []
        #iterate through all weights
        for i in range(w):
            for j in range(h):
                #if a node is zero now, but wasnt zero before, then it has been removed.
                #the last and is to check it was the most recent removed edge. 
                if res_graph[i][j] == 0 and graph[i][j] > 0 and hitNodes[i]:
                    #if that edge connected to the source, I.e is a background node
                    if i == 0:
                        #add it to the list of nodes in the background
                        bgNodes.append(j)

        #create a new np.array the same size as the original image
        results = np.zeros((OShape[0], OShape[1]), dtype=int)
        #count nodes
        count = 1
        #iterate through the original image co-ords
        for i in range(OShape[0]):
            for j in range(OShape[1]):
                #if the node is part of the background
                if count not in bgNodes:
                    #add a 0 to its value
                    results[i][j] = 1
                    #iterate node
                count += 1

        #return the binary array
        return results
        


    def segmentImage(self, I):
        #save image
        img = I

        #collect the shapes of the image, in compact form and expanded
        OShape = tuple(img.shape)
        w, h, d = tuple(img.shape)

        #count the nodes in the image
        nodes = img.shape[0]*img.shape[1]
        #create our adjacency matrix flow network of size node+2*node+2
        flow_network = np.zeros((nodes+2, nodes+2), dtype=int)
        #create a small list of the source and sink coordinates
        SourceNSink = list(self.x_a), list(self.x_b)

        #set source and sink as node value
        source = 0
        sink = nodes + 1
                        
        #node count
        cout = 1
        #iterate through the image coordinates
        for i in range(w):
            for j in range(h):
                #add the connections from 0-Cout node
                flow_network[0][cout] = 442-round(self.RGBDist(img[i][j], img[self.x_a[0]][self.x_a[1]]))
                #add connection from Cout node to Sink
                flow_network[cout][sink] = 442-round(self.RGBDist(img[i][j], img[self.x_b[0]][self.x_b[1]]))
                #Iterate node
                cout += 1


        #node iterator
        cout = 1
        #go over image
        for i in range(w):
            for j in range(h):
                #if there is another node to the right
                if not(j+1 >= w):
                    #Right Node
                    #check the distance from one another
                    if self.euclideanDist([i, j], [i, j+1]) < 2:
                        #if they are close, set weight to p0
                        flow_network[cout][cout+1] = self.p0
                #repeat the above for left, up, and bottom nodes.
                if not(j-1 < 0):
                    #Left Node
                    if self.euclideanDist([i, j], [i, j-1]) < 2:
                        flow_network[cout][cout-1] = self.p0

                if not(i-1 < 0):
                    #Up Node
                    if self.euclideanDist([i, j], [i-1, j]) < 2:
                        flow_network[cout][cout-w] = self.p0

                if not(i+1 >= h):
                    #Down Node
                    if self.euclideanDist([i, j], [i+1, j]) < 2:
                        flow_network[cout][cout+w] = self.p0
                cout += 1

        #Call our Ford Fulkersons algorythm and save results
        res = self.fFolk(flow_network, source, sink, OShape)
        #return our binary segmented matrix. 
        return res
        
        



