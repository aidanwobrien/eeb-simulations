## The World:
- A toroid, tile-based isometric 50x50 world grid with “empty” and “rock” tiles.
- “Empty” tiles can contain plants, herbivores and carnivores.
- “Rocks” are impassable (and are added to the world via Perlin noise)

## The Model:
- Designed to simulate Lotka-Volterra (LV) equations, the main goal was creating a 3-tiered “ecosystem” where the populations cycle through time in a stable phase, without any populations crashing.
- The typical LV equations do not account for space, meaning each tick the population would usually be “well-mixed”. But in this model, movement cost, localized reproduction and impassable “rocks” introduce clustering, refuges and overall “spatiality” (and thus noise vs the typical LV models).

## Phase Portrait:

![Phase Portrait Plot](docs/phase_portrait.png)

## Time-Series Plot:

![Time Series Plot](docs/time_series.png)

## The Rules:
- Plant tiles produce food (energy).
- Each tick, herbivores move one space in a random direction. If they’re on a plant tile they eat it and gain energy. Once eaten, that plant tile is removed and will regenerate after a fixed time (regen rate).
- Each tick, carnivores move two spaces towards the closest herbivore. If they’re on a tile with a herbivore, they eat it and gain energy. Carnivores must wait two ticks before eating again.
- Herbivores and carnivores reproduce when they have enough energy (defined by a reproduction threshold), and with a cost to their energy(defined by a reproduction cost). Their “offspring” appear in a random unblocked neighbour tile.If all neighbours are blocked, they do nothing that tick and keep their energy.
- Herbivores and carnivores lose energy each tick (a basal cost) and with each movement (a movement cost)