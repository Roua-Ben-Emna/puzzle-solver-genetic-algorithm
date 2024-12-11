# Puzzle Solver Using Genetic Algorithm

This project is a **puzzle solver** implemented using a **genetic algorithm**. The program slices an image into a grid of tiles and attempts to solve it using evolutionary techniques such as selection, crossover, and mutation. The project includes a graphical interface built with **Pygame** to visualize the solving process.

---

## Features
- **Customizable grid size**: Choose between easy (3x3), medium (4x4), and hard (5x5) grids.
- **Genetic Algorithm Solver**:
  - Uses selection, crossover, and adaptive mutation.
  - Handles stagnation and termination conditions.
- **Graphical Interface**:
  - Visualize the solving process step-by-step.
  - Display fitness, generation, and solution progress.
- **Restart functionality**: Restart the puzzle with a new configuration.

---

## Requirements

To run the project, install the required dependencies using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Dependencies:
- `pygame`: For graphical interface and visualization.
- `pygame_gui`: For additional GUI components (if required).

---

## How to Run

1. **Clone or download the repository.**
2. **Ensure you have Python 3.6+ installed.**
3. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the main file**:
   ```bash
   python main.py
   ```
5. **Select the grid size**:
   - Easy (3x3)
   - Medium (4x4)
   - Hard (5x5)
6. **Watch the puzzle-solving process!**

---

## Project Structure

```
project/
├── main.py               # Main file to run the program
├── genetic_algorithm.py  # Core genetic algorithm logic
├── requirements.txt      # Dependencies for the project
├── assets/               # Directory for images and resources
│   └── puzzle_image.jpg  # Image used for the puzzle
```

---

## How It Works

### Genetic Algorithm Workflow
1. **Initialization**: Create a random population of chromosomes (shuffled puzzle pieces).
2. **Evaluation**: Calculate the fitness of each chromosome based on:
   - Correct positions.
   - Penalties for misplaced tiles.
3. **Selection**: Use tournament selection to pick the best candidates for reproduction.
4. **Crossover**: Perform two-point crossover to combine parent chromosomes into offspring.
5. **Mutation**: Swap two random pieces in the chromosome to introduce variability.
6. **Termination**: Stop if a solution is found, or if stagnation occurs after 20 generations.

### GUI Features
- **Menu**: Allows the user to select the grid size.
- **Visualization**: Displays the puzzle-solving process with fitness and generation updates.
- **Restart Button**: Restart the puzzle with a new configuration.

