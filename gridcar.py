from typing import Tuple
from py2pddl import Domain, create_type
from py2pddl import predicate, action, goal, init


class GridCarDomain(Domain):

    Agent = create_type("Agent")
    X = create_type("X")
    Y = create_type("Y")

    @predicate
    def at(self, agent: Agent = None, x: X = None, y: Y = None):
        pass

    @predicate
    def is_occupied(self, x: X = None, y: Y = None):
        pass

    @action
    def up(self, agent=Agent("agent"),
           x_old=X("x_old"), y_old=Y("y_old"),
           x_new=X("x_new"), y_new=Y("y_new")):
        precond = [self.at(agent, x_old, y_old), ~
                   self.is_occupied(x_new, y_new)]
        effect = [~self.at(agent, x_old, y_old), self.at(agent, x_new, y_new)]
        return precond, effect

    @action
    def forward(self, agent=Agent("agent"),
           x_old=X("x_old"), y=Y("y"), x_new=X("x_new")):
        precond = [self.at(agent, x_old, y), ~
                   self.is_occupied(x_new, y)]
        effect = [~self.at(agent, x_old, y), self.at(agent, x_new, y)]
        return precond, effect


class GridCarProblem(GridCarDomain):

    def __init__(self):
        self.agent = GridCarDomain.Agent("agent1")
        self.xs = [GridCarDomain.X(x) for x in ["x0", "x1"]]

    @init
    def init(self):
        return [self.at(self.agent, "x0", "y0"),
                self.is_occupied("x0", "y1")]

    @goal
    def goal(self):
        return [self.at(self.agent, "x1", "y1")]
