import pygame
from pygame.locals import *
import os
import random

pygame.init()

WIDTH, HEIGHT = 1200, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
vec = pygame.math.Vector2
FPS = 60
VEL = 10


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cow Tipping")

class Background(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.bgimage = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'map.png')), (WIDTH, HEIGHT))
		self.bgY = 0
		self.bgX = 0

	def render(self):
		WIN.blit(self.bgimage, (self.bgX, self.bgY))

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'cowboy_idle.png')), (80, 120))
		self.rect = self.image.get_rect()

		self.pos = vec((600, 400))
		self.vel = vec
		self.walking = False
		self.direction = 'RIGHT'
		self.pushing = False

		self.push_frame = 0

	def move(self):

		keys_pressed = pygame.key.get_pressed()
		
		
		if keys_pressed[pygame.K_a] and self.pos.x - VEL > 40: # LEFT
			self.pos.x -= VEL
			
		if keys_pressed[pygame.K_d] and self.pos.x + VEL  < WIDTH - 40: # RIGHT
			self.pos.x += VEL
			
		if keys_pressed[pygame.K_w] and self.pos.y - VEL > 0 + 120: # UP
			self.pos.y -= VEL
			
		if keys_pressed[pygame.K_s] and self.pos.y + VEL < HEIGHT: # DOWN
			self.pos.y += VEL
			
		
		self.rect.midbottom = self.pos
		

	def push(self):
		if self.push_frame > 10:
			self.push_frame = 0
			self.pushing = False

		self.push_frame += 1
		




class Cow(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image =  pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'bull_idle.png')), (80, 120))
		self.image_tipped =  pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'bull_tipped.png')), (80, 120))
		self.rect = self.image.get_rect()
		self.rect = self.image_tipped.get_rect()
		self.pos = vec(0, 0)
		self.vel = 1
		self.tipped = False
		self.direction = random.randint(0,1) # 0 for Right, 1 for Left
		self.pos.x = random.randint(50, WIDTH - 50)
		self.pos.y = random.randint(50, HEIGHT - 50)
		self.moveTo = vec(random.randint(150, WIDTH - 150), random.randint(150, HEIGHT - 150))
		

	def update(self, Playergroup, player):
		hits = pygame.sprite.spritecollide(self, Playergroup, False)

		if hits and player.pushing == True:
			print("Pushing cow")
			self.tipped = True
		if hits:
			print('hit')

	def move(self):
		if self.pos.x >= (WIDTH-40):
			self.direction = 1
		elif self.pos.x <= 40:
			self.direction = 0
		if self.pos.y >= (HEIGHT-40):
			self.direction = 1
		elif self.pos.y <= 40:
			self.direction = 0

		if self.pos.y < self.moveTo.y - self.vel:
			self.pos.y += self.vel

		elif self.pos.y > self.moveTo.y + self.vel:
			self.pos.y -= self.vel

		if self.pos.x < self.moveTo.x - self.vel:
			self.pos.x += self.vel

		elif self.pos.x > self.moveTo.x + self.vel:
			self.pos.x -= self.vel

		if self.pos.y < self.moveTo.y + self.vel and self.pos.y > self.moveTo.y - self.vel and self.pos.x < self.moveTo.x + self.vel and self.pos.x > self.moveTo.x - self.vel:
			self.moveTo = vec(random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100))


		self.rect.center = self.pos	


	def render(self):
		if self.tipped:
			WIN.blit(self.image_tipped, (self.pos.x, self.pos.y))
		else:
			WIN.blit(self.image, (self.pos.x, self.pos.y))

class EventHandler():
	def __init__(self):
		self.cow_count = 0
		self.push = False
		self.cow_generation = pygame.USEREVENT + 1
		self.stage = 1

		self.stage_cows =[]
		for x in range(1, 21):
			if(x < 10):
				self.stage_cows.append(int(x))
				print(x)
			else:
				self.stage_cows.append(int(10))

	def stage_handler(self):
		pass
	
	def next_stage(self):
		self.stage += 1
		self.cow_count = 0
		print("Stage: " + str(self.stage))
		pygame.time.set_timer(self.cow_generation, 1)


def main():

	Cows = pygame.sprite.Group()
	handler = EventHandler()

	player = Player()
	Playergroup = pygame.sprite.Group()
	Playergroup.add(player)


	background = Background()
	cowsNum = 3
	
	clock = pygame.time.Clock()
	run = True
	while run:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_n:
					if handler.battle == True and len(Cows) == 0:
						handler.next_stage() 

				if event.key == pygame.K_SPACE:
					handler.next_stage()

				if event.key == pygame.K_k:
					if player.pushing == False:
						player.push()
						player.pushing = True

			if event.type == handler.cow_generation:
				if handler.cow_count < handler.stage_cows[handler.stage - 1]:
					cow = Cow()
					Cows.add(cow)
					handler.cow_count += 1 
					
					

		if player.pushing == True:
			player.push()
		player.move()
		background.render()
		WIN.blit(player.image, player.rect)
		for entity in Cows:
			entity.update(Playergroup, player)
			entity.move()
			entity.render()
		pygame.display.update()

	main()

if __name__ == "__main__":
	main()