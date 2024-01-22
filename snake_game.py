

import pygame, sys
from pygame.math import Vector2
from random import randint
from pygame import mixer
  

pygame.init()

# colours
white = pygame.Color(255, 255, 255)
black = pygame.Color(0, 0, 0)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 102, 0)
brown= pygame.Color(153, 76, 0)
yellow = pygame.Color(255, 255, 0)
blue = pygame.Color(0, 0, 204)
pink = pygame.Color(255, 0, 255)
purple= pygame.Color(102, 0, 204)
orange = pygame.Color(255, 153, 51)
lime = pygame.Color(178, 255, 102)
sky_blue = pygame.Color(153, 255, 255)

#load sounds
game_over_fx = mixer.Sound("audio/Game_Over.wav")
game_over_fx.set_volume(0.5)
pick_up_fx = mixer.Sound("audio/Snake_Pickup_Food.wav")
pick_up_fx.set_volume(0.5)


# game constants 
cell_size = 10
cell_number = 40
screen_dimensions = cell_size * cell_number
clock = pygame.time.Clock()
bk_color = black
screen = pygame.display.set_mode((screen_dimensions, screen_dimensions))
pygame.display.set_caption('Snake Game')
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 80)


class FRUIT:
    
    def __init__(self):
        self.randomize()
        self.fruit_color = pink
        
        
    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.position.x * cell_size), int(self.position.y * cell_size), cell_size, cell_size)
        pygame.draw.rect(screen, self.fruit_color, fruit_rect)
        
    def randomize(self):
        self.x = randint(0, cell_number - 1)
        self.y = randint(0, cell_number - 1)
        self.position = Vector2(self.x, self.y)
        
  
class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.add_new_body = False
        self.score = 0
        self.snake_color = purple
        
    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            body_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, self.snake_color, body_rect)
    
    def move_snake(self):
        if self.add_new_body == False:
            body_copy = self.body[:-1]
            body_copy.insert(0, (body_copy[0] + self.direction))
            self.body = body_copy[:]
        else:
            body_copy = self.body[:]
            body_copy.insert(0, (body_copy[0] + self.direction))
            self.body = body_copy[:]
            self.add_new_body = False
        
    def add_new_block(self):
        self.add_new_body = True
            
        
