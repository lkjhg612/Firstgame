#thư viện pygame
import pygame
pygame.init()

#biến khởi tạo trong game
p = 0.2 #biến trọng lực 

midbirdy = 0 #trục y của chim giữa 
 
score = 0 #điểm ban đẩu 

highscore = 0

gamefont = pygame.font.Font('04B_19.TTF', 40) #font

gameplay = True


def scoreview():
    if gameplay:
        scorefont = gamefont.render(f'Score: {int(score)}', True, (255, 255, 255))
        scorerectangle = scorefont.get_rect(center = (200, 100))
        screen.blit(scorefont, scorerectangle) # blit dùng để vẽ một đối tượng 
    if gameplay == False:
        #điểm chơi
        scorefont = gamefont.render(f'Score: {int(score)}', True, (255, 255, 255))
        scorerectangle = scorefont.get_rect(center = (200, 30))
        screen.blit(scorefont, scorerectangle) # blit dùng để vẽ một đối tượng 
        #điểm cao nhất   
        highscorefont = gamefont.render(f'highscore: {int(highscore)}', True, (255, 255, 255))
        highscorerectangle = highscorefont.get_rect(center = (200, 70))
        screen.blit(highscorefont, highscorerectangle) # blit dùng để vẽ một đối tượng 

#tiêu đề và icon 
pygame.display.set_caption('Flappy bird')
icon = pygame.image.load(r'assets\yellowbird-downflap.png')

#thêm background
background = pygame.image.load(r'D:\python project\vs code\flappybird\assets\background-night.png')
background = pygame.transform.scale2x(background) #kéo dài hình background lên hai lần

floor = pygame.image.load(r'D:\python project\vs code\flappybird\assets\floor.png')
floor = pygame.transform.scale2x(floor)
floorchay = 0

#set icon 
pygame.display.set_icon(icon)

#cửa sổ game
screen = pygame.display.set_mode((432, 768))

# chim giữa
midbird = pygame.image.load(r'D:\python project\vs code\flappybird\assets\yellowbird-midflap.png')
midbird = pygame.transform.scale2x(midbird)
midbird_rectangle = midbird.get_rect(center = (100, 386)) #tạo cho chinh thành 1 hình chữ nhật 


# game over
screenover = pygame.image.load(r'D:\python project\vs code\flappybird\assets\message.png')
screenover = pygame.transform.scale2x(screenover)
screenover_rectangle = screenover.get_rect(center = (216, 334)) #tạo cho chinh thành 1 hình chữ nhật giảm đi kích thước màn hình kết thức đi một nửa

#hàm kiểm tra va chạm
def check_vacham():
    if midbird_rectangle.bottom >= 668 or midbird_rectangle.top <= 75: #768 - 100
        return False
    else:
        return True  


#vòng lặp xử lý game
running = True
while running: 
    
    for event in pygame.event.get():
        # kiểm ấn x để thoát 
        if event.type == pygame.QUIT:
            running = False
            
        #kiểm tra ấn space để bay
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and gameplay:
                midbirdy = -6 
            if event.key == pygame.K_SPACE and gameplay == False:
                gameplay = True
                midbirdy = 0
                midbird_rectangle.center = (100, 386) 
                score = 0 

    # đưa hình vào chim
    screen.blit(background,(0,0)) 
    # floor chạy giảm trục x đi một đơn vị 
    floorchay -= 1 

    #tăng y lên 600 để floor xuống dưới 
    screen.blit(floor, (floorchay, 600)) 
    screen.blit(floor, (floorchay+432, 600))
    if floorchay == -432:
        floorchay = 0

    if gameplay:


    # đưa chim giữa vào
        screen.blit(midbird, (midbird_rectangle))

    #tăng trục y lên vs đơn vị là trọng lực 
        midbirdy += p 

        midbird_rectangle.centery += midbirdy

    #tăng điểm lên 1 
        score += 0.01
        if score > highscore: 
            highscore=score

        scoreview()

        gameplay = check_vacham()
    else:   
       screen.blit(screenover, screenover_rectangle)
       scoreview()


    pygame.display.update()