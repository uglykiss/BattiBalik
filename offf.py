import pygame
pygame.init()
import random

screen_width = 800
screen_height = 600

#font
font = pygame.font.SysFont('Verneer', 60)
white = (213, 78, 33)
text_col = white

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battı Balık')

uw = pygame.image.load("assets/uw.png").convert()
uw = pygame.transform.scale(uw, (screen_width, screen_height))
button_img = pygame.image.load("assets/yeni-Photoroom.png")
start_screen_img = pygame.image.load("assets/yeter.png")
start_screen_img = pygame.transform.scale(start_screen_img, (screen_width, screen_height))


def draw_text(text, font, white, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def reset_game():
    global scroll_speed, game_over, flying, pass_pipe
    pipe_group.empty()
    batti.rect.x = 100
    batti.rect.y = int(screen_height / 2)
    batti.vel = 0  # Kuşun hızını sıfırla
    batti.image = pygame.transform.rotate(batti.images[batti.index], 0)
    scroll_speed = 2  # kaydırma
    game_over = False
    flying = False
    pass_pipe = False
    score = 0
    return score

#BENDEN GÜNCELLEMELER
scroll_speed = 2
speed_multiplier = 2
max_speed_multiplier = 5
speed_increase_interval = 5
pipe_frequency_min = 3000
pipe_frequency_max = 8000
pipe_gap_min = 110
pipe_gap_max = 200
pipe_gap = random.randint(pipe_gap_min, pipe_gap_max)
pipe_frequency = random.randint(pipe_frequency_min, pipe_frequency_max)



# Arka plan
bg_x1 = 0
bg_x2 = screen_width

# Kaydırma hızı
scroll_speed = 2
flying = False
game_over = False
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.image = pygame.transform.scale(self.image, (300, 300))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True


        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/weedgreen.png')
        self.image = pygame.transform.scale(self.image, (110,400))
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

# Bird sınıfı
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 3):  # kaplus1, kaplus2
            img = pygame.image.load(f'assets/kaplus{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (70, 70))  # Görüntüboyut
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False
        self.mask = pygame.mask.from_surface(self.image) #çarpışma maskesi

    def update(self):
        global flying, game_over, last_pipe  # erişim için 

        if flying and not game_over:
            # Gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < screen_height:
                self.rect.y += int(self.vel)

            # Jump
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.vel = -8
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            # Animasyonun hızını kontrol et
            self.counter += 1
            flap_cooldown = 25  # 5 framede bir animasyon değişecek
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0 

            self.image = self.images[self.index] 

            # Rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -1)

        elif game_over:
            if self.rect.bottom < screen_height:
                self.vel +=0.5
                self.rect.y += int(self.vel)
            else:
                self.vel -= 0
            self.image = pygame.transform.rotate(self.images[self.index], -90)  # Oyun bittiğinde aşağı bak!!!!!!!!!!!




        import random  # Rastgele boru

        if not game_over and flying:
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > pipe_frequency:
                pipe_height = random.randint(-100,100)
                random_pipe_y = screen_height / 2 + random.randint(-100, 100)
                btm_pipe = Pipe(screen_width, random_pipe_y, -1)
                top_pipe = Pipe(screen_width, random_pipe_y, 1)
                pipe_group.add(btm_pipe)
                pipe_group.add(top_pipe)
                last_pipe = time_now


# Bird grubunu oluştur
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
batti = Bird(100, int(screen_height / 2))
bird_group.add(batti)

button = Button(screen_width // 2 - 170, screen_height // 2 - 170, button_img)

# Ana döngü
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
            flying = True


    # Arka planı hareket
    if not game_over:
        bg_x1 -= scroll_speed
        bg_x2 -= scroll_speed

    if bg_x1 <= -screen_width:
        bg_x1 = screen_width
    if bg_x2 <= -screen_width:
        bg_x2 = screen_width

    screen.blit(uw, (bg_x1, 0))
    screen.blit(uw, (bg_x2, 0))

    # güncelle ve ekrana çiz
    bird_group.update()
    bird_group.draw(screen)


    if not game_over:
        pipe_group.update()
        pipe_group.draw(screen)

    # check the score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    draw_text(str(score), font, white, int(730), 30)



    if pygame.sprite.spritecollide(batti, pipe_group, False, pygame.sprite.collide_mask):
        game_over = True

    # Eğer kuş yere çarptıysa
    if batti.rect.bottom >= screen_height:
        game_over = True
        flying = False
        scroll_speed = 0

    if game_over == True:
        if button.draw() == True:
            game_over = False
            score = reset_game()
    # Ekranı güncelle
    pygame.display.update()

    # FPS kontrolü
    pygame.time.Clock().tick(60)

pygame.quit()
