from py2pddl import Domain, create_type, create_objs
from py2pddl import predicate, action
from py2pddl import goal, init


class AirCargoDomain(Domain):

    Plane = create_type("Plane")
    Cargo = create_type("Cargo")
    Airport = create_type("Airport")

    @predicate(Cargo, Airport)
    def cargo_at(self, c, a):
        pass

    @predicate(Plane, Airport)
    def plane_at(self, p, a):
        pass

    @predicate(Cargo, Plane)
    def in_(self, c, p):
        pass

    @action(Cargo, Plane, Airport)
    def load(self, c, p, a):
        precond = [self.cargo_at(c, a), self.plane_at(p, a)]
        effect = [~self.cargo_at(c, a), self.in_(c, p)]
        return precond, effect

    @action(Cargo, Plane, Airport)
    def unload(self, c, p, a):
        precond = [self.in_(c, p), self.plane_at(p, a)]
        effect = [self.cargo_at(c, a), ~self.in_(c, p)]
        return precond, effect

    @action(Plane, Airport, Airport)
    def fly(self, p, orig, dest):
        precond = [self.plane_at(p, orig)]
        effect = [~self.plane_at(p, orig), self.plane_at(p, dest)]
        return precond, effect


class AirCargoProblem(AirCargoDomain):

    def __init__(self):
        super().__init__()
        self.cargos = create_objs(AirCargoDomain.Cargo, [1, 2], True, "c")
        self.planes = create_objs(AirCargoDomain.Plane, [1, 2], True, "p")
        self.airports = create_objs(
            AirCargoDomain.Airport, ["sfo", "jfk"], False)

    @init
    def init(self):
        at = [self.cargo_at(self.cargos["c1"], self.airports["sfo"]),
              self.cargo_at(self.cargos["c2"], self.airports["jfk"]),
              self.plane_at(self.planes["p1"], self.airports["sfo"]),
              self.plane_at(self.planes["p2"], self.airports["jfk"]), ]
        return at

    @goal
    def goal(self):
        return [self.cargo_at(self.cargos["c1"], self.airports["jfk"]),
                self.cargo_at(self.cargos["c2"], self.airports["sfo"])]
