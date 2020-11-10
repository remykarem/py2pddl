from typing import Tuple
from py2pddl import Domain, create_type
from py2pddl import predicate, action, goal, init


class BlocksDomain(Domain):

    Block = create_type("Block")

    @predicate
    def on(self, x: Block = None, y: Block = None):
        pass

    @predicate
    def ontable(self, x: Block = None):
        pass

    @predicate
    def clear(self, x: Block = None):
        pass

    @predicate
    def handempty(self):
        pass

    @predicate
    def holding(self, x: Block = None):
        pass

    @action
    def pick_up(self, x: Block = Block("x")):
        precond = [self.clear(x), self.ontable(x), self.handempty()]
        effect = [~self.ontable(x),
                  ~self.clear(x),
                  ~self.handempty(),
                  self.holding(x)]
        return precond, effect

    @action
    def put_down(self, x: Block = Block("x")):
        precond = [self.holding(x)]
        effect = [~self.holding(x),
                  self.clear(x),
                  self.handempty(),
                  self.ontable(x)]
        return precond, effect

    @action
    def stack(self, x: Block = Block("x"), y: Block = Block("y")):
        precond = [self.holding(x), self.clear(y)]
        effect = [~self.holding(x),
                  ~self.clear(y),
                  self.clear(x),
                  self.handempty(),
                  self.on(x, y)]
        return precond, effect

    @action
    def unstack(self, x: Block = Block("x"), y: Block = Block("y")):
        precond = [self.on(x, y), self.clear(x), self.handempty()]
        effect = [self.holding(x),
                  self.clear(y),
                  ~self.clear(x),
                  ~self.handempty(),
                  ~self.on(x, y)]
        return precond, effect


class BlocksProblem(BlocksDomain):

    def __init__(self):
        self.blocks = [BlocksDomain.Block(x) for x in list("DBAC")]

    @init
    def init(self):
        clear = [self.clear(b) for b in self.blocks]
        ontable = [self.ontable(b) for b in self.blocks]
        handempty = [self.handempty()]
        return clear + ontable + handempty

    @goal
    def goal(self):
        return [self.on("D", "C"),
                self.on("C", "B"),
                self.on("B", "A")]
