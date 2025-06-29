import pygame
import sys
import random
import getpass
import gestaoDB

gestaoDB.criarTabelaUsuario()



# Adiciona aqui o login antes de iniciar o pygame
'''
print("==== LOGIN OBRIGATÓRIO ====")
email = input("Email: ")
senha = getpass.getpass("Senha: ")

if not gestaoDB.login(email, senha):
    print("Email ou senha incorretos. Encerrando o jogo.")
    sys.exit()
else:
    print("Login bem-sucedido. Iniciando o jogo...")

pygame.init()
'''
# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GRAY  = (100, 100, 100)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)


def tela_login():
    ...
    screen.fill(WHITE) 

def tela_login():
    input_email = ""
    input_senha = ""
    digitando_email = True
    fonte = pygame.font.SysFont(None, 36)
    erro = ""
    login_sucesso = False

    while not login_sucesso:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    digitando_email = not digitando_email

                elif event.key == pygame.K_BACKSPACE:
                    if digitando_email:
                        input_email = input_email[:-1]
                    else:
                        input_senha = input_senha[:-1]

                elif event.key == pygame.K_RETURN:
                    if gestaoDB.login(input_email, input_senha):
                        login_sucesso = True
                    else:
                        erro = "Email ou senha incorretos"
                        input_email = ""
                        input_senha = ""
                        digitando_email = True

                else:
                    if event.unicode.isprintable():
                        if digitando_email:
                            input_email += event.unicode
                        else:
                            input_senha += event.unicode

        # Renderizar textos
        titulo = fonte.render("LOGIN", True, BLACK)
        email_text = fonte.render("Email: " + input_email, True, BLACK)
        senha_text = fonte.render("Senha: " + "*" * len(input_senha), True, BLACK)
        info_text = fonte.render("TAB para alternar - ENTER para entrar", True, GRAY)
        erro_text = fonte.render(erro, True, RED)

        screen.blit(titulo, (WIDTH // 2 - 40, 100))
        screen.blit(email_text, (100, 200))
        screen.blit(senha_text, (100, 250))
        screen.blit(info_text, (100, 320))
        if erro:
            screen.blit(erro_text, (100, 360))

        pygame.display.update()
        clock.tick(60)

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Rinhas de Rua")
clock = pygame.time.Clock()

tela_login() 


pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Rinhas de Rua")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Player
player = pygame.Rect(100, 500, 50, 80)
player_color = RED
vel = 5
jumping = False
jump_speed = 10
gravity = 1
y_velocity = 0
crouching = False
defending = False
attacking = False
player_health = 50
player_max_health = 50
player_damage_cooldown = 0  # cooldown para não tomar dano toda frame

# Enemy
enemy = pygame.Rect(600, 500, 50, 80)
enemy_color = BLUE
enemy_health = 50
enemy_max_health = 50
enemy_damage_cooldown = 0
enemy_vel = 3
enemy_direction = -1  # -1 = vai pra esquerda, 1 = pra direita
enemy_attacking = False
enemy_defending = False

font = pygame.font.SysFont(None, 30)

def draw_health_bar(x, y, health, max_health):
    ratio = health / max_health
    pygame.draw.rect(screen, BLACK, (x - 2, y - 2, 104, 24))  # borda preta
    pygame.draw.rect(screen, RED, (x, y, 100, 20))
    pygame.draw.rect(screen, GREEN, (x, y, 100 * ratio, 20))

def player_attack():
    global enemy_health, enemy_damage_cooldown
    if enemy_damage_cooldown == 0 and not enemy_defending:
        damage = random.randint(3, 5)
        enemy_health -= damage
        enemy_damage_cooldown = 30  # ~0.5 segundos de invulnerabilidade

def enemy_attack():
    global player_health, player_damage_cooldown, enemy_attacking
    if player_damage_cooldown == 0 and not defending:
        damage = random.randint(3, 5)
        player_health -= damage
        player_damage_cooldown = 30
        enemy_attacking = True

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # ataque
                attacking = True
            elif event.button == 3:  # defesa
                defending = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                attacking = False
            elif event.button == 3:
                defending = False

    keys = pygame.key.get_pressed()
    # Player movimento
    if keys[pygame.K_LEFT]:
        player.x -= vel
    if keys[pygame.K_RIGHT]:
        player.x += vel

    # Abaixar
    if keys[pygame.K_v]:
        crouching = True
    else:
        crouching = False

    # Pular
    if keys[pygame.K_UP] and not jumping:
        jumping = True
        y_velocity = -jump_speed

    if jumping:
        player.y += y_velocity
        y_velocity += gravity
        if player.y >= 500:
            player.y = 500
            jumping = False

    # Cooldowns diminuem
    if player_damage_cooldown > 0:
        player_damage_cooldown -= 1
    if enemy_damage_cooldown > 0:
        enemy_damage_cooldown -= 1

    # Ataque player - se estiver atacando e perto do inimigo (colisão)
    if attacking and player.colliderect(enemy.inflate(20, 20)):
        player_attack()

    # Movimento do inimigo - vai e volta entre 550 e 700
    enemy.x += enemy_vel * enemy_direction
    if enemy.x <= 550:
        enemy_direction = 1
    elif enemy.x >= 700:
        enemy_direction = -1

    # Lógica de ataque do inimigo: tenta atacar se perto do player e cooldown zerado
    if enemy.colliderect(player.inflate(20, 20)) and enemy_damage_cooldown == 0:
        enemy_attack()
    else:
        enemy_attacking = False  # Para animação quando não está atacando

    # Desenhar jogador
    player_draw_color = GRAY if defending else player_color
    if attacking:
        pygame.draw.rect(screen, BLACK, player.inflate(20, 10))
    elif crouching:
        pygame.draw.rect(screen, player_draw_color, pygame.Rect(player.x, player.y + 30, 50, 50))
    else:
        pygame.draw.rect(screen, player_draw_color, player)

    # Desenhar inimigo com animação igual ao player
    enemy_draw_color = GRAY if enemy_defending else enemy_color
    if enemy_attacking:
        pygame.draw.rect(screen, BLACK, enemy.inflate(20, 10))
    elif enemy_defending:
        pygame.draw.rect(screen, GRAY, enemy)
    else:
        pygame.draw.rect(screen, enemy_color, enemy)

    # Desenhar barras de vida
    draw_health_bar(20, 20, player_health, player_max_health)
    draw_health_bar(680, 20, enemy_health, enemy_max_health)

    # Mostrar texto de vida
    player_text = font.render(f"Vida: {player_health}", True, BLACK)
    enemy_text = font.render(f"Vida: {enemy_health}", True, BLACK)
    screen.blit(player_text, (20, 45))
    screen.blit(enemy_text, (680, 45))

    # Checar fim de jogo
    if player_health <= 0:
        tela_final = font.render("Você perdeu!", True, RED)
        screen.blit(tela_final, (WIDTH // 2 - 70, HEIGHT // 2))
        pygame.display.update()
        pygame.time.wait(3000)
        running = False

    if enemy_health <= 0:
        
        tela_final = font.render("Você venceu!", True, GREEN)
        screen.blit(tela_final, (WIDTH // 2 - 70, HEIGHT // 2))
        pygame.display.update()
        pygame.time.wait(3000)
        running = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
