import pygame
import os
import sys
import pygame.mixer

# pygame 초기화
pygame.init()
pygame.mixer.init()

# 화면 크기 설정
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("mine of zombies")
script_dir = os.path.dirname(__file__)
# 엔딩 화면 이미지 로드
ending_image = pygame.image.load(os.path.join(script_dir, "16_20230908235223.png"))  # 이미지 경로를 적절히 변경하세요

font = pygame.font.Font(None, 36)
ending_text = font.render("게임 클리어!", True, (0, 0, 0))
text_rect = ending_text.get_rect(center=(screen_width // 2, screen_height // 2))

# 초기 이미지 위치 설정
image_x = screen_width // 2 - ending_image.get_width() // 2
image_y = screen_height  # 아래에서 시작

background_music_path = os.path.join(script_dir, "risk-136788.wav")
pygame.mixer.music.load(background_music_path)
pygame.mixer.music.set_volume(0.3)  # 볼륨 조절 (0.0 ~ 1.0)
pygame.mixer.music.play(-1)

# 엔딩 화면 루프
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # ESC 키 누르면 종료
                pygame.quit()
                sys.exit()

    # 이미지 위로 이동
    image_y -= 1  # 움직이는 속도 조절

    # 화면 색깔 설정 (검은색)
    screen.fill((255, 255, 255))

    # 엔딩 이미지 출력
    screen.blit(ending_image, (image_x, image_y))
 

    # 화면 업데이트
    pygame.display.flip()

    # 프레임 설정 (60fps)
    clock.tick(60)
    
    # 이미지가 화면 위로 나가면 종료
    if image_y + ending_image.get_height() < 0:
        pygame.quit()
        sys.exit()