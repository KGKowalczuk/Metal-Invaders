import pygame
from sys import exit
from random import randint
import random
import numpy as np

WIDTH = 800
HEIGHT = 1000
FPS = 60

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale2x(pygame.image.load('assets/player/Layer1.png').convert_alpha())
        self.rect = self.image.get_rect(midbottom = (400, 900))
        self.max_health = 100
        self.health = 100
        self.max_heat = 100
        self.heat = 1
        self.player_shadow = pygame.sprite.GroupSingle()
        self.player_shadow.add(Player_shadow())
        self.bullets = pygame.sprite.Group()
        self.overheat = False
        self.cooldown = 0
        self.rocket_cooldown = 0
        self.rockets = 3

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.top >= 0:
            self.rect.y -= 5
        if keys[pygame.K_s] and self.rect.bottom <= HEIGHT:
            self.rect.y += 5
        if keys[pygame.K_a] and self.rect.left >= 0:
            self.rect.x -= 8
        if keys[pygame.K_d] and self.rect.right <= WIDTH:
            self.rect.x += 8
        if keys[pygame.K_SPACE] and not self.overheat and self.cooldown <=0:
            #self.shoot()
            shoot2(self.rect.center)
            self.cooldown = 8
            self.heat += 15
        if keys[pygame.K_e] and self.rocket_cooldown <=0 and self.rockets > 0:
            self.rockets -= 1
            shoot_rocket(self.rect.center, get_target_x(enemy_group))
            self.rocket_cooldown = 20

    def remove_health(self, health):
        self.health -= health
        if self.health > self.max_health: self.health = self.max_health

    def add_rockets(self,rockets):
        if self.rockets < 24: self.rockets += rockets

    def shoot(self):
        x,y = self.rect.center
        self.bullets.add(Bullet(x, y + 50))
        self.cooldown = 8
        self.heat += 15

    def healthbar(self):
        pygame.draw.rect(screen, (108,19,37), (self.rect.x, self.rect.y + self.image.get_height() + 10, self.image.get_width(), 10))
        pygame.draw.rect(screen, (0,183,0), (self.rect.x, self.rect.y + self.image.get_height() + 10, self.image.get_width() * (self.health/self.max_health), 10))

    def overheatbar(self):
        pygame.draw.rect(screen, (108,19,37), (self.rect.x, self.rect.y + self.image.get_height() + 20, self.image.get_width(), 10))
        pygame.draw.rect(screen, (251,205,38), (self.rect.x, self.rect.y + self.image.get_height() + 20, self.image.get_width() * (1 - (self.heat/self.max_heat)), 10))


    def number_of_rockets(self):
        return self.rockets

    def update(self):
        self.player_input()
        self.player_shadow.draw(screen)
        self.player_shadow.update(self.rect.x,self.rect.y)
        if self.cooldown > 0 : self.cooldown -= 1
        if self.rocket_cooldown > 0 : self.rocket_cooldown -= 1
        #self.bullets.draw(screen)
        #self.bullets.update()
        if self.heat >= 0: self.heat -= 1
        if self.heat >= 100: self.overheat = True
        if self.overheat and self.heat <= 0: self.overheat = False 
        self.healthbar()
        self.overheatbar()
        #self.collision()
    
    def get_health(self):
        return self.health

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale2x(pygame.image.load('assets/player/Layer3.png').convert_alpha())
        self.rect = self.image.get_rect(midbottom = (x,y))

    def move(self):
        self.rect.y -= 10

    def update(self):
        self.move()
        if self.rect.y <= 0: self.kill()

class Rocket(pygame.sprite.Sprite):
    def __init__(self,x,y,targetx):
        super().__init__()
        self.target_x = targetx
        self.image = pygame.transform.scale2x(pygame.image.load('assets/player/Layer11.png').convert_alpha())
        self.rect = self.image.get_rect(midbottom = (x,y))

        self.shadow = pygame.sprite.GroupSingle()
        self.shadow.add(Player_shadow())
    
    def move(self):
        self.rect.y -= 4
        if self.rect.x > self.target_x + 5: self.rect.x -= 4
        if self.rect.x < self.target_x - 5: self.rect.x += 4

    def update(self, targetx):
        self.move()
        self.shadow.update(self.rect.x,self.rect.y+5)
        self.shadow.draw(screen)
        self.target_x = targetx
        if self.rect.y <= 0: self.kill()

