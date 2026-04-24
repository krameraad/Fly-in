*This project has been created as part of the 42 curriculum by ekramer*
# Fly-in
[![fly-in-optimized.gif](https://i.postimg.cc/LX0sZ1JT/fly-in-optimized.gif)](https://postimg.cc/62nKkTL2)


In this project, we are tasked to build and run a simulation of drones moving
through a graph. The drones move towards a goal, and the drones may not collide
with eachother. Efficient pathfinding is important, with multiple agents.


## Instructions
Install dependencies and run the project using `make run`.
Alternatively, run the project directly using `uv run .` in the project root.
When running directly, you can additionally provide an argument,
which will load that specific map immediately without going through the menu.

Using `make run` or `uv run .`, a menu in the terminal will list
all available maps from the directories `maps` and `testmaps`.

After picking one,
the visualization will open and instructions will be visible on screen.

- **Click Mouse 1 / Left Mouse Button**:
    - All drones execute a turn.
- **Hold Mouse 2 / Right Mouse Button**:
    - Pan the view.
- **Press Space Bar**:
    - Enable/disable autoplay.

Movements of the drones will be printed in the terminal.


## Resources
For this project, I didn't use that many external resources.
There is some info on
[MAPF](https://en.wikipedia.org/wiki/Multi-agent_pathfinding) on Wikipedia,
and there are multiple smart ways to solve this problem, including 
[conflict-based search](https://www.youtube.com/watch?v=FnrZyL6965o) and
[cooperative A*](https://arongranberg.com/2015/06/cooperative-pathfinding-experiments/).

I didn't implement a very difficult algorithm, focusing on the visualization
using [pygame](https://www.pygame.org/docs/).

Other students and AI were helpful in guiding my design decisions.


## Algorithm
My pathfinding depends on
[Dijkstra's Algorithm](https://www.w3schools.com/dsa/dsa_algo_graphs_dijkstra.php)
to find the shortest path. For drones to avoid eachother, a *traffic* heuristic
was used.

All drones calculate their paths initially, in order of priority.
Lower priority drones take into account the movements of the drones with a higher priority.
**The path a drone takes increases the cost of travel of all its nodes for the drones that move after it.**
This means the lower priority drones consider alternative paths "shorter".


## Visualization
For the visual representation, I chose to use *pygame*.
I already had some experience with game development, although *pygame* was new to me.
Nevertheless, many concepts were familiar to me and I used it pretty effectively, I think.

It was one of the first things that I focused on,
because visualizing the simulation helps so much with debugging.
It also gives a solid impression to people seeing the project.
Not only that, but it's also fun to work on.
I made all the assets myself, including even the font.
This personal touch is important to me.