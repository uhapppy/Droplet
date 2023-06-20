from ellipse import Ellipse
from ray import IncomingRay , Ray
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc


plt.rcParams['font.size'] = '20'
class SimulationPath:
    def __init__(self,SCREEN_HEIGTH,LASER_RADIUS , NUMEBR_OF_RAYS ,LASER_HEIGHT,DROPLET_XRADIUS ,DROPLET_YRADIUS,INDEX_AIR,INDEX_WATER):
        self.screen_heigth = SCREEN_HEIGTH
        self.laser_radius = LASER_RADIUS
        self.number_of_rays = NUMEBR_OF_RAYS
        self.laser_height = LASER_HEIGHT
        self.droplet_xradius = DROPLET_XRADIUS
        self.droplet_yradius = DROPLET_YRADIUS
        self.index_air = INDEX_AIR
        self.index_water = INDEX_WATER


        

        self.rays = []
        self.droplet=None



    def create_ray(self):

        x_values = np.linspace(start = -self.laser_radius*2,stop= self.laser_radius*2,num = self.number_of_rays)

        for value in x_values:


            self.droplet = Ellipse(radius_x=self.droplet_xradius, radius_y=self.droplet_yradius)


            beam = IncomingRay(origin=np.array([value,self.laser_height]), direction=np.array([0,-1]), intensity=1)
            beam.end = beam.get_intersection_ellispse(self.droplet)


            normal_direction = self.droplet.get_normal(self.droplet.get_theta_from_x(beam.end[0]),outward=False)
            normal = Ray(origin=beam.end, direction=normal_direction, intensity=None)

            beam.get_rays(normal=normal, n_air=self.index_air, n_drop=self.index_water, ellipse=self.droplet, screen_heigth=self.screen_heigth,fresnel=False)

            self.rays.append(beam)


    def get_figure_ray(self):


        my_labels = {"Incident": "Incident", "Reflected": "Reflected", "Refracted": "Refracted", "Droplet": "Droplet" }


        for ray in self.rays:

            trace_incident = ray.get_line()
            plt.plot(trace_incident[0], trace_incident[1],label=my_labels["Incident"],color="red")

            trace_reflected = ray.reflected_ray.get_line()
            plt.plot(trace_reflected[0], trace_reflected[1],label=my_labels["Reflected"],color="green")

            trace_refracted__1 = ray.refracted_ray_1.get_line()
            plt.plot(trace_refracted__1[0], trace_refracted__1[1],label=my_labels["Refracted"],color="blue")

            trace_refracted__2 = ray.refracted_ray_2.get_line()
            plt.plot(trace_refracted__2[0], trace_refracted__2[1],color="blue")

            trace_refracted__3 = ray.refracted_ray_3.get_line()
            plt.plot(trace_refracted__3[0], trace_refracted__3[1],color="blue")


            droplet_curve  = self.droplet.get_curve(1000)
            plt.plot(droplet_curve[0], droplet_curve[1],label=my_labels["Droplet"],color="black")

            my_labels = {"Incident": "_nolegend_", "Reflected": "_nolegend_", "Refracted": "_nolegend_", "Droplet": "_nolegend_" }




        

        plt.axis('equal')

        plt.xlabel("x (m)")
        plt.ylabel("y (m)")

        plt.legend()
        plt.show()





            

        
        







        
