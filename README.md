# 🧠 Neurons-BOH

Simulation of a self-organizing neural network based on synaptic clusters and discrete logical functions.  
Each neuron has a potential, a threshold, and an output composed of a **SynapsisCluster** that branches out to other neurons.  
The system evolves autonomously in real time, visualizing activations and connections.

---

## 🔧 Requirements

- Python 3.10+
- `pygame`
- `matplotlib`

Install the required packages with:

```bash
pip install -r requirements.txt
```

## ▶️ Run

To launch the simulation:

```bash
python main.py
```

## 👁️‍🗨️ UI Overview

- **Neurons**: colored circles
  - Color intensity reflects the neuron's internal potential
  - The number inside each circle displays the neuron's current potential (`0.00` to `1.00`)
  - Above each neuron, the name of the activation function is shown (`AND`, `OR`, `XOR`) - not used 

- **Connections**: directional arrows
  - Represent synaptic links from one neuron to others via SynapsisClusters
  - Arrows are centered along the connection lines to avoid overlap with neuron bodies

- **Layout**: neurons are randomly positioned within the window
  - Scales well up to 256 neurons
  - Visual updates occur in real time and reflect changes in firing activity

---

## 📈 Analytical Output

After closing the graphical window, a plot will appear showing:

- The **percentage of active neurons per frame**
- Useful for detecting long-term stability, oscillatory behavior, or emergent bursts

---

## ⚙️ Technical Details

- Potentials and thresholds evolve using a stabilizing nonlinear function (`arctan_quadratic`)
- Synapses reinforce or weaken depending on signal propagation effectiveness
- The simulation can run at **maximum speed**, independent of a fixed framerate
- Scalable to **millions of cycles** and large topologies without loss of performance

---

## 🧪 Goal

To explore spontaneous pattern formation in minimal, biologically-inspired neural systems  
→ *Self-organization without explicit rules or hardcoded logic*

---

## 📄 License

MIT — free to use, modify, and experiment with.
