import pygame
import read_data as rd
import pandas as pd

# Lue kevennetty data CSV-tiedostosta
node3200 = rd.read_csv_raw("./data/node3200.kevennetty.csv")
DATEMIN = node3200.index.min()
DATEMAX = node3200.index.max()

# Muutamia karttapohjan sovitukseen liittyviä muuttujia
x_offset = 112  # 112 # x offset  # Sovita leveyssuunnassa - tämä riippuu paikannusjärjestelmän asennusparametreista
y_offset = 27  # 27 # y offset  # Sovita korkeussuunnassa - tämä riippuu paikannusjärjestelmän asennusparametreista
x_max = 1076;  # node_x_max = 10406 # kaupan leveys senttimetreinä
y_max = 563;  # node_y_max = 5220   # kaupan korkeus senttimetreinä
x_scale = 1166/10406    # Suhteutetaan kuvan koko reaalimaaliman dimensioihin
y_scale = 563/5220      # Suhteutetaan kuvan koko reaalimaaliman dimensioihin

raakadata = list(zip(node3200['x']*x_scale+x_offset, node3200['y']*y_scale+y_offset))


pisteet = [tupla for tupla in raakadata if tupla[0] > 160]

# Alusta Pygame
pygame.init()

# Määritä näyttötila
DISPLAY_WIDTH = 1400
DISPLAY_HEIGHT = 800
FPS = 10    # how many times per second we update the screen
display_surface = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption('Plottailua')

# Lataa kuva
image = pygame.image.load('kauppa.jpg')

# Aseta kuvan sijainti
image_x = 0
image_y = 0

# Luo kello-olio FPS-laskurin päivittämistä varten
clock = pygame.time.Clock()

def draw():
    [(pygame.draw.circle(display_surface, (255, 0, 0), piste, 2)) for piste in pisteet]

def animation(datapoint: int):
    [(pygame.draw.circle(display_surface, (255, 0, 0), piste, 2)) for piste in pisteet[:datapoint]]

# Pääsilmukka
running = True
coords = []
counter = 0
plot_all = False
animate = False
while running:
    counter += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            match (event.key):
                case pygame.K_q:
                    print("Quit game")
                    pygame.quit()
                case pygame.K_c:
                    print("Clear all coordinates")
                    coords.clear()
                case pygame.K_UP:
                    FPS += 5
                case pygame.K_DOWN:
                    FPS -= 5
                case pygame.K_r:
                    plot_all = not plot_all
                    animate = False
                    print("Plot all points")
                case pygame.K_a:
                    counter = 0
                    plot_all = False
                    animate = True
                    print("Animate")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Tarkista, onko klikattu hiiren vasenta painiketta
            if event.button == 1:
                # Tulosta hiiren koordinaatit
                coords.append(event.pos)
                print(f'Hiiren klikkaus koordinaateissa: {event.pos}')

    display_surface.fill((255, 255, 255))

    # Piirrä kuva näytölle
    display_surface.blit(image, (image_x, image_y))

    # Tarkista halutaanko plotata kaikki pisteet tai animoida kärryjen liikettä
    if plot_all:
        draw()
    if animate:
        counter+=1
        animation(counter)

    # Piirrä hiiren klikkauskohdan koordinaatit kuvaan
    font = pygame.font.SysFont(None, 24)
    text = font.render(f'{pygame.mouse.get_pos()}', True, (255, 0, 0))
    display_surface.blit(text, pygame.mouse.get_pos())
    if(coords):
        for point in coords:
                text = font.render(f'{point}', True, (255, 0, 0))
                display_surface.blit(text, point)
                pygame.draw.circle(display_surface, (255, 0, 0), point, 2)

    # Päivitä FPS-lukema
    if FPS < 1:
        FPS = 5
    elif FPS > 100:
        FPS = 100

    # Näytä ohjeet
    DATES = font.render(f'DATEMIN: {DATEMIN}\nDATEMAX: {DATEMAX}', True, (0, 0, 125))
    COMMANDS = font.render(f'Q = Quit \nA = Animate \nR = Plot all \nUP and DOWN arrows: adjust FPS {FPS}', True, (0, 0, 125))
    display_surface.blit(DATES, (20, 650))
    display_surface.blit(COMMANDS, (20, 700))

    # Päivitä näyttö
    pygame.display.update()

    # Rajoita FPS
    clock.tick(FPS)

# Lopeta Pygame
pygame.quit()
