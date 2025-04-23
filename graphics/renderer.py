import pygame
import math
from logic.precision import EPSILON

WIDTH, HEIGHT = 80, 80

class Renderer:
    def __init__(self, screen, neuron_radius=24):
        self.screen = screen
        self.neuron_radius = neuron_radius
        self.font = pygame.font.SysFont(None, 16)

    def draw_neurons(self, neurons, stats):
        for i, neuron in enumerate(neurons):
            intensity = int(min(255, 255 * neuron.potential / neuron.threshold + EPSILON))

            # Potenziale del neurone
            if not stats["verbose"]:
                pygame.draw.rect(self.screen, (intensity, 0, 0), (neuron.pos[0]-1, neuron.pos[1]-1, 2, 2), 1)
                continue
            else:
                pygame.draw.circle(self.screen, (intensity,0,0), neuron.pos, self.neuron_radius)

            # Attivazione del neurone
            pygame.draw.circle(self.screen, (255, 0, 0) if neuron.is_firing else 0, neuron.pos, self.neuron_radius, 2)

            # Testo del potenziale
            potential_text = self.font.render(f"{neuron.potential:.4f}", True, (255,255,255))
            potential_rect = potential_text.get_rect(center=neuron.pos)
            self.screen.blit(potential_text, potential_rect)

            # Testo del threshold
            threshold_text = self.font.render(f"{neuron.threshold:.3f}", True, (255,255,255))
            threshold_rect = threshold_text.get_rect(center=(neuron.pos[0], neuron.pos[1] + 12))
            self.screen.blit(threshold_text, threshold_rect)

            # Testo della funzione di attivazione
            activation_text = self.font.render(f"{neuron.activation_function.display_name}", True, (255,255,255))
            activation_rect = activation_text.get_rect(center=(neuron.pos[0], neuron.pos[1] - 12))
            self.screen.blit(activation_text, activation_rect)

    def draw_connections(self, neurons):
        for i, neuron in enumerate(neurons):
            for synapse in neuron.cluster.synapses:
                try:
                    self.draw_arrow(neuron.pos, synapse.target.pos)
                except ValueError:
                    continue

    def draw_arrow(self, start, end, color=(150, 150, 150), width=1, arrow_size=8):
        pygame.draw.line(self.screen, color, start, end, width)

        # Calcola direzione e angolo
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        mid = ((start[0] + end[0]) // 2, (start[1] + end[1]) // 2)
        angle = math.atan2(dy, dx)

        # Crea la punta della freccia (due segmenti)
        arrow_angle = math.radians(30)
        left = (
            mid[0] - arrow_size * math.cos(angle - arrow_angle),
            mid[1] - arrow_size * math.sin(angle - arrow_angle)
        )
        right = (
            mid[0] - arrow_size * math.cos(angle + arrow_angle),
            mid[1] - arrow_size * math.sin(angle + arrow_angle)
        )

        pygame.draw.line(self.screen, color, mid, left, width)
        pygame.draw.line(self.screen, color, mid, right, width)

    def draw_info(self, frame):
        # Draw the information box
        info_box = pygame.Surface((WIDTH, 18))
        info_box.fill((0, 0, 0))
        self.screen.blit(info_box, (0, 0))

        # Draw the text
        text = self.font.render(f"Step: {frame}", True, (255, 255, 255))
        self.screen.blit(text, (4, 4))

    def render(self, neurons, stats):
        self.screen.fill((255, 255, 255))
        self.draw_info(stats["frame"])

        if not stats["hide_ui"]:
            if stats["show_connections"]:
                self.draw_connections(neurons)
            self.draw_neurons(neurons, stats)

        pygame.display.flip()
