import pygame
import random
import math
import sys

pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 950, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Autonomous Cars — Genetic Algorithm Evolution")
clock = pygame.time.Clock()

# Couleurs (Thème Tech & Néon)
DARK_BG = (15, 18, 25)
WALL_COLOR = (255, 75, 75)     # Murs en rouge vif (danger)
TRACK_COLOR = (40, 50, 70)     # Route praticable en gris-bleu
CAR_COLOR = (0, 255, 157)      # Voitures en vert néon
BEST_CAR_COLOR = (255, 215, 0) # Or pour la meilleure voiture
WHITE = (255, 255, 255)
GRAY = (120, 130, 150)

# Polices
font_medium = pygame.font.SysFont("Arial", 20, bold=True)
font_small = pygame.font.SysFont("Arial", 15)

class Car:
    def __init__(self, brain=None):
        self.x = 150
        self.y = 520
        self.angle = -math.pi / 2
        self.speed = 0.0
        self.max_speed = 5.0
        self.alive = True
        self.fitness = 0
        
        # Cerveau (Poids synaptiques : 3 capteurs -> 2 commandes [virage, accélération])
        if brain:
            # Mutation des poids du parent
            self.brain = [w + random.gauss(0, 0.25) for w in brain]
        else:
            self.brain = [random.uniform(-1, 1) for _ in range(7)]

    def update(self, track_mask):
        if not self.alive:
            return

        # 1. Lire les 3 capteurs (Avant, Avant-Gauche, Avant-Droite)
        sensor_readings = self.get_sensors(track_mask)

        # 2. Réseau de neurones simple
        steer_input = (sensor_readings[1] - sensor_readings[2]) * 0.05
        accel_input = sensor_readings[0] * 0.05

        steer = steer_input * self.brain[0] + accel_input * self.brain[1] + self.brain[2]
        accel = accel_input * self.brain[3] + self.brain[4]

        self.angle += steer * 0.08
        self.speed = max(1.5, min(self.max_speed, self.speed + accel * 0.2))

        # Mouvement
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

        # Fitness (score basé sur la distance parcourue)
        self.fitness += self.speed

        # Vérifier les collisions avec les bords de l'écran ou les murs
        if not (0 <= int(self.x) < WIDTH and 0 <= int(self.y) < HEIGHT):
            self.alive = False
            return
            
        # Si la voiture touche un mur (couleur WALL_COLOR)
        color_at_pos = track_mask.get_at((int(self.x), int(self.y)))
        if color_at_pos[0] > 200 and color_at_pos[1] < 100: # Détection du mur rouge
            self.alive = False

    def get_sensors(self, track_mask):
        readings = []
        angles = [self.angle, self.angle - 0.6, self.angle + 0.6]
        
        for a in angles:
            dist = 0
            max_dist = 70
            while dist < max_dist:
                sx = int(self.x + math.cos(a) * dist)
                sy = int(self.y + math.sin(a) * dist)
                if not (0 <= sx < WIDTH and 0 <= sy < HEIGHT):
                    break
                # Si le rayon touche un mur
                col = track_mask.get_at((sx, sy))
                if col[0] > 200 and col[1] < 100:
                    break
                dist += 5
            readings.append(dist / max_dist)
        return readings

    def draw(self, surface, is_best=False):
        if not self.alive:
            return
        color = BEST_CAR_COLOR if is_best else CAR_COLOR
        car_surf = pygame.Surface((16, 10), pygame.SRCALPHA)
        pygame.draw.rect(car_surf, color, (0, 0, 16, 10), border_radius=3)
        
        rotated_surf = pygame.transform.rotate(car_surf, -math.degrees(self.angle))
        new_rect = rotated_surf.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(rotated_surf, new_rect.topleft)

# --- CRÉATION DU CIRCUIT DE TEST ---
def create_track_surface():
    surf = pygame.Surface((WIDTH, HEIGHT))
    # Fond = Mur rouge
    surf.fill(WALL_COLOR)
    
    # Route sécurisée (creusée au milieu)
    pygame.draw.rect(surf, TRACK_COLOR, (60, 60, WIDTH - 120, HEIGHT - 120), border_radius=80)
    # Îlot central (mur rouge au milieu)
    pygame.draw.rect(surf, WALL_COLOR, (220, 180, WIDTH - 440, HEIGHT - 360), border_radius=60)
    
    return surf

track_surface = create_track_surface()

# Paramètres de l'algorithme génétique
POPULATION_SIZE = 40
generation = 1
cars = [Car() for _ in range(POPULATION_SIZE)]

def next_generation():
    global cars, generation
    cars.sort(key=lambda c: c.fitness, reverse=True)
    
    # Garder les 3 meilleures voitures (Elitisme)
    best_brains = [car.brain for car in cars[:3]]
    
    new_cars = [Car(best_brains[0])] # Conserver la meilleure directement
    
    while len(new_cars) < POPULATION_SIZE:
        parent_brain = random.choice(best_brains)
        new_cars.append(Car(parent_brain))
        
    generation += 1
    return new_cars

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                generation = 1
                cars = [Car() for _ in range(POPULATION_SIZE)]

    # Mettre à jour toutes les voitures
    alive_count = 0
    for car in cars:
        car.update(track_surface)
        if car.alive:
            alive_count += 1

    # Si toutes les voitures sont mortes, passer à la génération suivante
    if alive_count == 0:
        cars = next_generation()

    # Trouver la meilleure voiture actuelle
    best_car = max(cars, key=lambda c: c.fitness)

    # --- RENDU GRAPHIQUE ---
    screen.fill(DARK_BG)
    screen.blit(track_surface, (0, 0))

    # Dessiner les voitures
    for car in cars:
        if car != best_car:
            car.draw(screen, is_best=False)
    best_car.draw(screen, is_best=True)

    # --- HUD ET STATISTIQUES ---
    title_txt = font_medium.render("IA & ALGORITHME GÉNÉTIQUE — VOITURES AUTONOMES", True, WHITE)
    screen.blit(title_txt, (WIDTH // 2 - title_txt.get_width() // 2, 12))

    stats_txt = font_small.render(f"Génération : {generation} | Voitures en vie : {alive_count} / {POPULATION_SIZE}", True, CAR_COLOR)
    screen.blit(stats_txt, (35, 20))

    inst_txt = font_small.render("L'IA apprend par évolution | R : Réinitialiser", True, GRAY)
    screen.blit(inst_txt, (WIDTH - inst_txt.get_width() - 35, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()