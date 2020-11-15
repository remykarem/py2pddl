from typing import Tuple
from itertools import product
from collections import namedtuple
from py2pddl import Domain, create_type
from py2pddl import predicate, action, goal, init


class GridCarDomain(Domain):

    Agent = create_type("Agent")
    Loc = create_type("Loc")

    @predicate(Agent, Loc)
    def at(self, agent, loc):
        pass

    @predicate(Loc)
    def occupied(self, loc):
        pass

    @action(Agent, Loc, Loc)
    def up(self, agent, loc_old, loc_new):
        precond = [self.at(agent, loc_old), ~self.occupied(loc_new)]
        effect = [~self.at(agent, loc_old), self.at(agent, loc_new)]
        return precond, effect


class GridCarProblem(GridCarDomain):

    def __init__(self):
        self.agent = [GridCarDomain.Agent("agent1")]
        self.loc = {f"x{x}y{y}": GridCarDomain.Loc(f"x{x}y{y}")
                    for x, y in product(range(3), range(4))}

    @init
    def init(self, loc=(1, 3)):
        x, y = loc
        at = [self.at(self.agent[0], self.loc[f"x{x}y{y}"])]
        occupied = [self.occupied(self.loc[f"x{x}y{y}"])
                    for x, y in [(0, 3), (1, 1), (2, 3)]]
        return occupied + at

    @goal
    def goal(self, loc=(2, 2)):
        x, y = loc
        return [self.at(self.agent[0], self.loc[f"x{x}y{y}"])]