class Enemy_Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale2x(pygame.image.load('assets/player/Layer10.png').convert_alpha())
        self.rect = self.image.get_rect(midbottom = (x,y))

    def move(self):
        self.rect.y += 7

    def update(self):
        self.move()
        if self.rect.y >= HEIGHT: self.kill()

class Player_shadow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frame_1 = pygame.transform.scale2x(pygame.image.load('assets/player/Layer6.png').convert_alpha())
        self.frame_2 = pygame.transform.scale2x(pygame.image.load('assets/player/Layer7.png').convert_alpha())
        self.frame_3 = pygame.transform.scale2x(pygame.image.load('assets/player/Layer8.png').convert_alpha())
        self.frame_4 = pygame.transform.scale2x(pygame.image.load('assets/player/Layer9.png').convert_alpha())
        self.frames = [self.frame_1, self.frame_2, self.frame_3, self.frame_4]
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midtop = (400, 900))

    def animate(self):
        self.animation_index += 0.1 
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self, x, y):
        self.animate()
        self.position(x, y) 

class Rocket_shadow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frame_1 = pygame.image.load('assets/player/Layer6.png').convert_alpha()
        self.frame_2 = pygame.image.load('assets/player/Layer7.png').convert_alpha()
        self.frame_3 = pygame.image.load('assets/player/Layer8.png').convert_alpha()
        self.frame_4 = pygame.image.load('assets/player/Layer9.png').convert_alpha()
        self.frames = [self.frame_1, self.frame_2, self.frame_3, self.frame_4]
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midtop = (400, 900))

    def animate(self):
        self.animation_index += 0.1 
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self, x, y):
        self.animate()
        self.position(x, y) 

class Enemy(pygame.sprite.Sprite):
    def __init__(self,type,x,y):
        super().__init__()
        if type == 'fighter': 
            self.image = pygame.transform.scale2x(pygame.image.load(f'assets/enemy1/Layer1.png').convert_alpha())
            self.speed = 2
            self.shadow = 1
            self.max_health = 5
            self.health = self.max_health
        if type == 'bomber': 
            self.image = pygame.transform.scale2x(pygame.image.load(f'assets/enemy2/Layer1.png').convert_alpha())
            self.speed = 1
            self.shadow = 2
            self.max_health = 10
            self.health = self.max_health
        if type == 'speed': 
            self.image = pygame.transform.scale2x(pygame.image.load(f'assets/enemy1/Layer2.png').convert_alpha())
            self.speed = 4
            self.shadow = 1
            self.max_health = 3
            self.health = self.max_health
        self.type = type
        self.rect = self.image.get_rect(midbottom = (x, y))
        self.rect.x = x
        self.rect.y = y

        self.enemy_shadow = pygame.sprite.GroupSingle()
        self.enemy_shadow.add(Enemy_shadow(self.shadow,x,y))

    
    def move(self):
        self.rect.y += self.speed

    def healthbar(self):
        pygame.draw.rect(screen, (108,19,37), (self.rect.x + self.image.get_width()/4, self.rect.y , 0.5 * self.image.get_width(), 5))
        pygame.draw.rect(screen, (0,183,0), (self.rect.x + self.image.get_width()/4, self.rect.y , 0.5 * self.image.get_width() * (self.health/self.max_health), 5))


    def update(self, playerx):
        global lives
        self.move()
        self.healthbar()
        self.enemy_shadow.draw(screen)
        self.enemy_shadow.update(self.rect.x,self.rect.y)
        self.check_health()
        if self.rect.y >= HEIGHT: 
            self.kill()
            lives -= 1

        if self.type == 'fighter':
            if self.rect.y >= 0:
                if randint(0, FPS*1.5) == 1:
                    shoot3(self.rect.center)

        if self.type == 'bomber':
            if self.rect.y >= 0:
                if randint(0, FPS*3) == 1:
                    shoot4(self.rect.center)

        if self.type == 'speed':
            if self.rect.y > HEIGHT/3:
                self.speed = 6
                if self.rect.x > playerx - 5: self.rect.x -= 3
                elif self.rect.x < playerx + 5: self.rect.x += 3
    
    def explode(self):
        self.speed = 0
        self.exploded = True
        self.explosion_frame = 0

    def remove_health(self, health):
        self.health -= health

    def check_health(self):
        if self.health <= 0: 
            self.kill()
            spawn_explosion(self.rect.center)
            if self.type == 'bomber' and randint(0,1)==1: spawn_rocket_perk(self.rect.center)

    def get_y(self):
        return self.rect.y

