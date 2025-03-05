import pygame
import random
import json
import os
import asyncio
import logging

# Initialize Pygame and Mixer
pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound

# Screen settings
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spider Attack")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

# Get script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(SCRIPT_DIR, "assets")

# File paths
SCORE_FILE = os.path.join(SCRIPT_DIR, "high_scores.json")
START_BACKGROUND = os.path.join(ASSETS_DIR, "startBackground.jpg")
HIGH_SCORE_BACKGROUND = os.path.join(ASSETS_DIR, "highscoreBackground.jpg")
TANK_IMAGE = os.path.join(ASSETS_DIR, "tank.png")
SPIDER1_IMAGE = os.path.join(ASSETS_DIR, "spider1.png")
SPIDER2_IMAGE = os.path.join(ASSETS_DIR, "spider2.png")
SPIDER3_IMAGE = os.path.join(ASSETS_DIR, "spider3.png")
BOMB_IMAGE = os.path.join(ASSETS_DIR, "bomb.png")
BULLETSPEED_UPGRADE_IMAGE = os.path.join(ASSETS_DIR, "bulletspeedUpgrade.png")
TANKSPEED_UPGRADE_IMAGE = os.path.join(ASSETS_DIR, "tankspeedUpgrade.png")
CANNON_UPGRADE_IMAGE = os.path.join(ASSETS_DIR, "cannonUpgrade.png")
FIRINGRATE_UPGRADE_IMAGE = os.path.join(ASSETS_DIR, "firingrateUpgrade.png")
# Sound file paths
SHOOT_SOUND = os.path.join(ASSETS_DIR, "shoot.wav")
SPIDER_HIT_SOUND = os.path.join(ASSETS_DIR, "spider_hit.wav")
UPGRADE_HIT_SOUND = os.path.join(ASSETS_DIR, "upgrade_hit.wav")
BOMB_HIT_SOUND = os.path.join(ASSETS_DIR, "bomb_hit.wav")

# Load assets asynchronously
async def load_assets():
    try:
        tank_image = pygame.transform.scale(pygame.image.load(TANK_IMAGE).convert_alpha(), (40, 50))
        spider_images = [
            pygame.transform.scale(pygame.image.load(SPIDER1_IMAGE).convert_alpha(), (40, 40)),
            pygame.transform.scale(pygame.image.load(SPIDER2_IMAGE).convert_alpha(), (40, 40)),
            pygame.transform.scale(pygame.image.load(SPIDER3_IMAGE).convert_alpha(), (40, 40))
        ]
        bomb_image = pygame.transform.scale(pygame.image.load(BOMB_IMAGE).convert_alpha(), (30, 30))
        bulletspeed_upgrade_image = pygame.transform.scale(pygame.image.load(BULLETSPEED_UPGRADE_IMAGE).convert_alpha(), (30, 30))
        tankspeed_upgrade_image = pygame.transform.scale(pygame.image.load(TANKSPEED_UPGRADE_IMAGE).convert_alpha(), (30, 30))
        cannon_upgrade_image = pygame.transform.scale(pygame.image.load(CANNON_UPGRADE_IMAGE).convert_alpha(), (30, 30))
        firingrate_upgrade_image = pygame.transform.scale(pygame.image.load(FIRINGRATE_UPGRADE_IMAGE).convert_alpha(), (30, 30))
        return tank_image, spider_images, bomb_image, bulletspeed_upgrade_image, tankspeed_upgrade_image, cannon_upgrade_image, firingrate_upgrade_image
    except pygame.error as e:
        logging.error(f"Error loading assets: {e}")
        raise

