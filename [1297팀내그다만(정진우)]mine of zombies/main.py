import pygame
import sys
import os
import subprocess

pygame.init()

screen_width = 1920

screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))

script_dir = os.path.dirname(__file__)

background_image_path = os.path.join(script_dir, "student_2_str.png")
image_path = os.path.join(script_dir, "4_20230806163223.png")
image2_path = os.path.join(script_dir, "5_20230810151945.png")
image3_path = os.path.join(script_dir, "17_20230909125926.png")
game_path = os.path.join(script_dir, "game.py")


screen = pygame.display.set_mode((screen_width, screen_height),pygame.FULLSCREEN)
pygame.display.set_caption("mine of zombies")

background_image = pygame.image.load(background_image_path)
image = pygame.image.load(image_path)
image2 = pygame.image.load(image2_path)
image3 = pygame.image.load(image3_path)


image3_width, image3_height = image3.get_size()

image3_width = 800
image3_height = 800
image3 = pygame.transform.scale(image3, (image3_width, image3_height))




image_width, image_height = image.get_size()
image2_width, image2_height = image2.get_size()


image_width = 350 
image_height = 350 
image = pygame.transform.scale(image, (image_width,  image_height))

image2_width = 250 
image2_height = 250 
image2 = pygame.transform.scale(image2, (image2_width,  image2_height))

background_image_width = 1920 
background_image_height = 1080
background_image = pygame.transform.scale(background_image, (background_image_width,  background_image_height))


background_image_x = screen_width // 2 -  background_image_width // 2 
background_image_y = screen_height // 2 - background_image_height // 2 

image3_x = screen_width // 2 - image3_width // 2
image3_y = screen_height // 2 - image3_height // 2 - 250


image_x = screen_width // 2 -  image_width // 2 
image_y = screen_height // 2 - image_height // 2 + 50

image2_x = screen_width // 2 - image2_width // 2 
image2_y = screen_height // 2 - image2_height // 2 + 200


background_music_path = os.path.join(script_dir, "음악완성본.mp3")
pygame.mixer.music.load(background_music_path)
pygame.mixer.music.set_volume(1.0)  # 볼륨 조절 (0.0 ~ 1.0)
pygame.mixer.music.play(-1)

button_clicked = False

game_file_path = game_path

def check_button_click(mouse_pos, button_x, button_y, button_width, button_height):
    return (
        button_x <= mouse_pos[0] <= button_x + button_width
        and button_y <= mouse_pos[1] <= button_y + button_height
    )


pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # ESC 키 누르면 종료
                pygame.quit()
                sys.exit()

            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
        
            if check_button_click(mouse_pos, image_x, image_y, image_width, image_height):
                button_clicked = True
            if check_button_click(mouse_pos, image2_x, image2_y, image2_width, image2_height):
                button_clicked2 = True

    # 이미지를 화면에 표시
    
    screen.blit(background_image, (background_image_x, background_image_y))
    screen.blit(image, (image_x, image_y))
    screen.blit(image2, (image2_x, image2_y))
    screen.blit(image3, (image3_x, image3_y))

    # 화면 업데이트
    pygame.display.update()

    if button_clicked:
            pygame.mixer.music.stop()
            subprocess.run(["python", game_file_path])
            pygame.quit()
            sys.exit()
            

       
