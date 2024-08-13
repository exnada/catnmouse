import argparse
from skimage.io import imread, imsave
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import json

# XXX XXX XXX
import ctypes
libPNG = ctypes.CDLL("/usr/lib/x86_64-linux-gnu/libpng.so", mode=ctypes.RTLD_GLOBAL)
libDrawMaze = ctypes.CDLL("./libdrawmaze.so")
# libDrawMaze.showMaze.argtypes=ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(ctypes.c_int))
# libDrawMaze.showMaze.argtypes=ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)
# XXX XXX XXX

class Maze:
    def __init__(self, height, width, debug_level=0):
        self.height = height
        self.width = width
        self.debug_level = debug_level
        self.full_width = 2 * self.width + 1
        self.full_height = 2 * self.height + 1
        self.grid = np.ones((self.full_height, self.full_width), dtype=np.uint8)
        self.start_node = Node((0, 1))
        self.visited = []
        self.visited.append(self.start_node.pos)
        self.goal_node = Node((2 * self.height, 2 * self.width - 1))
        self.player = None
        self.snakes = []
        self.deep_dead_ends = []
        self.shallow_dead_ends = []
        self.connections = None
        self.graph = None
        self.mazer_path = None
        self.mazer_solution = None
        self.mazer_path_steps = None
        self.mazer_solution_steps = None

    def get_start_position(self):
        return self.start_node.pos

    def get_goal_position(self):
        return self.goal_node.pos

    def set_player(self, player):
        if self.player != None:
            print("Warning: player has already been set. Rejecting reset.")
            exit(1)
        else:
            self.player = player

    def scan_for_player(self, exploration):
        res = []
        for i in range(len(exploration)):
            if exploration[i].pos == self.player.node.pos:
                res.append(exploration[i])
            else:
                for j in range(len(exploration[i].next_steps)):
                    if exploration[i].next_steps[j].pos == self.player.node.pos:
                        res.append(exploration[i])
        return res

    def kruskal(self, random_seed=0):
        forest = []
        for row in range(self.height):
            for col in range(self.width):
                forest.append([(2 * row + 1, 2 * col + 1)])
                self.grid[2 * row + 1][2 * col + 1] = 0
        self.grid[0][1] = 0
        self.grid[self.full_height - 1][self.full_width - 2] = 0
        edges = []
        for row in range(self.height):
            for col in range(1, self.width):
                edges.append((2 * row + 1, 2 * col))
        for row in range(1, self.height):
            for col in range(self.width):
                edges.append((2 * row, 2 * col + 1))
        np.random.seed(random_seed)
        np.random.shuffle(edges)

        while len(forest) > 1:
            current_edge_row, current_edge_column = edges[0]
            edges = edges[1:]
            if current_edge_row % 2 == 0:  # vertical connection
                tree_id_A = self._get_tree_id(
                    (current_edge_row - 1, current_edge_column), forest
                )
                tree_id_B = self._get_tree_id(
                    (current_edge_row + 1, current_edge_column), forest
                )
            else:  # odd-numbered row: horizontal connection
                tree_id_A = self._get_tree_id(
                    (current_edge_row, current_edge_column - 1), forest
                )
                tree_id_B = self._get_tree_id(
                    (current_edge_row, current_edge_column + 1), forest
                )
            if tree_id_A != tree_id_B:
                new_tree = forest[tree_id_A] + forest[tree_id_B]
                tree_A = list(forest[tree_id_A])
                tree_B = list(forest[tree_id_B])
                forest = [x for x in forest if x != tree_A]
                forest = [x for x in forest if x != tree_B]
                forest.append(new_tree)
                self.grid[current_edge_row][current_edge_column] = 0
        # XXX XXX XXX
        print(self.grid)
        # print(self.grid.flatten())
        libDrawMaze.connect()
        py_values = np.array([1, 2, 1, 4, 5], np.uint32);
        # print(type(self.grid))
        # print(list([[1,2,3], [4, 5, 6]]))
        # arr = (ctypes.c_int * len(py_values))(*py_values)
        # ctypes.POINTER(ctypes.POINTER(ctypes.c_int))
        # arr = (ctypes.POINTER(ctypes.c_int))(py_values)
        # py_values.ctypes.data_as(ctypes.POINTER(ctypes.c_uint))
        # libDrawMaze.showMaze(self.full_width, self.full_height, py_values.ctypes.data_as(ctypes.POINTER(ctypes.c_uint)))
        cmaze=self.grid.flatten().astype(np.uint32).ctypes.data_as(ctypes.POINTER(ctypes.c_uint))
        # libDrawMaze.showMaze(self.full_width, self.full_height, cmaze)
        libDrawMaze.drawMaze(self.width, self.height, cmaze)
        # libDrawMaze.showMaze(self.full_width, self.full_height, self.grid)
        # libDrawMaze.showMaze(self.full_width, self.full_height)
        # XXX XXX XXX

    def _get_tree_id(self, coordinate, forest):
        return sum(
            [
                tree_id if coordinate in tree else 0
                for tree_id, tree in enumerate(forest)
            ]
        )

    def _tag(self, node):
        self.nodes.append(node)
        self.node_positions.append(node.pos)

    def add_snake(self, snake_node):
        self.snakes.append(snake_node)

    def check_snake(self, position):
        return position in [snake.node.pos for snake in self.snakes]

    def update_connections(self, node_position, node_info):
        # Updates connection information stored in dictionary self.connections:
        # Given that all connections are bi-directional, all connections
        # first specify the node position with a smaller y value (entry node[0]).
        # if the nodes have the same y value, the x position is checked.
        # The connection data dictionary then uses that node and keeps a list of
        # its corresponding node and distance in each list entry.
        node_a = node_position
        node_b = node_info["previous_node"]
        # if node_a[0] < node_b[0]:
        #     main_node = node_a
        #     conn_node = node_b
        #     fs = node_info["last_step"]
        #     ls = node_info["first_step"]
        # elif node_a[0] > node_b[0]:
        #     main_node = node_b
        #     conn_node = node_a
        #     fs = node_info["first_step"]
        #     ls = node_info["last_step"]
        # elif node_a[1] <= node_b[1]:
        #     main_node = node_a
        #     conn_node = node_b
        #     fs = node_info["last_step"]
        #     ls = node_info["first_step"]
        # else:
        #     main_node = node_b
        #     conn_node = node_a
        #     fs = node_info["first_step"]
        #     ls = node_info["last_step"]
        # # conn_data = {"node": conn_node, "distance": node_info["distance"]}
        main_node = node_b
        conn_node = node_a
        fs = node_info["first_step"]
        ls = node_info["last_step"]
        conn_data = {"node": conn_node, "distance": node_info["distance"], "first_step": fs, "last_step": ls}
        if main_node not in self.connections:
            self.connections.update({main_node: [conn_data]})
        else:
            self.connections[main_node].append(conn_data)

    def graph_network(self):
        self.exploration_stack = []
        self.nodes = []
        self.connections = {}
        self.node_positions = []
        current_node = self.start_node
        self._tag(current_node)
        self.exploration_stack.append(current_node.walk((1, 1), self, self.visited))
        self.graph = {}

        while self.exploration_stack:
            node_info = self.exploration_stack.pop(0)
            node_position = node_info["current_node"]

            if node_position in self.node_positions:
                current_node = None
                for i in range(len(self.nodes)):
                    if node_position == self.nodes[i].pos:
                        current_node = self.nodes[i]
                if current_node == None:
                    print("ERROR: undefined node")
                    exit(1)
            else:
                current_node = Node(node_position)
                self._tag(current_node)

            self.update_connections(node_position, node_info)

            node_connections = node_info["connections"]
            while node_connections:
                current_connection = node_connections.pop()
                if current_connection["pos"] not in self.visited:
                    self.exploration_stack.append(
                        current_node.walk(current_connection["pos"], self, self.visited)
                    )

        ### Find positions of dead-ends within the graph (excluding start and finish)
        touch_points = {}
        sources = self.connections.keys()
        dists = {}
        for source in sources:
            for target in self.connections[source]:
                tn = target["node"]
                td = target["distance"]
                if source in dists:
                    dists[source] = td if td > dists[source] else dists[source]
                else:
                    dists[source] = td
                if tn in dists:
                    dists[tn] = td if td > dists[tn] else dists[source]
                else:
                    dists[tn] = td

                if source in touch_points.keys():
                    touch_points[source] += 1
                else:
                    touch_points[source] = 1
                if target["node"] in touch_points.keys():
                    touch_points[target["node"]] += 1
                else:
                    touch_points[target["node"]] = 1

        for target in touch_points.keys():
            if touch_points[target] < 2:
                if target != self.start_node.pos and target != self.goal_node.pos:
                    if dists[target] > 0:
                        self.deep_dead_ends.append(target)
                    else:
                        self.shallow_dead_ends.append(target)

    def draw_maze(self, filename, **kwargs):
        ### Draws maze to a png file.
        defaults = {
            "unknown_path_brightness": 30,
        }
        img = []
        if "overview" in kwargs.keys():
            overview = kwargs["overview"]
        if overview:
            upb = 255
        else:
            upb = (
                kwargs["unknown_path_brightness"]
                if "unknown_path_brightness" in kwargs
                else defaults["unknown_path_brightness"]
            )
        for row_id, row in enumerate(self.grid):
            img_row = []
            for pixel in row:
                img_row.append(
                    [upb - upb * pixel, upb - upb * pixel, upb - upb * pixel, 255]
                )
            img.append(img_row)

        if "player" in kwargs.keys():
            player = kwargs["player"]
            goal_coord = self.goal_node.pos
            img[goal_coord[0]][goal_coord[1]] = [0, 200, 0, 255]

            visited = list(set(player.past))
            for vis_id in range(len(visited)):
                img[visited[vis_id][0]][visited[vis_id][1]] = [100, 100, 100, 255]
            for track_id in range(len(player.track)):
                img[player.track[track_id][0]][player.track[track_id][1]] = [
                    225,
                    225,
                    255,
                    255,
                ]

            for id1 in range(len(player.exploration)):
                coord = player.exploration[id1].pos
                img[coord[0]][coord[1]] = [40, 255, 255, 255]
                for id2 in range(len(player.exploration[id1].next_steps)):
                    coord = player.exploration[id1].next_steps[id2].pos
                    if coord != player.node.pos:
                        img[coord[0]][coord[1]] = [35, 230, 230, 255]

            ppos = player.node.pos
            img[ppos[0]][ppos[1]] = [255, 225, 50, 255]  # yellow/gold

        if "snakes" in kwargs.keys():
            snakes = kwargs["snakes"]
            if len(snakes) > 0:
                for s in range(len(snakes)):
                    spos = snakes[s].node.pos
                    img[spos[0]][spos[1]] = [200, 0, 0, 255]

        imsave(filename, np.array(img, dtype=np.uint8))

    def draw_network(self, filename):
        G = nx.Graph()
        connections_graph = self.connections.copy()
        eldict = {}
        pos = {}
        while connections_graph:
            node_position = next(iter(connections_graph))
            node_info = connections_graph.pop(node_position)
            if str(node_position) not in pos:
                pos[str(node_position)] = np.array(
                    [node_position[1], -node_position[0]]
                )
            for i in range(len(node_info)):
                conn_node = node_info[i]["node"]
                if str(conn_node) not in pos:
                    pos[str(conn_node)] = np.array([conn_node[1], -conn_node[0]])
                G.add_edge(str(node_position), str(conn_node), color="green", weight=5)
                eldict[(str(node_position), str(conn_node))] = node_info[i]["distance"]
        nx.draw_networkx_edge_labels(G, pos, edge_labels=eldict, font_color="red")
        nx.draw(
            G,
            pos,
            edge_color="black",
            width=1,
            linewidths=1,
            node_size=50,
            node_color="violet",
            alpha=0.9,
            labels={node: node for node in G.nodes()},
        )
        plt.savefig(filename)

    def _get_next(self, connections, past):
        conns = [c for c in connections if c["node"] not in past]
        # print(conns)
        if len(conns)==0:
            return []
        elif len(conns) == 1:
            return conns[0]
        elif len(conns) > 1:
            gds=[]
            mgd = None
            mgd_i = []
            for i in range(len(conns)):
                gds.append(conns[i]["goal_dist"])
                if mgd:
                    if mgd >= conns[i]["goal_dist"]:
                        mgd = conns[i]["goal_dist"]
                        mgd_i.append(i)
                else:
                    mgd = conns[i]["goal_dist"]
                    mgd_i.append(i)
            if len(mgd_i) == 2:
                a = conns[mgd_i[0]]
                b = conns[mgd_i[1]]
                if a["goal_dist"]<b["goal_dist"]:
                    return a
                elif a["goal_dist"]>b["goal_dist"]:
                    return b 
                elif a["node"][0]>b["node"][0]:
                    return b 
                else:
                    return a
            elif len(mgd_i) == 1:
                return conns[mgd_i[0]]
            else:
                print("Error: _get_next() shows more than two connections with the identical goal distance.")
                exit(1)
        else:
            print("Error: _get_next() shows more than two outgoing connections, which should not be possible.")
            exit(1)


    def mimic_mazer(self):
        start_pos = self.get_start_position()
        goal_pos = self.get_goal_position()
        current_pos = start_pos
        delta_steps = 0
        self.mazer_path_steps = []
        self.mazer_path = []
        self.solution = []
        self.solution_steps = []
        while current_pos != goal_pos:
            if current_pos in self.connections.keys():
                conns = self.connections[current_pos]
                for c in conns:
                    c["goal_dist"] = np.sqrt((c["first_step"][0] - goal_pos[0])**2 + (c["first_step"][1] - goal_pos[1])**2)

                next_node = self._get_next(conns, self.mazer_path)
                if next_node != []:
                    backtrack = False
                    self.mazer_path.append(current_pos)
                    self.solution.append(current_pos)

                    current_pos = next_node.get("node")
                    delta_steps = next_node["distance"]
                    self.mazer_path_steps.append(delta_steps)
                    self.solution_steps.append(delta_steps)
                else:
                    self.mazer_path.append(current_pos)
                    current_pos = self.solution.pop()
                    delta_steps = self.solution_steps.pop()
                    self.mazer_path_steps.append(delta_steps)
            else:
                self.mazer_path.append(current_pos)
                current_pos = self.solution.pop()
                delta_steps = self.solution_steps.pop() - 2 
                self.mazer_path_steps.append(delta_steps)

        print("nbr of steps:", 2*np.sum(self.mazer_path_steps))






