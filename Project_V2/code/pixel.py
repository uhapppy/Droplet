import numpy as np

class Pixel :
    def __init__(self,width,start,end) -> None:
        self.start=start
        self.end=end
        self.width = width
        
        self.intensity = 0

        self.reflected_path = None
        self.reflected_rays = None

        self.refracted_path = []
        self.refracted_rays = []