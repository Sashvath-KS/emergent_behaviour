import pygame,sys , particles

#to start pygame

pygame.init()
pygame.mixer.init()

#window and its attributes
window_width=1200
window_height=800
window_size=(window_width,window_height)
window=pygame.display.set_mode(window_size)
pygame.display.set_caption('particle-life simulator')

#to regulate framerate
clock=pygame.time.Clock()


def main():
    
    #creates particles
    particles.create_particles(
        number_of_particles = 1000,
        surface = window)

    while True:

        #event loop that detects any keyboard input and mouse clicks
        for event in pygame.event.get():
            
            #to quit the game
            
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                sys.exit()
        
        
        #updates the sceen and controls FPS or frame rate
        pygame.display.update()
        clock.tick(100)


main()