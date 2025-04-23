# logic/synapse.py

from logic.precision import EPSILON, arctan_quadratic

class Synapse:
    def __init__(self, target_neuron, w=1-EPSILON):
        self.target = target_neuron
        self.w = w

    def transmit(self, signal_w, total_cluster_w):
        if total_cluster_w == 0:
            return
        signal = signal_w * (self.w / total_cluster_w)
        self.target.receive_input(signal)

    def reinforce(self, amount=EPSILON):
        w_sat = min(1, max(0, self.w + amount))
        self.w = arctan_quadratic(w_sat)

    def weaken(self, amount=EPSILON):
        self.w *= (1 - amount)
        if self.w < EPSILON:
            self.w = 0

class SynapsisCluster:
    def __init__(self, origin_neuron, w=1-EPSILON):
        self.origin = origin_neuron
        self.synapses = []
        self.w = w

    def add_synapse(self, synapse):
        try:
            if synapse.target == self.origin:
                raise ValueError("Cannot create a synapse to itself")   # self is not a valid target
            if synapse.target in [s.target for s in self.synapses]:
                raise ValueError("Synapse already exists")              # synapse already exists
            if self.origin in [s.target for s in synapse.target.cluster.synapses]:
                raise ValueError("Circular synapse")                   # circular synapse
            self.synapses.append(synapse)
        except ValueError:
            pass

    def total_w(self):
        return max(EPSILON, sum(s.w for s in self.synapses) + self.w)

    def propagate(self):
        a = self.origin.potential  # float
        tw = self.total_w()
        for synapse in self.synapses:
            synapse.transmit(a, tw)

    def reinforce(self, amount=EPSILON):
        w_sat = min(1, max(0, self.w + amount))
        self.w = arctan_quadratic(w_sat)
        for synapse in self.synapses:
            synapse.reinforce(amount)

    def weaken(self, amount=EPSILON):
        self.w *= (1 - amount)
        for synapse in self.synapses:
            synapse.weaken(amount)
