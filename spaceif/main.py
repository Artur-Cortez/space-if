import pygame, random, spritesheet, sys
from pygame import mixer
from button import Botao
from pygame.locals import *
import time #
pygame.init()

#inicializacao do módulo de som
pygame.mixer.pre_init(44100, -16, 2, 512)

#definir fontes e score, por preguiça está aqui
valorscore = 0
valorscoreX = 5
valorscoreY = 5

#funcao para o main menu
def get_font(size):
    return pygame.font.Font("assets/font/font.ttf", size)

#background da fase msm, por enquanto aqui
background = pygame.image.load('assets/img/espacolindo.png')

#a ajeitar essa largura e altura da tela
LARGURA = background.get_width()
ALTURA = background.get_height()

pygame.display.set_caption('Spaceif')

def desenhar_texto(texto, font, text_color, x, y, tela):
    img = font.render(texto, True, text_color)
    rect = img.get_rect(center=(x,y))
    tela.blit(img, rect)

def main_menu():
  #background do menu
  bg = pygame.image.load('assets/img/menu.png')

  screen = pygame.display.set_mode((600, 600), RESIZABLE)

  bp = pygame.font.Font('assets/font/BPimperialItalic.otf', 170)

  relogio = pygame.time.Clock()

  musica_menu = pygame.mixer.Sound('assets/sound/musica_menu.mp3')
  musica_menu.set_volume(0.25)
  musica_menu.play(loops= -1)

  click = pygame.mixer.Sound('assets/sound/click.wav')
  click.set_volume(0.5)

  zoom = pygame.mixer.Sound('assets/sound/zoom.wav')
  zoom.set_volume(0.25)
  
  global musica
  musica = pygame.mixer.Sound('assets/sound/musicafases.wav')
  musica.set_volume(0.1)

  def desenhar_fundo():
    screen.fill((0, 0, 0))
    global bg_rect
    bg_rect = bg.get_rect(center=(screen.get_width()/2, screen.get_height()/2))
    screen.blit(bg, bg_rect)
    

  while True:
    relogio.tick(60)
    desenhar_fundo()
    MENU_MOUSE_POS = pygame.mouse.get_pos()

    # spaceif = bp.render('SPACEIF', True, '#5e17fb')
    # spaceif_rect = spaceif.get_rect(center=(screen.get_width()/2, screen.get_height()/5))
    # screen.blit(spaceif, spaceif_rect)

    PLAY_BUTTON = Botao(bg_rect.centerx, bg_rect.centery, "PLAY", get_font(50), "White", "#8c52ff", image=None)
    OPTIONS_BUTTON = Botao(bg_rect.centerx, bg_rect.centery + 100, "OPTIONS", get_font(50), "White", "#8c52ff", image=None)
    QUIT_BUTTON = Botao(bg_rect.centerx, bg_rect.centery + 200, "QUIT", get_font(50), "White", "#8c52ff", image=None)

    for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
      button.changeColor(MENU_MOUSE_POS, screen)
      button.update(screen)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          pygame.quit()
      if event.type == VIDEORESIZE:
        screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
      if event.type == pygame.MOUSEBUTTONDOWN:
        if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
            musica_menu.stop()
            click.play()
            time.sleep(0.5)
            play()
        if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):           
            click.play()
            options()
        if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
            click.play()
            time.sleep(0.5)
            pygame.quit()

    pygame.display.update()
    pygame.display.flip()
  
