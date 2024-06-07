
from DataContainers.Mesh import Mesh
from DataContainers.Edge import Edge
from DataContainers.Element import Element
from ShapeFunctions.LinearBasisFunction import LinearBasisFunction

import matplotlib.pyplot as plt
import numpy as np

class Assembler:
    def __init__(self, mesh, h, alpha = 1, beta = 9):
        self.Mesh = mesh
        self.alpha = alpha
        self.beta = beta
        self.h = h
    

    def __get_element_matrix(self, element: Element):
        
        dof_nums = np.zeros((len(element.dof_list)))
        x_coords = np.zeros(len(element.node_list))
        y_coords = np.zeros(len(element.node_list))
        A_element = np.zeros((len(element.dof_list), len(element.dof_list)))
        f_element = np.zeros((len(element.dof_list)))

        for ind, dof in enumerate(element.dof_list):
            x_coords[ind] = dof.position[0]
            y_coords[ind] = dof.position[1]
            dof_nums[ind] = dof.dof_number

        area, b, c = LinearBasisFunction().evalulateGradientsLinearBasisFunction(x_coords, y_coords)

        A_element = area * (np.outer(b, b) + np.outer(c, c)) # classical stiffness matrix
        force_val = Mesh.RHSFunction(np.mean(x_coords), np.mean(y_coords))
        f_element =  area*np.full((len(element.dof_list)), force_val/(3))

        return A_element, f_element, dof_nums
    

    def __get_boundary_edge_matrix(self, edge: Edge):
        SE = np.zeros((6, 6))
        PE = np.zeros((6, 6))
        f_edge = np.zeros((6))
        dof_nums = np.zeros((6))
        x_coords_edge = np.zeros(2)
        y_coords_edge = np.zeros(2)
        x_coords_host = np.zeros(3)
        y_coords_host = np.zeros(3)
        
        for ind, dof in enumerate(edge.dof_list):
            x_coords_edge[ind] = dof.position[0]
            y_coords_edge[ind] = dof.position[1]

        host_element = edge.host_element
        
        for ind, dof in enumerate(host_element.dof_list):
            x_coords_host[ind] = dof.position[0]
            y_coords_host[ind] = dof.position[1]
            dof_nums[ind] = dof.dof_number

        weights = np.array([1, 4, 1])/6 # simpson integration rule
        transformation_matrix = np.array([[1,0], [0.5,0.5] ,[0,1]]) # integration points
        eval_x = transformation_matrix @ x_coords_edge
        eval_y = transformation_matrix @ y_coords_edge

        ds = np.sqrt(np.array([x_coords_edge[1]-x_coords_edge[0]])**2 + np.array([y_coords_edge[1]-y_coords_edge[0]])**2)
        nx = (y_coords_edge[1]-y_coords_edge[0])/ds
        ny = -(x_coords_edge[1]-x_coords_edge[0])/ds

        dist_to_host_centroid = np.linalg.norm(np.array([np.mean(x_coords_edge)+nx*self.h-np.mean(x_coords_host), np.mean(y_coords_edge)+ny*self.h-np.mean(y_coords_host)]))
        dist_to_slave_centroid = np.linalg.norm(np.array([np.mean(x_coords_edge)-nx*self.h-np.mean(x_coords_host), np.mean(y_coords_edge)-ny*self.h-np.mean(y_coords_host)]))

        if dist_to_host_centroid < dist_to_slave_centroid:
            nx = -nx
            ny = -ny

        #plt.plot([0,1,1,0,0],  [0,0,1,1,0], 'k-')
        #plt.plot(x_coords_edge, y_coords_edge, 'r-')
        #plt.plot(x_coords_host, y_coords_host, 'g-')
        #plt.plot(x_coords_slave, y_coords_slave, 'r-')
        #plt.plot([np.mean(x_coords_host)], [np.mean(y_coords_host)], 'go')
        #plt.plot([np.mean(x_coords_slave)], [np.mean(y_coords_slave)], 'ro')
        #plt.plot(eval_x, eval_y, 'k+',)
        #plt.plot([np.mean(x_coords_edge), np.mean(x_coords_edge)+nx*self.h], [np.mean(y_coords_edge), np.mean(y_coords_edge)+ny*self.h], 'b-')
        #plt.show()

        for ind, weight in enumerate(weights):

            lenght_subinterval = weight*ds
            value_host, _, b_host, c_host = LinearBasisFunction().evaluateLinearBasisFunction(x_coords_host, y_coords_host, eval_x[ind], eval_y[ind])
            jump = np.vstack((value_host , np.array([0,0,0])))
            average = np.vstack((nx*b_host + ny*c_host,  np.array([0,0,0])))/2
        
            PE += np.outer(jump, jump)*lenght_subinterval
            SE += np.outer(jump, average)*lenght_subinterval*2

        #plt.imshow(PE)
        #plt.show()
        #plt.imshow(SE)
        #plt.show()

        return PE, SE, f_edge, dof_nums


    def __get_internal_edge_matrix(self, edge: Edge):
        
        SE = np.zeros((6, 6))
        PE = np.zeros((6, 6))
        f_edge = np.zeros((6))
        dof_nums = np.zeros((6))

        x_coords_edge = np.zeros(2)
        y_coords_edge = np.zeros(2)
        x_coords_host = np.zeros(3)
        y_coords_host = np.zeros(3)
        x_coords_slave = np.zeros(3)
        y_coords_slave = np.zeros(3)

        for ind, dof in enumerate(edge.dof_list):
            x_coords_edge[ind] = dof.position[0]
            y_coords_edge[ind] = dof.position[1]

        host_element = edge.host_element
        slave_element = edge.slave_element
        
        if host_element.element_number == slave_element.element_number:
            raise Exception("Host and slave element are the same!")

        for ind, dof in enumerate(host_element.dof_list):
            x_coords_host[ind] = dof.position[0]
            y_coords_host[ind] = dof.position[1]
            dof_nums[ind] = dof.dof_number

        for ind, dof in enumerate(slave_element.dof_list):
            x_coords_slave[ind] = dof.position[0]
            y_coords_slave[ind] = dof.position[1]
            dof_nums[3+ind] = dof.dof_number
        
        weights = np.array([1, 4, 1])/6 # simpson integration rule
        transformation_matrix = np.array([[1,0], [0.5,0.5] ,[0,1]]) # integration points
        eval_x = transformation_matrix @ x_coords_edge
        eval_y = transformation_matrix @ y_coords_edge
        ds = np.sqrt(np.array([x_coords_edge[1]-x_coords_edge[0]])**2 + np.array([y_coords_edge[1]-y_coords_edge[0]])**2)
        nx = (y_coords_edge[1]-y_coords_edge[0])/ds
        ny = -(x_coords_edge[1]-x_coords_edge[0])/ds
        dist_to_host_centroid = np.linalg.norm(np.array([np.mean(x_coords_edge)+nx*self.h-np.mean(x_coords_host), np.mean(y_coords_edge)+ny*self.h-np.mean(y_coords_host)]))
        dist_to_slave_centroid = np.linalg.norm(np.array([np.mean(x_coords_edge)+nx*self.h-np.mean(x_coords_slave), np.mean(y_coords_edge)+ny*self.h-np.mean(y_coords_slave)]))

        if dist_to_host_centroid < dist_to_slave_centroid:
            nx = -nx
            ny = -ny

        #plt.plot([0,1,1,0,0],  [0,0,1,1,0], 'k-')
        #plt.plot(x_coords_edge, y_coords_edge, 'r-')
        #plt.plot(x_coords_host, y_coords_host, 'g-')
        #plt.plot(x_coords_slave, y_coords_slave, 'r-')
        #plt.plot([np.mean(x_coords_host)], [np.mean(y_coords_host)], 'go')
        #plt.plot([np.mean(x_coords_slave)], [np.mean(y_coords_slave)], 'ro')
        #plt.plot(eval_x, eval_y, 'k+',)
        #plt.plot([np.mean(x_coords_edge), np.mean(x_coords_edge)+nx*self.h], [np.mean(y_coords_edge), np.mean(y_coords_edge)+ny*self.h], 'b-')
        #plt.show()

        for ind, weight in enumerate(weights):

            lenght_subinterval = weight*ds
            value_host, _, b_host, c_host = LinearBasisFunction().evaluateLinearBasisFunction(x_coords_host, y_coords_host, eval_x[ind], eval_y[ind])
            value_slave, _, b_slave, c_slave = LinearBasisFunction().evaluateLinearBasisFunction(x_coords_slave, y_coords_slave, eval_x[ind], eval_y[ind])
            jump = np.vstack((value_host , -value_slave))
            average = np.vstack((nx*b_host + ny*c_host, nx*b_slave + ny*c_slave))/2
        
            PE += np.outer(jump, jump)*lenght_subinterval
            SE += np.outer(jump, average)*lenght_subinterval

        #plt.imshow(PE)
        #plt.show()
        #plt.imshow(SE)
        #plt.show()

        return PE, SE, f_edge, dof_nums
    

    def __get_neumann_edge_matrix(self, edge: Edge): # not implemented yet
        A_edge = np.zeros((2, 2))
        f_edge = np.zeros((2))
        return A_edge, f_edge
        

    def assemble_total(self):

        U = np.zeros((len(self.Mesh.dof_list), len(self.Mesh.dof_list)))
        P = np.zeros((len(self.Mesh.dof_list), len(self.Mesh.dof_list)))
        S = np.zeros((len(self.Mesh.dof_list), len(self.Mesh.dof_list)))
        A = np.zeros((len(self.Mesh.dof_list), len(self.Mesh.dof_list)))
        f = np.zeros((len(self.Mesh.dof_list)))

        internal_edges = self.Mesh.internal_edge_list
        neumann_edges = self.Mesh.neumann_edge_list

        for element in self.Mesh.element_list: # loop over all elements
            A_element, f_element, dof_nums = self.__get_element_matrix(element)
            for i, dof1 in enumerate(dof_nums):
                for j, dof2 in enumerate(dof_nums):
                    A[int(dof1), int(dof2)] += A_element[i, j]
                f[int(dof1)] += f_element[i]

        for edge in internal_edges: # loop over all internal edges
                
            PE, SE, _, dof_nums = self.__get_internal_edge_matrix(edge)

            for i, dof1 in enumerate(dof_nums):
                for j, dof2 in enumerate(dof_nums):
                    P[int(dof1), int(dof2)] += PE[i, j]
                    S[int(dof1), int(dof2)] += SE[i, j]
                
        for edge in neumann_edges: # loop over all neumann edges
            
            PE, SE, _, dof_nums = self.__get_boundary_edge_matrix(edge)

            for i, dof1 in enumerate(dof_nums[0:2]):
                for j, dof2 in enumerate(dof_nums[0:2]):
                    
                    P[int(dof1), int(dof2)] += PE[i, j]
                    S[int(dof1), int(dof2)] += SE[i, j]

        U = (A-S+self.alpha*np.transpose(S)+self.beta/self.h*P)
        
        return U, f


    
        




        
    