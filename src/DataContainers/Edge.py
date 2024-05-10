class Edge:
    def __init__(self, edge_num ,start_node, end_node):
        self.edge_num = edge_num
        self.start_node = start_node
        self.end_node = end_node
        self.type = "Internal"
    
    def setType(self, type):
        # internal
        # dirichletBC
        # neumannBC
        self.type = type