# Load high scores
async def load_high_scores():
    default_scores = [{"name": "Player", "score": 0}] * 10
    if not os.path.exists(SCORE_FILE):
        logging.info(f"High scores file not found at {SCORE_FILE}. Creating a new one.")
        await save_high_scores(default_scores)
        return default_scores
    try:
        with open(SCORE_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logging.error(f"Error loading high scores from {SCORE_FILE}: {e}. Creating a new file.")
        await save_high_scores(default_scores)
        return default_scores

# Save high scores
async def save_high_scores(scores):
    with open(SCORE_FILE, "w") as f:
        json.dump(scores, f)

# Get player name
async def get_player_name():
    name = ""
    input_active = True
    while input_active:
        await asyncio.sleep(1/60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.unicode.isalnum() and len(name) < 10:
                    name += event.unicode.upper()

        screen.fill(BLACK)
        prompt = font.render("Enter your name (max 10 chars):", True, WHITE)
        name_text = font.render(name, True, WHITE)
        screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
        clock.tick(60)
    return name

# Update high scores
async def update_high_scores(final_score):
    scores = await load_high_scores()
    if final_score >= scores[-1]["score"]:
        name = await get_player_name()
        scores.append({"name": name, "score": final_score})
        scores.sort(key=lambda x: x["score"], reverse=True)
        scores = scores[:10]
        await save_high_scores(scores)
    return scores

# Display start screen
async def show_start_screen():
    try:
        background = pygame.transform.scale(pygame.image.load(START_BACKGROUND).convert(), (WIDTH, HEIGHT))
    except pygame.error:
        logging.error(f"Error loading start background image from {START_BACKGROUND}. Using black background.")
        background = pygame.Surface((WIDTH, HEIGHT))
        background.fill(BLACK)

    while True:
        await asyncio.sleep(1/60)
        screen.blit(background, (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))

        title = font.render("Spider Attack", True, WHITE)
        prompt = font.render("Press Space to Start", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

        clock.tick(60)

# Display high scores
async def show_high_scores(scores, final_score):
    try:
        background = pygame.transform.scale(pygame.image.load(HIGH_SCORE_BACKGROUND).convert(), (WIDTH, HEIGHT))
    except pygame.error:
        logging.error(f"Error loading high score background image from {HIGH_SCORE_BACKGROUND}. Using black background.")
        background = pygame.Surface((WIDTH, HEIGHT))
        background.fill(BLACK)

    while True:
        await asyncio.sleep(1/60)
        screen.blit(background, (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))

        game_over_text = font.render(f"Game Over! Final Score: {final_score}", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 50))
        title = font.render("Top 10 High Scores", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        
        for i, entry in enumerate(scores):
            text = small_font.render(f"{i + 1}. {entry['name']} - {entry['score']}", True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 150 + i * 30))
        
        prompt = font.render("Space to Play Again, Q to Quit", True, WHITE)
        screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT - 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                if event.key == pygame.K_q:
                    return False

        clock.tick(60)

# Drawing functions
def draw_cannon(x, y, barrels, tank_image):
    screen.blit(tank_image, (x, y - 30))

def draw_spider(x, y, image_index, spider_images):
    screen.blit(spider_images[image_index], (x, y))

def draw_cannon_stats(fire_rate, bullet_speed, cannon_barrels, cannon_speed):
    stats_x = WIDTH - 150
    stats_y = 10
    block_size = 10
    spacing = 15

    fire_text = small_font.render("Fire Rate", True, WHITE)
    screen.blit(fire_text, (stats_x, stats_y))
    for i in range(2):
        color = GREEN if fire_rate <= 20 - (i + 1) * 5 else WHITE
        pygame.draw.rect(screen, color, (stats_x + i * (block_size + 5), stats_y + spacing, block_size, block_size))

    bullet_text = small_font.render("Bullet Speed", True, WHITE)
    screen.blit(bullet_text, (stats_x, stats_y + spacing * 2))
    for i in range(2):
        color = GREEN if bullet_speed >= 7 + (i + 1) * 2 else WHITE
        pygame.draw.rect(screen, color, (stats_x + i * (block_size + 5), stats_y + spacing * 3, block_size, block_size))

    barrel_text = small_font.render("Barrels", True, WHITE)
    screen.blit(barrel_text, (stats_x, stats_y + spacing * 4))
    for i in range(2):
        color = GREEN if cannon_barrels > i + 1 else WHITE
        pygame.draw.rect(screen, color, (stats_x + i * (block_size + 5), stats_y + spacing * 5, block_size, block_size))

    speed_text = small_font.render("Cannon Speed", True, WHITE)
    screen.blit(speed_text, (stats_x, stats_y + spacing * 6))
    for i in range(2):
        color = GREEN if cannon_speed >= 8 * (i + 2) else WHITE
        pygame.draw.rect(screen, color, (stats_x + i * (block_size + 5), stats_y + spacing * 7, block_size, block_size))

def draw_upgrade(x, y, upgrade_type, images):
    if upgrade_type == "fire_rate":
        screen.blit(images["firingrate"], (x, y))
    elif upgrade_type == "bullet_speed":
        screen.blit(images["bulletspeed"], (x, y))
    elif upgrade_type == "extra_barrel":
        screen.blit(images["cannon"], (x, y))
    elif upgrade_type == "clear_spiders":
        screen.blit(images["bomb"], (x, y))
    elif upgrade_type == "cannon_speed":
        screen.blit(images["tankspeed"], (x, y))

# Game state class
class GameState:
    def __init__(self):
        self.tank_x = WIDTH // 2 - 20
        self.tank_y = HEIGHT - 40
        self.base_cannon_speed = 8
        self.cannon_speed = self.base_cannon_speed
        self.cannon_barrels = 1
        self.bullet_speed = 7
        self.bullets = []
        self.fire_rate = 20
        self.fire_counter = 0
        self.spider_speed = 3
        self.spiders = []  # [x, y, image_index]
        self.upgrades = []
        self.upgrade_types = ["fire_rate", "bullet_speed", "extra_barrel", "clear_spiders", "cannon_speed"]
        self.score = 0
        self.lives = 3
        self.spider_spawn_counter = 0
        self.upgrade_spawn_counter = 0

async def handle_input(state, keys, shoot_sound):
    if keys[pygame.K_LEFT] and state.tank_x > 0:
        state.tank_x -= state.cannon_speed
    if keys[pygame.K_RIGHT] and state.tank_x < WIDTH - 40:
        state.tank_x += state.cannon_speed
    state.fire_counter += 1
    if keys[pygame.K_SPACE] and state.fire_counter >= state.fire_rate:
        barrel_offset = 40 // (state.cannon_barrels + 1)
        for i in range(state.cannon_barrels):
            bullet_x = state.tank_x + barrel_offset * (i + 1) - 2.5
            state.bullets.append([bullet_x, state.tank_y - 30])
        state.fire_counter = 0
        shoot_sound.play()  # Play shooting sound

async def update_entities(state):
    # Update bullets
    for bullet in state.bullets:
        bullet[1] -= state.bullet_speed
    state.bullets = [b for b in state.bullets if b[1] >= 0]

    # Update spiders with scaling difficulty
    state.spider_speed = 3 + state.score // 200
    for spider in state.spiders:
        spider[1] += state.spider_speed
        if spider[1] > HEIGHT:
            state.lives -= 1
            logging.debug(f"Spider passed tank. Lives remaining: {state.lives}")

    state.spiders = [s for s in state.spiders if s[1] <= HEIGHT]

    # Update upgrades
    for upgrade in state.upgrades:
        upgrade[1] += 2
    state.upgrades = [u for u in state.upgrades if u[1] <= HEIGHT]

    # Spawn entities
    state.spider_spawn_counter += 1
    if state.spider_spawn_counter >= max(30, 60 - state.score // 100):
        state.spiders.append([random.randint(0, WIDTH - 40), -40, random.randint(0, 2)])
        state.spider_spawn_counter = 0

    state.upgrade_spawn_counter += 1
    if state.upgrade_spawn_counter >= 300:
        state.upgrades.append([random.randint(0, WIDTH - 30), -30, random.choice(state.upgrade_types)])
        state.upgrade_spawn_counter = 0

async def handle_collisions(state, spider_hit_sound, upgrade_hit_sound, bomb_hit_sound):
    bullets_to_remove = []
    spiders_to_remove = []
    upgrades_to_remove = []

    for bullet in state.bullets:
        bullet_rect = pygame.Rect(bullet[0], bullet[1], 5, 10)
        for spider in state.spiders:
            spider_rect = pygame.Rect(spider[0], spider[1], 40, 40)
            if bullet_rect.colliderect(spider_rect) and bullet not in bullets_to_remove:
                bullets_to_remove.append(bullet)
                spiders_to_remove.append(spider)
                state.score += 10
                spider_hit_sound.play()  # Play spider hit sound
                break
        for upgrade in state.upgrades:
            upgrade_rect = pygame.Rect(upgrade[0], upgrade[1], 30, 30)
            if bullet_rect.colliderect(upgrade_rect) and bullet not in bullets_to_remove:
                bullets_to_remove.append(bullet)
                upgrades_to_remove.append(upgrade)
                if upgrade[2] == "fire_rate" and state.fire_rate > 10:
                    state.fire_rate -= 5
                    upgrade_hit_sound.play()  # Play upgrade hit sound
                elif upgrade[2] == "bullet_speed" and state.bullet_speed < 11:
                    state.bullet_speed += 2
                    upgrade_hit_sound.play()
                elif upgrade[2] == "extra_barrel" and state.cannon_barrels < 3:
                    state.cannon_barrels += 1
                    upgrade_hit_sound.play()
                elif upgrade[2] == "clear_spiders":
                    collected_upgrades = [u[2] for u in state.upgrades if u != upgrade]
                    for up_type in collected_upgrades:
                        if up_type == "fire_rate" and state.fire_rate > 10:
                            state.fire_rate -= 5
                            upgrade_hit_sound.play()
                        elif up_type == "bullet_speed" and state.bullet_speed < 11:
                            state.bullet_speed += 2
                            upgrade_hit_sound.play()
                        elif up_type == "extra_barrel" and state.cannon_barrels < 3:
                            state.cannon_barrels += 1
                            upgrade_hit_sound.play()
                        elif up_type == "cannon_speed" and state.cannon_speed < state.base_cannon_speed * 3:
                            state.cannon_speed += state.base_cannon_speed
                            upgrade_hit_sound.play()
                    spider_count = len(state.spiders)
                    state.spiders.clear()
                    state.score += spider_count * 20
                    bomb_hit_sound.play()  # Play bomb hit sound
                elif upgrade[2] == "cannon_speed" and state.cannon_speed < state.base_cannon_speed * 3:
                    state.cannon_speed += state.base_cannon_speed
                    upgrade_hit_sound.play()

    # Apply removals
    state.bullets = [b for b in state.bullets if b not in bullets_to_remove]
    state.spiders = [s for s in state.spiders if s not in spiders_to_remove]
    state.upgrades = [u for u in state.upgrades if u not in upgrades_to_remove]

async def render(state, tank_image, spider_images, upgrade_images):
    screen.fill(BLACK)
    draw_cannon(state.tank_x, state.tank_y, state.cannon_barrels, tank_image)
    for bullet in state.bullets:
        pygame.draw.rect(screen, WHITE, (bullet[0], bullet[1], 5, 10))
    for spider in state.spiders:
        draw_spider(spider[0], spider[1], spider[2], spider_images)
    for upgrade in state.upgrades:
        draw_upgrade(upgrade[0], upgrade[1], upgrade[2], upgrade_images)

    score_text = font.render(f"Score: {state.score}", True, WHITE)
    lives_text = font.render(f"Lives: {state.lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))
    draw_cannon_stats(state.fire_rate, state.bullet_speed, state.cannon_barrels, state.cannon_speed)

    pygame.display.flip()

async def play_game():
    state = GameState()
    try:
        tank_image, spider_images, bomb_image, bulletspeed_upgrade_image, tankspeed_upgrade_image, cannon_upgrade_image, firingrate_upgrade_image = await load_assets()
        upgrade_images = {
            "bomb": bomb_image, "bulletspeed": bulletspeed_upgrade_image, "tankspeed": tankspeed_upgrade_image,
            "cannon": cannon_upgrade_image, "firingrate": firingrate_upgrade_image
        }
        # Load sound effects
        shoot_sound = pygame.mixer.Sound(SHOOT_SOUND)
        spider_hit_sound = pygame.mixer.Sound(SPIDER_HIT_SOUND)
        upgrade_hit_sound = pygame.mixer.Sound(UPGRADE_HIT_SOUND)
        bomb_hit_sound = pygame.mixer.Sound(BOMB_HIT_SOUND)
    except Exception as e:
        logging.error(f"Failed to load assets or sounds: {e}. Using fallback graphics and no sound.")
        tank_image = pygame.Surface((40, 50))
        tank_image.fill(BLUE)
        spider_images = [pygame.Surface((40, 40)) for _ in range(3)]
        for img in spider_images:
            img.fill(RED)
        upgrade_images = {
            key: pygame.Surface((30, 30)) for key in ["bomb", "bulletspeed", "tankspeed", "cannon", "firingrate"]
        }
        for img in upgrade_images.values():
            img.fill(YELLOW)
        # Fallback: Silent sounds (no-op functions)
        class SilentSound:
            def play(self):
                pass
        shoot_sound = SilentSound()
        spider_hit_sound = SilentSound()
        upgrade_hit_sound = SilentSound()
        bomb_hit_sound = SilentSound()

    running = True
    while running:
        await asyncio.sleep(1/60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        await handle_input(state, pygame.key.get_pressed(), shoot_sound)
        await update_entities(state)
        await handle_collisions(state, spider_hit_sound, upgrade_hit_sound, bomb_hit_sound)
        await render(state, tank_image, spider_images, upgrade_images)
        clock.tick(60)

        if state.lives <= 0:
            running = False

    high_scores = await update_high_scores(state.score)
    return await show_high_scores(high_scores, state.score)

async def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Starting Spider Attack game...")
    await show_start_screen()
    play_again = True
    while play_again:
        play_again = await play_game()
    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())