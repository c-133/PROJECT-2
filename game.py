import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

hangman_status = 0
words = ['PYTHON', 'JAVA', 'RUBY', 'JAVASCRIPT', 'HTML', 'CSS']
word = random.choice(words)
guessed = []

RADIUS = 20
GAP = 15
letters = []
start_x = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
start_y = 400
A = 65
for i in range(26):
    x = start_x + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = start_y + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

FPS = 60
clock = pygame.time.Clock()
run = True

win_count = 0
loss_count = 0

def draw():
    win.fill(WHITE)

    text = TITLE_FONT.render("HANGMAN", 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 20))

    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (250, 200))

    for letter in letters:
        x, y, char, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(char, 1, BLACK)
            win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))

    win.blit(images[hangman_status], (0, 100))

    pygame.display.update()

def display_message(message):
    pygame.time.delay(1000)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLUE)
    win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

def reset_game():
    global hangman_status, word, guessed
    hangman_status = 0
    word = random.choice(words)
    guessed = []
    for letter in letters:
        letter[3] = True

while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for letter in letters:
                x, y, char, visible = letter
                if visible:
                    distance = ((x - mouse_x) ** 2 + (y - mouse_y) ** 2) ** 0.5
                    if distance < RADIUS:
                        letter[3] = False
                        guessed.append(char)
                        if char not in word:
                            hangman_status += 1

    draw()

    won = True
    for letter in word:
        if letter not in guessed:
            won = False
            break

    if hangman_status == 6:
        loss_count += 1
        draw()
        display_message("You lost!")
        reset_game()

    if won:
        win_count += 1
        draw()
        display_message("You won!")
        reset_game()

    win_count_text = LETTER_FONT.render("Wins: " + str(win_count), 1, BLACK)
    loss_count_text = LETTER_FONT.render("Losses: " + str(loss_count), 1, BLACK)
    win.blit(win_count_text, (10, 10))
    win.blit(loss_count_text, (10, 50))
    

    pygame.display.update()

    

pygame.quit()
