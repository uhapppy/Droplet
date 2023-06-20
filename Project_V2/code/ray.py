import numpy as np
import math

class Ray:
    def __init__(self, origin, direction,intensity):
        self.origin = origin 
        self.direction = direction #should be a unit vector
        self.intensity = intensity

        self.end = None
        self.lenght = None


    def get_point(self, t):
        return self.origin + t * self.direction
    
    def get_t_from_x(self, x):
        return (x - self.origin[0])/self.direction[0]
    
    def get_t_from_y(self, y):
        return (y - self.origin[1])/self.direction[1]
    
    def get_line(self):
        x=np.array([self.origin[0],self.end[0]])
        y=np.array([self.origin[1],self.end[1]])
        return np.array([x,y])



    #give the angle between the normal and the incident ray
    def get_normal_angle(self,normal_direction):

        return math.acos(np.dot(self.direction,normal_direction)/(np.linalg.norm(self.direction)*np.linalg.norm(normal_direction)))
    
    #give the angle between the normal and the transmitted ray
    def get_snell_angle(self,normal_direction,n_incident,n_transmitted):
        return math.asin(n_incident/n_transmitted * math.sin(self.get_normal_angle(normal_direction)))
    
    #return the xy point of intersection between the ray and the ellipse
    def get_intersection_ellispse(self, ellipse:Ellipsis) : 
        a = ellipse.radius_y**2 * self.direction[0]**2 + ellipse.radius_x**2 * self.direction[1]**2
        b = 2*ellipse.radius_y**2 * self.direction[0] * self.origin[0] + 2*ellipse.radius_x**2 * self.direction[1] * self.origin[1]
        c = ellipse.radius_y**2 * self.origin[0]**2 + ellipse.radius_x**2 * self.origin[1]**2 - ellipse.radius_x**2 * ellipse.radius_y**2 






        delta = b**2 - 4*a*c

        if delta < 0 :
            return None
        else :
            t1 = (-b - math.sqrt(delta))/(2*a)
            t2 = (-b + math.sqrt(delta))/(2*a)


        if t1>0:
            return self.get_point(t1)
        elif t2>0:
            return self.get_point(t2)
    
