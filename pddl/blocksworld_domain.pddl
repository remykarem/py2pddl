(define
	(domain blocks)
	(:requirements :strips :typing)
	(:types
		block
	)
	(:predicates
		(clear ?x - block)
		(holding ?x - block)
		(on ?x - block ?y - block)
		(ontable ?x - block)
	)
	(:action pickup
		:parameters (?x - block)
		:precondition (and (clear ?x) (ontable ?x))
		:effect (and (not (ontable ?x)) (not (clear ?x)) (holding ?x))
	)
	(:action putdown
		:parameters (?x - block)
		:precondition (holding ?x)
		:effect (and (not (holding ?x)) (clear ?x) (ontable ?x))
	)
	(:action stack
		:parameters (?top - block ?btm - block)
		:precondition (and (holding ?top) (clear ?btm))
		:effect (and (not (holding ?top)) (not (clear ?btm)) (clear ?top) (on ?top ?btm))
	)
	(:action unstack
		:parameters (?top - block ?btm - block)
		:precondition (and (on ?top ?btm) (clear ?top))
		:effect (and (holding ?top) (clear ?btm) (not (clear ?top)) (not (on ?top ?btm)))
	)
)