class Connection:
    def __init__(self, node_a, node_b, distance):
        self.node_a = node_a
        self.node_b = node_b
        self.distance = distance


class Node:
    def __init__(self, coordinate, desc=""):
        self.pos = coordinate
        self.desc = desc
        self.next_steps = []

    def move_to(self, coordinate):
        self.pos = coordinate

    def find_connections(self, maze, coord=None):
        available_connections = []
        if coord != None:
            y = coord[0]
            x = coord[1]
        else:
            y = self.pos[0]
            x = self.pos[1]
        height = np.shape(maze.grid)[0]
        width = np.shape(maze.grid)[1]
        if y > 0:
            if maze.grid[y - 1][x] == 0:
                available_connections.append({"pos": (y - 1, x), "desc": "path"})
        if y + 1 < height:
            if maze.grid[y + 1][x] == 0:
                available_connections.append({"pos": (y + 1, x), "desc": "path"})
        if x > 0:
            if maze.grid[y][x - 1] == 0:
                available_connections.append({"pos": (y, x - 1), "desc": "path"})
        if x + 1 < width:
            if maze.grid[y][x + 1] == 0:
                available_connections.append({"pos": (y, x + 1), "desc": "path"})
        for connection_id in range(len(available_connections)):
            if maze.check_snake(available_connections[connection_id]["pos"]):
                available_connections[connection_id]["desc"] = "Snake"
        return available_connections

    def walk(self, first_step, maze, visited=[]):
        distance = 0
        next_position = [{"pos": first_step}]
        previous_position = None
        current_position = self.pos
        first_step = None
        last_step = None
        while len(next_position) == 1:
            distance += 1
            if previous_position:
                visited.append(current_position)
            previous_position = current_position
            if first_step:
                last_step = current_position
            else:
                first_step = next_position[0]["pos"]
                last_step = current_position
            current_position = next_position[0]["pos"]
            next_position = [
                next_coord
                for next_coord in self.find_connections(maze, current_position)
                if next_coord["pos"] != previous_position
            ]
        return {
            "current_node": current_position,
            "previous_node": self.pos,
            "distance": distance,
            "first_step": first_step,
            "last_step": last_step,
            "connections": next_position,
        }

    def find_next_steps(self, maze, depth):
        self.depth = depth
        self.next_steps = [
            Node(connection["pos"], connection["desc"])
            for connection in self.find_connections(maze, self.pos)
        ]
        if self.depth > 0:
            for i in range(len(self.next_steps)):
                self.next_steps[i].find_next_steps(maze, self.depth - 1)
        return self.next_steps

    def show_next_steps(self):
        if self.next_steps != []:
            for i in range(len(self.next_steps)):
                print(self.pos, i, " > ", self.next_steps[i].pos)
                for j in range(len(self.next_steps[i].next_steps)):
                    print(self.pos, i, j, " >> ", self.next_steps[i].next_steps[j].pos)
