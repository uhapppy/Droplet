import numpy as np
import math

class Ellipse :

    def __init__(self, radius_x, radius_y):
        self.radius_x = radius_x
        self.radius_y = radius_y


    def get_point(self, theta):
        return np.array([self.radius_x * math.cos(theta), self.radius_y * math.sin(theta)])
    
    def get_theta_from_x(self, x):
        return math.acos(x/self.radius_x)
    
    def get_theta_from_y(self, y):
        return math.asin(y/self.radius_y)
    
    def get_curve(self, n):
        t = np.linspace(0,math.pi,n) #create an array of n values of t between 0 and pi
        points = np.zeros(shape = (2,n)) #create an  2 array of n point fill with zeros first line is x second line is y 


        index=0
        for value in t :  #for each value of t compute the point and add it to the points array
            points[0][index] = self.get_point(value)[0]
            points[1][index] = self.get_point(value)[1]
            index+=1
        return points #return the array of points


    def get_tangent(self, theta):
        tangent = np.array([-self.radius_x * math.sin(theta), self.radius_y * math.cos(theta)])
        return tangent/np.linalg.norm(tangent) #return the tangent vector normalized
    
    def get_normal(self, theta,outward):
        tangent = self.get_tangent(theta)

        if outward :
            return np.array([tangent[1], -tangent[0]]) #return the normal vector
        
        if not outward :
            return np.array([-tangent[1], tangent[0]])
    

    