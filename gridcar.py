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
    def occupied(self, x: X = None, y: Y = None):
        pass

    @action
    def up(self, agent: Agent = Agent("agent"),
           xold: X = X("xold"), yold: Y = Y("yold"),
           xnew: X = X("xnew"), ynew: Y = Y("ynew")):
        precond = [self.at(agent, xold, yold), ~
                   self.occupied(xnew, ynew)]
        effect = [~self.at(agent, xold, yold), self.at(agent, xnew, ynew)]
        return precond, effect

    @action
    def forward(self, agent: Agent = Agent("agent"),
                xold: X = X("xold"), y: Y = Y("y"), xnew: X = X("xnew")):
        precond = [self.at(agent, xold, y), ~
                   self.occupied(xnew, y)]
        effect = [~self.at(agent, xold, y), self.at(agent, xnew, y)]
        return precond, effect


class GridCarProblem(GridCarDomain):

    def __init__(self):
        self.agent = GridCarDomain.Agent("agent1")
        self.xs = [GridCarDomain.X(x) for x in ["x0", "x1"]]
        self.ys = [GridCarDomain.Y(y) for y in ["y0", "y1"]]

    @init
    def init(self):
        return [self.at(self.agent, "x0", "y0"),
                self.occupied("x0", "y1")]

    @goal
    def goal(self):
        return [self.at(self.agent, "x1", "y1")]
