import numpy as np
from Maze import *


class Player:
    def __init__(self, maze):
        self.desc = "Player"
        self.maze = maze
        self.node = Node(self.maze.get_start_position())
        self.set_defaults()

    def set_defaults(self):
        self.time = 0
        self.goal_position = self.maze.get_goal_position()
        self.past = []
        self.track = []
        self.exploration = []
        self.complete = False
        self.abort = False
        self.dead = False
        self.done = False
        self.fear = 0
        self.fear_threshold = 1.0

    def goal_dist(self, pos):
        xg = self.goal_position[1]
        yg = self.goal_position[0]
        xp = pos[1]
        yp = pos[0]
        return np.sqrt((xg - xp) ** 2 + (yg - yp) ** 2)

    def play_turn(self):
        self.time += 1
        if self.dead:
            return
        if self.in_danger():
            self.fear += self.raw_memory
        if self.fear < self.fear_threshold:
            if self.exploration == []:
                self.explore()
            else:
                self.move()
        else:
            self.fear_response()

        if self.time > 2:
            self.abort = self.node.pos == self.maze.get_start_position()
        self.fear -= 1
        if not (self.fear > 0.01):
            self.fear = 0
        self.done = self.complete or self.abort or self.dead

    def in_danger(self):
        return None


class Mazer(Player):
    def __init__(self, maze, raw_memory=None, nbr_of_snakes=None, random_seed=None):
        self.desc = "Mazer"
        self.maze = maze
        self.maze.set_player(self)
        self.node = Node((0, 1))
        if raw_memory == None:
            self.raw_memory = 5
        else:
            self.raw_memory = raw_memory
        self.nbr_of_snakes = nbr_of_snakes
        self.random_seed = random_seed
        self.set_defaults()

    def explore(self):
        self.dead = self.maze.check_snake(self.node.pos)
        if self.dead:
            return
        self.exploration = self.node.find_next_steps(self.maze, 2)
        new_coords = []
        for next_node_id in range(len(self.exploration)):
            if (
                self.exploration[next_node_id].pos not in self.past
                and self.exploration[next_node_id].desc != "Snake"
                and "Snake"
                not in [
                    subsequent_step.desc
                    for subsequent_step in self.exploration[next_node_id].next_steps
                ]
            ) or self.exploration[next_node_id].pos == self.goal_position:
                new_coords.append(self.exploration[next_node_id].pos)

    def move(self):
        self.dead = self.maze.check_snake(self.node.pos)
        if not self.dead:
            new_coords = []
            for next_node_id in range(len(self.exploration)):
                if (
                    self.exploration[next_node_id].pos not in self.past
                    and self.exploration[next_node_id].desc != "Snake"
                    and "Snake"
                    not in [
                        subsequent_step.desc
                        for subsequent_step in self.exploration[next_node_id].next_steps
                    ]
                    and len(self.exploration[next_node_id].next_steps) > 1
                ) or self.exploration[next_node_id].pos == self.goal_position:
                    new_coords.append(self.exploration[next_node_id].pos)

            if len(new_coords) > 0:
                self.past.append(self.node.pos)
                self.track.append(self.node.pos)
                goal_dists = [
                    self.goal_dist(new_coords[i]) for i in range(len(new_coords))
                ]
                self.node.move_to(new_coords[goal_dists.index(min(goal_dists))])
                if self.node.pos == self.goal_position:
                    self.complete = True
            else:
                self.past.append(self.node.pos)
                self.node.move_to(self.track.pop())
            self.dead = self.maze.check_snake(self.node.pos)
            self.exploration = []

    def fear_response(self):
        self.dead = self.maze.check_snake(self.node.pos)
        if self.dead:
            return
        self.exploration = []
        self.past.append(self.node.pos)
        self.node.move_to(self.track.pop())
        self.dead = self.maze.check_snake(self.node.pos)

    def in_danger(self):
        adjacents = []
        for i in range(len(self.exploration)):
            adjacents.append(self.maze.check_snake(self.exploration[i].pos))
            for j in range(len(self.exploration[i].next_steps)):
                adjacents.append(
                    self.maze.check_snake(self.exploration[i].next_steps[j].pos)
                )
        return True in adjacents


class Snake(Player):
    def __init__(self, maze, custom_snake_pos=None):
        self.desc = "Snake"
        self.maze = maze
        self.maze.add_snake(self)
        if custom_snake_pos:
            snake_pos = custom_snake_pos
        else:
            if len(maze.deep_dead_ends) > 0:
                snake_pos_id = np.random.randint(len(maze.deep_dead_ends))
                snake_pos = maze.deep_dead_ends.pop(snake_pos_id)
            else:
                snake_pos_id = np.random.randint(len(maze.shallow_dead_ends))
                snake_pos = maze.shallow_dead_ends.pop(snake_pos_id)
        self.node = Node(snake_pos)
        self.set_defaults()

    def explore(self):
        self.exploration = self.maze.scan_for_player(
            self.node.find_next_steps(self.maze, 2)
        )

    def move(self):
        self.node.move_to([e.pos for e in self.exploration][0])
        self.exploration = []
