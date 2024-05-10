
from DataContainers.Mesh import Mesh
from ShapeFunctions.HatFunction import HatFunction
import numpy as np

class Assembler:
    def __init__(self, Mesh: Mesh):
        self.Mesh = Mesh
        self.A = np.zeros((len(self.Mesh.dof_list), len(self.Mesh.dof_list)))
        self.f = np.zeros((len(self.Mesh.dof_list)))
    
    def get_element_matrix(element):
        
        x_coords = np.zeros(len(element.node_list))
        y_coords = np.zeros(len(element.node_list))
        A_element = np.zeros((len(element.dof_list), len(element.dof_list)))
        f_element = np.zeros((len(element.dof_list)))

        for ind, dof in enumerate(element.dof_list):
            x_coords[ind] = dof.position[0]
            y_coords[ind] = dof.position[1]


        area, b, c = HatFunction().HatGradients(x_coords, y_coords)

        A_element = area * (np.outer(b, b) + np.outer(c, c))
        force_val = Mesh.RHSFunction(np.mean(x_coords), np.mean(y_coords))
        f_element =  np.full((len(element.dof_list)), force_val/(3*area))

        return A_element, f_element
    

    def get_edge_matrix(self, edge):
        
        A_edge = np.zeros((len(edge.dof_list), len(edge.dof_list)))
        f_edge = np.zeros((len(edge.dof_list)))
        return A_edge, f_edge
        
    def assemble_total(self):
        A = np.zeros((len(self.Mesh.dof_list), len(self.Mesh.dof_list)))
        f = np.zeros((len(self.Mesh.dof_list)))

        for element in self.Mesh.element_list:
            A_element, f_element = Assembler.get_element_matrix(element)
            for i, dof1 in enumerate(element.dof_list):
                for j, dof2 in enumerate(element.dof_list):
                    A[dof1.dof_number, dof2.dof_number] += A_element[i, j]
                f[dof1.dof_number] += f_element[i]


        #for edge in self.Mesh.edge_list:
        #    A_edge, f_edge = Assembler.get_edge_matrix(edge)
        #    i, dof1 = 0, edge.dof_list[0]
        #    j, dof2 = 1, edge.dof_list[1]
        #        
        #    A[dof1.dof_number, dof2.dof_number] += A_edge[i, j]
        #    f[dof1.dof_number] += f_edge[i]
        #    f[dof2.dof_number] += f_edge[j]


    
        




        
    