class MAIN:
    click = False
    current_color = None
    
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
    
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
        
    def draw_elements(self):
        self.snake.draw_snake()
        self.fruit.draw_fruit()
    
    def check_collision(self):
        if self.fruit.position == self.snake.body[0]:
            pick_up_fx.play()
            self.snake.score += 1
            self.fruit.randomize()
            self.snake.add_new_block()
            
    def check_fail(self):
        # check if snake head collides with game borders
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            game_over_fx.play()
            self.game_over()
    
        # check if snake head hits its own body 
        for block in self.snake.body[2:]:
            if block == self.snake.body[0]:
                game_over_fx.play()
                self.game_over()
    
    def game_over(self):
        
        while True:
            
            
            mx, my = pygame.mouse.get_pos()
            retry_button = pygame.Rect(180, 190, 35, 20) 
            pygame.draw.rect(screen, bk_color, retry_button)
            self.draw_text("Retry!", 16, white, 180, 190)
            
            
                
            if retry_button.collidepoint((mx, my)):
                if MAIN.click:
                    new_game = MAIN()
                    if MAIN.current_color != None:
                        new_game.snake.snake_color = MAIN.current_color
                    new_game.main_menu()
                    
                  
            MAIN.click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        new_game = MAIN()
                        new_game.main_menu()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        MAIN.click = True
                        
            pygame.display.update()
            clock.tick(60)  
            
            
                
    def draw_text(self, text, font_size, color, x, y):
        font = pygame.font.SysFont('arial', font_size)
        textobj = font.render(text, True, color)
        screen.blit(textobj, (x, y))
        
    def main_menu(self):
        
        
        while True:
            
            screen.fill(white)
            self.draw_text("Main Menu", 18, black, 7, 10)
            
            mx, my = pygame.mouse.get_pos()
            
            play_button = pygame.Rect(50, 40, 70, 20)
            play_button.center = (43, 45)
            options_button = pygame.Rect(50, 40, 70,20)
            options_button.center = (43, 75)
            
            
            if play_button.collidepoint((mx, my)):
                if MAIN.click:
                    self.game()
            
            if options_button.collidepoint((mx, my)):
                if MAIN.click:
                    self.options()
                    
            pygame.draw.rect(screen, red, play_button)
            pygame.draw.rect(screen, red, options_button)
            
            self.draw_text("Play", 18,  black, 30, 33)
            self.draw_text("Options",18, black, 22, 63)
            
            MAIN.click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        MAIN.click = True
            
            pygame.display.update()
            clock.tick(60)   
                    
    def game(self):
        running = True
        while running:
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == SCREEN_UPDATE:
                    self.update()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_w:
                        if self.snake.direction.y != 1:
                            self.snake.direction = Vector2(0, -1)
                    if event.key == pygame.K_s:
                        if self.snake.direction.y != -1:
                            self.snake.direction = Vector2(0, 1)
                    if event.key == pygame.K_a:
                        if self.snake.direction.x != 1:
                            self.snake.direction = Vector2(-1, 0)
                    if event.key == pygame.K_d:
                        if self.snake.direction.x != -1:
                            self.snake.direction = Vector2(1, 0)
            
            screen.fill(bk_color)
            self.draw_text(f"Score: {self.snake.score}", 16, white, 5, 5)
            self.draw_elements()
            pygame.display.update()
            clock.tick(60)    
    
    
    def options(self):
        running = True
        while running:
            screen.fill(white)
            
            
            mx, my = pygame.mouse.get_pos()
            
            # menu for snake color option
            red_option = pygame.Rect(10, 35, cell_size * 3, cell_size * 3)
            pygame.draw.rect(screen, red, red_option)
            
            green_option = pygame.Rect(50, 35, cell_size * 3, cell_size * 3)
            pygame.draw.rect(screen, green, green_option)
            
            yellow_option = pygame.Rect(10, 75, cell_size * 3, cell_size * 3)
            pygame.draw.rect(screen, yellow, yellow_option)
            
            brown_option = pygame.Rect(50, 75, cell_size * 3, cell_size * 3)
            pygame.draw.rect(screen, brown, brown_option)
            
            blue_option = pygame.Rect(10, 115, cell_size * 3, cell_size * 3)
            pygame.draw.rect(screen, blue, blue_option)
            
            pink_option = pygame.Rect(50, 115, cell_size * 3, cell_size * 3)
            pygame.draw.rect(screen, pink, pink_option)
            
            purple_option = pygame.Rect(10, 155, cell_size * 3, cell_size * 3)
            pygame.draw.rect(screen, purple, purple_option)
            
            orange_option = pygame.Rect(50, 155, cell_size * 3, cell_size * 3)
            pygame.draw.rect(screen, orange, orange_option)
            
            lime_option = pygame.Rect(10, 195, cell_size * 3, cell_size * 3)
            pygame.draw.rect(screen, lime, lime_option)
            
            sky_blue_option = pygame.Rect(50, 195, cell_size * 3, cell_size * 3)
            pygame.draw.rect(screen, sky_blue, sky_blue_option)
            
            
            # color menu logic  
            if red_option.collidepoint((mx, my)):
                if MAIN.click:
                        option_game = MAIN()
                        option_game.snake.snake_color = red
                        MAIN.current_color = red
                        option_game.game()
            elif green_option.collidepoint((mx, my)):
                if MAIN.click:
                        option_game = MAIN()
                        option_game.snake.snake_color = green
                        MAIN.current_color = green
                        option_game.game()
            elif yellow_option.collidepoint((mx, my)):
                if MAIN.click:
                        option_game = MAIN()
                        option_game.snake.snake_color = yellow
                        MAIN.current_color = yellow
                        option_game.game()
            elif brown_option.collidepoint((mx, my)):
                if MAIN.click:
                        option_game = MAIN()
                        option_game.snake.snake_color = brown
                        MAIN.current_color = brown
                        option_game.game()
            elif blue_option.collidepoint((mx, my)):
                if MAIN.click:
                        option_game = MAIN()
                        option_game.snake.snake_color = blue
                        MAIN.current_color = blue
                        option_game.game()
            elif pink_option.collidepoint((mx, my)):
                if MAIN.click:
                        option_game = MAIN()
                        option_game.snake.snake_color = pink
                        MAIN.current_color = pink
                        option_game.game()
            elif purple_option.collidepoint((mx, my)):
                if MAIN.click:
                        option_game = MAIN()
                        option_game.snake.snake_color = purple
                        MAIN.current_color = purple
                        option_game.game()
            elif orange_option.collidepoint((mx, my)):
                if MAIN.click:
                        option_game = MAIN()
                        option_game.snake.snake_color = orange
                        MAIN.current_color = orange
                        option_game.game()
            elif lime_option.collidepoint((mx, my)):
                if MAIN.click:
                        option_game = MAIN()
                        option_game.snake.snake_color = lime
                        MAIN.current_color = lime
                        option_game.game()
            elif sky_blue_option.collidepoint((mx, my)):
                if MAIN.click:
                        option_game = MAIN()
                        option_game.snake.snake_color = sky_blue
                        MAIN.current_color = sky_blue
                        option_game.game()
                                                
            
            self.draw_text("Select a color for the snake", 16,black , 8, 8)
            
            MAIN.click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        MAIN.click = True
                        
            pygame.display.update()
            clock.tick(60)
                            
            
            
main_game  = MAIN()
main_game.main_menu()


