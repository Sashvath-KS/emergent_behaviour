import pygame
import numpy as np
from numba import jit



# Constants
WIDTH, HEIGHT = 1200, 800
NUM_TYPES = 6
types_limit = 5
COLOR_STEP = 360 // NUM_TYPES
NUM_PARTICLES = 2000
particles_limit = 2000
K = 0.05
force = 10
force_limit = 9999999
FRICTION = 0.85
RADIUS = 2

#Initializing pygame

pygame.init()

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
particles_display = pygame.Surface((5*WIDTH/6 , HEIGHT))
pygame.display.set_caption("emergent-behaviour")
clock = pygame.time.Clock()

@jit(nopython=True)



def update_particles(positions, velocities, types, forces, min_distances, radii):
    num_particles = len(positions)
    new_positions = np.empty_like(positions)
    new_velocities = np.empty_like(velocities)

    for i in range(num_particles):
        total_force_x, total_force_y = 0.0, 0.0
        pos_x, pos_y = positions[i]
        vel_x, vel_y = velocities[i]
        p_type = types[i]
        
        for j in range(num_particles): 
            if i != j:
                dir_x = positions[j, 0] - pos_x
                dir_y = positions[j, 1] - pos_y
                
                # Apply periodic boundary conditions
                if dir_x > 0.5 * WIDTH:
                    dir_x -= WIDTH
                if dir_x < -0.5 * WIDTH:
                    dir_x += WIDTH
                if dir_y > 0.5 * HEIGHT:
                    dir_y -= HEIGHT
                if dir_y < -0.5 * HEIGHT:
                    dir_y += HEIGHT
                
                dis = np.sqrt(dir_x**2 + dir_y**2)
                if dis > 0:
                    dir_x, dir_y = dir_x / dis, dir_y / dis # Normalize the direction vector
                    other_type = types[j]
                    if dis < min_distances[p_type, other_type]:
                        force = abs(forces[p_type, other_type]) * -3 * (1 - dis / min_distances[p_type, other_type]) * K
                        total_force_x += dir_x * force
                        total_force_y += dir_y * force
                    if dis < radii[p_type, other_type]:
                        force = forces[p_type, other_type] * (1 - dis / radii[p_type, other_type]) * K
                        total_force_x += dir_x * force
                        total_force_y += dir_y * force

        new_vel_x = vel_x + total_force_x
        new_vel_y = vel_y + total_force_y
        new_pos_x = (pos_x + new_vel_x) % WIDTH
        new_pos_y = (pos_y + new_vel_y) % HEIGHT
        new_vel_x *= FRICTION
        new_vel_y *= FRICTION
        
        new_positions[i] = new_pos_x, new_pos_y
        new_velocities[i] = new_vel_x, new_vel_y

    return new_positions, new_velocities

def set_parameters():
    forces = np.random.uniform(0.3, 1, (NUM_TYPES, NUM_TYPES))
    mask = np.random.random((NUM_TYPES, NUM_TYPES)) < 0.5
    forces[mask] *= -1
    min_distances = np.random.uniform(30, 50, (NUM_TYPES, NUM_TYPES))
    radii = np.random.uniform(70, 250, (NUM_TYPES, NUM_TYPES))
    return forces, min_distances, radii

###############################################################################################################
### The actual control panel UI ####
bg_color = (43, 41, 41)
font = pygame.font.Font(None, 20)
font_color = (255,255,255)

control_panel = pygame.Surface((WIDTH/6, HEIGHT))
control_panel.fill(bg_color)

#No of particles
text_noofpart = font.render('No of particles:' , False, font_color) 
text_particles_input = font.render(str(NUM_PARTICLES), False, font_color)
textbox_noofpart = pygame.Rect(120,15, 60,20)
active_particles = False

pygame.draw.rect(control_panel, (75,84,92), textbox_noofpart)
control_panel.blit(text_noofpart, (5,20))
control_panel.blit(text_particles_input, (textbox_noofpart.x + 5, textbox_noofpart.y +5))

#Types of particles
text_typespart = font.render('Types of particles:' , False, font_color) 
text_types_input = font.render(str(NUM_TYPES), False, font_color)
textbox_typespart = pygame.Rect(120,50, 60,20)
active_types = False

pygame.draw.rect(control_panel, (75,84,92), textbox_typespart)
control_panel.blit(text_typespart, (5,50))
control_panel.blit(text_types_input, (textbox_typespart.x + 5, textbox_typespart.y +5))

