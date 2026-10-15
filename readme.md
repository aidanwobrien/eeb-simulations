# Evolutionary Games

A PySide6 desktop app that houses interactive **ecology and evolutionary biology (EEB) "games"**: small, parametrizable simulations for exploring core concepts in the field. Pick a game from the launcher, set its parameters, run the simulation, and watch the dynamics unfold through live plots and a real-time visualization.

![Game selection screen](docs/launcher.png)

## Games

| Game | Status | Concept |
|------|--------|---------|
| [Lotka-Volterra](#lotka-volterra-population-game) | Available | Predator-prey population dynamics in a spatial, three-tier ecosystem |
| Hawk-Dove | In development | Evolutionary game theory: conflict strategies and evolutionarily stable strategies (ESS) |

More "games" may be added over time.

## Getting Started

### Requirements

- Python 3.10+
- PySide6 (6.9)
- pygame-ce (2.5.6)
- matplotlib (3.10.8)
- numpy (2.2.4)

### Install

```bash
git clone https://github.com/aidanwobrien/eeb-simulations
cd eeb-simulations
pip install -r requirements.txt
```

### Run

```bash
python app.py
```

## Using the App

1. **Select a game** from the list on the left of the launcher. A description of the model and a link to further reading appear on the right.
2. Click **Select** to open that game's simulation window.
3. Adjust parameters, then use the controls to run the simulation:
   - **Run** starts the simulation.
   - **Pause** freezes it so you can inspect the current state.
   - **Stop** ends the run.
4. Watch the results in the live plots and the visualization window.

---

## Lotka-Volterra Population Game

![Lotka-Volterra simulation](docs/lotka_volterra.png)

The Lotka-Volterra (LV) equations are a foundational model in ecology describing how two interacting species, a predator and its prey, change in abundance over time. This simulation implements an agent-based, spatial version of the model and extends it to a three-tiered ecosystem of plants, herbivores and carnivores.

### The World

- A toroidal (wrapping), tile-based isometric grid. The size is configurable (width and height).
- Tiles are either **empty** or **rock**.
  - Empty tiles can contain plants, herbivores and carnivores.
  - Rocks are impassable and are generated with Perlin noise.

### The Model

- The main goal was to build a 3-tiered ecosystem whose populations cycle through time in a stable phase, without any population crashing.
- The classic LV equations ignore space: the populations are effectively "well-mixed" every tick. In this model, movement costs, localized reproduction and impassable rocks introduce clustering, refuges and overall spatiality, and therefore more noise than the classic equations produce.

### The Rules

- Plant tiles produce food (energy).
- Each tick, **herbivores** move one space in a random direction. If they land on a plant tile, they eat it and gain energy. Once eaten, the plant is removed and regenerates after a fixed time (the regeneration rate).
- Each tick, **carnivores** move two spaces toward the closest herbivore. If they are on a tile with a herbivore, they eat it and gain energy. Carnivores must wait two ticks before eating again.
- Herbivores and carnivores **reproduce** when their energy reaches a reproduction threshold, at an energy cost (the reproduction cost). Offspring appear on a random unblocked neighbouring tile. If all neighbours are blocked, the animal does nothing that tick and keeps its energy.
- Herbivores and carnivores **lose energy** every tick (a basal cost) and with each movement (a movement cost).

### Parameters

The parameter panel (scrollable) controls the world and food settings, including:

| Parameter | Description |
|-----------|-------------|
| Initial prey population | Starting number of herbivores |
| Initial predator population | Starting number of carnivores |
| Grid width / height | Size of the world in tiles |
| Frames per generation | Number of rendered frames per simulation tick |

Further parameters (such as energy gains and costs, reproduction threshold and cost, and plant regeneration time) are available further down the panel.

<!-- TODO: list the remaining parameters and their defaults -->

### Visualization

- **Simulation window (pygame):** a real-time isometric view of the world with a live counter of the current time, plants, herbivores and carnivores. Herbivores are drawn in blue and carnivores in red.
- **Time Series plot:** population of plants, herbivores and carnivores against ticks.
- **Phase Plot:** the phase portrait of predator vs. prey abundance, where stable cycling appears as a closed orbit.

<!-- TODO: add screenshots of the Time Series and Phase Plot tabs -->

---

## Hawk-Dove Game

*In development.*

The Hawk-Dove game is a classic model from evolutionary game theory in which individuals compete over a resource using either an aggressive (Hawk) or a passive (Dove) strategy. It will be used to explore how strategy frequencies evolve and when a stable mixed strategy (ESS) emerges.

<!-- TODO: fill in rules, parameters and visualization once implemented -->

## Project Structure

```
.
├── app.py              # App entry point / game launcher
├── games/
│   ├── lotka_volterra/  # Lotka-Volterra simulation
│   └── hawk_dove/       # Hawk-Dove simulation (WIP)
├── docs/                # Screenshots
└── requirements.txt
```

<!-- TODO: update to match your actual layout -->

## Further Reading

- [Lotka-Volterra equations (Wikipedia)](https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations)
- [Hawk-dove game (Wikipedia)](https://en.wikipedia.org/wiki/Chicken_(game))