import numpy as np
import matplotlib.pyplot as plt
import meshpy.triangle as triangle
from Node import Node
from Element import Element

class Mesh:
    def __init__(self):
        self.points
        self.triangles
        self.facets
        self.node_list 
        self.element_list
        self.node_connectivity_matrix
        self.edge_connectivity_matrix
    

    def initialize_basic_square_mesh(self):

        def round_trip_connect(start, end):
            return [(i, i + 1) for i in range(start, end)] + [(end, start)]

        points = [(1, 0), (1, 1), (-1, 1), (-1, -1), (1, -1), (1, 0)]
        facets = round_trip_connect(0, len(points) - 1)

        circ_start = len(points)
        points.extend(
            (3 * np.cos(angle), 3 * np.sin(angle))
            for angle in np.linspace(0, 2 * np.pi, 30, endpoint=False)
        )

        facets.extend(round_trip_connect(circ_start, len(points) - 1))

        def needs_refinement(vertices, area):
            bary = np.sum(np.array(vertices), axis=0) / 3
            max_area = 0.001 + (np.linalg.norm(bary, np.inf) - 1) * 0.01
            return bool(area > max_area)

        info = triangle.MeshInfo()
        info.set_points(points)
        info.set_holes([(0, 0)])
        info.set_facets(facets)

        mesh = triangle.build(info, refinement_func=needs_refinement)


        self.points = np.array(mesh.points)
        self.triangles = np.array(mesh.elements)
        self.facets = np.array(mesh.facets)

    
    def plot_mesh(self):
        plt.triplot(self.points[:, 0], self.points[:, 1], self.triangles, linewidth = 1)
        plt.show()

    def fillNodeList(self):
        self.node_list = []
        for num, point in enumerate(self.points):
            node = Node(num, point[num,:])
            self.node_list.append(node)

    def fillElementList(self):
        self.element_list = []
        for num, nodelist in enumerate(self.triangles):

            node_num_list = self.triangles[num,:]
            node1_num = node_num_list[0]
            node2_num = node_num_list[1]
            node3_num = node_num_list[2]

            nodelist = [self.node_list[node1_num], 
                        self.node_list[node2_num],
                        self.node_list[node3_num]]
            
            edges = None

            self.element_list.append(Element(num, nodelist, edges))


    def calculate_point_connectivity_matrix():
        point_connectivity_matrix = np.zeros((10))
        return point_connectivity_matrix

    def calculate_edge_connectivity_matrix():
        edge_connectivity_matrix = np.zeros((10))
        return edge_connectivity_matrix
    
