import pygame
import random 
  

#general setup
pygame.init()
screen_width = 400
screen_height = 750
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('GUESS CODE')
running = True


score = 0

#load high score
try:
    with open("highscore.txt", "r") as f:
        high_score = int(f.read())
except:
    high_score = 0


#clock
timer = pygame.time.Clock()
framerate = 60

game_over = False
numbers = 0
turn_active = True   


#importing image

surface_image = pygame.image.load("C:/Users/ACER/Downloads/8558071.jpg")

turn    = 0
board   = [[" ", " ", " ", " "],
           [" ", " ", " ", " "],
           [" ", " ", " ", " "],
           [" ", " ", " ", " "],
           [" ", " ", " ", " "],
           [" ", " ", " ", " "],
           [" ", " ", " ", " "],
           [" ", " ", " ", " "],
           [" ", " ", " ", " "],
           [" ", " ", " ", " "],]

huge = pygame.font.Font('freesansbold.ttf',26)

def draw_board():
    global turn
    global board
    for col in range(0,4):
        for row in range(0,10):
            pygame.draw.rect( screen , "white" ,[ col*60 + 15 , row*60 + 15 , 50 , 50 ], 3 ,3 )
            place_text = huge.render(board[row][col],True,'white')
            screen.blit(place_text,(col*60+25,row*60+25))
    pygame.draw.rect( screen , "green" ,[ 10 , turn * 60 + 10 , 240 , 60 ], 2 ,2 )

#Game function

# generates a four-digit code 
def gene():  
    code = [] 
    
    for i in range(4): 
        index = random.randint(0, 9) 
        code.append(index) 
          
    return code 
      
#initialising generate function and converting array 
#to int and then int to string
secret_number = str("".join(map(str, gene())))
print("New Result :",secret_number)

def check_board():
    global turn
    global board
    global secret_number
    for col in range(0,4):
        for row in range(0,10):
            if secret_number[col] == board[row][col] and turn > row :
                pygame.draw.rect( screen , "green" ,[ col*60 + 15 , row*60 + 15 , 50 , 50 ], 0 ,3 )
            elif board[row][col] in secret_number and turn > row :
                pygame.draw.rect( screen , "orange" ,[ col*60 + 15 , row*60 + 15 , 50 , 50 ], 0 ,3 )


        
        
while running:
    #event

    timer.tick(framerate)

    screen.fill("darkgrey")
    screen.blit(surface_image,(-1260,-650))
    check_board()
    draw_board() 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.TEXTINPUT and turn_active and not game_over:
            entry = event.__getattribute__('text')
            board[turn][numbers] = entry
            numbers += 1 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and numbers > 0:
                board[turn][numbers-1] = ' '
                numbers -= 1
            if event.key == pygame.K_SPACE and not game_over:
                turn += 1
                numbers = 0
            if event.key == pygame.K_SPACE and game_over:
                turn = 0
                game_over = False
                secret_number = str("".join(map(str, gene())))
                print("New Result :",secret_number)
                board   = [[" ", " ", " ", " "],
                           [" ", " ", " ", " "],
                           [" ", " ", " ", " "],
                           [" ", " ", " ", " "],
                           [" ", " ", " ", " "],
                           [" ", " ", " ", " "],
                           [" ", " ", " ", " "],
                           [" ", " ", " ", " "],
                           [" ", " ", " ", " "],
                           [" ", " ", " ", " "]]
                numbers = -1
       
    
    for row in range(0,10):
        guess = board[row][0]+ board[row][1]+ board[row][2]+ board[row][3]
        if guess == secret_number and row < turn and not game_over:
           game_over = True
           score +=1
           #high score
           # Update high score
           if score > high_score:
               high_score = score
               with open("highscore.txt", "w") as f:
                   f.write(str(high_score))
           break
    
    
    if numbers == 4:
        turn_active = False
    if numbers < 4:
        turn_active = True      
    #draw the game

    if turn == 10:
        game_over = True
        score = 0 
        loser_text = huge.render('Loser! (Woo woo!!)',True,"yellow")
        screen.blit(loser_text,(40,650))
        

    if game_over and turn < 10:
        winner_text = huge.render('Winner!',True,"yellow")
        screen.blit(winner_text,(40,650))
        
    
    score_display = huge.render('Your Score :'+ str(score),True,"yellow")
    screen.blit(score_display,(20,710))

    high_score_display = huge.render('High Score : ' + str(high_score), True, "yellow")
    screen.blit(high_score_display, (200, 710))


    pygame.display.update()


pygame.quit()