class IncomingRay(Ray):
    def __init__(self, origin, direction,intensity):
        super().__init__(origin, direction,intensity)
        

        

        self.reflected_ray=None
        self.refracted_ray_1=None
        self.refracted_ray_2=None
        self.refracted_ray_3=None





    def get_rays(self,normal, n_air, n_drop,ellipse,screen_heigth,fresnel):
        self.get_reflected_ray(normal)
        self.get_refracted_rays(normal,n_air,n_drop,ellipse)

        self.reflected_ray.end = self.reflected_ray.get_point(self.reflected_ray.get_t_from_y(screen_heigth))
        self.refracted_ray_3.end = self.refracted_ray_3.get_point(self.refracted_ray_3.get_t_from_y(screen_heigth))



        if fresnel=="schlick":

            if self.end[0]<0:
                reflected_angle = -self.get_normal_angle(normal.direction)
            if self.end[0]>=0:
                reflected_angle = self.get_normal_angle(normal.direction)


            R0 = ((n_air-n_drop)/(n_air+n_drop))**2


            R = R0 + (1-R0)*((1-np.cos(reflected_angle))**5)

            

            self.reflected_ray.intensity = self.intensity*R
            self.refracted_ray_3.intensity = self.intensity*(1-R)



        if fresnel=="normal":
            if self.end[0]<0:
                reflected_angle = -self.get_normal_angle(normal.direction)
            if self.end[0]>=0:
                reflected_angle = self.get_normal_angle(normal.direction)


            cos_transmitted_angle = math.sqrt(1-(n_air/n_drop)**2*math.sin(reflected_angle)**2)


            #Rs 
            Rs_numerator = n_air * math.cos(reflected_angle) - n_drop * cos_transmitted_angle
            Rs_denominator = n_air * math.cos(reflected_angle) + n_drop * cos_transmitted_angle

            Rs = (Rs_numerator/Rs_denominator)**2

            #Rp

            Rp_numerator = n_air * cos_transmitted_angle - n_drop * math.cos(reflected_angle)
            Rp_denominator = n_air * cos_transmitted_angle + n_drop * math.cos(reflected_angle)

            Rp = (Rp_numerator/Rp_denominator)**2

            R = (Rs+Rp)/2
            
            self.reflected_ray.intensity = self.intensity*R
            self.refracted_ray_3.intensity = self.intensity*(1-R)





        return self.reflected_ray, self.refracted_ray_1, self.refracted_ray_2, self.refracted_ray_3
        




    def get_reflected_ray(self, normal): #returns the reflected ray

        if self.end[0]<0:
            reflected_angle = -2*self.get_normal_angle(normal.direction)
        if self.end[0]>=0:
            reflected_angle = 2*self.get_normal_angle(normal.direction)




        reflected_origin = normal.origin 
        x_direction = math.sin(reflected_angle)
        y_direction = math.cos(reflected_angle)
        reflected_direction = np.array([x_direction,y_direction])



        self.reflected_ray = Ray(origin=reflected_origin,
                                 direction=reflected_direction,
                                 intensity=self.intensity)
        
        
        
        
        
    def get_refracted_rays(self,normal, n_air, n_drop,ellipse):

        #ray 1 
        ray_1_angle = self.get_snell_angle(normal.direction,n_incident = n_air , n_transmitted = n_drop)
        ray_1_origin = self.end


        if self.end[0]>=0:
            x_direction = math.sin(ray_1_angle-self.get_normal_angle(normal.direction))
            y_direction = -math.cos(ray_1_angle-self.get_normal_angle(normal.direction))

        if self.end[0]<0:
            x_direction = math.sin(self.get_normal_angle(normal.direction)-ray_1_angle)
            y_direction = -math.cos(self.get_normal_angle(normal.direction)-ray_1_angle)








        ray_1_direction = np.array([x_direction,y_direction])

        refracted_ray_1 = Ray(origin=ray_1_origin,direction=ray_1_direction,intensity=self.intensity)

        self.refracted_ray_1 = refracted_ray_1
        
        self.refracted_ray_1.end = self.refracted_ray_1.get_point(self.refracted_ray_1.get_t_from_y(0))




        
        #ray 2

        ray_2_origin = self.refracted_ray_1.end

        ray_2_angle = self.refracted_ray_1.get_normal_angle(np.array([0,1]))


        if self.end[0]<0:
            x_direction = math.sin(ray_2_angle)
            y_direction = -math.cos(ray_2_angle)

        if self.end[0]>=0:
            x_direction = -math.sin(ray_2_angle)
            y_direction = -math.cos(ray_2_angle)

        ray_2_direction = np.array([x_direction,y_direction])

        self.refracted_ray_2 = Ray(origin=ray_2_origin,direction=ray_2_direction,intensity=self.intensity)

        self.refracted_ray_2.end = self.refracted_ray_2.get_intersection_ellispse(ellipse)
        


        #ray 3
        
        ray_3_origin = self.refracted_ray_2.end


        normal_3 = ellipse.get_normal(ellipse.get_theta_from_x(ray_3_origin[0]),outward=True)

        ray_3_angle = self.refracted_ray_2.get_snell_angle(normal_3,n_incident=n_drop,n_transmitted=n_air)


        if self.end[0]>=0:
            x_direction = -math.sin(ray_3_angle-self.get_normal_angle(normal.direction))
            y_direction = math.cos(ray_3_angle-self.get_normal_angle(normal.direction))

        if self.end[0]<0:
            x_direction = -math.sin(self.get_normal_angle(normal.direction)-ray_3_angle)
            y_direction = math.cos(self.get_normal_angle(normal.direction)-ray_3_angle)

        ray_3_direction = np.array([x_direction,y_direction])

        self.refracted_ray_3 = Ray(origin=ray_3_origin,direction=ray_3_direction,intensity=self.intensity)
        
        





    