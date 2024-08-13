from skimage.io import imread, imsave
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import json
from Maze import *
from Players import *
import time

class Game:
    def __init__(self, **kwargs):
        self._init_parameters(**kwargs)
        self.maze = Maze(self.height, self.width, self.debug_level)
        self.maze.kruskal(self.random_seed)
        self.maze.graph_network()
        self.maze.mimic_mazer()
        self._init_player()
        self._init_snakes()
        if self.debug_level > 2:
            self.maze.draw_maze(
                self._fn(series_id="overview"), overview=True, player=self.player, snakes=self.snakes
            )
            self.maze.draw_maze(
                self._fn(), overview=False, player=self.player, snakes=self.snakes
            )

    def simulate(self):
        while self.player.done == False:
            self.time += 1
            self.player.play_turn()
            for i in range(len(self.snakes)):
                self.snakes[i].play_turn()
            if self.debug_level > 1:
                print("Simulating...          sim time = ", self.time, end="\r")
            if self.debug_level > 2:
                self.maze.draw_maze(
                    self._fn(), overview=False, player=self.player, snakes=self.snakes
                )
        if int(self.debug_level) > 1:
            print("Simulation done. Total sim time")
        if int(self.debug_level) > 2:
            for extra_time in range(self.over_time):
                self.maze.draw_maze(
                    self._fn(time=self.time + extra_time),
                    overview=False,
                    player=self.player,
                    snakes=self.snakes,
                )
        elif int(self.debug_level) > 0:
            self.maze.draw_maze(
                self._fn(), overview=False, player=self.player, snakes=self.snakes
            )
        termination_code = (
            0 * self.player.complete + 1 * self.player.abort + 2 * self.player.dead
        )
        return termination_code

    def _init_parameters(self, **kwargs):
        ### initializes game parameters via kwargs where available and via defaults where not.
        ### Note that additional parameters are defined here, too, which cannot be changed via kwargs.
        defaults = {
            "height": 5,
            "width": 5,
            "debug_level": 0,
            "random_seed": 0,
            "raw_memory": 0,
            "nbr_snakes": 2,
            "custom_snakes": None,
            "over_time": 20,
            "series_id": None,
        }
        parameters = {}
        for key in defaults.keys():
            if defaults.keys():
                parameters[key] = kwargs[key] if key in kwargs.keys() else defaults[key]

        self.height = parameters["height"]
        self.width = parameters["width"]
        self.debug_level = parameters["debug_level"]
        self.random_seed = parameters["random_seed"]
        self.raw_memory = parameters["raw_memory"]
        self.nbr_snakes = parameters["nbr_snakes"]
        self.custom_snakes = parameters["custom_snakes"]
        self.over_time = parameters["over_time"]
        self.series_id = parameters["series_id"]

        self.start_position = (0, 1)
        self.goal_position = (2 * self.height + 1, 2 * self.width + 1)
        self.time = 0
        self.player = None
        self.snakes = []

        if self.debug_level > 1:
            print("Game._init_parameters():")
            print("- height:", self.height)
            print("- width:", self.width)
            print("- debug_level:", self.debug_level)
            print("- random_seed:", self.random_seed)
            print("- raw_memory:", self.raw_memory)
            print("- nbr_snakes:", self.nbr_snakes)
            print("- custom_snakes:", self.custom_snakes)
            print("- over_time:", self.over_time)
            print("- series_id:", self.series_id)
            print("- time:", self.time)

    def _fn(self, **kwargs):
        ### Returns png output file name
        if "time" in kwargs.keys():
            time = kwargs["time"]
        else:
            time = self.time
        if "series_id" in kwargs.keys():
            fn = "mazer_%ix%i_r%05i_f%02i_s%i_%s_t%05i.png" % (
                self.height,
                self.width,
                self.random_seed,
                self.raw_memory,
                self.nbr_snakes,
                kwargs["series_id"],
                time,
            )
        else:
            fn = "mazer_%ix%i_r%05i_f%i_s%02i_t%05i.png" % (
                self.height,
                self.width,
                self.random_seed,
                self.raw_memory,
                self.nbr_snakes,
                time,
            )
        return "./pics/" + fn

    def _init_player(self):
        self.player = Mazer(self.maze, self.raw_memory)

    def _init_snakes(self):
        if self.custom_snakes:
            for s in range(len(self.custom_snakes)):
                self.snakes.append(Snake(self.maze, self.custom_snakes[s]))
        else:
            for s in range(self.nbr_snakes):
                self.snakes.append(Snake(self.maze))
