# logic/neuron.py

import random
from logic.activation import activation_functions

from logic.synapse import SynapsisCluster
from logic.activation import apply_activation
from logic.precision import EPSILON, arctan_quadratic

class Neuron:
    def __init__(self, pos):
        self.pos = pos
        self.potential = EPSILON
        self.threshold = random.uniform(EPSILON, 1-EPSILON)
        self.incoming_signals = []
        self.cluster = SynapsisCluster(self)
        self.activation_function = random.choice(activation_functions)
        self.is_firing = False

    def receive_input(self, value):
        self.incoming_signals.append(value)

    def integrate_inputs(self):
        self.potential += sum(self.incoming_signals)
        self.incoming_signals.clear()

    def step(self, stats):
        self.is_firing = False
        self.weaken()
        self.integrate_inputs()

        if len(self.cluster.synapses) > 0:
            self.is_firing = apply_activation(self, self.activation_function)
            if self.is_firing:
                self.is_firing = True
                self.cluster.propagate()
                self.reinforce()

                # log activity
                stats["firing_count"] += 1

    def reinforce(self):
        p_del = self.potential - self.threshold
        t_sat = self.potential
        self.potential = arctan_quadratic(p_del)      # leave residual potential
        self.threshold = arctan_quadratic(t_sat)
        self.cluster.reinforce(t_sat)

    def weaken(self):
        self.threshold *= (1-EPSILON)       # decay threshold
        self.potential *= (1-EPSILON)       # decay potential
        self.cluster.weaken()
