from abc import ABC, abstractmethod
from collections import defaultdict
import math


class MCTS:
    def __init__(self, exploration_weight=1, max_depth=10):#10 works better

        self.Q = defaultdict(int)
        self.N = defaultdict(int)
        self.children = dict()
        self.exploration_weight = exploration_weight
        self.max_depth = max_depth

    def choose(self, node):
        
        if node.depth() >= self.max_depth:
            raise RuntimeError(f"choose called on node exceeding max depth {node}")

        if node not in self.children:
            return node.find_random_child()

        def score(n):
            if self.N[n] == 0:
                return float("-inf")
            return self.Q[n] / self.N[n]

        return max(self.children[node], key=score)

    def do_rollout(self, node):
        path = self._select(node)
        leaf = path[-1]
        self._expand(leaf)
        reward = self._simulate(leaf)
        self._backpropagate(path, reward)

    def _select(self, node):
        #print("check 2")

        path = []
        while node:
            #print("check 2")

            path.append(node)
            if node.is_terminal() or node.depth() >= self.max_depth:
                return path

            if not self.children.get(node):
                return path

            unexplored = self.children[node] - set(self.children.keys())
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path

            node = self._uct_select(node)

        return path  # Add a default return to handle the case when 'node' becomes None

    def _expand(self, node):
        #print("check 2")
        if node in self.children:
            return
        self.children[node] = node.find_children()

    def _simulate(self, node):
        while node:
            if node.is_terminal() or not self.children.get(node):
                return node.reward()

            # Adjust this part to handle when no moves are possible
            next_node = node.find_random_child()
            if next_node is None:  # Handle the case when no valid moves are left
                return node.reward()  # Return current node's reward as the outcome

            node = next_node

    def _backpropagate(self, path, reward):
        #print("check 4")
        for node in reversed(path):
            self.N[node] += 1
            self.Q[node] += reward

    def _uct_select(self, node):
        assert all(n in self.children[node] for n in self.children[node])
        print(f"Selecting from children of node: {node}")

        log_N_vertex = math.log(self.N[node])
        print(f"Log visit count for {node}: {log_N_vertex}")

        def uct(n):
            if self.N[n] == 0:
                print(f"Returning inf for node {n}")
                return float('inf')  # If the child node has not been visited yet, prioritize it
            if self.Q[n] < 0 or self.N[n] < 0:
                raise ValueError(f"Invalid values for Q or N: Q[n]={self.Q[n]}, N[n]={self.N[n]}")  # Handle invalid values
            
            uct_value = self.Q[n] / self.N[n] + self.exploration_weight * math.sqrt(
                2 * log_N_vertex / self.N[n]
            )
            print(f"UCT value for node {n}: {uct_value}")
            return uct_value

        selected_node = max(self.children[node], key=uct)
        print(f"Selected node: {selected_node}")
        return selected_node


class Node(ABC):
    @abstractmethod
    def find_children(self):#used for expansion 
        return set()

    @abstractmethod
    def find_random_child(self):#used for simulation
        return None

    @abstractmethod
    def is_terminal(self):#checks if the node is terminal
        return True

    @abstractmethod
    def reward(self):#reward during backpropigation
        return 0

    @abstractmethod
    def depth(self):#checks the depth of the node
        return 0

    @abstractmethod
    def __hash__(self):#the name of the node
        return 123456789

    @abstractmethod
    def __eq__(node1, node2):#this is used to compare nodes to each other
        return True
