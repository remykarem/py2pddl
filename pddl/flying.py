from py2pddl import Domain, create_type
from py2pddl import predicate, action
from py2pddl import goal, init


class AirCargoDomain(Domain):

    Plane = create_type("Plane")
    Cargo = create_type("Cargo")
    Airport = create_type("Airport")

    @predicate
    def at(self, c: Cargo = None, p: Plane = None):
        pass

    @predicate
    def in_(self, c: Cargo = None, p: Plane = None):
        pass

    @action
    def load(self,
             c: Cargo = Cargo("c"),
             p: Plane = Plane("p"),
             a: Airport = Airport("a")):
        precond = [self.at(c, a), self.at(p, a)]
        effect = [~self.at(c, a), self.in_(c, p)]
        return precond, effect

    @action
    def unload(self,
               c: Cargo = Cargo("c"),
               p: Plane = Plane("p"),
               a: Airport = Airport("a")):
        precond = [self.in_(c, p), self.at(p, a)]
        effect = [self.at(c, a), ~self.in_(c, p)]
        return precond, effect

    @action
    def fly(self,
            p: Plane = Plane("p"),
            orig: Airport = Airport("orig"),
            dest: Airport = Airport("dest")):
        precond = [self.at(p, orig)]
        effect = [~self.at(p, orig), self.at(p, dest)]
        return precond, effect


class AirCargoProblem(AirCargoDomain):

    def __init__(self):
        self.cargos = [AirCargoDomain.Cargo(x)
                       for x in ["C1", "C2"]]
        self.planes = [AirCargoDomain.Plane(x)
                       for x in ["P1", "P2"]]
        self.airports = [AirCargoDomain.Airport(x)
                         for x in ["SFO", "JFK"]]

    @init
    def init(self):
        at = [self.at("C1", "SFO"), self.at("C2", "JFK"),
              self.at("P1", "SFO"), ]
        return at

    @goal
    def goal(self):
        return [self.at("C1", "JFK"), self.at("C2", "SFO")]
