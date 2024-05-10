
from DataContainers.Mesh import Mesh
import numpy as np

class Assembler:
    def __init__(self, Mesh: Mesh):
        self.Mesh = Mesh
        self.global_stiffness_matrix = np.zeros((self.Mesh.number_of_dofs, self.Mesh.number_of_dofs))
        self.global_force_vector = None
        self.A = None
        self.f = None
    
    def assemble_element(self):

    def assemble_edge(self):
        
    
    def assemble_total(self):
        A = np.zeros(len(self.Mesh.dof_list), len(self.Mesh.dof_list))
        f = np.zeros(len(self.Mesh.dof_list))

        for element in self.Mesh.element_list:
            A_element, f_element = Assembler.get_element_matrix(element)
            for i, dof1 in enumerate(element.dof_list):
                for j, dof2 in enumerate(element.dof_list):
                    A[dof1.dof_number, dof2.dof_number] += A_element[i, j]
                f[dof1.dof_number] += f_element[i]




        for edge in self.Mesh.edge_list:
            A_edge, f_edge = Assembler.get_edge_matrix(edge)
            i, dof1 = 0, edge.dof_list[0]
            j, dof2 = 1, edge.dof_list[1]
                
            A[dof1.dof_number, dof2.dof_number] += A_edge[i, j]
            f[dof1.dof_number] += f_edge[i]
            f[dof2.dof_number] += f_edge[j]


    def get_element_matrix(self, element):
        

        return
    

    def get_edge_matrix(self, edge):
        

        return
        




        
    