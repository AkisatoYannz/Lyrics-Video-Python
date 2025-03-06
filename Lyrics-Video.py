import pygame
import cv2
import time
import numpy as np

VIDEO_PATH = "your video location"  #your video background
AUDIO_PATH = "your music location with wav format" #your music here
LYRICS = [
    ("the lyrics as long as you want", 0.5), #timestamp for setting lyrics duration
    ("lyrics", 0.5),
    ("lyrics", 0.8),
]

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Lyrics Video")
font = pygame.font.Font(None, 48)
clock = pygame.time.Clock()

pygame.mixer.init()
pygame.mixer.music.load(AUDIO_PATH)
pygame.mixer.music.play()

cap = cv2.VideoCapture(VIDEO_PATH)

def render_lyrics(text, alpha, exposure):
    color = (255, 255, 255)
    text_surface = font.render(text, True, (min(255, int(color[0] * exposure)),
                                             min(255, int(color[1] * exposure)),
                                             min(255, int(color[2] * exposure))))
    text_surface.set_alpha(alpha)
    screen.blit(text_surface, (200, 300))

exposure = 20.0  # Exposure text setting (higher = brighter)
running = True
lyrics_index = 0
start_time = time.time()
alpha = 0
fade_in = True

while running:
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (800, 600))
    frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
    screen.blit(frame, (0, 0))
    
    if lyrics_index < len(LYRICS):
        text, duration = LYRICS[lyrics_index]
        elapsed_time = time.time() - start_time
        
        if fade_in:
            alpha += 10
            if alpha >= 255:
                alpha = 255
                fade_in = False
                start_time = time.time()
        elif elapsed_time >= duration:
            alpha -= 10
            if alpha <= 0:
                alpha = 0
                lyrics_index += 1
                fade_in = True
                start_time = time.time()
        
        render_lyrics(text, alpha, exposure)
    
    pygame.display.flip()
    clock.tick(30)

cap.release()
pygame.mixer.music.stop()
pygame.quit()
