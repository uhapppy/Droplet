from simulation_path import SimulationPath
from simulation_interference import SimulationInterference
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import moviepy.video.io.ImageSequenceClip
from PIL import Image, ImageFile

#simulation parameters

SCREEN_HEIGTH = 5e-3 #m
SCREEN_INCREMENT = 0 #m


LASER_WAVELENGTH = 632.8e-9 #m
LASER_RADIUS = 0.33e-3 #m 
NUMEBR_OF_RAYS =2000
LASER_HEIGHT = 4e-3#m


DROPLET_XRADIUS = 5e-3 #m
DROPLET_YRADIUS = 1e-3 #m

DROPLET_XRADIUS_INCREMENT = -0.0000004e-3 #m
DROPLET_YRADIUS_INCREMENT = -0.0000004e-3 #m

FRESNEL_TYPE = "schlick" # None , normal , schlick

INDEX_AIR=1
INDEX_WATER=4/3

NUMBER_OF_PIXELS = 1000





#data parameters
INTENSITY = True
RAYS = False

FIGURE = True


#type of visualization
GRAPH="2d"   #"2d" or "3d"


#Figure parameters



TITLE = "schlick"

GET_DATA_VIDEO = False
GET_FIGURE_VIDEO = False
GET_VIDEO = False


DATA_PATH = "C:/Users/Jfyol/OneDrive/Bureau/Project_V2/data/"
FIGURE_PATH = "C:/Users/Jfyol/OneDrive/Bureau/Project_V2/figure/"
VIDEO_PATH = "C:/Users/Jfyol/OneDrive/Bureau/Project_V2/video/"

DPI=600
NUMBER_OF_FRAMES = 2000
FRAME_RATE = 50







if RAYS :
    simulation_path = SimulationPath(SCREEN_HEIGTH,LASER_RADIUS , NUMEBR_OF_RAYS ,LASER_HEIGHT,DROPLET_XRADIUS ,DROPLET_YRADIUS,INDEX_AIR,INDEX_WATER)
    simulation_path.create_ray()
    simulation_path.get_figure_ray()



if INTENSITY :
    if FIGURE:
        simulation_interference = SimulationInterference(SCREEN_HEIGTH,SCREEN_INCREMENT,
                LASER_RADIUS , NUMEBR_OF_RAYS ,LASER_HEIGHT,LASER_WAVELENGTH,
                DROPLET_XRADIUS ,DROPLET_YRADIUS,DROPLET_XRADIUS_INCREMENT,DROPLET_YRADIUS_INCREMENT,
                INDEX_AIR,INDEX_WATER,
                NUMBER_OF_PIXELS,FRESNEL_TYPE)
    
        simulation_interference.create_ray()
        simulation_interference.get_figure_interferance(GRAPH)

    elif GET_DATA_VIDEO:
        simulation_interference = SimulationInterference(SCREEN_HEIGTH,SCREEN_INCREMENT,
                LASER_RADIUS , NUMEBR_OF_RAYS ,LASER_HEIGHT,LASER_WAVELENGTH,
                DROPLET_XRADIUS ,DROPLET_YRADIUS,DROPLET_XRADIUS_INCREMENT,DROPLET_YRADIUS_INCREMENT,
                INDEX_AIR,INDEX_WATER,
                NUMBER_OF_PIXELS,FRESNEL_TYPE)
        
        simulation_interference.get_all_data_interferance(DATA_PATH,TITLE,NUMBER_OF_FRAMES)
        

    elif GET_FIGURE_VIDEO :
        maximum=0
        for i in range(1,NUMBER_OF_FRAMES+1):
            print(i)
            data = np.load(DATA_PATH+TITLE+"_"+str(i)+".npy")
            if maximum<max(data[1]):
                    maximum=max(data[1])

        for i in range(1,NUMBER_OF_FRAMES+1):
            print(i)
            data = np.load(DATA_PATH+TITLE+"_"+str(i)+".npy")
            distance = data[0]
            Intensity = data[1]
            Intensity=Intensity/maximum


            if GRAPH=="2d":
                plt.ylim([0,1])
                plt.plot(distance,Intensity,color="black",label="intensity")
                plt.xlabel("Radial Distance (m)")
                plt.ylabel("Relative Intensity")
                

            if GRAPH=="3d":
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




                C = plt.contourf(xx2, yy2, zz2, 75, cmap="gist_heat",vmin=0., vmax=1.)

                m = plt.cm.ScalarMappable(cmap="gist_heat")
                m.set_array(zz2)
                m.set_clim(0., 1.)
                clb=plt.colorbar(m,ticks=[0,0.25,0.5,0.75,1] )




                #clb=plt.colorbar(ticks=[0,0.25,0.5,0.75,1],location="right",pad=0.08)
                clb.set_label('Relative Intensity', rotation=270,labelpad=20)
                plt.clim(0,1)
                plt.axis('equal')
                plt.xlabel("x(m)")
                plt.ylabel("y(m)")
            plt.savefig(FIGURE_PATH+TITLE+"_"+str(i)+".png",dpi=DPI,bbox_inches='tight')
            plt.clf()

    elif GET_VIDEO:
        ImageFile.LOAD_TRUNCATED_IMAGES = True

        image_files = []

        for img_number in range(1,NUMBER_OF_FRAMES+1): 
            print(img_number)
            image_files.append(FIGURE_PATH+TITLE+"_"+str(img_number)+".png") 

        

        clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=FRAME_RATE)

        clip.write_videofile("C:/Users/Jfyol/OneDrive/Bureau/Project_V2/video/"+TITLE+".mp4")




