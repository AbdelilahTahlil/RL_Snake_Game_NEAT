import sys
import os

import pygame
import random
import numpy as np


pygame.init()
font = pygame.font.Font('arial.ttf', 25)



BLACK= 0, 0, 0
BLUE= 0, 0, 255
GREEN = 0, 128, 0
WHITE= 255, 255, 255
BLOCK_SIZE= 20
BLOCK_DISTANCE= 2
#WINDOW_SIZE = BLOCK_SIZE*30
SPEED= 50

APPLE = pygame.image.load(os.path.join('img', 'apple.png'))
APPLE= pygame.transform.smoothscale(APPLE, (BLOCK_SIZE, BLOCK_SIZE)) 
apple_rect= APPLE.get_rect()


class Point:
    def __init__(self, x, y):
        self.x=x
        self.y=y

class Direction:
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3
    

class Snake():
    def __init__(self,x,y,radars_range, window_width, window_height):
        self.is_alive = True

        self.direction = Direction.RIGHT
        self.w = window_width
        self.h = window_height

        self.head = Point(x,y)
        self.body = [
            self.head,
            Point(self.head.x- BLOCK_SIZE, self.head.y),
            Point(self.head.x-2*BLOCK_SIZE , self.head.y),
        ]
        self.radars_range= radars_range
        self.radars =[] # list of coordinates of start point and end point of every one of the 3 radars
        self.dist_radars =[] # the distance of the closest obstacles from the radars (max = radars_range)
        self.apple_radars_dist = [] # the distance of the apple from the radars (max = radars_range)
    
    def update_radars(self, obstacles, apple): 
        
        # update self.dist_radars, self.apple_radars_dist
        self._check_radars(obstacles, apple) 

        # update self.radars
        if self.direction == Direction.RIGHT:
            self.radars = [
                (((self.head.x+BLOCK_SIZE//2), self.head.y), ((self.head.x+BLOCK_SIZE//2), self.head.y - self.dist_radars[0]*BLOCK_SIZE)),
                (((self.head.x+BLOCK_SIZE), self.head.y+BLOCK_SIZE//2), ((self.head.x+BLOCK_SIZE*(self.dist_radars[1]+1)), self.head.y+BLOCK_SIZE//2)),
                (((self.head.x+BLOCK_SIZE//2), self.head.y+BLOCK_SIZE), ((self.head.x+BLOCK_SIZE//2), self.head.y + (self.dist_radars[2]+1)*BLOCK_SIZE))
            ]
        elif self.direction == Direction.DOWN :
            self.radars = [
                ((self.head.x+BLOCK_SIZE, self.head.y+BLOCK_SIZE//2), (self.head.x+BLOCK_SIZE*(self.dist_radars[0]+1), self.head.y+BLOCK_SIZE//2)),
                ((self.head.x+BLOCK_SIZE//2, self.head.y+BLOCK_SIZE), (self.head.x+BLOCK_SIZE//2, self.head.y+BLOCK_SIZE*(self.dist_radars[1]+1))),
                ((self.head.x, self.head.y+BLOCK_SIZE//2), (self.head.x-BLOCK_SIZE*self.dist_radars[2], self.head.y+BLOCK_SIZE//2))
            ]
        
        elif self.direction == Direction.LEFT:
            self.radars =  [
                ((self.head.x+BLOCK_SIZE//2, self.head.y+BLOCK_SIZE), (self.head.x+BLOCK_SIZE//2, self.head.y+BLOCK_SIZE*(self.dist_radars[0]+1))),
                ((self.head.x, self.head.y+BLOCK_SIZE//2), (self.head.x-BLOCK_SIZE*self.dist_radars[1], self.head.y+BLOCK_SIZE//2)),
                ((self.head.x+BLOCK_SIZE//2, self.head.y), (self.head.x+BLOCK_SIZE//2, self.head.y-BLOCK_SIZE*(self.dist_radars[2])))
            ]
        elif self.direction == Direction.UP:
            self.radars = [
                ((self.head.x, self.head.y+BLOCK_SIZE//2), (self.head.x-BLOCK_SIZE*self.dist_radars[0], self.head.y+BLOCK_SIZE//2)),
                ((self.head.x+BLOCK_SIZE//2, self.head.y), (self.head.x+BLOCK_SIZE//2, self.head.y-BLOCK_SIZE*self.dist_radars[1])),
                ((self.head.x+BLOCK_SIZE, self.head.y+BLOCK_SIZE//2), (self.head.x+BLOCK_SIZE*(self.dist_radars[2]+1), self.head.y+BLOCK_SIZE//2))
            ]



    def _check_radars(self, obstacles, apple):
        dist_radar_l, dist_radar_s, dist_radar_r = self.radars_range, self.radars_range, self.radars_range # radar_left, radar_straight, radar_right
        for obst in obstacles:
            temp_dist_radar_l, temp_dist_radar_s, temp_dist_radar_r = self._compute_radars_distance(obst)
            if temp_dist_radar_l < dist_radar_l:
                dist_radar_l = temp_dist_radar_l
            if temp_dist_radar_s < dist_radar_s:
                dist_radar_s = temp_dist_radar_s
            if temp_dist_radar_r < dist_radar_r:
                dist_radar_r = temp_dist_radar_r
        

        for part in self.body[1:]:
            temp_dist_radar_l, temp_dist_radar_s, temp_dist_radar_r = self._compute_radars_distance(part)
            if temp_dist_radar_l < dist_radar_l:
                dist_radar_l = temp_dist_radar_l
            if temp_dist_radar_s < dist_radar_s:
                dist_radar_s = temp_dist_radar_s
            if temp_dist_radar_r < dist_radar_r:
                dist_radar_r = temp_dist_radar_r
        
        self.apple_radars_dist= self._compute_radars_distance(apple)
        self.dist_radars= (dist_radar_l, dist_radar_s, dist_radar_r)
    


    def _compute_radars_distance(self, point):
        dist_radar_l, dist_radar_s, dist_radar_r = self.radars_range, self.radars_range, self.radars_range
        if self.direction==Direction.RIGHT:
            if point.x==self.head.x and point.y < self.head.y:
                if (abs(point.y-self.head.y)//BLOCK_SIZE)-1 < dist_radar_l:
                    dist_radar_l = (abs(point.y-self.head.y)//BLOCK_SIZE)-1
            elif point.x==self.head.x and point.y > self.head.y:
                if (abs(point.y-self.head.y)//BLOCK_SIZE)-1 < dist_radar_r:
                    dist_radar_r = (abs(point.y-self.head.y)//BLOCK_SIZE)-1
            elif point.y==self.head.y and point.x > self.head.x:
                if (abs(point.x-self.head.x)//BLOCK_SIZE)-1 < dist_radar_s:
                    dist_radar_s = (abs(point.x-self.head.x)//BLOCK_SIZE)-1
        
        if self.direction==Direction.DOWN:
            if point.y==self.head.y and point.x > self.head.x:
                if (abs(point.x-self.head.x)//BLOCK_SIZE)-1 < dist_radar_l:
                    dist_radar_l = (abs(point.x-self.head.x)//BLOCK_SIZE)-1
            elif point.y==self.head.y and point.x < self.head.x:
                if (abs(point.x-self.head.x)//BLOCK_SIZE)-1 < dist_radar_r:
                    dist_radar_r = (abs(point.x-self.head.x)//BLOCK_SIZE)-1
            elif point.x==self.head.x and point.y > self.head.y:
                if (abs(point.y-self.head.y)//BLOCK_SIZE)-1 < dist_radar_s:
                    dist_radar_s = (abs(point.y-self.head.y)//BLOCK_SIZE)-1
        
        if self.direction==Direction.LEFT:
            if point.x==self.head.x and point.y > self.head.y:
                if (abs(point.y-self.head.y)//BLOCK_SIZE)-1 < dist_radar_l:
                    dist_radar_l = (abs(point.y-self.head.y)//BLOCK_SIZE)-1
            elif point.x==self.head.x and point.y < self.head.y:
                if (abs(point.y-self.head.y)//BLOCK_SIZE)-1 < dist_radar_r:
                    dist_radar_r = (abs(point.y-self.head.y)//BLOCK_SIZE)-1
            elif point.y==self.head.y and point.x < self.head.x:
                if (abs(point.x-self.head.x)//BLOCK_SIZE)-1 < dist_radar_s:
                    dist_radar_s = (abs(point.x-self.head.x)//BLOCK_SIZE)-1
        
        if self.direction==Direction.UP:
            if point.y==self.head.y and point.x < self.head.x:
                if (abs(point.x-self.head.x)//BLOCK_SIZE)-1 < dist_radar_l:
                    dist_radar_l = (abs(point.x-self.head.x)//BLOCK_SIZE)-1
            elif point.y==self.head.y and point.x > self.head.x:
                if (abs(point.x-self.head.x)//BLOCK_SIZE)-1 < dist_radar_r:
                    dist_radar_r = (abs(point.x-self.head.x)//BLOCK_SIZE)-1
            elif point.x==self.head.x and point.y < self.head.y:
                if (abs(point.y-self.head.y)//BLOCK_SIZE)-1 < dist_radar_s:
                    dist_radar_s = (abs(point.y-self.head.y)//BLOCK_SIZE)-1

        return  (dist_radar_l, dist_radar_s, dist_radar_r)

    def move(self, direction, obstacles, apple):
        ate_apple = False
        self.direction = direction
                
        self.head = self.next_point(direction)
        self.body.insert(0, self.head)

        if (self.head.x == apple.x and
            self.head.y == apple.y):
            reward = 20
            ate_apple = True
        else: 
            reward = 0
            self.body.pop()
        
        if self.is_dead(obstacles):
            self.is_alive = False
            reward = -10
        
        self.update_radars(obstacles, apple)
        return reward, ate_apple
    
    def next_point(self, direction) :
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            if x + BLOCK_SIZE >= self.w:
                x = 0
            else:
                x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            if x <= 0:
                x = self.w -BLOCK_SIZE
            else:
                x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            if y + BLOCK_SIZE >= self.h:
                y = 0
            else:
                y += BLOCK_SIZE
        elif direction == Direction.UP:
            if y <= 0:
                y = self.h -BLOCK_SIZE
            else:
                y -= BLOCK_SIZE
        return Point(x, y)

    def is_dead(self, obstacles):
        for part in self.body[1:]:
            if (self.head.x == part.x) and (self.head.y == part.y):
                return True
        for obst in obstacles:
            if (self.head.x == obst.x) and (self.head.y == obst.y):
                return True
        return False
    

    def get_state(self) :
        radars_l, radar_s, radar_r = self.apple_radars_dist
        
        apple_l, apple_s, apple_r = self.apple_radars_dist

        return [radars_l, radar_s, radar_r, apple_l, apple_s, apple_r]





class SnakeGameAI:

    def __init__(self,nets, snakes, width= 640, height= 480, num_obstacles=5, radars_range=3):
        self.w = width
        self.h = height
        self.nets = nets
        self.snakes = snakes
        self.frame_iteration = 0 
        #--self.score = 0

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake Game AI')
        self.clock = pygame.time.Clock()
        self.num_obstacles = num_obstacles
        #--self.radars_range= radars_range
        #--self.reset()
        #--self.direction = Direction.RIGHT
        
        self.place_apple_and_obstacles()
        self._update_all_radars(self.obstacles, self.apple)
        self.update_ui()
        



    def place_apple_and_obstacles(self):
        self.apple = apple_rect
        self.apple.x, self.apple.y = (
            random.randint(0,self.w//BLOCK_SIZE -5)*BLOCK_SIZE,
            random.randint(0,self.h//BLOCK_SIZE -5)*BLOCK_SIZE
        )

        list_of_x = random.choices(
            list(set(range(self.w//BLOCK_SIZE)).difference({self.apple.x//BLOCK_SIZE})),
            k=self.num_obstacles
        )
        list_of_y = random.choices(
            list(set(range(self.h//BLOCK_SIZE)).difference({self.apple.y//BLOCK_SIZE})),
            k=self.num_obstacles
        )
        self.obstacles= [
            Point(
                x*BLOCK_SIZE,
                y*BLOCK_SIZE
            ) for x,y in zip(list_of_x, list_of_y)
        ]
    

    def _update_all_radars(self, obstacles, apple):
        for snake in self.snakes:
            snake.update_radars(obstacles, apple)



    def update_ui(self):
        self.display.fill(BLACK)
        for snake in self.snakes:
            if snake.is_alive:
                for part in snake.body:
                    pygame.draw.rect(
                        self.display,
                        BLUE,
                        pygame.Rect(part.x,
                        part.y,
                        BLOCK_SIZE-BLOCK_DISTANCE,
                        BLOCK_SIZE-BLOCK_DISTANCE
                        )
                    )
                for radar in snake.radars:
                    depart_pos = radar[0]
                    arrival_pos = radar[1]
                    pygame.draw.line(self.display, (0, 255, 0), depart_pos, arrival_pos, 1)
                    pygame.draw.circle(self.display, (0, 255, 0), arrival_pos, 5)
            
        for obst in self.obstacles:
            pygame.draw.rect(
                self.display,
                WHITE,
                pygame.Rect(
                    obst.x,
                    obst.y,
                    BLOCK_SIZE-BLOCK_DISTANCE,
                    BLOCK_SIZE-BLOCK_DISTANCE
                )
            )
        
        self.display.blit(APPLE, apple_rect)

        #-----text = font.render(f"Score: {self.score}. Game: {n_game}.", True, WHITE)
        #-------self.display.blit(text, [0, 0])
        pygame.display.flip()

    def play(self):
        # action = [left, straight, right]
        self.frame_iteration += 1

        # check if user closed the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        still_alive = 0
        rewards = [0]*len(self.snakes)
        for i, snake in enumerate(self.snakes) :
            if snake.is_alive:
                still_alive += 1
                
                state = snake.get_state()
                current_direction = snake.direction

                output = self.nets[i].activate(state)
                action = [0,0,0]
                action[output.index(max(output))] = 1

                # convert action to direction
                next_direction = current_direction
                if np.array_equal(action, [1, 0, 0]): # action = turn left
                    next_direction = (current_direction-1)%4
                elif np.array_equal(action, [0, 0, 1]): # action = turn right
                    next_direction = (current_direction+1)%4

                reward, ate_apple = snake.move(next_direction, self.obstacles, self.apple)
                rewards[i] = reward

                if ate_apple :
                    self.place_apple_and_obstacles()
                    
        

        # update user interface
        self.update_ui()
        self.clock.tick(SPEED)

        game_over = False
        if ((still_alive == 0) or
            (self.frame_iteration > 300)):
            game_over = True

        return game_over, still_alive, rewards

