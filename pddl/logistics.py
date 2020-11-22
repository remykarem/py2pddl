from py2pddl import Domain, create_type
from py2pddl import predicate, action, goal, init


class LogisticsDomain(Domain):

    Object = create_type("Object")
    City = create_type("City", Object)
    Place = create_type("Place", Object)
    Physobj = create_type("Physobj", Object)

    Airport = create_type("Airport", Place)
    Location = create_type("Location", Place)

    Package = create_type("Package", Physobj)
    Vehicle = create_type("Vehicle", Physobj)

    Truck = create_type("Truck", Vehicle)
    Airplane = create_type("Airplane", Vehicle)

    @predicate(Place, City)
    def in_city(self, place, city):
        """Complete the method signature and specify
        the respective types in the decorator"""

    @predicate(Physobj, Place)
    def at(self, physobj, place):
        """Complete the method signature and specify
        the respective types in the decorator"""

    @predicate(Package, Vehicle)
    def in_(self, pkg, veh):
        """Complete the method signature and specify
        the respective types in the decorator"""

    @action(Package, Truck, Place)
    def load_truck(self, pkg, truck, loc):
        precond: list = [self.at(truck, loc), self.at(pkg, loc)]
        effect: list = [~self.at(pkg, loc), self.in_(pkg, truck)]
        return precond, effect

    @action(Package, Airplane, Place)
    def load_airplane(self, pkg, airplane, loc):
        precond: list = [self.at(pkg, loc), self.at(airplane, loc)]
        effect: list = [~self.at(pkg, loc), self.in_(pkg, airplane)]
        return precond, effect

    @action(Package, Truck, Place)
    def unload_truck(self, pkg, truck, loc):
        precond: list = [self.at(truck, loc), self.in_(pkg, truck)]
        effect: list = [~self.in_(pkg, truck), self.at(pkg, loc)]
        return precond, effect

    @action(Package, Airplane, Place)
    def unload_airplane(self, pkg, airplane, loc):
        precond: list = [self.in_(pkg, airplane), self.at(airplane, loc)]
        effect: list = [~self.in_(pkg, airplane), self.at(pkg, loc)]
        return precond, effect

    @action(Airplane, Airport, Airport)
    def fly_airplane(self, airplane, loc_from, loc_to):
        precond: list = [self.at(airplane, loc_from)]
        effect: list = [~self.at(airplane, loc_from),
                        self.at(airplane, loc_to)]
        return precond, effect

    @action(Truck, Place, Place, City)
    def drive_truck(self, truck, loc_from, loc_to, city):
        precond: list = [self.at(truck, loc_from), self.in_city(loc_from, city),
                         self.in_city(loc_to, city)]
        effect: list = [~self.at(truck, loc_from), self.at(truck, loc_to)]
        return precond, effect


class LogisticsProblem(LogisticsDomain):

    def __init__(self):
        """To fill in"""
        super().__init__()
        self.trucks = LogisticsDomain.Truck.create_objs(["truck"])
        self.airplanes = LogisticsDomain.Airplane.create_objs(["plane"])
        self.airports = LogisticsDomain.Airport.create_objs(["cdg", "lhr"])
        self.locations = LogisticsDomain.Location.create_objs(["north", "south"])
        self.cities = LogisticsDomain.City.create_objs(["london", "paris"])
        self.pkgs = LogisticsDomain.Package.create_objs(["p1", "p2"])

    @init
    def init(self) -> list:
        in_city = [
            self.in_city(self.airports["cdg"], self.cities["paris"]),
            self.in_city(self.airports["lhr"], self.cities["london"]),
            self.in_city(self.locations["north"], self.cities["paris"]),
            self.in_city(self.locations["south"], self.cities["paris"]),
        ]
        at = [
            self.at(self.airplanes["plane"], self.airports["lhr"]),
            self.at(self.trucks["truck"], self.airports["cdg"]),
            self.at(self.pkgs["p1"], self.airports["lhr"]),
            self.at(self.pkgs["p2"], self.airports["lhr"]),
        ]
        return in_city + at

    @goal
    def goal(self) -> list:
        # To fill in
        # Return type is a list
        return [self.at(self.pkgs["p1"], self.locations["north"]),
                self.at(self.pkgs["p2"], self.locations["south"])]
