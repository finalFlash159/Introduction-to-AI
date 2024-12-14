def printMST(self, parent, d_temp, t):
        # print("Edge \tWeight")
        sum_weight = 0
        min1 = 10000
        min2 = 10000
        r_temp = {} # Reverse dictionary
        for k in d_temp:
            r_temp[d_temp[k]] = k
        for i in range(1, self.V):
            # print(parent[i], "-", i, "\t", self.graph[i][parent[i]])
            sum_weight = sum_weight + self.graph[i][parent[i]]
            if (graph[0][r_temp[i]] < min1):
                min1 = graph[0][r_temp[i]]
            if (graph[0][r_temp[parent[i]]] < min1):
                min1 = graph[0][r_temp[parent[i]]]
            if (graph[t][r_temp[i]] < min2):
                min2 = graph[t][r_temp[i]]
            if (graph[t][r_temp[parent[i]]] < min2):
                min2 = graph[t][r_temp[parent[i]]]
        return (sum_weight + min1 + min2) % 10000
    
    # A utility function to find the vertex 
    # with minimum distance value, from the set of vertices
    # not yet included in shortest path tree
    def minKey(self, key, mstSet):
        # Initilaize min value
        min = sys.maxsize
        for v in range(self.V):
            if key[v] < min and mstSet[v] == False:
                min = key[v]
                min_index = v
        return min_index