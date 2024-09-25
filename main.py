import pygame
import numpy as np
from numba import jit
from pygame import mixer

# Constants
WIDTH, HEIGHT = 1200, 800
NUM_TYPES = 6
types_limit = 5
COLOR_STEP = 360 // NUM_TYPES
NUM_PARTICLES = 2000
particles_limit = 2000
K = 0.05
start = 100


FRICTION = 0.85
RADIUS = 2
fps = 60
fps_limit = 120
#Initializing pygame

pygame.mixer.pre_init()
pygame.init()
mixer.init()

#music variables
music_state = {"sun mother" : False, "ultimate" : True, "is playing" : False, "cornfield chase" : False}

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
particles_display = pygame.Surface((5*WIDTH/6 , HEIGHT))
pygame.display.set_caption("emergent-behaviour")
clock = pygame.time.Clock()
start_surf = pygame.image.load("bg.jpg").convert_alpha()



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

#music initialisation

pygame.mixer.music.load("sun mother.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)


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
textbox_typespart = pygame.Rect(120, 50, 60, 20)
active_types = False


pygame.draw.rect(control_panel, (75,84,92), textbox_typespart)
control_panel.blit(text_typespart, (5,50))
control_panel.blit(text_types_input, (textbox_typespart.x + 5, textbox_typespart.y +5))

#Force
text_fps = font.render('FPS:' , False, font_color) 
text_fps_input = font.render(str(fps), False, font_color)
textbox_fps = pygame.Rect(120,80, 60,20)
active_fps = False

pygame.draw.rect(control_panel, (75,84,92), textbox_fps)
control_panel.blit(text_fps, (5,50))
control_panel.blit(text_fps_input, (textbox_fps.x + 5, textbox_fps.y +5))

#Big bang
text_bang = font.render('Big bang!', False, font_color)
box_bang = pygame.Rect(60, 120, 70, 20)
pygame.draw.rect(control_panel, (75,84,92), box_bang)
control_panel.blit(text_bang, (box_bang.x+5, box_bang.y+5))

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

    #Update display for types of particles
    pygame.draw.rect(control_panel, (75,84,92), textbox_typespart)
    text_types_input = font.render(str(NUM_TYPES), False, font_color)
    control_panel.blit(text_types_input, (textbox_typespart.x + 5, textbox_typespart.y+ 5))
    control_panel.blit(text_typespart, (5,50))

    #Update display for fps
    pygame.draw.rect(control_panel, (75,84,92), textbox_fps)
    text_fps_input = font.render(str(fps), False, font_color)
    control_panel.blit(text_fps_input, (textbox_fps.x + 5, textbox_fps.y+ 5))
    control_panel.blit(text_fps, (5,80))
    
    #Big bang
    text_bang = font.render('Big bang!', False, font_color)
    box_bang = pygame.Rect(60, 120, 70, 20)
    pygame.draw.rect(control_panel, (75,84,92), box_bang)
    control_panel.blit(text_bang, (box_bang.x+5, box_bang.y+5))
    

############################################################################################################################3

#def main(NUM_PARTICLES):
    
#To fix the error
active_fps = False
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

    keys = pygame.key.get_pressed()

    if keys[pygame.K_1]:
        if not music_state["sun mother"]:
            music_state["sun_mother"] = True
            music_state["ultimate"] = False
            music_state["corfield chase"] = False
            pygame.mixer.music.load('Sun Mother.mp3')
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1)
            music_state["is playing"] = True
        elif music_state["is playing"]:
            pygame.mixer.music.pause()
            music_state["is playing"] = False
        else:
            pygame.mixer.music.unpause()
            music_state["is playing"] = True

    if keys[pygame.K_2]:
        if not music_state["ultimate"]:
            music_state["ultimate"] = True
            music_state["sun mother"] = False
            music_state["cornfield chase"] = False
            pygame.mixer.music.load('ultimate.mp3')
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1)
            music_state["is playing"] = True
        elif music_state["is playing"]:
            music_state["is playing"] = False
            pygame.mixer.music.pause()
        else:
            music_state["is playing"] = True
            pygame.mixer.music.unpause()

    if keys[pygame.K_3]:
        if not music_state["cornfield chase"]:
            music_state["cornfield chase"] = True
            music_state["sun mother"] = False
            music_state["ultimate"] = False
            pygame.mixer.music.load('music.mp3')
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1)
            music_state["is playing"] = True
        elif music_state["is playing"]:
            music_state["is playing"] = False
            pygame.mixer.music.pause()
        else:
            music_state["is playing"] = True
            pygame.mixer.music.unpause()


        



         
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
                # Recreates all the particles with updated value for the number of particles
                positions = np.random.rand(NUM_PARTICLES, 2) * [WIDTH, HEIGHT]
                velocities = np.zeros((NUM_PARTICLES, 2))
                types = np.random.randint(0, NUM_TYPES, NUM_PARTICLES)
                forces, min_distances, radii = set_parameters()
            if active_types:
                number = event.key - pygame.K_0
                NUM_TYPES =number
                if NUM_TYPES>types_limit:
                    NUM_TYPES = types_limit
                if NUM_TYPES<1:
                    NUM_TYPES = 1
                #Recreates all the particles with the updated value for the types of particles
                types = np.random.randint(0, NUM_TYPES, NUM_PARTICLES)
                forces, min_distances, radii = set_parameters()
                    
            if active_fps:
                if event.key == pygame.K_BACKSPACE:
                    fps = int(fps/10)
                else:
                    number = event.key - pygame.K_0
                    fps = (fps*10)+number
                    if fps>fps_limit:
                        fps = fps_limit #################################### Control Panel UI stuff ends here
                
            if event.key == pygame.K_r:
                forces, min_distances, radii = set_parameters()
            elif event.key == pygame.K_ESCAPE:
                running = False
        ######################### <Control Panel>
        if event.type == pygame.MOUSEBUTTONDOWN:
            if textbox_noofpart.collidepoint(event.pos): 
                active_particles = True
                active_types = False
                active_fps = False
                
            elif textbox_typespart.collidepoint(event.pos):
                active_particles = False
                active_types = True
                active_fps = False

            elif textbox_fps.collidepoint(event.pos):
                active_fps= True
                active_particles = False
                active_types = False
            else:
                active_particles = False
                active_types = False
                active_fps = False
            if box_bang.collidepoint(event.pos):
                positions=np.full((NUM_PARTICLES,2) , (HEIGHT/2,WIDTH/2))
                
    ##################################### </Control Panel>
    
    while start >= 0:
            screen.blit(start_surf, (0,0))
            pygame.display.update()
            start -= 1
            clock.tick(60)


    update_display()
    if fps != 0:
        particles_display.fill((0, 0, 0))  # Clear screen with black
        positions, velocities = update_particles(positions, velocities, types, forces, min_distances, radii)

        for i in range(NUM_PARTICLES):
            color = pygame.Color(0)
            color.hsva = (types[i] * COLOR_STEP, 100, 100, 100)
            pygame.draw.circle(particles_display, color, (int(positions[i, 0]), int(positions[i, 1])), RADIUS)
    
    
    screen.blit(particles_display, (WIDTH/6,0))
    screen.blit(control_panel, (0,0))
    
    pygame.display.flip()
    clock.tick(fps)  # Limit to 60 FPS

pygame.quit()
#main(NUM_PARTICLES)
