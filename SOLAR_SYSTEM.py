import pygame
import sys

# ─── Data ──────────────────────────────────────────────────────────────────────
Planets = {
    "Mercury": (2439.7,   57.9,   (169, 169, 169)),
    "Venus":   (6051.8,  108.2,   (218, 165,  32)),
    "Earth":   (6371.0,  149.6,   (  0, 102, 204)),
    "Mars":    (3389.5,  227.9,   (188,  39,  50)),
    "Jupiter": (69911.0, 778.6,   (255, 165,   0)),
    "Saturn":  (58232.0,1433.5,   (210, 180, 140)),
    "Uranus":  (25362.0,2872.5,   (173, 216, 230)),
    "Neptune": (24622.0,4495.1,   (  0,   0, 128)),
}

Moons = {
    "Moon":      (1737.4,   0.384,   (200, 200, 200), "Earth"),
    "Phobos":    ( 11.267,  0.009,   (169, 169, 169), "Mars"),
    "Deimos":    (  6.2,    0.023,   (211, 211, 211), "Mars"),
    "Io":        (1821.6,   0.422,   (218, 165,  32), "Jupiter"),
    "Europa":    (1560.8,   0.671,   (245, 245, 245), "Jupiter"),
    "Ganymede":  (2634.1,   1.070,   (192, 192, 192), "Jupiter"),
    "Callisto":  (2410.3,   1.882,   (169, 169, 169), "Jupiter"),
    "Titan":     (2575.5,   1.221,   (255, 228, 181), "Saturn"),
    "Rhea":      ( 764.3,   0.527,   (211, 211, 211), "Saturn"),
    "Iapetus":   ( 734.5,   3.561,   (240, 230, 140), "Saturn"),
    "Enceladus": ( 252.1,   0.238,   (245, 245, 245), "Saturn"),
    "Titania":   ( 788.9,   0.436,   (173, 216, 230), "Uranus"),
    "Oberon":    ( 761.4,   0.586,   (176, 196, 222), "Uranus"),
    "Ariel":     ( 578.9,   0.191,   (175, 238, 238), "Uranus"),
    "Umbriel":   ( 584.7,   0.266,   (119, 136, 153), "Uranus"),
    "Triton":    (1353.4,   0.355,   (176, 196, 222), "Neptune"),
    "Proteus":   ( 210.0,   0.117,   (169, 169, 169), "Neptune"),
    "Nereid":    ( 170.0,   5.513,   (211, 211, 211), "Neptune"),
    "Larissa":   (  97.0,   0.073,   (190, 190, 190), "Neptune"),
}

SUN_RADIUS_KM = 695700
SUN_COLOR = (255, 255, 0)

# ─── Pygame Setup ───────────────────────────────────────────────────────────────
pygame.init()
WIDTH, HEIGHT = 1920, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("1D Solar System (Proper KM Scale)")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 18)

# ─── Scaling Setup ──────────────────────────────────────────────────────────────
max_dist_km = max(dist_mkm for (_, dist_mkm, _) in Planets.values()) * 1e6
margin = 100
min_scale = (WIDTH - 2 * margin) / max_dist_km  # px/km for full system to fit
scale = min_scale
max_scale = 200000 * min_scale  # allow zooming in

offset_x = margin

# ─── Helpers ─────────────────────────────────────────────────────────────────────
def world_to_screen(dist_mkm):
    return offset_x + dist_mkm * 1e6 * scale  # Convert mkm → km → px

# ─── Interaction State ──────────────────────────────────────────────────────────
dragging = False
last_mouse_x = 0

show_moon_labels = True
show_planet_labels = True
show_sun_label = True

set_minimum_size = False
# ─── Main Loop ───────────────────────────────────────────────────────────────────
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Zooming
        elif event.type == pygame.MOUSEWHEEL:
            mx, _ = pygame.mouse.get_pos()
            world_x_km = (mx - offset_x) / scale
            scale *= 1 + event.y * 0.1
            scale = max(min_scale, min(max_scale, scale))
            offset_x = mx - world_x_km * scale

        # Dragging with mouse
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            dragging = True
            last_mouse_x = event.pos[0]
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            dragging = False

        # Arrow keys
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                offset_x += 50
            elif event.key == pygame.K_RIGHT:
                offset_x -= 50
            elif event.key == pygame.K_m:
                show_moon_labels = not show_moon_labels
            elif event.key == pygame.K_p:
                show_planet_labels = not show_planet_labels
            elif event.key == pygame.K_s:
                show_sun_label = not show_sun_label
            elif event.key == pygame.K_k:
                pygame.image.save(screen, "C:/Users/JEDTL/Desktop/Python/solar_system_snapshot.png")
                print("Snapshot saved as solar_system_snapshot.png")
            elif event.key == pygame.K_o:
                if set_minimum_size:
                    set_minimum_size = False
                    continue 
                if not set_minimum_size:
                    set_minimum_size = True
    if dragging:
        mx = pygame.mouse.get_pos()[0]
        offset_x += (mx - last_mouse_x)
        last_mouse_x = mx

    # ─── Draw ────────────────────────────────────────────────────────────────────
    screen.fill((0, 0, 0))

    # Sun
    sun_x = world_to_screen(0)
    if not set_minimum_size:
        sun_r = max(0, int(SUN_RADIUS_KM * scale))
    else:
        sun_r = max(5, int(SUN_RADIUS_KM * scale))
    pygame.draw.circle(screen, SUN_COLOR, (int(sun_x), HEIGHT // 2), sun_r)
    if show_sun_label:
        screen.blit(font.render("Sun", True, (255, 255, 255)),
                    (sun_x + sun_r + 5, HEIGHT // 2 - sun_r))

    # Planets & Moons
    for pname, (pr_km, pd_mkm, color) in Planets.items():
        x = world_to_screen(pd_mkm)
        if not set_minimum_size:
            r = max(0, int(pr_km * scale))
        if set_minimum_size:
            r = max(2, int(pr_km * scale))
        pygame.draw.circle(screen, color, (int(x), HEIGHT // 2), r)
        if show_planet_labels:
            screen.blit(font.render(pname, True, (255, 255, 255)),
                        (x - r, HEIGHT // 2 + r + 4))

        for mname, (mr_km, md_mkm, mcolor, parent) in Moons.items():
            if parent == pname:
                mx = world_to_screen(pd_mkm + md_mkm)
                if not set_minimum_size:
                    mr = max(0, int(mr_km * scale))
                else:
                    mr = max(2, int(mr_km * scale))
                pygame.draw.circle(screen, mcolor, (int(mx), HEIGHT // 2), mr)
                if show_moon_labels:
                    screen.blit(font.render(mname, True, (200, 200, 200)),
                                (mx - mr, HEIGHT // 2 + mr + 2))

    # ─── Scale Readout ───────────────────────────────────────────────────────────
    scale_text = f"Scale: {scale:.3e} px/km"
    txt = font.render(scale_text, True, (255, 255, 255))
    screen.blit(txt, (WIDTH - txt.get_width() - 10, HEIGHT - txt.get_height() - 5))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
