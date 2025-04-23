# main.py

import pygame
import random
from logic.neuron import Neuron
from logic.synapse import Synapse
from graphics.renderer import Renderer, WIDTH, HEIGHT
from logic.precision import EPSILON

# Inizializza Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neural Cluster Visualizer")
clock = pygame.time.Clock()

# Plotting statistics

import matplotlib.pyplot as plt
activity_log = []  # lista che conterrà il numero di neuroni attivi a ogni frame

# Neuron settings
stats = {
    "total_count": 4096,        # numero totale di neuroni
    "max_connections": 32,      # numero massimo di sinapsi per neurone
    "max_steps": 10000,         # numero di cicli temporali
    "step_per_second": 0,       # 0 = max FPS
    "inputs_frequency": 1,      # stimola un neurone ogni 1 frame
    "verbose": False,           # True = mostra potenziale, soglia, funzione di attivazione e neuroni come cerchi
    "show_connections": False,  # True = mostra le connessioni
    "hide_ui": True,            # True = nasconde la UI (performance)
    "firing_count": 0,          # numero di neuroni attivi (non modificare, serve per plotting)
    "frame": 0                  # numero di frame (non modificare)
}

# Crea neuroni e connessioni
neurons = []
for _ in range(stats["total_count"]):
    pos = (random.randint(24, WIDTH - 24), random.randint(24, HEIGHT - 24))
    neurons.append(Neuron(pos))

# Crea sinapsi random tra neuroni (escludendo se stessi)
for i, neuron in enumerate(neurons):
    targets = random.sample([n for j, n in enumerate(neurons) if j != i], k=random.randint(1, stats["max_connections"]))
    for target in targets:
        syn = Synapse(target)
        neuron.cluster.add_synapse(syn)

# Inizializza renderer grafico
renderer = Renderer(screen)

# Simulazione
running = True
while running and stats["frame"] < stats["max_steps"]:
    if stats["step_per_second"] > 0:
        clock.tick(stats["step_per_second"])         # FPS
    stats["firing_count"] = 0

    # Gestione eventi
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Stimola n1 ogni 2 secondi circa
    if stats["frame"] % stats["inputs_frequency"] == 0:
        neuron = random.choice(neurons)
        neuron.potential = min(1, max(0, neuron.potential + random.uniform(EPSILON, 1 - EPSILON)))

    # Tick logico dei neuroni
    for n in neurons:
        n.step(stats)

    # Tick logico dei neuroni
    activity_log.append(stats["firing_count"] / len(neurons))

    # Disegna
    renderer.render(neurons, stats)
    stats["frame"] += 1

pygame.quit()

plt.figure(figsize=(12, 4))
plt.plot(activity_log, label="Percentuale neuroni attivi")
plt.xlabel("Ciclo temporale (frame)")
plt.ylabel("Attività media")
plt.ylim(0, max(activity_log) * 1.1)
plt.xlim(0, stats["frame"])
plt.grid(True)
plt.legend()
plt.show()