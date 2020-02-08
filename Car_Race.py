import pygame
from pygame.locals import *
import sys
import time
import random


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800
DEFAULT_FPS = 50
DEFAULT_DELAY = 1.0 / DEFAULT_FPS
fps = 0

class Race_Car:
    def __init__(self,window):
        self.window = window
        self.img = pygame.image.load("img/Race_Car.png")
        self.width = 75
        self.height = 100
        self.img = pygame.transform.scale(self.img,(self.width,self.height))
        self.x = 37.5
        self.y = 500


    def move_right(self):
        if self.x < 487.5:
            self.x += 150
            print(self.x)

    def move_left(self):
        if self.x > 37.5:
            self.x -= 150

    def show(self):
        self.window.blit(self.img, (self.x, self.y))


class Obstacle:
    def __init__(self, window):
        self.window = window
        self.img = pygame.image.load("img/obstacle.jpg")
        self.width = 100
        self.height = 100
        self.img = pygame.transform.scale(self.img, (self.width, self.height))
        lane_no = random.randint(0,4)
        self.x = 25 + lane_no * 150
        self.y = 0

    def drop(self):
        self.y += 10

    def is_out(self):
        return self.y >= 800

    def show(self):
        self.drop()
        self.window.blit(self.img, (self.x, self.y))


if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    pygame.display.set_caption('Car Race')

    bg = pygame.image.load('img/Lane.jpg')
    font = pygame.font.Font('font/happy.ttf', 28)

    sound = pygame.mixer.Sound("snd/bomb.wav")

    pygame.mixer_music.load("snd/bg2.ogg")
    pygame.mixer_music.play(-1)

    obstacles = []
    loop_count = 0
    is_over = False
    score = 0
    car = Race_Car(window)


    while True:
        start = time.time()

        window.blit(bg, (0, 0))
        fps_text = font.render('FPS: %d' % fps, True, (0xFF, 0, 0))
        window.blit(fps_text, (460, 15))
        score_text = font.render('Score: %d' % score, True, (0xFF, 0, 0))
        window.blit(score_text, (20, 15))
        car.show()

        if is_over:
            finish_font = pygame.font.Font('font/happy.ttf', 50)
            finish_text = finish_font.render('Game Over', True, (0xFF, 0, 0))
            window.blit(finish_text, (200, 200))

            finish_score_text = finish_font.render('Score: %d' % score, True, (0xFF, 0, 0))
            window.blit(finish_score_text, (220, 300))

            quit_text = finish_font.render('Press Q to quit', True, (0xFF, 0, 0))
            window.blit(quit_text, (150, 400))

            bomb = pygame.image.load("img/bomb.png")
            window.blit(bomb, (car.x, car.y))

            pygame.display.flip()

            events = pygame.event.get()
            for event in events:
                if event.type == KEYDOWN and event.key == K_q:
                    pygame.quit()
                    sys.exit(0)

        if not is_over:
            if loop_count % 60 == 0:
                number_of_obstacles = random.randint(1,2)
                print(number_of_obstacles)
                obstacle = Obstacle(window)
                for i in range(number_of_obstacles):
                    obstacle = Obstacle(window)
                    obstacles.append(obstacle)
                score += 10

            obstacles = [obstacle for elem in obstacles if not elem.is_out()]
            print(obstacles)
            for obstacle in obstacles:
                obstacle.show()

            pygame.display.flip()

            car_rect = pygame.Rect(car.x, car.y, car.width, car.height)
            for obstacle in obstacles:
                obstacle_rect = pygame.Rect(obstacle.x, obstacle.y, obstacle.width, obstacle.height)
                collide = pygame.Rect.colliderect(car_rect, obstacle_rect)
                if collide:
                    sound.play()
                    is_over = True


            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        car.move_right()
                    if event.key == K_LEFT:
                        car.move_left()

            end = time.time()
            cost = end - start
            if cost < DEFAULT_DELAY:
                sleep = DEFAULT_DELAY - cost
            else:
                sleep = 0

            time.sleep(sleep)
            end = time.time()
            fps = 1.0 / (end - start)
            loop_count += 1