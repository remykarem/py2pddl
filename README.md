# py2pddl (Python to PDDL)

Design:

As a user, I want to be able to

* define the domain and problem simply.
* be warned with pylint static checking on wrong types
* be warned with type checking while parsing
* not have any silly errors in the generated pddl file

## Defining the domain

1. Inherit from `Domain`
2. Define types at the top (here, it's `Block`)
3. Define predicates as methods decorated with `@predicate`
4. Define actions as methods decorated with `@action`

```python
from py2pddl import Domain, create_type
from py2pddl import predicate, action

class BlocksDomain(Domain):

    Block = create_type("Block")

    @predicate
    def on(self, x: Block = None, y: Block = None):
        pass

    @predicate
    def holding(self, x: Block = None):
        pass

    @action
    def pick_up(self, x: Block = Block("x")):
        precond = [self.on(x), self.holding(x)]
        effect = [~self.on(x), ~self.holding(x)]
        return precond, effect
```

## Defining the problem

1. Inherit from `BlocksDomain`, the class above
2. Define objects in `__init__`
3. Define init with a method decorated with `@init`
4. Define goal with a method decorated with `@goal`

```python
from py2pddl import goal, init

class BlocksProblem(BlocksDomain):

    def __init__(self):
        self.blocks = [BlocksDomain.Block(x) for x in list("DBAC")]

    @init
    def init(self):
        on = [self.on(b) for b in self.blocks]
        clear = [self.clear(b) for b in self.blocks]
        return on + ontable

    @goal
    def goal(self):
        return [self.on("D", "C"),
                self.on("C", "B"),
                self.on("B", "A")]
```
