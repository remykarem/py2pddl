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