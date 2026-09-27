*This project has been created as part of the 42 curriculum by ahmounsi.*

# Fly-in

## Description

Fly-in is a Python simulation of drones travelling through connected zones.
The program reads a map, finds routes from the start zone to the goal zone,
assigns routes to the drones, and prints their movements turn by turn.

Maps can define:

- The number of drones.
- A start zone and an end zone.
- Other zones and their connections.
- Zone types and capacity limits.
- Connection capacity limits.

## Instructions

### Requirements

- Python 3.10 or newer
- `uv`

### Install

```bash
make install
```

This installs the dependencies from `pyproject.toml` and `uv.lock`.

### Run

Run the default map:

```bash
make run
```

Run another map:

```bash
make run MAP=maps/medium/01_dead_end_trap.txt
```

The program prints each drone movement for every simulation turn. It returns
an error message when the map or command-line argument is invalid.

Other useful commands are:

```bash
make clean
make lint
```

## How it works

1. The parser reads the map file and builds a graph of zones and connections.
2. Dijkstra's algorithm calculates the best route from the start to the goal.
3. A second route is searched when the graph allows multiple routes.
4. Drones are distributed between the available routes according to route
   length and capacity.
5. The simulation moves drones one turn at a time while respecting zone and
   connection capacities.

Normal zones take one turn to cross. Restricted zones take two turns.
Blocked zones cannot be used, and priority zones are preferred by the
pathfinding logic.

## Map format

A map starts with the number of drones, followed by zones and connections.
For example:

```text
nb_drones: 2

start_hub: start 0 0 [color=green]
hub: waypoint1 1 0 [color=blue]
end_hub: goal 2 0 [color=red]

connection: start-waypoint1
connection: waypoint1-goal
```

## Example

Command:

```bash
make run MAP=maps/easy/01_linear_path.txt
```

Example output:

```text
D0-waypoint1
D0-waypoint2 D1-waypoint1
D0-goal D1-waypoint2
D1-goal
```

Each item has the form `D<id>-<zone>`, meaning that the specified drone
moved to that zone during the current turn.

## Visual representation

The project uses ANSI terminal colors for zone names when a map specifies a
color. This makes the start, intermediate, priority, restricted, and goal
zones easier to distinguish in terminal output. The project does not include a
graphical interface.

## Resources

- [Python documentation](https://docs.python.org/3/)
- [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- `en.subject-flyin-1.6.pdf` — project subject and rules
- `maps/README.md` — included map categories and test scenarios

### AI usage

AI was used to help read the project subject, inspect the existing code, and
draft this README. It was used for documentation only; the README content was
checked against the source files, Makefile, sample map, and program output.
