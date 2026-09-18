import math
import pygame
import random

WIDTH, HEIGHT = 2000, 1200
BACKGROUND_COLOR = (0, 0, 0)
FPS = 60
SCALE = 20

WORDS = ["love you", "Love You", "LOVE YOU"]
CENTER_TEXT = " Love You "
COLORS = [
    (70, 130, 180),
    (30, 144, 255),
    (0, 191, 255),
    (100, 149, 237),
    (65, 105, 225)
    ] 



class Particle:
    __slots__ = ('x', 'y', 'order', 'kind', 'word', 'color', 'alpha', 'flicker', 'font', 'delay', 'size_mult')
    
    def __init__(self, x, y, order, kind):
        self.x = x
        self.y = y
        self.order = order
        self.kind = kind
        self.word = random.choice(WORDS)
        self.color = random.choice(COLORS)
        self.alpha = 0
        self.flicker = random.uniform(0, math.pi * 2)
        self.font = pygame.font.SysFont('Arial', 20)
        self.delay = 0
        self.size_mult = random.uniform(0.85, 1.15)


def heart_xy(t):
    x = 16 * (math.sin(t) ** 3)
    y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
    return x, -y


def to_screen(x, y):
    return x * SCALE + WIDTH / 2, y * SCALE + HEIGHT / 2


def build_heart_particles(n_outline, min_gap=30):
    particles = []
    placed = []
    for i in range(n_outline):
        t = (i / n_outline) * 2 * math.pi
        bx, by = heart_xy(t)
        sx, sy = to_screen(bx, by)
        if any(math.hypot(sx - px, sy - py) < min_gap for (px, py) in placed):
            continue
        placed.append((sx, sy))
        particles.append(Particle(sx, sy, i, 'outline'))
    return particles


def build_fill_particles(n_fill, min_gap=40):
    particles = []
    placed = []
    attempts = 0
    max_attempts = n_fill * 80

    while len(particles) < n_fill and attempts < max_attempts:
        attempts += 1
        t = random.uniform(0, 2 * math.pi)
        r = random.uniform(0.0, 0.86)  
        bx, by = heart_xy(t)
        px, py = bx * r, by * r
        sx, sy = to_screen(px, py)

        if any(math.hypot(sx - qx, sy - qy) < min_gap for (qx, qy) in placed):
            continue

        placed.append((sx, sy))
        particles.append(Particle(sx, sy, random.randint(0, 320), "fill"))  

    return particles


def draw_glow_text(glow_layer, screen_layer, font, word, color, x, y, alpha, size_mult=1.0):
    if alpha <= 0:
        return

    if size_mult != 1.0:
        scaled_font = pygame.font.Font(None, int(font.get_height() * size_mult))
        txt = scaled_font.render(word, True, color)
    else:
        txt = font.render(word, True, color)

    txt.set_alpha(alpha)
    txt_rect = txt.get_rect(center=(x, y))

    if alpha > 10:
        glow_big = pygame.transform.smoothscale(txt, (int(txt.get_width() * 2.4), int(txt.get_height() * 2.4)))
        glow_big.set_alpha(max(0, alpha // 7))
        glow_rect = glow_big.get_rect(center=(x, y))
        glow_layer.blit(glow_big, glow_rect)
        
        glow_small = pygame.transform.smoothscale(txt, (int(txt.get_width() * 1.6), int(txt.get_height() * 1.6)))
        glow_small.set_alpha(max(0, alpha // 3))
        glow_rect = glow_small.get_rect(center=(x, y))
        glow_layer.blit(glow_small, glow_rect)
    
    screen_layer.blit(txt, txt_rect)


def reset_animation(font_outline, font_fill):
    outline = build_heart_particles(n_outline=160)
    fill = build_fill_particles(n_fill=130)
    
    outline_span = max(p.order for p in outline) if outline else 0
    frames_per_step = 1.6
    fill_start_frame = int(outline_span * frames_per_step) + 30
    
    for p in fill:
        p.delay = fill_start_frame + p.order
    for p in outline:
        p.delay = int(p.order * frames_per_step)
    
    particles = outline + fill
    for p in particles:
        p.font = font_outline if p.kind == "outline" else font_fill

    return particles, fill_start_frame


def main():
    pygame.init()

    info = pygame.display.Info()
    global WIDTH, HEIGHT
    WIDTH, HEIGHT = info.current_w, info.current_h

    audio_loaded = False
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("a.mp3")
        pygame.mixer.music.play()
        audio_loaded = True
    except Exception as e:
        print(f"Audio failed: {e}")

    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.DOUBLEBUF)
    pygame.display.set_caption("I Love you")
    clock = pygame.time.Clock()

    font_outline = pygame.font.SysFont("arial", 20, bold=True)
    font_fill = pygame.font.SysFont("arial", 17, bold=True)
    font_center = pygame.font.SysFont("georgia", 54, bold=True)
    
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill(BACKGROUND_COLOR)
    
    particles, fill_start_frame = reset_animation(font_outline, font_fill)
    
    running = True
    frame = 0
    glow_layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    text_layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        if audio_loaded and not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
            particles, fill_start_frame = reset_animation(font_outline, font_fill)
            frame = 0
        
        screen.blit(background, (0, 0))
        glow_layer.fill((0, 0, 0, 0))
        text_layer.fill((0, 0, 0, 0))
        frame += 1
        
        for p in particles:
            if frame > p.delay and p.alpha < 255:
                p.alpha = min(255, p.alpha + 14 + random.randint(0, 4))
            
            if p.alpha >= 255:
                flick = 0.75 + 0.25 * math.sin(frame * 0.04 + p.flicker)
            else:
                flick = 1.0
            
            alpha = int(p.alpha * flick)
            if alpha <= 0:
                continue
            
            draw_glow_text(glow_layer, text_layer, p.font, p.word, p.color, 
                        p.x, p.y, alpha, p.size_mult)
        
        screen.blit(glow_layer, (0, 0))
        screen.blit(text_layer, (0, 0))
        
        center_start = fill_start_frame + 200
        if frame > center_start:
            progress = min(1.0, (frame - center_start) / 60)
            center_alpha = int(255 * (1 - math.exp(-progress * 8)))
            
            pulse = 1.0 + 0.025 * math.sin(frame * 0.05)
            center_surf = font_center.render(CENTER_TEXT, True, (255, 250, 245))
            
            new_width = int(center_surf.get_width() * pulse)
            new_height = int(center_surf.get_height() * pulse)
            if new_width > 0 and new_height > 0:
                center_surf = pygame.transform.smoothscale(center_surf, (new_width, new_height))
            
            center_surf.set_alpha(center_alpha)
            
            if center_alpha > 10:
                glow_center = pygame.transform.smoothscale(
                    center_surf, (int(center_surf.get_width() * 1.4), int(center_surf.get_height() * 1.4))
                )
                glow_center.set_alpha(center_alpha // 5)
                glow_rect = glow_center.get_rect(center=(WIDTH/2, HEIGHT/2))
                screen.blit(glow_center, glow_rect)
            
            text_rect = center_surf.get_rect(center=(WIDTH/2, HEIGHT/2))
            screen.blit(center_surf, text_rect)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("OCURRIO UN ERROR:", e)
        import traceback
        traceback.print_exc()