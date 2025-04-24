# 🧠 Neurons-BOH

### Abstract

**Neurons-BOH** is a simulation of a self-organizing neural system based on clustered synaptic structures and discrete logical activation functions.  
The network evolves autonomously over time, with internal dynamics driven by reinforcement and decay of both neuron thresholds and synaptic weights.

Each neuron possesses a continuous-valued **potential**, a **threshold**, and an output structure called a **SynapsisCluster**, which branches toward other neurons via multiple **Synapsis** (individual synaptic links). This mirrors the biological distinction between axons (single output structure) and dendritic trees (multiple targets).

Unlike classical fully connected neural networks, this model introduces:
- Directional, branching output structures
- Activation functions as boolean logic gates applied to continuous internal states
- Local homeostatic mechanisms that stabilize the system without global rules

The **total effective signal** transmitted through a synaptic connection is computed as:

```math
S = P \cdot \frac{w_i}{\sum_j w_j + W_c}
```

Where:
- **P** – neuron's current potential  
- **W<sub>c</sub>** – cluster strength (SynapsisCluster global weight)  
- **w<sub>i</sub>** – weight of individual synapse  
- **∑w<sub>j</sub>** – sum of all synaptic weights in the cluster  

This formulation ensures signal conservation and gradual saturation of outgoing branches as they proliferate, enforcing an implicit regularization on connection growth.

---

## 🧬 1. Introduction

Biological neural systems do not rely on fully connected architectures, centralized training, or gradient-based optimization.  
Instead, they develop through self-organizing processes, local reinforcement, and adaptive pruning of connections over time.

**Neurons-BOH** is an experimental simulation that explores how complex patterns can emerge from minimalistic and biologically-inspired components:
- neurons that interact through simple logic-based activation functions,
- synaptic clusters that evolve by reinforcement or decay,
- and no global controller or training signal.

This model aims to serve as a testbed for studying **spontaneous structure formation**, **signal propagation**, and **long-term stability** in networks that learn through direct interaction with their own activity.

### 🎯 1.1 Objectives

This system does not pursue a fixed task or goal.  
Its primary objective is to **observe the spontaneous behavior** of the network under varying structural and dynamic conditions.  
In particular, the simulation is used to:

- identify potential **emergent patterns** in activation and connectivity,
- verify whether the network exhibits **self-stabilizing** dynamics over time,
- monitor how structural changes (e.g., synapse creation, reinforcement, or decay) impact global activity,
- explore whether long-term autonomy is possible without external tuning or supervision.

In this framework, **emergent behavior is not programmed**, but expected to arise naturally from the interaction of simple computational elements.

---

## 📐 2. Formal Model

The network is composed of a set of neurons **N = {n<sub>1</sub>, n<sub>2</sub>, ..., n<sub>k</sub>}**, each defined by:

- a potential **P<sub>i</sub>** ∈ [0, 1]
- a threshold **θ<sub>i</sub>** ∈ [0, 1]
- a set of incoming synapses (for receiving input)
- a single SynapsisCluster responsible for outgoing connections

### 🧮 2.1 Synaptic Transmission

Each neuron has a single output structure called a SynapsisCluster, with global strength **W<sub>c</sub>** ∈ [0, 1].  
The cluster contains multiple synapses **S<sub>j</sub>** with individual weights **W<sub>j</sub>** ∈ [0, 1].

When neuron nᵢ fires, it propagates its potential to each connected neuron as:

```math
Sⱼ = Pᵢ \cdot \frac{wⱼ}{\sum_j wⱼ + W_c}
```

Where:
- **P<sub>i</sub>** — current potential of neuron nᵢ  
- **W<sub>c</sub>** — strength of the SynapsisCluster  
- **W<sub>j</sub>** — weight of the individual synapse  
- **∑w<sub>j</sub>** — sum of all synaptic weights in the cluster (∈ [0, N])

This formulation ensures:
- signal conservation
- decay of influence with increasing fan-out
- smooth saturation as connectivity grows

### ⚡ 2.2 Neuron Activation

Each neuron receives input signals **I<sub>i</sub>** and updates its potential as:

```math
P_i ← P_i + \sum_{incoming} S
```

Then, a boolean activation function **f(P<sub>i</sub>, θ<sub>i</sub>)** is applied.  
If the result is True, the neuron fires, propagates its signal, and reinforces itself.

### 🔁 2.3 Reinforcement and Decay

If a neuron fires, internal parameters are updated using a stabilizing nonlinear function:

```math
θ_i ← arcquad(P_i - θ_i)
```
```math
W_c ← arcquad(W_c + δ)
```

If it does **not** fire, decay is applied to all relevant variables:

```math
θ_i ← θ_i · (1 - λ)
```
```math
P_i ← P_i · (1 - λ)
```
```math
w_j ← w_j · (1 - λ)
```

