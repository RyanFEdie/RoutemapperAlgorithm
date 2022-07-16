from utilities import strHash

# A node in the graph. Contains a list of relations to other vertexes, as well as a label and a list of packages.
class Vertex:
    def __init__(self, label):
        self.label = label
        self.relativesTable = []
        self.packages = []
        self.visited = False


class Graph:
    def __init__(self, vertexCount=30):
        self.totalVertexes = []
        for i in range(vertexCount):
            self.totalVertexes.append([])

    def addVertex(self, newVertex):
        vertex = Vertex(newVertex)
        vertKey = strHash(vertex.label) % len(self.totalVertexes)
        while self.totalVertexes[vertKey] != vertex:
            if (
                self.totalVertexes[vertKey] != []
                and vertKey < len(self.totalVertexes) - 1
            ):
                vertKey += 1
            elif (
                self.totalVertexes[vertKey] != []
                and vertKey >= len(self.totalVertexes) - 1
            ):
                vertKey = 0
            else:
                self.totalVertexes[vertKey] = vertex

    def addWeightedEdge(self, vertA, vertB, weight=100):
        self.addDirectedEdge(vertA, vertB, weight)
        self.addDirectedEdge(vertB, vertA, weight)

    # addDirectedEdge creates a tuple with a node name and a distance.
    # This is in perspective to a given node.
    def addDirectedEdge(self, fromVertex, toVertex, weight):
        edgeRelation = (toVertex, weight)
        vertKey = strHash(fromVertex) % len(self.totalVertexes)
        targetVert = self.totalVertexes[vertKey]
        while True:
            if self.totalVertexes[vertKey] != [] and fromVertex == targetVert.label:
                break
            elif vertKey == len(self.totalVertexes) - 1:
                vertKey = 0
            else:
                vertKey += 1
            targetVert = self.totalVertexes[vertKey]
        targetVert.relativesTable.append(edgeRelation)

    # searchByAddress() finds a vertex in the hash table based on an address string.
    # Hash lookup that reverts to linear search.
    def searchByAddress(self, searchVertex):
        vertKey = strHash(searchVertex) % len(self.totalVertexes)
        vertex = Vertex("Unassigned")
        while vertex.label != searchVertex:
            # This component reverts the search to linear. If the hash matches the input, return the vertex associated with the hash string- otherwise,
            # begin linear search, and return once a match is met.
            if (
                self.totalVertexes[vertKey] != []
                and (self.totalVertexes[vertKey]).label == searchVertex
            ):
                vertex = self.totalVertexes[vertKey]
                return vertex
            elif vertKey >= len(self.totalVertexes) - 1:
                vertKey = 0
            elif vertKey <= len(self.totalVertexes):
                vertKey += 1

    # searchByPakID returns a package object from the map hash table. Each node must be searched individually.
    # Time complexity is O(N*M).
    def searchByPakID(self, searchVertex):
        for vertex in self.totalVertexes:
            if vertex != []:
                for package in vertex.packages:
                    if package.pakID == searchVertex:
                        return package
        print("Package Not Found!")

    # addPackage adds a new package to the map hash table.
    def addPackage(self, newPackage):
        vertex = self.searchByAddress(newPackage.delAddress)
        vertex.packages.append(newPackage)
