import pygame , random

'''
this file has all the functions and properties of particles
particle class will contain the properties and functions pertaining to particles
create_particles will create a certain number of particles based on the parameter
'''

class Particle:
    def __init__(self,position,velocity,colour,mass,surface):
        self.position=position
        self.velocity=velocity
        self.colour=colour
        self.mass=mass
        self.surface=surface
        pygame.draw.circle(color=self.colour,center=self.position,radius=1,surface=self.surface)
        pygame.display.update()

def create_particles(number_of_particles , surface):
    
    particle_list=[]

    #list of colours:
    red = (255, 0, 0)
    blue = (0,0,255)
    green = (0,255,0)
    
    for i in range(number_of_particles):
        #defining the position,colour and mass of each particle
        position = (random.randint(0,1200) , random.randint(0,800))
        colour = random.choice([red,blue,green])
        mass = random.randint(1 , 10)

        particle_list.append(
            Particle(
                position = position , 
                colour = colour , 
                velocity = 0 , 
                mass = mass , 
                surface = surface
                )
        )
    return particle_list