with **λ ∈ ]0, 1[**, and a small **ε > 0** (manually-tuned, typically 10⁻⁴) used to prevent collapse at the interval boundaries of [0, 1].

These dynamics ensure:
- neurons become more or less sensitive over time  
- unused connections weaken and fade  
- activity is sustained only through effective propagation

### 🌀 2.4 Stabilizing Nonlinearity: arcquad

The function `arcquad(x)` is a lightweight, arctangent-inspired nonlinearity used to stabilize neuron thresholds and cluster weights.  
Its purpose is to prevent runaway reinforcement by introducing diminishing returns: as a variable grows, its future increments have less effect.

`arcquad(x)` approximates the behavior of `arctan(x)` but maps smoothly into the [0, 1] interval, with horizontal asymptotes and symmetry around 0.5.

The function is defined as:

```math
arcquad(x) = \frac{2x^2}{(2x - 1)^2 + 1}
```

**Key properties:**
- `arcquad(0)` = 0
- `arcquad(0.5)` = 0.5
- `arcquad(1)` = 1
- Symmetric with respect to `x = 0.5`
- Smooth, continuous, and monotonic for `x ∈ [0, 1]`

![arcquad_plot](https://github.com/user-attachments/assets/e7e43c56-57d1-4796-8392-1711a65636e7)

> **Figure 1 – Plot of the arcquad(x) function in [0, 1].**  
> This function approximates the behavior of `arctan(x)`, but maps smoothly into the [0, 1] interval.  
> It introduces horizontal asymptotes and diminishing returns, enforcing stability and preventing parameter explosion during reinforcement.

---

## 📊 3. Observation

The system exhibits a characteristic dynamic pattern across configurations:  
- a **high activation spike** occurs in the very first steps due to the initial input stimulation
- this is followed by a **self-regulating drop**, converging to low, quasi-stable firing rates
- over time, the network maintains low activity interspersed with **occasional higher spikes**

This behavior strongly suggests the presence of an **internal homeostatic mechanism**, emerging from the interaction between reinforcement, decay, and the structure of the synaptic clusters.

Below is the average neuron activation rate over 1 million frames, recorded from a typical run with 256 neurons:

![Figure_2](https://github.com/user-attachments/assets/66159b65-021c-4a6c-b7a8-37eef1cd0308)

> **Figure 1 – Average neural activity over time.**  
> The system shows a high initial spike in activity, quickly followed by a drop to a lower, stable regime.  
> Spontaneous bursts reappear intermittently, indicating the presence of internal feedback and homeostatic stabilization.

The graph shows:
- initial turbulence (dense activation)
- long-term self-stabilization with sparse but persistent spontaneous bursts

---

## 🛠️ 4. Setup

- Python 3.10+
- `pygame`
- `matplotlib`

Install dependencies with:

```bash
pip install -r requirements.txt
```

---

## ▶️ 5. Run

Launch the simulation with:

```bash
python main.py
```

Upon exit, a plot will automatically be displayed showing activation over time.

---

## 🎚️ 6. Customization

All core simulation parameters are defined directly in `main.py`.  
You can adjust:

- number of neurons
- connection density (range and randomness)
- input frequency and strength
- reinforcement and decay functions
- graphical update rate (or disable UI altogether)

Additional notes:
- The simulation can run at **maximum speed** (just set framerate to zero), independent of a fixed framerate
- It is scalable to **millions of cycles** and large topologies without loss of performance

### 🔬 6.1 Numerical Precision and `EPSILON`

The constant `EPSILON` is defined in `logic/precision.py` and used to avoid edge values of 0 and 1.  
It ensures that:

- neuron potentials and thresholds stay within the open interval ]0, 1[
- synaptic weights do not collapse to zero and remain numerically stable

Typical default:  
```math
EPSILON = 1e-4
```

Adjusting EPSILON affects:
- how aggressively synapses weaken
- how close thresholds can drift toward inactivity
- overall numerical resilience in long simulations

### 🖥️ 6.2 UI Controls

Several UI-related flags can be configured to tailor the visual simulation experience:

- `verbose` (default: `False`)  
  Enables debug printing of internal neuron activity (activation function, potentaial, threshold and firing).

- `show_connections` (default: `True`)  
  Toggles drawing of synaptic arrows between neurons.  
  Useful to reduce clutter or improve performance on large networks.

- `hide_ui` (default: `False`)  
  If set to `True`, disables the runtime rendering except for step count number.
  Neurons will be not longer shown, usefull when dealing with expensive setups.
  Allows headless execution for performance benchmarking or purely analytical runs.

These parameters are set as constants in your `main.py` script, inside `stats` variable.

---

## ✅ 7. Conclusions

**Neurons-BOH** demonstrates that even a simple biologically-inspired system with discrete logic and local learning rules can give rise to:

- persistent activity patterns,
- self-limiting excitation,
- stable yet dynamic connectivity topologies.

These results support the feasibility of designing **emergent, task-free networks** that evolve purely based on internal structure and local interaction — without supervision or global objectives.

---

## 🚀 8. Future Work

This project is designed with extensibility in mind. Next steps may include:

- Implementation of **parallel execution** using `PyTorch` or `NumPy` for GPU-accelerated simulation
- Support for **topological constraints** (e.g. spatial distance, clusters)
- Addition of **plasticity mechanisms** beyond threshold and weight tuning
- Integration with **temporal encoders** for simulating sensor inputs

Due to its modular structure and independence from external training signals, Neurons-BOH could also serve as a component for cognitive models, reinforcement-learning world simulators, or generative memory systems.

---

## 📄 License

MIT — free to use, modify, and experiment with.
