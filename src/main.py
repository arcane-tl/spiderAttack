import pygame
import random
import json
import os
import asyncio
import logging

# Initialize Pygame (synchronous, but needed initially)
pygame.init()

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

# Load tank, spider, bomb, and upgrade images asynchronously (simulated)
async def load_assets():
    try:
        await asyncio.sleep(0.1)  # Non-blocking delay to simulate async loading
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

# Load high scores (async I/O simulation)
async def load_high_scores():
    if os.path.exists(SCORE_FILE):
        await asyncio.sleep(0.1)  # Simulate async I/O
        with open(SCORE_FILE, "r") as f:
            return json.load(f)
    return [{"name": "Player", "score": 0}] * 10

# Save high scores (async I/O simulation)
async def save_high_scores(scores):
    await asyncio.sleep(0.1)  # Simulate async I/O
    with open(SCORE_FILE, "w") as f:
        json.dump(scores, f)

# Get player name (async simulation)
async def get_player_name():
    name = ""
    input_active = True
    while input_active:
        await asyncio.sleep(0.01)  # Non-blocking delay for event loop
        for event in pygame.event.get():  # Synchronous loop, wrapped in async
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
        clock.tick(30)
    return name

# Update high scores (async simulation)
async def update_high_scores(final_score):
    scores = await load_high_scores()
    if final_score > scores[-1]["score"]:
        name = await get_player_name()
        scores.append({"name": name, "score": final_score})
        scores.sort(key=lambda x: x["score"], reverse=True)
        scores = scores[:10]
        await save_high_scores(scores)
    return scores

# Display start screen (async simulation)
async def show_start_screen():
    try:
        background = pygame.image.load(START_BACKGROUND).convert()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    except pygame.error:
        logging.error(f"Error loading start background image from {START_BACKGROUND}. Using black background.")
        background = pygame.Surface((WIDTH, HEIGHT))
        background.fill(BLACK)

    while True:
        await asyncio.sleep(0.01)  # Non-blocking delay
        screen.blit(background, (0, 0))
        
        # Create a semi-transparent overlay for better text readability
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))

        title = font.render("Spider Attack", True, WHITE)
        prompt = font.render("Press Space to Start", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 + 10))

        pygame.display.flip()

        for event in pygame.event.get():  # Synchronous loop, wrapped in async
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

        clock.tick(30)

# Display high scores (async simulation)
async def show_high_scores(scores, final_score):
    try:
        background = pygame.image.load(HIGH_SCORE_BACKGROUND).convert()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    except pygame.error:
        logging.error(f"Error loading high score background image from {HIGH_SCORE_BACKGROUND}. Using black background.")
        background = pygame.Surface((WIDTH, HEIGHT))
        background.fill(BLACK)

    while True:
        await asyncio.sleep(0.01)  # Non-blocking delay
        screen.blit(background, (0, 0))
        
        # Create a semi-transparent overlay for better text readability
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

        for event in pygame.event.get():  # Synchronous loop, wrapped in async
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                if event.key == pygame.K_q:
                    return False

        clock.tick(30)

# Draw cannon with single image (remains synchronous but called in async context)
def draw_cannon(x, y, barrels, tank_image):
    screen.blit(tank_image, (x, y - 30))

# Draw spider with random image (remains synchronous but called in async context)
def draw_spider(x, y, image_index, spider_images):
    screen.blit(spider_images[image_index], (x, y))

# Draw cannon stats (remains synchronous but called in async context)
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

# Draw upgrades (remains synchronous but called in async context)
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