class Perk(pygame.sprite.Sprite):
    def __init__(self,type,x,y):
        super().__init__()
        if type == 'health': 
            self.image = pygame.transform.scale_by(pygame.image.load(f'assets/player/Layer12.png').convert_alpha(), 4)
        if type == 'rocket': 
            self.image = pygame.transform.scale_by(pygame.image.load(f'assets/player/Layer13.png').convert_alpha(), 4)
        self.speed = 2
        self.type = type
        self.rect = self.image.get_rect(midbottom = (x, y))
        self.rect.x = x
        self.rect.y = y
    
    def move(self):
        self.rect.y += self.speed

    def update(self):
        self.move()
        if self.rect.y >= HEIGHT: 
            self.kill()
        
class Enemy_shadow(pygame.sprite.Sprite):
    def __init__(self,type,x,y):# type = 1 or type = 2
        super().__init__()
        self.frame_1 = pygame.transform.scale2x(pygame.image.load(f'assets/enemy{type}/Layer3.png').convert_alpha())
        self.frame_2 = pygame.transform.scale2x(pygame.image.load(f'assets/enemy{type}/Layer4.png').convert_alpha())
        self.frame_3 = pygame.transform.scale2x(pygame.image.load(f'assets/enemy{type}/Layer5.png').convert_alpha())
        self.frames = [self.frame_1, self.frame_2, self.frame_3]
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midtop = (x, y))

    def animate(self):
        self.animation_index += 0.1 
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self, x, y):
        self.animate()
        self.position(x, y)

class Explosion(pygame.sprite.Sprite):
    def __init__(self,type,x,y,scalefactor):
        super().__init__()
        if type == 'fighter': 
            self.image = pygame.transform.scale2x(pygame.image.load(f'assets/enemy1/Layer1.png').convert_alpha())
            self.speed = 3
            self.shadow = 1
        if type == 'bomber': 
            self.image = pygame.transform.scale2x(pygame.image.load(f'assets/enemy2/Layer1.png').convert_alpha())
            self.speed = 1
            self.shadow = 2
        if type == 'speed': 
            self.image = pygame.transform.scale2x(pygame.image.load(f'assets/enemy1/Layer2.png').convert_alpha())
            self.speed = 5
            self.shadow = 1
        self.frame_1 = pygame.transform.scale2x(pygame.image.load(f'assets/enemy2/Layer6.png').convert_alpha())
        self.frame_2 = pygame.transform.scale2x(pygame.image.load(f'assets/enemy2/Layer7.png').convert_alpha())
        self.frame_3 = pygame.transform.scale2x(pygame.image.load(f'assets/enemy2/Layer8.png').convert_alpha())
        self.frame_4 = pygame.transform.scale2x(pygame.image.load(f'assets/enemy2/Layer9.png').convert_alpha())
        self.frame_5 = pygame.transform.scale2x(pygame.image.load(f'assets/enemy2/Layer10.png').convert_alpha())
        self.frame_6 = pygame.transform.scale2x(pygame.image.load(f'assets/enemy2/Layer11.png').convert_alpha())
        self.frame_7 = pygame.transform.scale2x(pygame.image.load(f'assets/enemy2/Layer12.png').convert_alpha())
        if scalefactor == 4:
            self.frame_1 = pygame.transform.scale2x(self.frame_1)
            self.frame_2 = pygame.transform.scale2x(self.frame_2)
            self.frame_3 = pygame.transform.scale2x(self.frame_3)
            self.frame_4 = pygame.transform.scale2x(self.frame_4)
            self.frame_5 = pygame.transform.scale2x(self.frame_5)
            self.frame_6 = pygame.transform.scale2x(self.frame_6)
            self.frame_7 = pygame.transform.scale2x(self.frame_7)
        self.frames = [self.frame_1, self.frame_2, self.frame_3, self.frame_4, self.frame_5, self.frame_6, self.frame_7]
        self.animation_index = 0
        #self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(center = (x, y))

    def animate(self):
        self.animation_index += 0.2 
        if self.animation_index >= len(self.frames): self.kill()
        else: self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animate()

def shoot2(xy):
    x, y = xy
    bullets.add(Bullet(x, y + 50))

