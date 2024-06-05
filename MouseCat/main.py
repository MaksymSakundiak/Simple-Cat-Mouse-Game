import pygame
import sys
import random

pygame.init()

screen_width = 512
screen_height = 384

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cat and Mouse Chase")


def load_image(filename, scale_to_screen=False):
    try:
        image = pygame.image.load(filename).convert_alpha()
        if scale_to_screen:
            image = pygame.transform.scale(image,
                                           (screen_width, screen_height))
        return image
    except pygame.error as e:
        print(f"Unable to load image {filename}: {e}")
        pygame.quit()
        sys.exit()
    except FileNotFoundError as e:
        print(
            f"File not found: {filename}. Please make sure the file is in the correct directory."
        )
        pygame.quit()
        sys.exit()


cat_img = load_image('Cat.png')
mouse_img = load_image('Mouse.png')
cheese_img = load_image('cheese.png')
game_over_img = load_image('gameover.webp', scale_to_screen=True)
win_img = load_image('win.jpeg', scale_to_screen=True)

cat_pos = [50, 50]
mouse_pos = [200, 200]

cheese_list = []
num_cheese = 5
for _ in range(num_cheese):
    cheese_list.append([
        random.randint(0, screen_width - cheese_img.get_width()),
        random.randint(0, screen_height - cheese_img.get_height())
    ])

score = 0
mouse_speed = 6
cat_speed = 3
font = pygame.font.Font(None, 36)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def reset_game():
    global mouse_pos, cat_pos, cheese_list, score, cheese_collected
    mouse_pos = [200, 200]
    cat_pos = [50, 50]
    cheese_list = []
    for _ in range(num_cheese):
        cheese_list.append([
            random.randint(0, screen_width - cheese_img.get_width()),
            random.randint(0, screen_height - cheese_img.get_height())
        ])
    score = 0
    cheese_collected = 0


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


def main():
    global score, mouse_pos, cat_pos, cheese_collected

    pygame.mixer.music.load(
        'itty-bitty-8-bit-kevin-macleod-main-version-7983-03-13.mp3')
    pygame.mixer.music.play(-1)

    running = True
    game_over = False
    game_started = False
    cheese_collected = 0

    play_again_button = pygame.Rect(screen_width // 2 - 50, screen_height // 2,
                                    100, 50)
    start_game_button = pygame.Rect(screen_width // 2 - 50, screen_height // 2,
                                    100, 50)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif game_over or not game_started:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if play_again_button.collidepoint((mouse_x, mouse_y)):
                        reset_game()
                        game_over = False
                        game_started = True
                    elif start_game_button.collidepoint((mouse_x, mouse_y)):
                        reset_game()
                        game_started = True

        if game_started and not game_over:
            cat_dx = mouse_pos[0] - cat_pos[0]
            cat_dy = mouse_pos[1] - cat_pos[1]
            distance = (cat_dx**2 + cat_dy**2)**0.5
            if distance != 0:
                cat_speed_x = cat_speed * cat_dx / distance
                cat_speed_y = cat_speed * cat_dy / distance
                cat_pos[0] += cat_speed_x
                cat_pos[1] += cat_speed_y

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                mouse_pos[0] -= mouse_speed
            if keys[pygame.K_RIGHT]:
                mouse_pos[0] += mouse_speed
            if keys[pygame.K_UP]:
                mouse_pos[1] -= mouse_speed
            if keys[pygame.K_DOWN]:
                mouse_pos[1] += mouse_speed

            mouse_pos[0] = max(
                0, min(screen_width - mouse_img.get_width(), mouse_pos[0]))
            mouse_pos[1] = max(
                0, min(screen_height - mouse_img.get_height(), mouse_pos[1]))

            mouse_rect = mouse_img.get_rect(topleft=mouse_pos)
            for cheese in cheese_list:
                cheese_rect = cheese_img.get_rect(topleft=cheese)
                if mouse_rect.colliderect(cheese_rect):
                    score += 1
                    cheese_collected += 1
                    cheese_list.remove(cheese)

            cat_rect = cat_img.get_rect(topleft=cat_pos)
            if cat_rect.colliderect(mouse_rect):
                game_over = True

            if cheese_collected > 0:
                cheese_list.append([
                    random.randint(0, screen_width - cheese_img.get_width()),
                    random.randint(0, screen_height - cheese_img.get_height())
                ])
                cheese_collected -= 1

        screen.fill(WHITE)

        if game_over or score >= 25:
            if score >= 25:
                screen.blit(win_img, (0, 0))
                draw_text('You Win!', font, WHITE, screen,
                          screen_width // 2 - 70, screen_height // 2 - 50)
            else:
                screen.blit(game_over_img, (0, 0))
                draw_text('Game Over', font, BLACK, screen,
                          screen_width // 2 - 70, screen_height // 2 - 50)
            pygame.draw.rect(screen, BLACK, play_again_button)
            draw_text('Play Again', font, WHITE, screen,
                      screen_width // 2 - 45, screen_height // 2 + 10)
        elif not game_started:
            draw_text('Cat and Mouse Chase', font, BLACK, screen,
                      screen_width // 2 - 100, screen_height // 2 - 50)
            pygame.draw.rect(screen, BLACK, start_game_button)
            draw_text('Start Game', font, WHITE, screen,
                      screen_width // 2 - 45, screen_height // 2 + 10)
        else:
            screen.blit(cat_img, cat_pos)
            screen.blit(mouse_img, mouse_pos)
            for cheese in cheese_list:
                screen.blit(cheese_img, cheese)
            score_text = font.render(f'Score: {score}', True, BLACK)
            screen.blit(score_text, (10, 10))

        pygame.display.flip()
        pygame.time.Clock().tick(30)


if __name__ == "__main__":
    main()
