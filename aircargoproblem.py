from typing import Tuple
from pddl import Domain, predicate, action, create_type
import pddl


class AirCargoDomain(Domain):

    Object = create_type("Object")

    City = create_type("City", Object)
    Place = create_type("Place", Object)
    PhysObj = create_type("PhysObj", Object)

    Airport = create_type("Airport", Place)
    Location = create_type("Location", Place)

    Package = create_type("Package", PhysObj)
    Vehicle = create_type("Vehicle", PhysObj)

    Truck = create_type("Truck", Vehicle)
    Airplane = create_type("Truck", Vehicle)

    predicates = ["at", "in_city", "in_"]

    @predicate
    def at(self, pkg: Package, loc: Location):
        pass

    @predicate
    def in_city(self, loc: Location, city: City):
        pass

    @predicate
    def in_(self, pkg: Package, veh: Vehicle):
        pass

    @action
    def load_airplane(self, pkg: Package, airplane: Airplane, loc: Place):
        precond = self.at(pkg, loc) and self.at(airplane, loc)
        effect = not self.at(pkg, loc) and self.in_(pkg, airplane)
        return precond, effect

    @action
    def unload_truck(self, pkg: Package, truck: Truck, loc: Place):
        precond = self.at(truck, loc) and self.in_(pkg, truck)
        effect = not self.in_(pkg, truck) and self.at(pkg, loc)
        return precond, effect


class AirCargoProblem(AirCargoDomain):

    plane = AirCargoDomain.Airplane("p")
    truck = AirCargoDomain.Truck("t")
    cdg = AirCargoDomain.Airport("cdg")
    lhr = AirCargoDomain.Airport("lhr")
    south = AirCargoDomain.Location("south")
    north = AirCargoDomain.Location("north")
    paris = AirCargoDomain.City("paris")
    london = AirCargoDomain.City("london")
    p1 = AirCargoDomain.Package("p1")
    p2 = AirCargoDomain.Package("p2")

    init = {
        "in_city": {(cdg, paris), (lhr, london), (north, paris),
                    (south, paris)},
        "at": {(plane, lhr), (truck, cdg), (p1, lhr), (p2, lhr)}
    }

    goal = {
        "at": {(p1, north), (p2, south)}
    }

    # pddl.compile(AirCargoProblem)
    # pddl.parse(AirCargoProblem)
