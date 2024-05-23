import numpy as np
import matplotlib.pyplot as plt
import meshpy.triangle as triangle
import meshpy.tet as tet
from DataContainers.Node import Node
from DataContainers.Edge import Edge
from DataContainers.Element import Element
from DataContainers.DOF import DOF
import h5py

class Mesh:
    def __init__(self):
        self.points = None
        self.triangles = None
        self.facets = None
        self.dof_list = None
        self.node_list = None
        self.element_list = None
        self.edge_list = None
        self.internal_edge_list = None
        self.neumann_edge_list = None
        self.connectivity = None
        
    def RHSFunction(x, y):
        return 2*np.pi**2*np.sin(np.pi*x)*np.sin(np.pi*y)

    def generate_square_mesh_with_hole(self):

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


    def generate_basic_square_mesh(self, max_vol = 0.01, min_angle=30):

        points = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]
        facets = [[0, 1], [1, 2], [2, 3], [3, 1]]

        def round_trip_connect(start, end):
            return [(i, i + 1) for i in range(start, end)] + [(end, start)]

        facets = round_trip_connect(0, len(points)-1)

        info = triangle.MeshInfo()
        info.set_points(points)
        info.set_facets(facets)

        mesh = triangle.build(info, max_volume=max_vol, min_angle=min_angle)

        self.points = np.array(mesh.points)
        self.triangles = np.array(mesh.elements)
        self.facets = np.array(mesh.facets)

    
    def plot_mesh(self, ax = None):
        if ax is None:
            plt.triplot(self.points[:, 0], self.points[:, 1], self.triangles, linewidth = 1)
            plt.show()
        else:
            ax.triplot(self.points[:, 0], self.points[:, 1], self.triangles, linewidth = 1)


    def fillNodeList(self):
        self.node_list = []
        for num, p in enumerate(self.points):
            node = Node(num, self.points[num,:])
            self.node_list.append(node)

    def fillDOFList(self):
        self.dof_list = []
        dof_ind = 0
        for element in self.element_list:
            for node in element.node_list:
                dof = DOF(dof_ind, node.coordinates, node.node_number)
                self.dof_list.append(dof)
                node.addDOF(dof)
                element.addDOF(dof)
                dof_ind += 1

    def fillElementList(self):
        self.element_list = []
        self.edge_list = []

        edge_num = 0

        for num, nodelist in enumerate(self.triangles):
            node_num_list = self.triangles[num,:]
            node1_num = node_num_list[0]
            node2_num = node_num_list[1]
            node3_num = node_num_list[2]

            nodelist = [self.node_list[node1_num], 
                        self.node_list[node2_num],
                        self.node_list[node3_num]]
            
            self.element_list.append(Element(num, nodelist))

            edge_num += 3

    def fillEdgeList(self):
        self.connectivity = np.zeros((len(self.node_list), len(self.node_list)))
        self.neumann_edge_list = []
        self.internal_edge_list = []

        for num, nl in enumerate(self.triangles):
            nodelist = self.triangles[num,:]
            self.connectivity[nodelist[0], nodelist[1]] += 1
            self.connectivity[nodelist[1], nodelist[0]] += 1
            self.connectivity[nodelist[1], nodelist[2]] += 1
            self.connectivity[nodelist[2], nodelist[1]] += 1
            self.connectivity[nodelist[2], nodelist[0]] += 1
            self.connectivity[nodelist[0], nodelist[2]] += 1

        #plt.imshow(self.connectivity)
        #plt.show()
        edge_num = 0
        for ind1 in range(len(self.connectivity)):
            for ind2 in range(len(self.connectivity)):
                if ind2 < ind1:
                    continue
                if self.connectivity[ind1, ind2] == 1:
                    edge = Edge(edge_num, self.node_list[ind1], self.node_list[ind2])
                    edge.setType("Neumann")

                    for dof in self.dof_list:
                        if dof.node_number == self.node_list[ind1].node_number:
                            index_1 = dof.dof_number
                        elif dof.node_number == self.node_list[ind2].node_number:
                            index_2 = dof.dof_number
                    cnt = 0
                    for element in self.element_list:
                        if self.node_list[ind1].node_number in element.node_num_list and self.node_list[ind2].node_number in element.node_num_list:
                            
                            if cnt == 0:
                                edge.assigned_to_host = True
                                edge.host_element = element
                                cnt += 1
                            else:
                                raise Exception("More than 1 elements connected to an boundary edge")
                            
                    edge.dof_list = [self.dof_list[index_1], self.dof_list[index_2]]
                    self.edge_list.append(edge)
                    self.neumann_edge_list.append(edge)
                    edge_num += 1
                
                elif self.connectivity[ind1, ind2] == 2:
                    edge = Edge(edge_num, self.node_list[ind1], self.node_list[ind2])
                    edge.setType("Internal")
                    cnt = 0
                    for element in self.element_list:
                        if self.node_list[ind1].node_number in element.node_num_list and self.node_list[ind2].node_number in element.node_num_list:
                            
                            if cnt == 0:
                                edge.assigned_to_host = True
                                edge.host_element = element

                                for dof in element.dof_list:
                                    if dof.node_number == self.node_list[ind1].node_number:
                                        index_1 = dof.dof_number
                                    elif dof.node_number == self.node_list[ind2].node_number:
                                        index_2 = dof.dof_number

                                edge.dof_list = [self.dof_list[index_1], self.dof_list[index_2]]
                                element.addEdge(edge)
                                cnt += 1
                            elif cnt == 1:
                                edge.slave_element = element
                            else:
                                raise Exception("More than 2 elements connected to an edge")

                    self.edge_list.append(edge)
                    self.internal_edge_list.append(edge)
                    edge_num += 1


    def fillNeumannEdgeList(self):
        self.neumann_edge_list = []
        for element1 in self.element_list:
            for edge1 in element1.edges:
                edge1.counter += 1
            
    def getDOFPositions(self):
        dof_positions = np.zeros((len(self.dof_list), 2))
        for dof in self.dof_list:
            dof_positions[dof.dof_number, :] = dof.position
        return dof_positions

    def getDOFTriangles(self):
        dof_triangles = np.zeros((len(self.element_list), 3))
        for element in self.element_list:
            for ind, dof in enumerate(element.dof_list):
                dof_triangles[element.element_number, ind] = dof.dof_number
        return dof_triangles
    
    def saveMesh(self, file):
        
        with h5py.File(file, 'w') as hf:
            hf.create_dataset("points",  data=self.points)
            hf.create_dataset("triangles",  data=self.triangles)
            hf.create_dataset("facets",  data=self.facets)

        
    def loadMesh(self, file):
        f = h5py.File(file, "r")
        self.points = np.array(f["points"])
        self.triangles = np.array(f["triangles"])
        self.facets = np.array(f["facets"])
        f.close()


    
    
    

