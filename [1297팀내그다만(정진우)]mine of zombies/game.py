import pygame
import sys
import os
import math
import random
import subprocess
import pygame.mixer
from pygame.locals import *
pygame.init()
# 이미지 로드 함수
def load_image(image_path, size):
    image = pygame.image.load(image_path)
    return pygame.transform.scale(image, size)

def calculate_distance(rect1, rect2):
    x1, y1 = rect1.center
    x2, y2 = rect2.center
    distance = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
    return distance

def check_collision(rect1, rect2, threshold):
    distance = calculate_distance(rect1, rect2)
    return distance < threshold

font = pygame.font.Font(None, 36)
text_color = (0, 0, 0)  # 텍스트 색상 설정
text_position = (10, 50) 
text2_position = (150, 50)# 텍스트 위치 설정


# 게임 루프
running = True
last_skill_collision_time = pygame.time.get_ticks()
class Character:
    def __init__(self, x, y, image_path):
        self.image = pygame.image.load(image_path)  # 이미지 로드
        self.image = pygame.transform.scale(self.image, (300, 300))  # 이미지 크기 조절
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 3
        self.last_frame_update = pygame.time.get_ticks()

    def move_towards(self, target_rect):
        dx = self.rect.centerx - target_rect.centerx  # 플레이어 위치와 좀비 위치의 차이를 계산
        dy = self.rect.centery - target_rect.centery  # 플레이어 위치와 좀비 위치의 차이를 계산
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance != 0:
            dx /= distance
            dy /= distance
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        # 이 부분을 추가하여 좀비가 일정 높이 아래로 내려가지 못하게 함
        

    def update(self):
        self.rect.x = max(0, min(screen_width - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(screen_height - self.rect.height, self.rect.y))


class Obstacle:
    def __init__(self, x, y, image_path):
        self.image = pygame.image.load(image_path)  # 이미지 로드
        self.image = pygame.transform.scale(self.image, (100, 100))  # 이미지 크기 조절
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2  # 장애물의 이동 속도
        self.move_start_time = pygame.time.get_ticks()

    def move(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.x = screen_width
            self.move_start_time = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.move_start_time > 5000:
            self.rect.x = screen_width
            self.move_start_time = pygame.time.get_ticks()

# 초기화
pygame.init()

# 윈도우 크기 설정
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

# 현재 스크립트 디렉토리 경로
script_dir = os.path.dirname(__file__)

# 이미지 경로 설정
background_image_path = os.path.join(script_dir, "47jd73h.jpg")
background_music_path = os.path.join(script_dir, "음악완성본.mp3")
player_path = os.path.join(script_dir, "sss3.png")

heart_image = pygame.image.load(os.path.join(script_dir, "g8dj494.png"))  # 하트 이미지 파일 경로
heart_size = (50, 50)


zombie_sound = pygame.mixer.Sound(os.path.join(script_dir, "zombie-growl-3-6863.wav"))
zombie_sound.set_volume(0.5)  # 소리 볼륨 설정

player_image = pygame.image.load(player_path)

heart_image = pygame.image.load(os.path.join(script_dir, "g8dj494.png"))  # 하트 이미지 파일 경로


zombie_image_path = os.path.join(script_dir, "zombie_student.png")
zombie_image = pygame.image.load(zombie_image_path)
zombie_image = pygame.transform.scale(zombie_image, (300, 300))

player_width = 100
player_heigh = 100

zombie_image = pygame.transform.scale(zombie_image, (300, 300))

zombie_x = screen_width
zombie_y = screen_height // 2
zombie_speed = 5
item_frame_size = (50, 50)
item_image_path = os.path.join(script_dir, "item_frame.png")
item_image = pygame.image.load(item_image_path)
item_image = pygame.transform.scale(item_image, item_frame_size)

item_rect = pygame.Rect(800, 300, 30, 30)
item_speed = 1  # 아이템의 이동 속도

# 배경 이미지 로드
background_image_path = os.path.join(script_dir, "47jd73h.jpg")
background = load_image(background_image_path, (screen_width, screen_height))

# 화면 설정
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("mine of zombies")

player = Character(screen_width // 2, screen_height // 2, player_path)

# 좀비 초기 위치 설정 (화면 오른쪽에서 시작)
zombie_initial_x = screen_width
zombie_rect = pygame.Rect(zombie_initial_x, screen_height // 2, 300, 300)



zombie_rect = zombie_image.get_rect()
zombie_rect.center = (zombie_x, zombie_y)
zombie = Character(screen_width, screen_height // 2, zombie_image_path)


player_rect = pygame.Rect(screen_width // 2, screen_height // 2, 300, 300)
player_speed = 3

zombie_x = 0      # 좀비의 초기 x 좌표

zombie_speed -= 1

hearts = [pygame.Rect(50 * i + 10, 10, 30, 30) for i in range(3)]
remaining_hearts = 3
heart_index = 1500
speed_decrease = False
freeze = False
freeze_start_time = 0
background_x1 = 0
background_x2 = screen_width

skill_images = [load_image(os.path.join(script_dir, "skill1.png"), (100, 100)),
                load_image(os.path.join(script_dir, "skill2.png"), (100, 100)),
                load_image(os.path.join(script_dir, "skill3.png"), (100, 100)),
                load_image(os.path.join(script_dir, "skill4.png"), (100, 100))]

# 스킬 이미지의 이동 속도 설정
skill_speed = 2.5

# 스킬 활성화 여부 설정
skill_active = False

# 쿨타임 타이머 설정
cooldown_timer = 30

# 스킬 이미지가 움직이는 방향 설정
skill_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # 오른쪽, 왼쪽, 아래, 위

skill_rects = []

item_image_path2 = os.path.join(script_dir, "item_frame2.png")
item_image2 = pygame.image.load(item_image_path2)
item_size2 = (50, 50)
collected_items = 0  # 초기 아이템 수집 횟수

ending_path3 =os.path.join(script_dir, "ending.py")
ending_path2 =os.path.join(script_dir, "ending.py")
ending_path = os.path.join(script_dir, "ending.py")
    
zombie_width = 30
zombie_height = 30
pygame.mixer.init()
pygame.mixer.music.load(background_music_path)
pygame.mixer.music.set_volume(1.0)  # 볼륨 조절 (0.0 ~ 1.0)
pygame.mixer.music.play(-1)
        
pygame.display.update()
# 메인 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # ESC 키 누르면 종료
                pygame.quit()
                sys.exit()

    #hp+ itams        
    heart_index_text = font.render(f'Hp: {heart_index}', True, text_color)
    collected_items_text = font.render(f'items max 3: {collected_items}', True, text_color)
            
    for i, heart in enumerate(hearts[:len(hearts) - heart_index]):
        heart_rect = pygame.Rect(50 * i + 10, 10, 30, 30)
        screen.blit(pygame.transform.scale(heart_image, (30, 30)), heart_rect)
    
    for heart in hearts[:3 - remaining_hearts]:
        screen.blit(pygame.transform.scale(heart_image, (30, 30)), heart_rect)
    item_rect.x -= item_speed

    # 아이템이 화면 왼쪽을 벗어나면 새로운 위치로 이동
    if item_rect.right < 0:
        item_rect.x = screen_width
        item_rect.y = random.randint(0, screen_height - item_rect.height)

        skill_rects = [image.get_rect(center=(random.randint(0, screen_width), random.randint(0, screen_height))) for image in skill_images]

       
        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_f] and not skill_active and pygame.time.get_ticks() - cooldown_timer >= 2000:
        # F 키를 눌렀고 스킬이 활성화되지 않았으며 쿨타임이 지난 경우
        skill_active = True
        cooldown_timer = pygame.time.get_ticks()
        
        # 스킬 이미지의 초기 위치 설정 (랜덤한 위치)
        
    if skill_active:
        for i, skill_rect in enumerate(skill_rects):
            if skill_rect.left < screen_width and skill_rect.top <= 500:  # y 좌표가 300 이하일 때만 이동
                dx, dy = skill_directions[i]
                skill_rect.x += dx * skill_speed
                skill_rect.y += dy * skill_speed
            else:
                skill_active = False
                
            # 스킬 이미지의 위치를 좀비의 위치로 업데이트
            skill_rect.center = (zombie.rect.centerx, zombie.rect.centery)
                
            if skill_rect.left < -300 or skill_rect.right > screen_width + 300 or skill_rect.top < -300 or skill_rect.bottom > screen_height +300:
                skill_active = False
            if not skill_rects:  # 모든 스킬 이미지가 화면을 벗어나면 활성화 상태 비활성화
                    skill_active = False
            
            # 스킬과 플레이어 충돌 검사
    for skill_rect in skill_rects:
            if player.rect.colliderect(skill_rect):
                if heart_index > 0:
                    heart_index -= 1
                    player_speed -=100

    distance_to_zombie = math.sqrt((zombie_x - player.rect.centerx) ** 2 + (zombie_y - player.rect.centery) ** 2)
    if distance_to_zombie < 20:  # 원하는 거리로 조절
        pygame.mixer.Sound.play(zombie_sound)

    item_rect.x -= item_speed

    # 아이템이 화면 왼쪽을 벗어나면 새로운 위치로 이동
    if item_rect.right < 0:
        item_rect.x = screen_width
        item_rect.y = random.randint(0, screen_height - item_rect.height)

        skill_rects = [image.get_rect(center=(random.randint(0, screen_width), random.randint(0, screen_height))) for image in skill_images]
        
    zombie.move_towards(player.rect)
    player.move_towards(zombie.rect)
    
    if zombie.rect.x > screen_width:
        zombie.rect.x = -zombie.rect.width
    elif zombie.rect.x < -zombie.rect.width:
        zombie.rect.x = screen_width

    if zombie.rect.y > screen_height:
        zombie.rect.y = -zombie.rect.height
    elif zombie.rect.y < -zombie.rect.height:
        zombie.rect.y = screen_height

    # 캐릭터가 화면을 벗어났을 때, 화면 반대편으로 이동
    if player.rect.x > screen_width:
        player.rect.x = -player.rect.width
    elif player.rect.x < -player.rect.width:
        player.rect.x = screen_width

    if player.rect.y > screen_height:
        player.rect.y = -player.rect.height
    elif player.rect.y < -player.rect.height:
        player.rect.y = screen_height
        
    # 좀비의 움직임을 WASD 키로 조작
    

    zombie_x -= 1  # 좀비 초기 위치를 뒤로 밀어냄
    if zombie_x + zombie_image.get_width() < 0:
        zombie_x = screen_height
        zombie_y = 500  # 좀비 초기 y 좌표 설정

    if zombie_x < 0:  # 좀비가 화면 왼쪽을 벗어나면
        zombie_x = screen_width  # 화면 오른쪽에서 다시 시작

    if speed_decrease:
        player.speed = 5
        if pygame.time.get_ticks() - freeze_start_time > 1500:
            speed_decrease = False
            player.speed = 5

            
    keys = pygame.key.get_pressed()  # 키 입력을 받아옴
    if keys[pygame.K_LEFT]:
        player.rect.x -= player.speed
    if keys[pygame.K_RIGHT]:
        player.rect.x += player.speed
    if keys[pygame.K_UP]:
        player.rect.y -= player.speed
    if keys[pygame.K_DOWN]:
        player.rect.y += player.speed
    if player.rect.y < 300:
        player.rect.y = 300
    
     # 좀비의 움직임을 WASD 키로 조작
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        zombie_x -= zombie_speed
    if keys[pygame.K_d]:
        zombie_x += zombie_speed
    if keys[pygame.K_w]:
        zombie_y -= zombie_speed
        
    if keys[pygame.K_s]:
        zombie_y += zombie_speed
    if zombie_y < 300:
            zombie_y = 300 
        
    zombie_rect.x -= zombie_speed

    # 좀비가 왼쪽 화면 밖으로 나갔을 때 처리
    if zombie_rect.right < 0:
        zombie_rect.x = screen_width

    # 캐릭터와 좀비 충돌 검사
     #하트인덱스가 0이면 엔딩실행               
    if heart_index <= 0:
        pygame.mixer.music.stop()
        subprocess.run(["python", ending_path3])  # 엔딩 파일 실행
        pygame.quit()
        sys.exit()
        
       # 좀비와 플레이어 충돌 검사
    zombie_rect = pygame.Rect(zombie_x, zombie_y, zombie_width, zombie_height)
    player_rect = pygame.Rect(player.rect.x, player.rect.y, player_width, player_heigh)

    if zombie_rect.colliderect(player_rect):
        heart_index -= 1
        if heart_index <= 0:
            game_over = True
            game_over_timer = pygame.time.get_ticks()
            pygame.mixer.music.stop()
            subprocess.run(["python", ending_path2])  # 엔딩 파일 실행
            pygame.quit()
            sys.exit()
          # 엔딩 파일 실행
        
        
    speed_decrease = True
    freeze_start_time = pygame.time.get_ticks()
            
    if player.rect.colliderect(item_rect):
        item_rect.x = -100  # 아이템을 화면 밖으로 이동시켜 획득처리
        collected_items += 1

    if collected_items >= 3:
        pygame.mixer.music.stop()
        subprocess.run(["python", ending_path])  # 엔딩 파일 실행
        pygame.quit()
        sys.exit()





    background_x1 -= 6
    background_x2 -= 6
    if background_x1 < -background.get_width():
        background_x1 = background.get_width()
    if background_x2 < -background.get_width():
        background_x2 = background.get_width()
        




    screen.fill((0, 0, 0))
    screen.blit(background, (background_x1, 0))
    screen.blit(background, (background_x2, 0))
    screen.blit(pygame.transform.scale(heart_image, (30, 30)), pygame.Rect(10, 10, 30, 30))
    screen.blit(heart_index_text, text_position)
    screen.blit(collected_items_text, text2_position)

    screen.blit(item_image, item_rect)

    screen.blit(zombie_image, (zombie_x, zombie_y)), screen.blit(player.image, player.rect)
    for skill_image, skill_rect in zip(skill_images, skill_rects):
        screen.blit(skill_image, skill_rect)
    pygame.display.flip()  # 화면을 업데이트합니다.

pygame.quit()

    
    
