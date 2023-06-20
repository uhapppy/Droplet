import numpy as np 
import matplotlib.pyplot as plt 


plt.rcParams['font.size'] = '20'


data_none = np.load("C:/Users/Jfyol/OneDrive/Bureau/Project_V2/data/none_1.npy")
data_schlick = np.load("C:/Users/Jfyol/OneDrive/Bureau/Project_V2/data/schlick_1.npy")
data_normal = np.load("C:/Users/Jfyol/OneDrive/Bureau/Project_V2/data/normal_1.npy")


maxi = np.max(np.array([data_none[1],data_schlick[1],data_normal[1]]))



intensiter_none = data_none[1]/np.max(data_none[1])
intensiter_schlick = data_schlick[1]/np.max(data_schlick[1])
intensiter_normal = data_normal[1]/np.max(data_normal[1])

distance_none = data_none[0]
distance_schlick = data_schlick[0]
distance_normal = data_normal[0]


diff_per = abs(intensiter_schlick-intensiter_normal)/((intensiter_schlick+intensiter_normal)/2)*100

print(np.mean(diff_per))



plt.plot(distance_none,intensiter_none,label="None",color="black")

#plt.plot(distance_schlick,intensiter_schlick,label="Schlick",color="black")
#plt.plot(distance_normal,intensiter_normal,label="Fresnel",color="blue",linestyle="dashed")

plt.xlabel("Radial Distance (m)")
plt.ylabel("Relative Intensity")

#plt.plot(distance_schlick,diff_per,color="black")
#plt.xlabel("Radial Distance (m)")
#plt.ylabel("Relative Difference (%)")



Intensity=data_none[1]/np.max(data_none[1])
x=distance_none
y=distance_none
distance=distance_none

phi = np.linspace(0, np.pi, 6000)

xx2 = np.zeros((len(Intensity), len(phi)))
yy2 = np.zeros((len(Intensity), len(phi)))
zz2 = np.zeros((len(Intensity), len(phi)))

for zz in range(len(Intensity)):
        xx2[zz, :] = distance[zz] * np.cos(phi)
        yy2[zz, :] = distance[zz] * np.sin(phi)
        zz2[zz, :] = Intensity[zz] 

#C = plt.contourf(xx2, yy2, zz2, 100, cmap="gist_heat",vmin=0.0001, vmax=1)
#clb=plt.colorbar(ticks=[0,0.25,0.5,0.75,1],location="right")
#clb.set_label('Relative Intensity', rotation=270,labelpad=20)
#plt.axis('equal')
#plt.xlabel("x(m)")
#plt.ylabel("y(m)")

#plt.yticks([-0.001,-0.0005,0,0.0005,0.001])
#plt.xticks([-0.001,-0.0005,0,0.0005,0.001])








plt.legend()
plt.show()