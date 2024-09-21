import pygame 
pygame.init()


###Simulation variables###
particles = 2000
particles_limit = 2000
types = 2
types_limit = 5
force = 10

##########################

resolution_x = 1200
resolution_y = 800
fps = 60

window = pygame.display.set_mode((resolution_x,resolution_y))
window.fill((0,0,0))
###########################################
### The actual control panel UI ####
bg_color = (43, 41, 41)
font = pygame.font.Font(None, 20)
font_color = (255,255,255)

control_panel = pygame.Surface((resolution_x/6, resolution_y))
control_panel.fill(bg_color)

#No of particles
text_noofpart = font.render('No of particles:' , False, font_color) 
text_particles_input = font.render(str(particles), False, font_color)
textbox_noofpart = pygame.Rect(120,15, 60,20)
active_particles = False

pygame.draw.rect(control_panel, (75,84,92), textbox_noofpart)
control_panel.blit(text_noofpart, (5,20))
control_panel.blit(text_particles_input, (textbox_noofpart.x + 5, textbox_noofpart.y +5))

#Types of particles
text_typespart = font.render('Types of particles:' , False, font_color) 
text_types_input = font.render(str(types), False, font_color)
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
window.blit(control_panel, (0,0))
############################################
def update_display():
    #Clearing the display
    control_panel.fill(bg_color)
    
    #Update display for no of particles
    pygame.draw.rect(control_panel, (75,84,92), textbox_noofpart)
    text_particles_input = font.render(str(particles), False, font_color)
    control_panel.blit(text_particles_input, (textbox_noofpart.x + 5, textbox_noofpart.y+ 5))
    control_panel.blit(text_noofpart, (5,20))

    #Update display for types of particles
    pygame.draw.rect(control_panel, (75,84,92), textbox_typespart)
    text_types_input = font.render(str(types), False, font_color)
    control_panel.blit(text_types_input, (textbox_typespart.x + 5, textbox_typespart.y+ 5))
    control_panel.blit(text_typespart, (5,50))

    #Update display for force
    pygame.draw.rect(control_panel, (75,84,92), textbox_force)
    text_force_input = font.render(str(force), False, font_color)
    control_panel.blit(text_force_input, (textbox_force.x + 5, textbox_force.y+ 5))
    control_panel.blit(text_force, (5,80))

    window.blit(control_panel, (0,0))
    pygame.display.flip()

#########################################3

pygame.display.flip()
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

        if event.type == pygame.KEYDOWN:
            if active_particles:
                if event.key == pygame.K_BACKSPACE:
                    particles = int(particles/10)
                else:
                    number = event.key - pygame.K_0
                    particles = (particles*10)+number
                    if particles> particles_limit:
                        particles = particles_limit
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
                    # if force>types_limit:
                    #     types = types_limit
        
        #if event.type == pygame.KEYDOWN:
    
    update_display()
            


