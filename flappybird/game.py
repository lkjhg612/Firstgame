#thư viện pygame
import pygame, sys, random, os

pygame.init()

#biến khởi tạo trong game
p = 0.2 #biến trọng lực 

midbirdy = 0 #trục y của chim giữa 
 
score = 0 #điểm ban đẩu 

highscore = 0

ttf_path = os.path.join(sys.path[0], '04B_19.TTF')

gamefont = pygame.font.Font('04B_19.TTF', 40) #font

gameplay = True


#thay đổi lần thứ 1
#thay đổi lần thứ 2 
#thay đổi lần thứ 3



#tiêu đề và icon 
pygame.display.set_caption('Flappy bird')
icon = pygame.image.load(r'flappybird\assets\yellowbird-downflap.png')

#thêm background
background = pygame.image.load(r'flappybird\assets\background-night.png')
background = pygame.transform.scale2x(background) #kéo dài hình background lên hai lần

# floor
floor = pygame.image.load(r'flappybird\assets\floor.png')
floor = pygame.transform.scale2x(floor)
floorchay = 0

#set fps cho game
clock = pygame.time.Clock() 

#set icon 
pygame.display.set_icon(icon)

#cửa sổ game
screen = pygame.display.set_mode((432, 768))

#âm thanh 
flap_sound = pygame.mixer.Sound(r'flappybird\sound\sfx_wing.wav')#đập cánh
hit_sound = pygame.mixer.Sound(r'flappybird\sound\sfx_hit.wav')#đụng cột 
score_sound = pygame.mixer.Sound(r'flappybird\sound\sfx_point.wav') # có điểm
score_sound_count = 100

# chim giữa
midbird = pygame.image.load(r'flappybird\assets\yellowbird-midflap.png')
midbird = pygame.transform.scale2x(midbird)
midbird_rectangle = midbird.get_rect(center = (100, 386)) #tạo cho chinh thành 1 hình chữ nhật 

#ống 
pipesurface = pygame.image.load(r'flappybird\assets\pipe-green.png')
pipesurface = pygame.transform.scale2x(pipesurface)
pipe_list = []

#thời gian ống xuất hiện
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 4000) #1.2 giây sẽ tạo ra ống mới 
pipeheight = [200, 300 , 400] #chọn ra 3 chiều cao ngẫu nhiên 

# game over
screenover = pygame.image.load(r'flappybird\assets\message.png')
screenover = pygame.transform.scale2x(screenover)
screenover_rectangle = screenover.get_rect(center = (216, 334)) #tạo cho chinh thành 1 hình chữ nhật giảm đi kích thước màn hình kết thức đi một nửa


#hàm điểm 
def scoreview():
    # điểm đang chơi 
    if gameplay:
        scorefont = gamefont.render(f'Score: {int(score)}', True, (255, 255, 255))
        scorerectangle = scorefont.get_rect(center = (200, 100))
        screen.blit(scorefont, scorerectangle) # blit dùng để vẽ một đối tượng 
    #game over
    if gameplay == False:
        #điểm chơi
        scorefont = gamefont.render(f'Score: {int(score)}', True, (255, 255, 255))
        scorerectangle = scorefont.get_rect(center = (200, 30))
        screen.blit(scorefont, scorerectangle) # blit dùng để vẽ một đối tượng 
        #điểm cao nhất   
        highscorefont = gamefont.render(f'highscore: {int(highscore)}', True, (255, 255, 255))
        highscorerectangle = highscorefont.get_rect(center = (200, 70))
        screen.blit(highscorefont, highscorerectangle) # blit dùng để vẽ một đối tượng 
 
#hàm tạo ống 
def create_pipe():
    randompipe = random.choice(pipeheight)
    new_pipe = pipesurface.get_rect(midtop = (500, randompipe))
    toppipe = pipesurface.get_rect(midtop = (500, randompipe-650))
    return new_pipe, toppipe

#hàm di chuyển ống 
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx-=5
    return pipes
# ham vẽ ong 
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipesurface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipesurface, False, True) # với trục x là fale trục y là true là lật theo trục y
            screen.blit(flip_pipe, pipe)

def checkcollision(pipes):
    for pipe in pipes:
        if midbird_rectangle.colliderect(pipe):
            hit_sound.play()
            return False
    if midbird_rectangle.bottom >= 668: #768 - 100 or midbird_rectangle.top <= 75
        hit_sound.play()
        return False
 
    return True  
#hàm kiểm tra va chạm
# def check_vacham(pipes):
#     for pipe in pipes:
#         if midbird_rectangle.bottom >= 668: #768 - 100 or midbird_rectangle.top <= 75
#             return False
#         else:
#             return True  

# def rotate_bird(bird1):
#     new_bird = pygame.transform.rotozoom(bird1, midbirdy, 1)
#     return new_bird
def rotate_bird(bird1):
    newbird = pygame.transform.rotozoom(bird1, -midbirdy*2, 1) #chúi xuống 4 lần 
    return newbird

#vòng lặp xử lý game
running = True
while running: 
    
    for event in pygame.event.get():
        # kiểm ấn để thoát 
        if event.type == pygame.QUIT:
            running = False                 
            
        #kiểm tra ấn space để bay
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_SPACE and gameplay:
                midbirdy = -6 
                flap_sound.play()
            if event.key == pygame.K_SPACE and gameplay == False:       
                gameplay = True
                midbirdy = 0
                midbird_rectangle.center = (100, 386) 
                score = 0 
                pipe_list.clear()

        if event.type == spawnpipe:
                pipe_list.extend(create_pipe()) #thêm ống vào danh sách 
                # print(create_pipe)

    # đưa hình vào chim
    screen.blit(background,(0,0)) 

    #pipe
    pipe_list = move_pipe(pipe_list)
    draw_pipe(pipe_list)

    # floor chạy giảm trục x đi một đơn vị 
    floorchay -= 1 

    #tăng y lên 600 để floor xuống dưới 
    screen.blit(floor, (floorchay, 650)) 
    screen.blit(floor, (floorchay+432, 650))    
    if floorchay == -432:
        floorchay = 0

    if gameplay:

        # screen.blit(midbird, (midbird_rectangle))
        
    #tăng trục y lên vs đơn vị là trọng lực 
        midbirdy += p 
       
         # đưa chim giữa vào
        midbird_rectangle.centery += midbirdy

        #xoay chim
        birdrotate = rotate_bird(midbird)
        
        # screen.blit(midbird, midbird_rectangle)
        # screen.blit(midbird, midbird_rectangle)
        screen.blit(birdrotate, midbird_rectangle)

        # gameplay = check_vacham()   #kiểm tra chạm sàn
        gameplay = checkcollision(pipe_list) #kiểm tra con chim va chạm ống 
        score_sound_count -= 1
        if score_sound_count <= 0:
            score_sound.play()
            score_sound_count = 100

        
    #tăng điểm lên 1 
        score += 0.01
        if score > highscore: 
            highscore=score

        scoreview()

 

    else:   
       screen.blit(screenover, screenover_rectangle)
       scoreview()


    pygame.display.update()
    clock.tick(120) #120 fps 