def play():
  screen = pygame.display.set_mode((600, 600), pygame.RESIZABLE)

  screen.fill("black")

  #cores
  VERMELHO = (255, 0, 0)
  VERDE = (0, 255, 0)
  BRANCO = (255, 255, 255)

  #configs para a quantia de pyhtonaliens
  linha = 4
  coluna = 5

  level = 1
  ultimo_tiro_alien = pygame.time.get_ticks()
  alien_cooldown = 1000
  countdown = 3
  ultima_contagem = pygame.time.get_ticks()
  global game_over
  game_over = 0 #0 é game over, 1 o player ganhou, -1 o player perdeu

  #o quanto de x que os aliens descem a cada movimentação
  aliens_desce = 10

  relogio = pygame.time.Clock()

  font = pygame.font.Font('freesansbold.ttf', 20)

  #carregar sons
  # woom = pygame.mixer.Sound('assets/sound/sweep.wav')
  # woom.set_volume(0.25)
  # global canal_explo
  # canal_explo = pygame.mixer.Channel(1)
  som_explosao = pygame.mixer.Sound('assets/sound/explosion.wav')
  som_explosao.set_volume(0.2)

  laser = pygame.mixer.Sound('assets/sound/laser.wav')
  laser.set_volume(0.2)  
  
  def desenhar_fundo():
    screen.blit(background, (0, 0))

  #definir criar texto
  def mostrarscore(x, y):
    score = font.render("Score: " + str(valorscore),
                          True, (BRANCO))
    screen.blit(score, (x , y ))

  #cria classe da nave
  class Nave(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
      pygame.sprite.Sprite.__init__(self)
      self.image = pygame.image.load("assets/img/naveboa.png")
      self.rect = self.image.get_rect()
      self.rect.center = [x, y]
      self.vida_inicial = health
      self.vida_restante = health
      self.ultimo_tiro = pygame.time.get_ticks()
      

    def update(self):
      #definir velocidade de movimento
      velocidade = 8
      #delay p atirar em milisegundos
      cooldown = 500
      game_over = 0
      #procurar por teclas pressionadas
      key = pygame.key.get_pressed()
      if key[pygame.K_LEFT] and self.rect.left > 0:
        self.rect.x -= velocidade      
      if key[pygame.K_RIGHT] and self.rect.right < LARGURA:
        self.rect.x += velocidade
        

      #codigo para a nave atirar
      #gravar tempo atual
      tempo_agora = pygame.time.get_ticks()
      if key[pygame.K_SPACE] and tempo_agora - self.ultimo_tiro > cooldown:
        tiro = Tiro(self.rect.centerx, self.rect.top)
        pygame.mixer.Channel(1).play(laser)
        grupo_tiro.add(tiro)
        self.ultimo_tiro = tempo_agora

      #updeitar mascara
      self.mask = pygame.mask.from_surface(self.image)    

      #desenhar barra de vida
      pygame.draw.rect(screen, VERMELHO, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
      if self.vida_restante > 0:
        pygame.draw.rect(screen, VERDE, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.vida_restante / self.vida_inicial)), 15))
      elif self.vida_restante <= 0:
        pygame.mixer.Channel(2).play(som_explosao)
        explosao = Explosion(self.rect.centerx, self.rect.centery, 3)
        grupo_explosao.add(explosao)
        self.kill()
        game_over = -1
      if pygame.sprite.spritecollide(self, grupo_alien, True, pygame.sprite.collide_mask):
        self.vida_restante = 0
        pygame.mixer.Channel(2).play(som_explosao)
        explosao = Explosion(self.rect.centerx, self.rect.centery, 3)
        grupo_explosao.add(explosao)
      return game_over

  #criar classe do tiro
  class Tiro(pygame.sprite.Sprite):
    def __init__(self, x, y):
      pygame.sprite.Sprite.__init__(self)
      self.image = pygame.image.load("assets/img/bala.png")
      self.rect = self.image.get_rect()
      self.rect.center = [x, y]

    def update(self):
      self.rect.y -= 5
      if self.rect.bottom < 0:
        self.kill()
      if pygame.sprite.spritecollide(self, grupo_alien, True):
        global valorscore
        valorscore += 1
        self.kill()
        pygame.mixer.Channel(2).play(som_explosao)
        explosao = Explosion(self.rect.centerx, self.rect.centery, 1.9)
        grupo_explosao.add(explosao)        
      
  #criar classe dos python-aliens
  class Pythonaliens(pygame.sprite.Sprite):
    def __init__(self, x, y,):
      pygame.sprite .Sprite.__init__(self)
      self.image = pygame.image.load("assets/img/pythonoficial.png")
      self.rect = self.image.get_rect()
      self.rect.center = [x, y]
      self.contador_de_movimentos = 0
      #comeca se movendo p direita
      self.direcao_movimento = 1
      
    def update(self):
      self.rect.x += self.direcao_movimento
      self.contador_de_movimentos += 1
      if abs(self.contador_de_movimentos) > 75:
        #faz os aliens descerem
        self.rect.y += 20
        self.direcao_movimento *= -1
        self.contador_de_movimentos *= self.direcao_movimento        
      
  class Tiroalien(pygame.sprite.Sprite):
    def __init__(self, x, y):
      pygame.sprite.Sprite.__init__(self)
      self.image = pygame.image.load("assets/img/tiroalien.png")
      self.rect = self.image.get_rect()
      self.rect.center = [x, y]

    def update(self):
      self.rect.y += 2
      if self.rect.top > ALTURA:
        self.kill()
      if pygame.sprite.spritecollide(self, grupo_nave, False, pygame.sprite.collide_mask):
        self.kill()
        #reduzir a vida da espaçonave
        nave.vida_restante -= 1
        pygame.mixer.Channel(2).play(som_explosao)
        explosao = Explosion(self.rect.centerx, self.rect.centery, 1.2)
        grupo_explosao.add(explosao)

  class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
      pygame.sprite.Sprite.__init__(self)
      self.escala = scale
      self.images = []
      explosion = pygame.image.load('assets/img/explosion.png')
      explo = spritesheet.Spritesheet(explosion)
      for a in range(10):
        self.images.append(explo.pegar_imagem(a, 34, 34, self.escala, (0,0,0)))
      self.index = 0
      self.image = self.images[self.index]
      self.rect = self.image.get_rect()
      self.rect.center = [x, y]
      self.counter = 0

    def update(self):
      #valor n pode ser maior q 0
      velocidade_de_explosao = 3
      #updeitar anim. de explosao
      self.counter += 1

      if self.counter >= velocidade_de_explosao and self.index < len(self.images) - 1:
        self.counter = 0
        self.index += 1
        self.image = self.images[self.index]

      #se a animação acabar, deleta a explosão
      if self.index >= len(self.images) - 1 and self.counter >= velocidade_de_explosao:
        self.kill()
    
  #cria grupo de sprite
  grupo_nave = pygame.sprite.Group()
  grupo_tiro = pygame.sprite.Group()
  grupo_alien = pygame.sprite.Group()
  grupo_tiro_alien = pygame.sprite.Group()
  grupo_explosao = pygame.sprite.Group()

  #cria alien
  def criar_aliens():
    #gerar aliens
    for linha in range(4):
      for item in range(coluna):
        alien = Pythonaliens(100 + item * 100, 70 + linha * 70)
        grupo_alien.add(alien)  

  criar_aliens()

  #cria player
  nave = Nave(int(LARGURA/2), ALTURA - 75, 3)
  grupo_nave.add(nave)

  run = True
  while run:

    relogio.tick(60)
    desenhar_fundo()

    if countdown == 0:
      
      musica.play(loops =-1)
      #criar tiro dos aliens de forma aleatória
      #gravar tempo atual
      tempo_atual = pygame.time.get_ticks()
      #atirar
      if tempo_atual - ultimo_tiro_alien > alien_cooldown and len(grupo_tiro_alien) < 5 and len(grupo_alien) > 0:
        alien_atirador = random.choice(grupo_alien.sprites())
        tiro_alien = Tiroalien((alien_atirador.rect.centerx), (alien_atirador.rect.bottom))
        grupo_tiro_alien.add(tiro_alien)
        #som de laser alien
        ultimo_tiro_alien = tempo_atual
      
      #verifica se todos os aliens de uma fase morreram
      if len(grupo_alien) == 0:
        game_over = 1

      if game_over == 0:
        
        #updeita a nave
        game_over = nave.update()

        #updeita grupos de sprite
        grupo_tiro.update()
        grupo_alien.update()
        grupo_tiro_alien.update()
      
      else:
        time.sleep(0.4)
        fim_de_jogo()

    if countdown > 0:
      desenhar_texto('Prepare-se', get_font(40), 'white', int(screen.get_width() / 2), int(screen.get_height() / 2 + 100), screen)
      desenhar_texto(str(countdown), get_font(40), 'white', int(screen.get_width() / 2), int(screen.get_height() / 2 + 150), screen)
      count_timer = pygame.time.get_ticks()
      if count_timer - ultima_contagem > 1000:
        countdown -= 1
        ultima_contagem = count_timer


    #animacao explosao
    grupo_explosao.update()
          
    #desenha grupos de sprites
    grupo_nave.draw(screen)  
    grupo_tiro.draw(screen)
    grupo_alien.draw(screen)
    grupo_tiro_alien.draw(screen)
    grupo_explosao.draw(screen)
    
    #mostrar score
    mostrarscore(valorscoreX, valorscoreY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            sys.exit()
    
    key = pygame.key.get_pressed()
    if key[pygame.K_l]:
      game_over = 1
    if key[pygame.K_f]:
      game_over = -1    

    pygame.display.update()

def options():
  pass

def fim_de_jogo():
  
  screen = pygame.display.set_mode((600, 600))
  musica.stop()
  
  def desenhar_fundo():
    screen.fill((0, 0, 0))
    global background_rect
    background_rect = background.get_rect(center=(screen.get_width()/2, screen.get_height()/2))
    screen.blit(background, background_rect)

  run = True
  while run:
    desenhar_fundo()
    if game_over == -1:
      desenhar_texto('Game Over!', get_font(40), 'white', int(screen.get_width() / 2), int(screen.get_height() / 2 - 60), screen)
    
    if game_over == 1:
      desenhar_texto('Voce venceu!', get_font(40), 'white', int(screen.get_width() / 2), int(screen.get_height() / 2 - 60), screen)
    
    RESTART = Botao(background_rect.centerx, background_rect.centery + 50, 'RESTART', get_font(30), 'white', "#8c52ff", image=None)
    NEXT_LEVEL = Botao(background_rect.centerx, background_rect.centery + 50, 'N', get_font(30), 'white', "#8c52ff", image=None)


    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          pygame.quit()

    pygame.display.update()
    pygame.display.flip()

main_menu()
