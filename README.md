# py2pddl (Python to PDDL)

Design:

As a user, I want to be able to

* define the domain and problem simply.
* be warned with pylint static checking on wrong types
* be warned with type checking while parsing
* not have any silly errors in the generated pddl file

## Defining the domain

In `flying.py`,

1. Inherit from `Domain`
2. Define types at the top (here, it's `Block`)
3. Define predicates as methods decorated with `@predicate`
4. Define actions as methods decorated with `@action`

```python
from py2pddl import Domain, create_type
from py2pddl import predicate, action

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
```

## Defining the problem

In `flying.py`,

1. Inherit from `BlocksDomain`, the class above
2. Define objects in `__init__`
3. Define init with a method decorated with `@init`
4. Define goal with a method decorated with `@goal`

```python
from py2pddl import goal, init

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
```

To generate the PDDL files

```python
from flying import AirCargoProblem
p = AirCargoProblem()
p.generate_domain_pddl()
p.generate_problem_pddl()
```

Here is the generated `domain.pddl` file.

```text
(define
	(domain grid_world)
	(:requirements :strips :typing)
	(:types
		airport
		cargo
		plane
	)
	(:predicates
		(at ?c - cargo ?p - plane)
		(in_ ?c - cargo ?p - plane)
	)
	(:action fly
		:parameters (?p - plane ?orig - airport ?dest - airport)
		:precondition (at ?p ?orig)
		:effect (and (not (at ?p ?orig)) (at ?p ?dest))
	)
	(:action load
		:parameters (?c - cargo ?p - plane ?a - airport)
		:precondition (and (at ?c ?a) (at ?p ?a))
		:effect (and (not (at ?c ?a)) (in_ ?c ?p))
	)
	(:action unload
		:parameters (?c - cargo ?p - plane ?a - airport)
		:precondition (and (in_ ?c ?p) (at ?p ?a))
		:effect (and (at ?c ?a) (not (in_ ?c ?p)))
	)
)
```

And here is the generated `problem.pddl` file.

```text
(define
	(problem grid_world)
	(:domain somedomain)
	(:objects
		SFO JFK - airport
		C1 C2 - cargo
		P1 P2 - plane
	)
	(:init (at C1 SFO) (at C2 JFK) (at P1 SFO))
	(:goal (and (at C1 JFK) (at C2 SFO)))
)
```