def shoot_rocket(xy, target):
    x,y = xy
    rockets.add(Rocket(x, y +50, target))

def shoot3(xy):
    x, y = xy
    enemy_bullets.add(Enemy_Bullet(x, y + 50))

def shoot4(xy):
    x, y = xy
    enemy_bullets.add(Enemy_Bullet(x, y + 50))

def background_update():
    global background_1,background_2,background_1_y,background_2_y,ui
    def increment(y):
        if y >= -2200 and y <= 1000:
            y += 2
        if y > 1001:
            y = -2200
        return y
    def draw1(background, y):
        if y >= -1600 and y <= 1000:
            screen.blit(background, (0,y))
    draw1(background_1, background_1_y)
    draw1(background_2, background_2_y)
    background_1_y = increment(background_1_y)
    background_2_y = increment(background_2_y)
    
def get_target_x(enemy_group):
    j = 0
    x = 800/2
    for enemy in enemy_group.sprites():
        if enemy.rect.y > j : 
            x = enemy.rect.x
    return x
   
def check_collisions():
    global lives
    for enemy_bullet in enemy_bullets.sprites():
        p = pygame.sprite.spritecollide(enemy_bullet, player, False, pygame.sprite.collide_mask)
        if p:
            p[0].remove_health(10)
            enemy_bullet.kill()

    for perk in perks.sprites():
        p = pygame.sprite.spritecollide(perk, player, False, pygame.sprite.collide_mask)
        if p:
            if perk.type == 'health': 
                p[0].remove_health(-30) 
                if lives < 16:lives += 1
            elif perk.type == 'rocket': p[0].add_rockets(3)
            perk.kill()

    for enemy in enemy_group.sprites():
        p = pygame.sprite.spritecollide(enemy, player, False, pygame.sprite.collide_mask)
        if p:
            p[0].remove_health(20)
            enemy.remove_health(10000)

    for bullet in bullets.sprites():
        enemy_list = pygame.sprite.spritecollide(bullet, enemy_group, False, pygame.sprite.collide_mask)
        if enemy_list:
            bullet.kill()
            enemy_list[0].remove_health(1)
    
    for rocket in rockets.sprites():
        enemy_list = pygame.sprite.spritecollide(rocket, enemy_group, False, pygame.sprite.collide_mask)
        if enemy_list:
            spawn_big_explosion(rocket.rect.midtop)
            rocket_explosion(rocket.rect.midtop)
            rocket.kill()

def rocket_explosion(xy):
    x, y = xy
    for enemy in enemy_group:
        if np.sqrt((enemy.rect.x - x)**2 + (enemy.rect.y - y)**2) < 200:
            enemy.remove_health(10)
            
def spawn_explosion(xy):
    x, y = xy
    explosions.add(Explosion('fighter',x,y,2)) 

def spawn_rocket_perk(xy):
    x, y = xy
    perks.add(Perk('rocket',x - 120,y - 100))
    #perks.add(Perk('rocket', 400,-400))

def spawn_big_explosion(xy):
    x, y = xy
    explosions.add(Explosion('fighter',x-50,y,4)) 

def spawn_wave():
    global wave_is_active
    wave_is_active = True
    wave_size = 5 + current_wave
    choice_list = [1,1,2,2,2,3,3,3,3,4,4]
    for i in range(wave_size):
        choice = random.choice(choice_list)
        if choice == 1: enemy_group.add(Enemy('bomber',randint(0, WIDTH - 100), randint(int(-400*(1+current_wave/5)),-200)))
        elif choice == 2: enemy_group.add(Enemy('speed',randint(0, WIDTH - 100), randint(int(-400*(1+current_wave/5)),-200)))
        elif choice == 3: enemy_group.add(Enemy('fighter',randint(0, WIDTH - 100), randint(int(-400*(1+current_wave/5)),-200)))
        elif choice == 4: 
            perks.add(Perk('health',randint(0, WIDTH - 150), randint(int(-400*(1+current_wave/5)),-200)))
            choice_list = [1,1,2,2,2,3,3,3,3]
        
