from typing import Tuple
from py2pddl import Domain, create_type
from py2pddl import predicate, action, goal, init


class ExampleDomain(Domain):

    Plane = create_type("Plane")
    City = create_type("City")

    @predicate
    def at(self, plane: Plane = None, city: City = None):
        pass

    @action
    def fly(self, plane=Plane("plane"), org=City("org"), dst=City("dst")):
        precond = self.at(plane, org)
        effect = [~self.at(plane, org), self.at(plane, dst)]
        return precond, effect

    @action
    def flow(self, plane=Plane("plane"), org=City("org"), dst=City("dst")):
        precond = self.at(plane, org)
        effect = [~self.at(plane, org), self.at(plane, dst)]
        return precond, effect


class ExampleProblem(ExampleDomain):

    def __init__(self):
        self.p1 = ExampleDomain.Plane("p1")
        self.p2 = ExampleDomain.Plane("p2")

    @init
    def init(self):
        return [self.at("p1", "paris"), self.at("p2", "london")]

    @goal
    def goal(self):
        return [self.at(a, a) for a in range(10)]
