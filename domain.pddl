(define
	(domain grid_world)
	(:requirements :strips :typing)
	(:types
		agent
		x
		y
	)
	(:predicates
		(at ?agent - agent ?x - x ?y - y)
		(occupied ?x - x ?y - y)
	)
	(:action forward
		:parameters (?agent - agent ?xold - x ?y - y ?xnew - x)
		:precondition (and (at ?agent ?xold ?y) (not (occupied ?xnew ?y)))
		:effect (and (not (at ?agent ?xold ?y)) (at ?agent ?xnew ?y))
	)
	(:action up
		:parameters (?agent - agent ?xold - x ?yold - y ?xnew - x ?ynew - y)
		:precondition (and (at ?agent ?xold ?yold) (not (occupied ?xnew ?ynew)))
		:effect (and (not (at ?agent ?xold ?yold)) (at ?agent ?xnew ?ynew))
	)
)