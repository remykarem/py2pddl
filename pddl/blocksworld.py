from typing import Tuple
from py2pddl import Domain, create_type
from py2pddl import predicate, action, goal, init


class BlocksDomain(Domain):

    Block = create_type("Block")

    @predicate(Block, Block)
    def on(self, x, y):
        pass

    @predicate(Block)
    def ontable(self, x):
        pass

    @predicate(Block)
    def clear(self, x):
        pass

    @predicate(Block)
    def holding(self, x):
        pass

    @action(Block)
    def pickup(self, x):
        precond = [self.clear(x), self.ontable(x)]
        effect = [~self.ontable(x),
                  ~self.clear(x),
                  self.holding(x)]
        return precond, effect

    @action(Block)
    def putdown(self, x):
        precond = [self.holding(x)]
        effect = [~self.holding(x),
                  self.clear(x),
                  self.ontable(x)]
        return precond, effect

    @action(Block, Block)
    def stack(self, top, btm):
        precond = [self.holding(top), self.clear(btm)]
        effect = [~self.holding(top),
                  ~self.clear(btm),
                  self.clear(top),
                  self.on(top, btm)]
        return precond, effect

    @action(Block, Block)
    def unstack(self, top, btm):
        precond = [self.on(top, btm), self.clear(top)]
        effect = [self.holding(top),
                  self.clear(btm),
                  ~self.clear(top),
                  ~self.on(top, btm)]
        return precond, effect


class BlocksProblem(BlocksDomain):

    def __init__(self):
        self.blocks = BlocksDomain.Block.create_objs(list("abcd"))

    @init
    def init(self):
        clear = [self.clear(self.blocks["a"]), self.clear(self.blocks["b"])]
        ontable = [self.ontable(self.blocks["a"]), self.clear(self.blocks["b"])]
        return clear + ontable

    @goal
    def goal(self):
        return [self.on(self.blocks["a"], self.blocks["b"])]