def ui():
    global score
    rockets =  player.sprites()[0].number_of_rockets()
    heart_image = pygame.transform.scale_by(pygame.image.load(f'assets/player/Layer12.png').convert_alpha(), 2)
    rocket_image = pygame.transform.scale_by(pygame.image.load(f'assets/player/Layer13.png').convert_alpha(), 2)
    j = 0
    k = 0
    a = 0 
    b = 0
    c = 0
    d = 0
    for i in range(lives):
        j += 1
        a += 1
        screen.blit(heart_image, (-60 + a*40,HEIGHT - 70*(1 + c*0.5)))
        if j >= 8: 
            a=0
            j=0
            c+=1
    for i in range(rockets):
        k += 1
        b += 1
        screen.blit(rocket_image, (WIDTH -60 - b*40,HEIGHT - 70*(1 + d*0.5)))
        if k >= 8: 
            b=0
            k=0
            d+=1
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = font.render(f'Score: {current_time}',False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    wave_surf = font.render(f'Wave: {current_wave}',False,(64,64,64))
    wave_rect = score_surf.get_rect(center = (410,100))
    screen.blit(score_surf,score_rect)
    screen.blit(wave_surf, wave_rect)
    score = current_time

pygame.init()
font = pygame.font.Font('font/Pixeltype.ttf', 50)
big_font = pygame.font.Font('font/Pixeltype.ttf', 100)
game_active = False
start_time = 0
score = 0
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Metal Invaders')

background_1 = pygame.transform.scale(pygame.image.load('assets/background/Layer3.png').convert(),(WIDTH,WIDTH*2))
background_2 = pygame.transform.scale(pygame.image.load('assets/background/Layer4.png').convert(),(WIDTH,WIDTH*2))
background_y_down = -600
background_y_up = -2200
background_1_y = background_y_down
background_2_y = background_y_up

player = pygame.sprite.GroupSingle()
lives = 1
player_object = Player()
player.add(player_object)
enemy_group = pygame.sprite.Group()
bullets = pygame.sprite.Group()
rockets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
perks = pygame.sprite.Group()
explosions = pygame.sprite.Group()

current_wave = 0
wave_is_active = False

spawn_wave()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
   
    if game_active:
        background_update()
        check_collisions()
        player.draw(screen)
        player.update()

        enemy_group.draw(screen)
        enemy_group.update(player.sprites()[0].rect.x)
        if len(enemy_group) == 0:
            current_wave += 1
            wave_is_active = False
        if not wave_is_active: spawn_wave()

        bullets.draw(screen)
        bullets.update()

        enemy_bullets.draw(screen)
        enemy_bullets.update()

        explosions.draw(screen)
        explosions.update()

        rockets.draw(screen)
        rockets.update(get_target_x(enemy_group))

        perks.draw(screen)
        perks.update()

        if lives <= 0 or player.sprites()[0].get_health() <= 0: game_active = False

        get_target_x(enemy_group)
        ui()
    else:
        if score == 0:
            screen.fill((14,10,15))
            message = big_font.render('METAL INVADERS', False, (108,19,37))
            message_rect = message.get_rect(center = (400,220))
            score_message = font.render('Press space to start',False,(64,64,64))
            instructions = font.render('w,a,s,d to move',False,(64,64,64))
            instructions2 = font.render('space to shoot',False,(64,64,64))
            instructions3 = font.render('e to launch rocket',False,(64,64,64))
            score_message_rect = score_message.get_rect(center = (400,330))
            instructions_rect = instructions.get_rect(center = (400, 430))
            instructions_rect2 = instructions.get_rect(center = (395, 480))
            instructions_rect3 = instructions.get_rect(center = (375, 530))
            screen.blit(message,message_rect)
            screen.blit(score_message,score_message_rect)
            screen.blit(instructions, instructions_rect)
            screen.blit(instructions2, instructions_rect2)
            screen.blit(instructions3, instructions_rect3)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 1000)
                    current_wave = 0
                    lives = 5
                    enemy_group.empty()
        else:
            screen.fill((14,10,15))
            message = big_font.render('YOU DIED!', False, (108,19,37))
            message_rect = message.get_rect(center = (400,220))
            score_message = font.render(f'Your score: {score}',False,(64,64,64))
            score_message_rect = score_message.get_rect(center = (400,330))
            screen.blit(score_message,score_message_rect)
            screen.blit(message,message_rect)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 1000)
                    current_wave = 0
                    player.empty()
                    lives = 5
                    enemy_group.empty()
                    perks.empty()
                    bullets.empty()
                    rockets.empty()
                    enemy_bullets.empty()
                    explosions.empty()
                    player_object = Player()
                    player.add(player_object)

    pygame.display.update()
    clock.tick(FPS)
