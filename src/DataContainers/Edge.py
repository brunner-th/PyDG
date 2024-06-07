from DataContainers.Node import Node
from DataContainers.DOF import DOF


class Edge:
    def __init__(self, edge_num: int, start_node: Node, end_node: Node):
        self.edge_num = edge_num
        self.start_node = start_node
        self.end_node = end_node
        self.type = "Uninitialized"
        self.node_list = [start_node, end_node]
        self.dof_list = []
        self.counter = 0
        self.assigned_to_host = False
        self.host_element = None
        self.slave_element = None
    
    def setType(self, type: str):
        # internal
        # dirichletBC
        # neumannBC
        self.type = type

    
    

        