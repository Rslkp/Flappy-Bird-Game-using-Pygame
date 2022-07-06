import pygame,sys,random

from pygame.constants import K_SPACE

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 444))
    screen.blit(floor_surface,(floor_x_pos + 288, 444))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (412,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (412,random_pipe_pos - 150))
    return bottom_pipe, top_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -=5
    visible_pipes = [pipe for pipe in pipes if pipe.right > -25]
    return visible_pipes

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)

def check_collision(pipes):
    global can_score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            can_score = True 
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= 444:
        fall_under__sound.play()
        can_score = True
        return False

    return True  

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-bird_movement*3,1)
    return new_bird

def bird_animation():
    new_bird = bird_frame[bird_index]
    new_bird_rect = new_bird.get_rect(center = (50,bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == "main_game":
        score_surface = game_font.render(str(int(score)),True,(0,0,0))
        score_rect = score_surface.get_rect(center = (144,50))
        screen.blit(score_surface,score_rect)
    if game_state == "game_over":
        score_surface = game_font.render(f"Score; {int(score)}",True,(0,0,0))
        score_rect = score_surface.get_rect(center = (144,50))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f"High Score; {int(high_score)}",True,(0,0,0))
        high_score_rect = high_score_surface.get_rect(center = (144,425))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score
        
def pipe_score_check():
    global score , can_score

    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and can_score: 
                score +=1
                score_sound.play()
                can_score = False

            if pipe.centerx < 0:
                can_score = True

pygame.init()

screen = pygame.display.set_mode((288,512))
clock = pygame.time.Clock()
game_font = pygame.font.Font("04B_19.TTF",20)

#variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True

bg_surface = pygame.image.load("background-night.png")

floor_surface = pygame.image.load("base.png")
floor_x_pos = 0

bird_downflap = pygame.image.load("bluebird-downflap.png")
bird_midflap = pygame.image.load("bluebird-midflap.png")
bird_upflap = pygame.image.load("bluebird-upflap.png")
bird_frame = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frame[bird_index]
bird_rect = bird_surface.get_rect(center = (50,256))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)

bird_surface = pygame.image.load("bluebird-midflap.png")
bird_rect = bird_surface.get_rect(center = (50,256))

pipe_surface = pygame.image.load("pipe-red.png")
pipe_list = []
SWANPIPE = pygame.USEREVENT
pygame.time.set_timer(SWANPIPE,1200)
pipe_height = [200,300,400]

game_over_surface = pygame.image.load("message.png")
game_over_rect = game_over_surface.get_rect(center=(144,256))


flap_sound = pygame.mixer.Sound("sound track\sfx_wing.wav")
death_sound = pygame.mixer.Sound("sound track\sfx_hit.wav")
fall_under__sound = pygame.mixer.Sound("sound track\sfx_die.wav")
down_going_sound = pygame.mixer.Sound("sound track\sfx_swooshing.wav")
score_sound = pygame.mixer.Sound("sound track\sfx_point.wav")
score_sound_cuntdown = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement = -7
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50,256)
                bird_movement = 0
                score = 0
        if event.type == SWANPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index <2:
                bird_index += 1
            else:
                bird_index = 0 
            bird_surface,bird_rect = bird_animation()


    
    screen.blit(bg_surface,(0,0))
   
    if game_active:
        #bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collision(pipe_list)

        #pipe
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)

        #score
        pipe_score_check()
        score_display('main_game')
        
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display("game_over")
    

    #floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -288:
        floor_x_pos = 0

    
    

    pygame.display.update()
    clock.tick(60)


