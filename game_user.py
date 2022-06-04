import sys
import os

import pygame
import random


pygame.init()



BLACK= 0, 0, 0
BLUE= 0, 0, 255
GREEN = 0, 128, 0
WHITE= 255, 255, 255
BLOCK_SIZE= 20
BLOCK_DISTANCE= 2
WINDOW_SIZE = BLOCK_SIZE*30
SPEED= 8

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
    


class SnakeGame:

    def __init__(self, width= 640, height= 480, num_obstacles=5):
        self.w = width
        self.h = height
        

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()

        self.head = Point(self.w/2, self.h/2)
        self.snake = [
            self.head,
            Point(self.head.x- BLOCK_SIZE, self.head.y),
            Point(self.head.x-2*BLOCK_SIZE , self.head.y),
        ]
        self.num_obstacles = num_obstacles
        self.place_apple_and_obstacles()
        
        self.direction = Direction.RIGHT
        self.score = 0

        self.update_ui()
    
    def place_apple_and_obstacles(self):
        self.apple = apple_rect
        self.apple.x, self.apple.y = (
            random.randint(0,WINDOW_SIZE//BLOCK_SIZE -1)*BLOCK_SIZE,
            random.randint(0,WINDOW_SIZE//BLOCK_SIZE -1)*BLOCK_SIZE
        )

        list_of_x = random.choices(range(self.w//BLOCK_SIZE), k=self.num_obstacles)
        list_of_y = random.choices(range(self.h//BLOCK_SIZE), k=self.num_obstacles)
        self.obstacles= [
            Point(
                x*BLOCK_SIZE,
                y*BLOCK_SIZE
            ) for x,y in zip(list_of_x, list_of_y)
        ]

    def update_ui(self):
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
        self.display.blit(APPLE, apple_rect)
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
        pygame.display.flip()


    def _move(self, direction):
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
        
        self.head = Point(x, y)
        self.snake.insert(0, self.head)
        if (self.head.x in range(self.apple.x, self.apple.x + BLOCK_SIZE) and
            self.head.y in range(self.apple.y, self.apple.y + BLOCK_SIZE)):
            self.score += 1
            self.place_apple_and_obstacles()
        else: 
            self.snake.pop()
        

    def play(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = (self.direction-1)%4
                elif event.key == pygame.K_RIGHT:
                    self.direction = (self.direction+1)%4
        
        self._move(self.direction)
        self.update_ui()
        self.clock.tick(SPEED)

        return self._is_collision(), self.score


    
    def _is_collision(self):
        for part in self.snake[1:]:
            if (self.head.x == part.x) and (self.head.y == part.y):
                return True
        for obst in self.obstacles:
            if (self.head.x == obst.x) and (self.head.y == obst.y):
                return True
        return False



if __name__ == '__main__':
    game= SnakeGame(width=WINDOW_SIZE, height=WINDOW_SIZE)

    while True:
        is_collision, score = game.play()
        if is_collision:
            print('Score: ', score)
            sys.exit()
    
    
    




        