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
SPEED= 20

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
    


class SnakeGameAI:

    def __init__(self, width= 640, height= 480, num_obstacles=5, radars_range=3):
        self.w = width
        self.h = height
        
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake Game AI')
        self.clock = pygame.time.Clock()
        self.num_obstacles = num_obstacles
        self.radars_range= radars_range
        self.reset()
        self.update_ui(0)
    
    def reset(self):
        self.frame_iteration = 0 
        self.score = 0

        self.head = Point(self.w/2, self.h/2)
        self.snake = [
            self.head,
            Point(self.head.x- BLOCK_SIZE, self.head.y),
            Point(self.head.x-2*BLOCK_SIZE , self.head.y),
        ]
        
        self.direction = Direction.RIGHT
        
        self.place_apple_and_obstacles()
        self._update_radars()
        
        
    def _update_radars(self): 
        self._check_radars()
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
    

    def _check_radars(self):
        dist_radar_l, dist_radar_s, dist_radar_r = self.radars_range, self.radars_range, self.radars_range # radar_left, radar_straight, radar_right
        for obst in self.obstacles:
            temp_dist_radar_l, temp_dist_radar_s, temp_dist_radar_r = self._compute_radars_distance(obst)
            if temp_dist_radar_l < dist_radar_l:
                dist_radar_l = temp_dist_radar_l
            if temp_dist_radar_s < dist_radar_s:
                dist_radar_s = temp_dist_radar_s
            if temp_dist_radar_r < dist_radar_r:
                dist_radar_r = temp_dist_radar_r
        

        for part in self.snake[1:]:
            temp_dist_radar_l, temp_dist_radar_s, temp_dist_radar_r = self._compute_radars_distance(part)
            if temp_dist_radar_l < dist_radar_l:
                dist_radar_l = temp_dist_radar_l
            if temp_dist_radar_s < dist_radar_s:
                dist_radar_s = temp_dist_radar_s
            if temp_dist_radar_r < dist_radar_r:
                dist_radar_r = temp_dist_radar_r
        
        self.apple_radars_dist= self._compute_radars_distance(self.apple)
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


    def update_ui(self, n_game):
        self.display.fill(BLACK)
        for part in self.snake:
            pygame.draw.rect(
                self.display,
                BLUE,
                pygame.Rect(part.x,
                part.y,
                BLOCK_SIZE-BLOCK_DISTANCE,
                BLOCK_SIZE-BLOCK_DISTANCE
                )
            )
        
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
        
        for radar in self.radars:
            depart_pos = radar[0]
            arrival_pos = radar[1]
            pygame.draw.line(self.display, (0, 255, 0), depart_pos, arrival_pos, 1)
            pygame.draw.circle(self.display, (0, 255, 0), arrival_pos, 5)
        self.display.blit(APPLE, apple_rect)

        text = font.render(f"Score: {self.score}. Game: {n_game}.", True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def play(self, action, n_game):
        # action = [left, straight, right]
        self.frame_iteration += 1

        # check if user closed the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # convert action to direction
        if np.array_equal(action, [1, 0, 0]): # action = turn left
            self.direction = (self.direction-1)%4
        elif np.array_equal(action, [0, 0, 1]): # action = turn right
            self.direction = (self.direction+1)%4
        
        # move and get the reward of that move
        reward = self._move(self.direction)

        game_over = False
        # check if game over
        if (self._is_collision(self.head) or
            self.frame_iteration > 100*len(self.snake)): # to avoid infinite loops
            game_over = True
            reward = -10
            return game_over, reward, self.score
        
        # update user interface
        self.update_ui(n_game)
        self.clock.tick(SPEED)

        return game_over, reward, self.score
    

    def _move(self, direction):
                
        self.head = self._next_point(direction)
        self.snake.insert(0, self.head)
        if (self.head.x == self.apple.x and
            self.head.y == self.apple.y):
            self.score += 1
            reward = 20
            self.place_apple_and_obstacles()
        else: 
            reward = 0
            self.snake.pop()
        
        self._update_radars()
        return reward
    
    def _next_point(self, direction) :
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
    

    def _is_collision(self, point):
        for part in self.snake[1:]:
            if (point.x == part.x) and (point.y == part.y):
                return True
        for obst in self.obstacles:
            if (point.x == obst.x) and (point.y == obst.y):
                return True
        return False

    
    def get_state(self):
        # danger location
        danger_left = self._is_collision(self._next_point((self.direction-1)%4))
        danger_straight = self._is_collision(self._next_point(self.direction))
        danger_right = self._is_collision(self._next_point((self.direction+1)%4))

        # current direction
        dir_r = self.direction == Direction.RIGHT
        dir_d = self.direction == Direction.DOWN
        dir_l = self.direction == Direction.LEFT
        dir_u = self.direction == Direction.UP

        # apple location
        apple_left = ((dir_r and self.apple.y < self.head.y) or 
            (dir_d and self.apple.x > self.head.x) or 
            (dir_l and self.apple.y > self.head.y) or 
            (dir_u and self.apple.x < self.head.x))

        apple_straight = ((dir_r and self.apple.x > self.head.x) or 
            (dir_d and self.apple.y > self.head.y) or 
            (dir_l and self.apple.x < self.head.x) or 
            (dir_u and self.apple.y < self.head.y))

        apple_right = ((dir_r and self.apple.y > self.head.y) or 
            (dir_d and self.apple.x < self.head.x) or 
            (dir_l and self.apple.y < self.head.y) or 
            (dir_u and self.apple.x > self.head.x))

        return [
            danger_left,
            danger_straight,
            danger_right,
            #dir_r,
            #dir_d,
            #dir_l,
            #dir_u,
            apple_left,
            apple_straight,
            apple_right
        ]