# Main game function (async)
async def play_game():
    tank_x = WIDTH // 2 - 20
    tank_y = HEIGHT - 40
    base_cannon_speed = 8
    cannon_speed = base_cannon_speed
    cannon_barrels = 1
    bullet_speed = 7
    bullets = []
    fire_rate = 20
    fire_counter = 0
    spider_speed = 3
    spiders = []  # Store spiders as [x, y, image_index]
    upgrades = []
    upgrade_types = ["fire_rate", "bullet_speed", "extra_barrel", "clear_spiders", "cannon_speed"]
    score = 0
    lives = 3
    spider_spawn_counter = 0
    upgrade_spawn_counter = 0

    # Load assets asynchronously
    tank_image, spider_images, bomb_image, bulletspeed_upgrade_image, tankspeed_upgrade_image, cannon_upgrade_image, firingrate_upgrade_image = await load_assets()
    upgrade_images = {
        "bomb": bomb_image,
        "bulletspeed": bulletspeed_upgrade_image,
        "tankspeed": tankspeed_upgrade_image,
        "cannon": cannon_upgrade_image,
        "firingrate": firingrate_upgrade_image
    }

    running = True
    while running:
        await asyncio.sleep(0.01)  # Non-blocking delay to yield to the event loop

        # Handle events synchronously within async context
        events = pygame.event.get()  # Get events as a list
        for event in events:  # Use synchronous for loop
            if event.type == pygame.QUIT:
                running = False
                return False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and tank_x > 0:
            tank_x -= cannon_speed
        if keys[pygame.K_RIGHT] and tank_x < WIDTH - 40:
            tank_x += cannon_speed

        fire_counter += 1
        if keys[pygame.K_SPACE] and fire_counter >= fire_rate:
            barrel_offset = 40 // (cannon_barrels + 1)
            for i in range(cannon_barrels):
                bullet_x = tank_x + barrel_offset * (i + 1) - 2.5
                bullets.append([bullet_x, tank_y - 30])
            fire_counter = 0

        # Spider spawning with async delay
        spider_spawn_counter += 1
        if spider_spawn_counter >= 60:
            spiders.append([random.randint(0, WIDTH - 40), -40, random.randint(0, 2)])
            spider_spawn_counter = 0
            await asyncio.sleep(0)  # Yield to prevent blocking

        # Upgrade spawning with async delay
        upgrade_spawn_counter += 1
        if upgrade_spawn_counter >= 300:
            upgrades.append([random.randint(0, WIDTH - 30), -30, random.choice(upgrade_types)])
            upgrade_spawn_counter = 0
            await asyncio.sleep(0)  # Yield to prevent blocking

        # Update bullets
        for bullet in bullets[:]:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)

        # Update spiders
        for spider in spiders[:]:
            spider[1] += spider_speed
            if spider[1] > HEIGHT:
                spiders.remove(spider)
                lives -= 1
                if lives <= 0:
                    running = False

        # Update upgrades
        for upgrade in upgrades[:]:
            upgrade[1] += 2
            if upgrade[1] > HEIGHT:
                upgrades.remove(upgrade)

        # Handle collisions (remains synchronous but wrapped in async context)
        for bullet in bullets[:]:
            bullet_rect = pygame.Rect(bullet[0], bullet[1], 5, 10)
            for spider in spiders[:]:
                spider_rect = pygame.Rect(spider[0], spider[1], 40, 40)
                if bullet_rect.colliderect(spider_rect):
                    bullets.remove(bullet)
                    spiders.remove(spider)
                    score += 10
                    break
            for upgrade in upgrades[:]:
                upgrade_rect = pygame.Rect(upgrade[0], upgrade[1], 30, 30)
                if bullet_rect.colliderect(upgrade_rect):
                    bullets.remove(bullet)
                    if upgrade[2] == "fire_rate" and fire_rate > 10:
                        fire_rate -= 5
                    elif upgrade[2] == "bullet_speed" and bullet_speed < 11:
                        bullet_speed += 2
                    elif upgrade[2] == "extra_barrel" and cannon_barrels < 3:
                        cannon_barrels += 1
                    elif upgrade[2] == "clear_spiders":
                        # Collect all visible upgrades before clearing spiders
                        collected_upgrades = []
                        for other_upgrade in upgrades[:]:
                            if other_upgrade != upgrade:  # Skip the bomb itself
                                collected_upgrades.append(other_upgrade[2])
                        
                        # Apply each collected upgrade
                        for up_type in collected_upgrades:
                            if up_type == "fire_rate" and fire_rate > 10:
                                fire_rate -= 5
                            elif up_type == "bullet_speed" and bullet_speed < 11:
                                bullet_speed += 2
                            elif up_type == "extra_barrel" and cannon_barrels < 3:
                                cannon_barrels += 1
                            elif up_type == "cannon_speed" and cannon_speed < base_cannon_speed * 3:
                                cannon_speed += base_cannon_speed

                        # Clear all spiders and award double points
                        spider_count = len(spiders)
                        spiders.clear()
                        score += spider_count * 20
                    elif upgrade[2] == "cannon_speed" and cannon_speed < base_cannon_speed * 3:
                        cannon_speed += base_cannon_speed
                    upgrades.remove(upgrade)
                    break

        # Draw everything (synchronous, but wrapped in async context)
        screen.fill(BLACK)
        draw_cannon(tank_x, tank_y, cannon_barrels, tank_image)
        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, (bullet[0], bullet[1], 5, 10))
        for spider in spiders:
            draw_spider(spider[0], spider[1], spider[2], spider_images)
        for upgrade in upgrades:
            draw_upgrade(upgrade[0], upgrade[1], upgrade[2], upgrade_images)

        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))

        draw_cannon_stats(fire_rate, bullet_speed, cannon_barrels, cannon_speed)

        pygame.display.flip()
        clock.tick(60)

    high_scores = await update_high_scores(score)
    return await show_high_scores(high_scores, score)

# Main async loop
async def main():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    logger.debug("Starting Spider Attack game...")
    await show_start_screen()
    play_again = True
    while play_again:
        play_again = await play_game()

    pygame.quit()

# Run the async main function for WebAssembly
if __name__ == "__main__":
    asyncio.run(main())