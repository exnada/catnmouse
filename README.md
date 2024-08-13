# Cat and mouse game
 
Maze solver.

## How to run the demo
- run: `make demo` 
- movie results are in: `src/mpeg/`

## Prerequisites
- docker
- developer tools and command-line environment (tested on Mac, not tested on Windows)

## Notes:

### Code and json variables
- `height` height of the maze (as number of cells; number of pixels is `2*height + 1`)
- `width` width of the maze (as number of cells; number of pixels is `2*width + 1`)
- `fear_memory` describes, after detecting a snake, how many times (for how many rounds) the robot drops exploring its surroundings in favor of moving away.
- `raw_memory` describes, after detecting a snake, how many rounds the robot remembers that it had seen a snake. By definition, `fear_memory = (raw_memory - 1)/2` because the robot moves every other turn anyway. Specifically, if `raw_memory` is 0, the robot seeks to escape the snake and just treats it as a wall. If `raw_memory` is 1, the robot simply tries to avoid the snake right after it detected the snake (when it was going to move anyway), which is equal to `fear_memory` = 0. Then, `raw_memory` 2 simply seeks to avoid the snake for two moves (one of which would normally be a look-around). The relevant numbers for `raw_memory` are 1, 3, 5, 7, ..., as they are equivalent to `fear_memory` 0, 1, 2, 3,...
- `nbr_snakes` sets how many snakes are set at dead-ends within the maze.
- `random_seed` sets the random seed value that is used to initialize the random number generator that then builds the maze and (typically) selects the positions of the snakes.
- `debug_level` sets the amount of output that mazer produces.
	- `0`: no output, other than the summary line reporting the result of the simulation.
	- `1`: level 0 output plus png image showing the result.
	- `2`: level 1 output plus simulation details console output.
	- `3`: level 2 output plus png image for each round of the simulation.
- `compute_failed` determines if mazes should be computed if they could not be solved for (the same configuration with) less snakes. This dramatically increases speed of scans that go to high numbers of snakes. Recommended setting is `false`.

### Recreating plots
Once data is computed (and saved as a `.csv` in the `data/` folder), launch the docker container using `make bash`. Adjust the details inside `config.json` to point to your `.csv` data file. Then, from the `src` directory, launch the data processor and reference your profile (here: `mazer-scan-publication`):
```
python data/process_data.py -p mazer-scan-publication
```

### Concepts and naming
These files were originally developed as project mazer. What is now referred to as a cat and mouse game, where the mouse tries to solve the maze, was originally conceptualized as a robot, called mazer (maze solver) trying to find the exit while avoiding snakes (instead of cats). The code still reflects that, since this is how the computations were done.

## Copyright notice
Copyright (c) 2024 ExNada Inc. All right reserved.
