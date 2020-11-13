from typing import Type
from py2pddl import Domain, create_type
from py2pddl import predicate, action, goal, init


class EightpuzzleDomain(Domain):

    Tile = create_type("Tile")
    Loc = create_type("Loc")

    @predicate(Tile, Loc)
    def on(self, t, loc):
        """Complete the method signature"""

    @predicate(Loc)
    def blank(self, loc):
        """Complete the method signature"""

    @predicate(Loc, Loc)
    def adjacent(self, loc1, loc2):
        """Complete the method signature"""

    @action(Tile, Loc, Loc)
    def slide(self, t, loc1, loc2):
        """This should be a pass"""
        precond: list = [self.on(t, loc1), self.blank(loc2),
                         self.adjacent(loc1, loc2)]
        effect: list = [self.on(t, loc2), self.blank(loc1),
                        ~self.on(t, loc1), ~self.blank(loc2)]
        return precond, effect


class EightpuzzleProblem(EightpuzzleDomain):

    def __init__(self):
        self.locs = [EightpuzzleDomain.Loc(f"loc{i}")
                     for i in range(1, 9)]
        self.tiles = [EightpuzzleDomain.Tile(f"tile{i}")
                      for i in range(1, 9)]

    @init
    def init(self) -> list:
        tiles = [7, 2, 4, 5, 6, 8, 3, 1]
        locs = [1, 2, 3, 4, 6, 7, 8, 9]

        on = [self.on(EightpuzzleDomain.Tile(f"tile{tile}"), f"loc{loc}")
              for tile, loc in zip(tiles, locs)]
        blank = [self.blank("loc5")]

        adjacent_locs_ = [f"tile{i}" for i in [1, 2, 3, 6, 9, 8, 7, 4, 1]]
        adjacent_locs = [adjacent_locs_[i:i+2]
                         for i in range(len(adjacent_locs_)-1)]
        adjacent = [self.adjacent(*adj) for adj in adjacent_locs]
        return on + blank + adjacent

    @goal
    def goal(self) -> list:
        tiles = list(range(1, 9))
        locs = list(range(2, 10))

        adjacent_locs_ = [f"tile{i}" for i in [2, 3, 6, 5, 4, 7, 8, 9]]
        adjacent_locs = [adjacent_locs_[i:i+2]
                         for i in range(len(adjacent_locs_)-1)]
        adjacent_locs += [["tile2", "tile5"],
                          ["tile5", "tile8"], ["tile6", "tile9"]]
        adjacent = [self.adjacent(*adj) for adj in adjacent_locs]

        on = [self.on(f"tile{tile}", f"loc{loc}")
              for tile, loc in zip(tiles, locs)]
        blank = [self.blank("loc1")]

        return on + blank + adjacent