#Force 
text_force = font.render('Force:' , False, font_color) 
text_force_input = font.render(str(force), False, font_color)
textbox_force = pygame.Rect(120,80, 60,20)
active_force = False

pygame.draw.rect(control_panel, (75,84,92), textbox_force)
control_panel.blit(text_force, (5,50))
control_panel.blit(text_force_input, (textbox_force.x + 5, textbox_force.y +5))

#Overall blitting control panel on the window
screen.blit(control_panel, (0,0))

def update_display():
    #Clearing the display
    control_panel.fill(bg_color)
    
    #Update display for no of particles
    pygame.draw.rect(control_panel, (75,84,92), textbox_noofpart)
    text_particles_input = font.render(str(NUM_PARTICLES), False, font_color)
    control_panel.blit(text_particles_input, (textbox_noofpart.x + 5, textbox_noofpart.y+ 5))
    control_panel.blit(text_noofpart, (5,20))
    print("Reaching here 1")

    #Update display for types of particles
    pygame.draw.rect(control_panel, (75,84,92), textbox_typespart)
    text_types_input = font.render(str(NUM_TYPES), False, font_color)
    control_panel.blit(text_types_input, (textbox_typespart.x + 5, textbox_typespart.y+ 5))
    control_panel.blit(text_typespart, (5,50))
    print("Reaching here 2")

    #Update display for force
    pygame.draw.rect(control_panel, (75,84,92), textbox_force)
    text_force_input = font.render(str(force), False, font_color)
    control_panel.blit(text_force_input, (textbox_force.x + 5, textbox_force.y+ 5))
    control_panel.blit(text_force, (5,80))
    print("Reaching here 3")

    
    

############################################################################################################################3

def main(NUM_PARTICLES):
    
    #To fix the error
    active_force = False
    active_particles = False
    active_types = False

    # Create particles
    positions = np.random.rand(NUM_PARTICLES, 2) * [WIDTH, HEIGHT]
    velocities = np.zeros((NUM_PARTICLES, 2))
    types = np.random.randint(0, NUM_TYPES, NUM_PARTICLES)
    forces, min_distances, radii = set_parameters()

    # Main game loop
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if active_particles:####################################################   Control Panel UI Stuff starts here
                    if event.key == pygame.K_BACKSPACE:
                        NUM_PARTICLES= int(NUM_PARTICLES/10)
                    else:
                        number = event.key - pygame.K_0
                        NUM_PARTICLES = (NUM_PARTICLES*10)+number
                        if NUM_PARTICLES> particles_limit:
                            NUM_PARTICLES = particles_limit
                if active_types:
                    if event.key == pygame.K_BACKSPACE:
                        types = int(types/10)
                    else:
                        number = event.key - pygame.K_0
                        types = (types*10)+number
                        if types>types_limit:
                            types = types_limit
                if active_force:
                    if event.key == pygame.K_BACKSPACE:
                        force = int(force/10)
                    else:
                        number = event.key - pygame.K_0
                        force = (force*10)+number
                        if force>types_limit:
                            types = types_limit #################################### Control Panel UI stuff ends here
                if event.key == pygame.K_r:
                    forces, min_distances, radii = set_parameters()
                elif event.key == pygame.K_ESCAPE:
                    running = False
            ######################### <Control Panel>
            if event.type == pygame.MOUSEBUTTONDOWN:
                if textbox_noofpart.collidepoint(event.pos): 
                    active_particles = True
                    active_types = False
                    active_force = False
                    
                elif textbox_typespart.collidepoint(event.pos):
                    active_particles = False
                    active_types = True
                    active_force = False

                elif textbox_force.collidepoint(event.pos):
                    active_force= True
                    active_particles = False
                    active_types = False
                else:
                    active_particles = False
                    active_types = False
                    active_force = False
        ##################################### </Control Panel>
        particles_display.fill((0, 0, 0))  # Clear screen with black
        update_display()
        positions, velocities = update_particles(positions, velocities, types, forces, min_distances, radii)

        for i in range(NUM_PARTICLES):
            color = pygame.Color(0)
            color.hsva = (types[i] * COLOR_STEP, 100, 100, 100)
            pygame.draw.circle(particles_display, color, (int(positions[i, 0]), int(positions[i, 1])), RADIUS)
            
        screen.blit(particles_display, (WIDTH/6,0))
        screen.blit(control_panel, (0,0))
        
        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS
    
    pygame.quit()
main(NUM_PARTICLES)
