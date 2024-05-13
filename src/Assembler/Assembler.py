
from DataContainers.Mesh import Mesh
from DataContainers.Edge import Edge
from DataContainers.Element import Element
from ShapeFunctions.HatFunction import HatFunction
import numpy as np

class Assembler:
    def __init__(self, mesh):
        self.Mesh = mesh
        self.beta = 1
        self.h = 0.1
    
    def __get_element_matrix(self, element: Element):
        
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
    

    def __get_internal_edge_matrix(self, edge: Edge):
        A_edge = np.zeros((2, 2))
        f_edge = np.zeros((2))

        x_coords = np.zeros(len(edge.node_list))
        y_coords = np.zeros(len(edge.node_list))
        for ind, dof in enumerate(edge.dof_list):
            x_coords[ind] = dof.position[0]
            y_coords[ind] = dof.position[1]


        grad_u_host = [1,1]
        grad_u_slave = [1,1]

        grad_v_host = [1,1]
        grad_v_slave = [1,1]

        u_host = 1
        u_slave = 0.5

        v_host = 1
        v_slave = 0.5
        
        ds = np.linalg.norm(np.array([x_coords[1]-x_coords[0], y_coords[1]-y_coords[0]]))
        nx = (y_coords[1]-y_coords[0])/ds
        ny = -(x_coords[1]-x_coords[0])/ds

        A_ii = np.ones((2,2))*np.mean([grad_u_host[0]*nx + grad_u_host[1]*ny, grad_u_slave[0]*nx + grad_u_slave[1]*ny])*ds*(v_host - v_slave)

        A_iii = np.ones((2,2))*np.mean([grad_v_host[0]*nx + grad_v_host[1]*ny, grad_v_slave[0]*nx + grad_v_slave[1]*ny])*ds*(u_host - u_slave)

        A_iv = np.ones((2,2))*self.beta/self.h*ds*(u_host - u_slave)*(v_host - v_slave)

        A_edge = A_ii + A_iii + A_iv


        return A_edge, f_edge
    
    def __get_neumann_edge_matrix(self, edge: Edge):
        A_edge = np.zeros((2, 2))
        f_edge = np.zeros((2))
        return A_edge, f_edge
        
    def assemble_total(self):
        A = np.zeros((len(self.Mesh.dof_list), len(self.Mesh.dof_list)))
        f = np.zeros((len(self.Mesh.dof_list)))

        internal_edges = self.Mesh.internal_edge_list
        neumann_edges = self.Mesh.neumann_edge_list

        for element in self.Mesh.element_list:
            A_element, f_element = self.__get_element_matrix(element)
            for i, dof1 in enumerate(element.dof_list):
                for j, dof2 in enumerate(element.dof_list):
                    A[dof1.dof_number, dof2.dof_number] += A_element[i, j]
                f[dof1.dof_number] += f_element[i]

        for edge in internal_edges:
                
            A_edge, f_edge = self.__get_internal_edge_matrix(edge)
            i, dof1 = 0, edge.dof_list[0]
            j, dof2 = 1, edge.dof_list[1]

            A[dof1.dof_number, dof2.dof_number] += A_edge[i, j]
            f[dof1.dof_number] += f_edge[i]
            f[dof2.dof_number] += f_edge[j]


        for edge in neumann_edges:
            A_edge, f_edge = self.__get_neumann_edge_matrix(edge)
            i, dof1 = 0, edge.dof_list[0]
            j, dof2 = 1, edge.dof_list[1]

            A[dof1.dof_number, dof2.dof_number] += A_edge[i, j]
            f[dof1.dof_number] += f_edge[i]
            f[dof2.dof_number] += f_edge[j]
            

        return A, f


    
        




        
    