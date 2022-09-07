import pygame
import math
import time
from utils import scale_image, blit_rotate_center

GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("imgs/track.png"), 0.9)
TRACK_BORDER = scale_image(pygame.image.load("imgs/track-border.png"), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = pygame.image.load("imgs/finish.png")
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITIONS = (130, 250)
RED_CAR = scale_image(pygame.image.load("imgs/red-car.png"), 0.55)
GREEN_CAR = scale_image(pygame.image.load("imgs/green-car.png"), 0.55)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Racing Game!")
FPS = 60
PATH = [(160, 133), (118, 75), (58, 124), (58, 429), (82, 502), (244, 662), (338, 741), (396, 712), 
(408, 563), (458, 488), (559, 488), (602, 551), (608, 686), (674, 736), (752, 683), (739, 396), (689, 371),
 (454, 369), (409, 331), (439, 267), (693, 264), (744, 199), (736, 107), (681, 80), (321, 78),
(275, 134), (276, 352), (235, 423), (181, 373), (166, 281)]

class AbstractCar:

    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel  = 0
        self.rotation_vel = rotation_vel
        self.angle = 180
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left= False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle-= self.rotation_vel   

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)  

    def move_forward(self):
        self.vel = min(self.vel +self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move(self):
        radians =  math.radians(self.angle)
        verticle = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.x -= horizontal
        self.y -= verticle

    def collide(self, mask, x=0 , y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x-x), int(self.y-y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0 
        self.vel = 0   

class PlayerCar(AbstractCar):

    IMG = RED_CAR
    START_POS = (180, 200)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()    

    def bounce(self):
        self.vel =- self.vel
        self.move()

class ComputerCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (150, 200)

    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel)
        self.path  = path
        self.current_point =0 
        self.vel = max_vel

    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255, 0, 0), point, 5)   

    def draw(self, win):
        super().draw(win)
        self.draw_points(win)   

    def calculate_angle(self):
        target_x , target_y  = self.path[self.current_point]
        x_diff = target_x -self.x
        y_diff = target_y -self.y

        if y_diff ==0:
            desired_radian_angle = math.pi/2
        else:
            desired_radian_angle = math.atan(x_diff/y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi    



    def move(self):
        if self.current_point >= len(self.path):
            return


        self.calculate_angle()
        self.update_path_point()
        super().move()             

def draw(win, images, player_car, computer_car):
    for img, pos in images:
        win.blit(img, pos)
    
    player_car.draw(win)
    computer_car.draw(win)
    pygame.display.update()



def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False



    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)        
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()        
    
    if keys[pygame.K_x]:
        moved = True
        player_car.move_backward() 

    if not moved:
        player_car.reduce_speed()



run = True
clock = pygame.time.Clock()
images = [(GRASS, (0,0)), (TRACK, (0,0)), (FINISH, FINISH_POSITIONS), (TRACK_BORDER, (0,0))]

player_car = PlayerCar(4, 4)
computer_car = ComputerCar(4,4, PATH)
while run:
    clock.tick(FPS)
    draw(WIN, images, player_car, computer_car)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break


    move_player(player_car)

    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()

    finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POSITIONS)

    if finish_poi_collide != None:
        if finish_poi_collide[1]==0 :
            player_car.bounce()  
        else: 
            player_car.reset()
            print("Finish")   

print(computer_car.path)
pygame.quit()        

