import logging
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

from lgp.logic.action import Action


class LGPTree(object):
    logger = logging.getLogger(__name__)

    def __init__(self, domain, problem):
        self.domain = domain
        self.problem = problem
        self.tree = nx.DiGraph(name=self.problem.name)
        self.init_state = self.problem.state
        self.goal_states = []
        self.build_graph()

    def build_graph(self):
        '''
        Build LGP tree from PDDL domain and problem
        '''
        positive_goals = self.problem.positive_goals
        negative_goals = self.problem.negative_goals
        state = self.problem.state
        if LGPTree.applicable(state, positive_goals, negative_goals):
            LGPTree.logger.info('Goals are already achieved!')
        self.tree.clear()
        # Grounding process, i.e. assign parameters substitutions to predicate actions to make propositional actions
        ground_actions = self.domain.ground_actions()
        # BFS Search to build paths
        fringe = deque()
        fringe.append(state)
        while fringe:
            state = fringe.popleft()
            for act in ground_actions:
                if LGPTree.applicable(state, act.positive_preconditions, act.negative_preconditions):
                    new_state = LGPTree.apply(state, act.add_effects, act.del_effects)
                    if not self.tree.has_edge(state, new_state):
                        if LGPTree.applicable(new_state, positive_goals, negative_goals):
                            self.goal_states.append(new_state)  # store goal states
                        self.tree.add_edge(state, new_state, action=act)
                        if act.extensions[Action.UNDO_TAG] is not None:
                            self.tree.add_edge(new_state, state, action=act.extensions[Action.UNDO_TAG])
                        fringe.append(new_state)

    def plan(self, state=None):
        if self.tree.size() == 0:
            LGPTree.logger.warn('LGP Tree is not built yet! Plan nothing.')
            return []
        if state is None:
            state = self.init_state
        if not self.tree.has_node(state):
            LGPTree.logger.warn('State: %s \n is not recognized in LGP tree! Plan nothing.' % str(state))
            return []
        paths = []
        act_seqs = []
        path = nx.shortest_path(self.tree, source=state)
        for g in self.goal_states:
            try:
                p = path[g]
                paths.append(p)
                act_seq = [self.tree[p[i]][p[i + 1]]['action'] for i in range(len(p) - 1)]
                act_seqs.append(act_seq)
            except:  # noqa
                LGPTree.logger.warn('No path found between source %s and goal %s' % (str(state), str(g)))
        return paths, act_seqs

    def draw_tree(self, init_state=None, paths=None, label=True, show=True):
        node_color = self._color_states(init_state)
        edge_color = None
        if paths is not None:
            edge_color = self._color_edges(paths)
        nx.draw(self.tree, with_labels=label, node_color=node_color, edge_color=edge_color, font_size=5)
        if show:
            plt.show()

    def _color_states(self, init_state=None):
        if init_state is None:
            init_state = self.init_state
        color_map = []
        for n in self.tree:
            if n == init_state:
                color_map.append('green')
            elif n in self.goal_states:
                color_map.append('red')
            else:
                color_map.append('skyblue')
        return color_map

    def _color_edges(self, paths):
        edges = tuple((p[i], p[i + 1]) for p in paths for i in range(len(p) - 1))
        edge_color = []
        for e in self.tree.edges():
            if e in edges:
                edge_color.append('red')
            else:
                edge_color.append('black')
        return edge_color

    @staticmethod
    def applicable(state, positive, negative):
        return positive.issubset(state) and negative.isdisjoint(state)

    @staticmethod
    def apply(state, positive, negative):
        return state.difference(negative).union(positive)
