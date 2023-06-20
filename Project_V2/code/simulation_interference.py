from ellipse import Ellipse
from ray import IncomingRay , Ray
from pixel import Pixel
import numpy as np
import matplotlib.pyplot as plt
import math



plt.rcParams['font.size'] = '20'

class SimulationInterference:
    def __init__(self,SCREEN_HEIGTH,SCREEN_INCREMENT,
                LASER_RADIUS , NUMEBR_OF_RAYS ,LASER_HEIGHT,LASER_WAVELENGTH,
                DROPLET_XRADIUS ,DROPLET_YRADIUS,DROPLET_XRADIUS_INCREMENT,DROPLET_YRADIUS_INCREMENT,
                INDEX_AIR,INDEX_WATER,
                NUMBER_OF_PIXELS,FRESNEL):



        self.screen_heigth = SCREEN_HEIGTH
        self.screen_increment = SCREEN_INCREMENT

        self.laser_radius = LASER_RADIUS
        self.number_of_rays = NUMEBR_OF_RAYS
        self.laser_height = LASER_HEIGHT
        self.laser_wavelength = LASER_WAVELENGTH


        self.droplet_xradius = DROPLET_XRADIUS
        self.droplet_yradius = DROPLET_YRADIUS
        self.drop_xradius_increment = DROPLET_XRADIUS_INCREMENT
        self.drop_yradius_increment = DROPLET_YRADIUS_INCREMENT

        self.index_air = INDEX_AIR
        self.index_water = INDEX_WATER

        self.number_of_pixels = NUMBER_OF_PIXELS

        self.fresnel = FRESNEL


        self.rays = []
        self.droplet=None
        


    def create_ray(self):

        x_values = np.linspace(start = -self.laser_radius*2,stop= self.laser_radius*2,num = self.number_of_rays)
        
        for value in x_values:
            

            I=math.exp(-2*(value**2)/(self.laser_radius**2))

            self.droplet = Ellipse(radius_x=self.droplet_xradius, radius_y=self.droplet_yradius)


            beam = IncomingRay(origin=np.array([value,self.laser_height]), direction=np.array([0,-1]), intensity=I)
            beam.end = beam.get_intersection_ellispse(self.droplet)


            normal_direction = self.droplet.get_normal(self.droplet.get_theta_from_x(beam.end[0]),outward=False)
            normal = Ray(origin=beam.end, direction=normal_direction, intensity=None)

            beam.get_rays(normal=normal, n_air=self.index_air, n_drop=self.index_water, ellipse=self.droplet, screen_heigth=self.screen_heigth,fresnel = self.fresnel)

            self.rays.append(beam)
            



    def get_data_interferance(self,Data_file_path,frame_number):
        #create the screen
        screen=[]
        x=[]
        y=[]

        for i in range(0,len(self.rays)-1):
            x_1 = self.rays[i].reflected_ray.end[0]
            x_2 = self.rays[i+1].reflected_ray.end[0]

            width = abs(x_1-x_2)

            start = x_1+width/2
            end = start+width

            x.append(start)
            y.append(self.screen_heigth)

            screen.append(Pixel(width,start,end))
            

        for IncomingRay in self.rays:

            ray = IncomingRay
            ray.lenght = np.sqrt((ray.end[0]-ray.origin[0])**2+(ray.end[1]-ray.origin[1])**2)

            reflected = IncomingRay.reflected_ray
            reflected.lenght = np.sqrt((reflected.end[0]-reflected.origin[0])**2+(reflected.end[1]-reflected.origin[1])**2)

            refracted_1 = IncomingRay.refracted_ray_1
            refracted_1.lenght = np.sqrt((refracted_1.end[0]-refracted_1.origin[0])**2+(refracted_1.end[1]-refracted_1.origin[1])**2)

            refracted_2 = IncomingRay.refracted_ray_2
            refracted_2.lenght = np.sqrt((refracted_2.end[0]-refracted_2.origin[0])**2+(refracted_2.end[1]-refracted_2.origin[1])**2)

            refracted_3 = IncomingRay.refracted_ray_3
            refracted_3.lenght = np.sqrt((refracted_3.end[0]-refracted_3.origin[0])**2+(refracted_3.end[1]-refracted_3.origin[1])**2)


            total_refracted_lenght = ray.lenght+self.index_water*(refracted_1.lenght+refracted_2.lenght)+refracted_3.lenght
            total_reflected_lenght = ray.lenght+reflected.lenght

            for i in range(0,len(screen)):
        
                if screen[i].start<=reflected.end[0] and screen[i].end>reflected.end[0] :
                    screen[i].reflected_rays=reflected
                    screen[i].reflected_path=total_reflected_lenght
            
                if screen[i].start<=refracted_3.end[0] and screen[i].end>refracted_3.end[0]:
            
                    screen[i].refracted_rays.append(refracted_3)
                    screen[i].refracted_path.append(total_refracted_lenght)

        for pixel in screen:
            closer_ray=None
            Closest_distance=10000000
            path=None



            if len(pixel.refracted_rays)==0:
                pixel.intensity=0
                pass

            if len(pixel.refracted_rays)==1:
                closer_ray=pixel.refracted_rays[0]
                path=pixel.refracted_path[0]
                pixel.intensity = closer_ray.intensity+pixel.reflected_rays.intensity+2*np.sqrt(closer_ray.intensity*pixel.reflected_rays.intensity)*np.cos(2*np.pi*(pixel.reflected_path-path)/self.laser_wavelength)


            if len(pixel.refracted_rays)>1:
                for ray in pixel.refracted_rays:
                    if abs(ray.end[0]-pixel.reflected_rays.end[0])<Closest_distance:
                        closer_ray=ray
                        Closest_distance=abs(ray.end[0]-pixel.reflected_rays.end[0])
                        path=pixel.refracted_path[pixel.refracted_rays.index(ray)]
                        pixel.intensity = closer_ray.intensity+pixel.reflected_rays.intensity+2*np.sqrt(closer_ray.intensity*pixel.reflected_rays.intensity)*np.cos(2*np.pi*(path-pixel.reflected_path)/self.laser_wavelength)

        distance=[]
        Intensity=[]
        for pixel in screen:
            if pixel.intensity>0:
                distance.append(pixel.start+pixel.width/2)
                Intensity.append(pixel.intensity)
        


       
        output = np.array([distance,Intensity])
        np.save(Data_file_path+"_"+str(frame_number), output)





    def get_all_data_interferance(self,Data_file_path,title,number_of_frames):
        for i in range(1,number_of_frames+1):

            self.create_ray()
            self.get_data_interferance(Data_file_path+title,i)

            self.rays=[]

            self.screen_heigth+=self.screen_increment
            self.droplet_xradius+=self.drop_xradius_increment
            self.droplet_yradius+=self.drop_yradius_increment

            






    def get_figure_interferance(self,graph_style):


        #create the screen
        screen=[]
        x=[]
        y=[]

        for i in range(0,len(self.rays)-1):
            x_1 = self.rays[i].reflected_ray.end[0]
            x_2 = self.rays[i+1].reflected_ray.end[0]

            width = abs(x_1-x_2)

            start = x_1+width/2
            end = start+width

            x.append(start)
            y.append(self.screen_heigth)

            screen.append(Pixel(width,start,end))
            

        for IncomingRay in self.rays:

            ray = IncomingRay
            ray.lenght = np.sqrt((ray.end[0]-ray.origin[0])**2+(ray.end[1]-ray.origin[1])**2)

            reflected = IncomingRay.reflected_ray
            reflected.lenght = np.sqrt((reflected.end[0]-reflected.origin[0])**2+(reflected.end[1]-reflected.origin[1])**2)

            refracted_1 = IncomingRay.refracted_ray_1
            refracted_1.lenght = np.sqrt((refracted_1.end[0]-refracted_1.origin[0])**2+(refracted_1.end[1]-refracted_1.origin[1])**2)

            refracted_2 = IncomingRay.refracted_ray_2
            refracted_2.lenght = np.sqrt((refracted_2.end[0]-refracted_2.origin[0])**2+(refracted_2.end[1]-refracted_2.origin[1])**2)

            refracted_3 = IncomingRay.refracted_ray_3
            refracted_3.lenght = np.sqrt((refracted_3.end[0]-refracted_3.origin[0])**2+(refracted_3.end[1]-refracted_3.origin[1])**2)


            total_refracted_lenght = ray.lenght+self.index_water*(refracted_1.lenght+refracted_2.lenght)+refracted_3.lenght
            total_reflected_lenght = ray.lenght+reflected.lenght

            for i in range(0,len(screen)):
        
                if screen[i].start<=reflected.end[0] and screen[i].end>reflected.end[0] :
                    screen[i].reflected_rays=reflected
                    screen[i].reflected_path=total_reflected_lenght
            
                if screen[i].start<=refracted_3.end[0] and screen[i].end>refracted_3.end[0]:
            
                    screen[i].refracted_rays.append(refracted_3)
                    screen[i].refracted_path.append(total_refracted_lenght)

        for pixel in screen:
            closer_ray=None
            Closest_distance=10000000
            path=None



            if len(pixel.refracted_rays)==0:
                pixel.intensity=0
                pass

            if len(pixel.refracted_rays)==1:
                closer_ray=pixel.refracted_rays[0]
                path=pixel.refracted_path[0]
                pixel.intensity = closer_ray.intensity+pixel.reflected_rays.intensity+2*np.sqrt(closer_ray.intensity*pixel.reflected_rays.intensity)*np.cos(2*np.pi*(pixel.reflected_path-path)/self.laser_wavelength)


            if len(pixel.refracted_rays)>1:
                for ray in pixel.refracted_rays:
                    if abs(ray.end[0]-pixel.reflected_rays.end[0])<Closest_distance:
                        closer_ray=ray
                        Closest_distance=abs(ray.end[0]-pixel.reflected_rays.end[0])
                        path=pixel.refracted_path[pixel.refracted_rays.index(ray)]
                        pixel.intensity = closer_ray.intensity+pixel.reflected_rays.intensity+2*np.sqrt(closer_ray.intensity*pixel.reflected_rays.intensity)*np.cos(2*np.pi*(path-pixel.reflected_path)/self.laser_wavelength)

        distance=[]
        Intensity=[]
        for pixel in screen:
            if pixel.intensity>0:
                distance.append(pixel.start+pixel.width/2)
                Intensity.append(pixel.intensity)
    

        Intensity=Intensity/max(Intensity)


        if graph_style=="2d":
            plt.plot(distance,Intensity,color="black",label="intensity")
            plt.xlabel("Radial Distance (m)")
            plt.ylabel("Relative Intensity")
            plt.show()

        if graph_style=="3d":
            x=distance
            y=distance



            phi = np.linspace(0, np.pi, 3000)

            xx2 = np.zeros((len(Intensity), len(phi)))
            yy2 = np.zeros((len(Intensity), len(phi)))
            zz2 = np.zeros((len(Intensity), len(phi)))

            for zz in range(len(Intensity)):
                xx2[zz, :] = distance[zz] * np.cos(phi)
                yy2[zz, :] = distance[zz] * np.sin(phi)
                zz2[zz, :] = Intensity[zz] 

            C = plt.contourf(xx2, yy2, zz2, 100, cmap="gist_heat",vmin=0.0001, vmax=1)
            clb=plt.colorbar(ticks=[0,0.25,0.5,0.75,1],location="right")
            clb.set_label('Relative Intensity', rotation=270,labelpad=20)
            plt.axis('equal')
            plt.xlabel("x(m)")
            plt.ylabel("y(m)")

            #plt.yticks([-0.001,-0.0005,0,0.0005,0.001])
            #plt.xticks([-0.001,-0.0005,0,0.0005,0.001])
            plt.show()


       

    def get_video_interferance():
        pass
