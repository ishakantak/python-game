import pygame
from pygame.locals import *
import pickle

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Soccer Game')

# define game variables
tile_size = 50
# for border
tile_sizes = 50
# game over condition
game_over = 0
# main_menu
main_menu = True

# load images
sun_img = pygame.image.load('sun.png')
bg_img = pygame.image.load('sky.jpg')
restart_img = pygame.image.load('restart_btn.png')
start_img = pygame.image.load('start_btn.png')
exit_img = pygame.image.load('exit_btn.png')

#
# def draw_grid():
#     for line in range(0, 12):
#         pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
#         pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        # action is what the mouse button does
        action = False

        # get mouse position

        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                # button is clicked, the action is true, the button is clicked
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        screen.blit(self.image, self.rect)

        return action


class Player():
    def __init__(self, x, y):
        self.reset(x, y)
        # code below not needed
        # self.images_right = []
        # self.images_left = []
        # self.index = 0
        # self.counter = 0
        # for num in range(1, 5):
        #     img_right = pygame.image.load(f'player{num}.png')
        #     img_right = pygame.transform.scale(img_right, (40, 80))
        #     img_left = pygame.transform.flip(img_right, True, False)
        #     self.images_right.append(img_right)
        #     self.images_left.append(img_left)
        # self.dead_image = pygame.image.load('ghost (1).png')
        # self.image = self.images_right[self.index]
        # self.rect = self.image.get_rect()
        # self.rect.x = x
        # self.rect.y = y
        # self.width = self.image.get_width()
        # self.height = self.image.get_height()
        # self.vel_y = 0
        # self.jumped = False
        # self.direction = 0

    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 5

        if game_over == 0:
            # get keypresses
            key = pygame.key.get_pressed()
            # self.in_air makes it sure you jump once
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # handle animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # check for collision
            self.in_air = True
            for tile in world.tile_list:
                # check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # check if above the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            # check for collision with enemies
            if pygame.sprite.spritecollide(self, fireball_group, False):
                # game_over = -1 is when the player dies
                game_over = -1
                print(game_over)

            # update player coordinates
            self.rect.x += dx
            self.rect.y += dy

            # if self.rect.bottom > screen_height:
            #     self.rect.bottom = screen_height
            #     dy = 0

        # if game_over
        elif game_over == -1:
            self.image = self.dead_image
            if self.rect.y > 200:
                self.rect.y -= 5

        # draw player onto screen
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        return game_over

    # reset method
    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.image.load(f'player{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load('ghost (1).png')
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        # jumping, player is currently jumping and seeing
        # if you are landing on something
        self.in_air = True


class World():
    def __init__(self, data):
        self.tile_list = []

        # load images
        dirt_img = pygame.image.load('dirt.png')
        grass_img = pygame.image.load('grass.png')
        cloud_img = pygame.image.load('Fluffy-white-cartoon-cloud-on-blue-sky-on-transparent-PNG.png')
        blue_img = pygame.image.load('blue.jpg')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    img = pygame.transform.scale(cloud_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 4:
                    fireball = Enemy(col_count * tile_size, row_count * tile_size + 15)
                    fireball_group.add(fireball)
                if tile == 5:
                    img = pygame.transform.scale(blue_img, (5, 50))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_sizes
                    img_rect.y = row_count * tile_sizes
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('download-removebg-preview-1.png.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # causes it to move
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            # >50 is how far the blob goes to move the other way
            self.move_direction *= -1
            self.move_counter *= -1


# not needed, need to use level.data to this main.py
world_data = [
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [5, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1],
    [5, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 0, 0, 0, 0, 1],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
    [5, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [5, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1],
    [5, 0, 0, 0, 0, 7, 2, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [5, 0, 0, 0, 2, 0, 4, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],

]

player = Player(80, screen_height - 130)

fireball_group = pygame.sprite.Group()

# load in level and data done with library pickle
# pickle_in = open("level1_data", 'rb')
# world_data = pickle.load(pickle_in)
world = World(world_data)

# create buttons
restart_button = Button(screen_width // 2, screen_height // 2, restart_img)
start_button = Button(screen_width // 2 - 450, screen_height // 2 - 50, start_img)
exit_button = Button(screen_width // 2 + 200, screen_height // 2 - 50, exit_img)

run = True
while run:

    clock.tick(fps)

    # screen.blit(bg_img, (0, 0))
    # screen.blit(sun_img, (100, 100))

    # main_menu: == main_menu == True
    if main_menu == True:
        screen.blit(bg_img, (0, 0))
        if exit_button.draw() == True:
            run = False
        if start_button.draw() == True:
            main_menu = False
    else:

        screen.blit(bg_img, (0, 0))
        screen.blit(sun_img, (100, 100))

        world.draw()

        if game_over == 0:
            fireball_group.update()

        fireball_group.draw(screen)

        game_over = player.update(game_over)

        # if player died
        if game_over == -1:
            if restart_button.draw():
                print('reset')
                player.reset(80, screen_height - 130)
                game_over = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()

# import pygame
# from pygame.locals import *
#
# pygame.init()
#
# clock = pygame.time.Clock()
# fps = 60
#
# screen_width = 600
# screen_height = 600
#
# screen = pygame.display.set_mode((screen_width, screen_height))
# pygame.display.set_caption('Soccer Game')
#
# # define game variables
# tile_size = 50
#
# # load images
# # image of sun
# sun_img = pygame.image.load('sun.png')
# # background image
# bg_img = pygame.image.load('sky.jpg')
#
#
# # create grid in game used to place game variables (optional)
# def draw_grid():
#     for line in range(0, 17):
#         pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
#         pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))
#
#
# class Player():
#     def __init__(self, x, y):
#         # creating the player
#
#         self.images_right = []
#         self.images_left = []
#         # position
#         self.index = 0
#         # speed of the player with counter
#         self.counter = 0
#         # change the player walking animation
#         for num in range(1, 5):
#             img_right = pygame.image.load(f'player{num}.png')
#             img_right = pygame.transform.scale(img_right, (40, 80))
#             img_left = pygame.transform.flip(img_right, True, False)
#             self.images_right.append(img_right)
#             self.images_left.append(img_left)
#         # player initial standing image
#         self.image = self.images_right[self.index]
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y
#         # player's width and height
#         self.width = self.image.get_width()
#         self.height = self.image.get_height()
#         self.vel_y = 0
#         # to stop jumping
#         self.jumped = False
#         # direction facing
#         self.direction = 0
#
#     def update(self):
#         dx = 0
#         dy = 0
#         # so the player does not move too fast
#         walk_cooldown = 5
#
#         # get keypresses
#         key = pygame.key.get_pressed()
#
#         # if space button jump
#         if key[pygame.K_SPACE] and self.jumped == False:
#             self.vel_y = -15
#             self.jumped = True
#         # fall down after jump
#         if not key[pygame.K_SPACE]:
#             self.jumped = False
#         # if left arrow move left
#         if key[pygame.K_LEFT]:
#             dx -= 5
#             self.counter += 1
#             self.direction = -1
#         # if right arrow move right
#         if key[pygame.K_RIGHT]:
#             dx += 5
#             self.counter += 1
#             self.direction = 1
#         if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
#             self.counter = 0
#             self.index = 0
#             if self.direction == 1:
#                 self.image = self.images_right[self.index]
#             if self.direction == -1:
#                 self.image = self.images_left[self.index]
#
#         # handle animation
#         if self.counter > walk_cooldown:
#             self.counter = 0
#             self.index += 1
#             if self.index >= len(self.images_right):
#                 self.index = 0
#             if self.direction == 1:
#                 self.image = self.images_right[self.index]
#             if self.direction == -1:
#                 self.image = self.images_left[self.index]
#
#         # add gravity to jump and player can go back down
#         self.vel_y += 1
#         if self.vel_y > 10:
#             self.vel_y = 10
#         dy += self.vel_y
#
#         # check for collision
#         for tile in world.tile_list:
#             # check for collision in x direction
#             if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
#                 dx = 0
#             # check for collision in y direction
#             if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
#                 # check if below the ground i.e. jumping
#                 if self.vel_y < 0:
#                     dy = tile[1].bottom - self.rect.top
#                     self.vel_y = 0
#                 # check if above the ground i.e. falling
#                 elif self.vel_y >= 0:
#                     dy = tile[1].top - self.rect.bottom
#                     self.vel_y = 0
#
#         # update player coordinates
#         self.rect.x += dx
#         self.rect.y += dy
#
#         # if the player is below screen height
#         if self.rect.bottom > screen_height:
#             self.rect.bottom = screen_height
#             dy = 0
#
#         # draw player onto screen
#         screen.blit(self.image, self.rect)
#         # draws rectangle arounf it
#         pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
#
#
# class World():
#     def __init__(self, data):
#         self.tile_list = []
#
#         # load images
#         dirt_img = pygame.image.load('dirt.png')
#         grass_img = pygame.image.load('grass.png')
#         cloud_img = pygame.image.load('Fluffy-white-cartoon-cloud-on-blue-sky-on-transparent-PNG.png')
#
#         row_count = 0
#         for row in data:
#             col_count = 0
#             for tile in row:
#                 if tile == 1:
#                     # border size is 50 by 50
#                     img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
#                     # create rectangle from img
#                     img_rect = img.get_rect()
#                     # img x coordinate increasing by tile size
#                     img_rect.x = col_count * tile_size
#                     # img y coordinate increasing by tile size
#                     img_rect.y = row_count * tile_size
#                     tile = (img, img_rect)
#                     # this will extract the useful stuff from the data list tile_list
#                     self.tile_list.append(tile)
#                 if tile == 2:
#                     img = pygame.transform.scale(grass_img, (tile_size, tile_size))
#                     img_rect = img.get_rect()
#                     img_rect.x = col_count * tile_size
#                     img_rect.y = row_count * tile_size
#                     tile = (img, img_rect)
#                     self.tile_list.append(tile)
#
#                 if tile == 3:
#                     img = pygame.transform.scale(cloud_img, (tile_size, tile_size))
#                     img_rect = img.get_rect()
#                     img_rect.x = col_count * tile_size
#                     img_rect.y = row_count * tile_size
#                     tile = (img, img_rect)
#                     self.tile_list.append(tile)
#
#                 if tile == 4:
#                     # enemy
#                     fireball = Enemy(col_count * tile_size, row_count * tile_size)
#                     # add fireball to group
#                     fireball_group.add(fireball)
#                 col_count += 1
#             row_count += 1
#
#     def draw(self):
#         for tile in self.tile_list:
#             screen.blit(tile[0], tile[1])
#             # pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)
#
#
# # new class for enemy
# class Enemy(pygame.sprite.Sprite):
#     # enemy is the child of the Sprit class
#     def __init__(self, x, y):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = pygame.image.load('blob.png')
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y
#         self.move_direction = 1
#         self.move_counter = 0
#
#     def update(self):
#         self.rect.x += self.move_direction
#         self.move_counter += 1
#         if abs(self.move_counter) > 50:
#             self.move_direction *= -1
#             self.move_counter *= -1
#
#
# world_data = [
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # border
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # border
#     [1, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 1],
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1],
#     [1, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 1],
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#     [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1],
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#     [1, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 1],
#     [1, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 1],
#     [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#
# ]
#
# player = Player(100, screen_height - 130)
#
# # enemy group (fireball)
# fireball_group = pygame.sprite.Group()
#
# world = World(world_data)
#
# run = True
# while run:
#
#     clock.tick(fps)
#
#     screen.blit(bg_img, (0, 0))
#     screen.blit(sun_img, (100, 100))
#
#     world.draw()
#
#     fireball_group.update()
#     fireball_group.draw(screen)
#
#     # add player onto screen
#     player.update()
#
#     # draw the grid on the screen
#     draw_grid()
#
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False
#
#     pygame.display.update()
#
# pygame.quit()
