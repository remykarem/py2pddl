(define
	(domain somedomain)
	(:requirements :strips :typing)
	(:types
		airport
		cargo
		plane
	)
	(:predicates
		(cargo-at ?c - cargo ?a - airport)
		(in ?c - cargo ?p - plane)
		(plane-at ?p - plane ?a - airport)
	)
	(:action fly
		:parameters (?p - plane ?orig - airport ?dest - airport)
		:precondition (plane-at ?p ?orig)
		:effect (and (not (plane-at ?p ?orig)) (plane-at ?p ?dest))
	)
	(:action load
		:parameters (?c - cargo ?p - plane ?a - airport)
		:precondition (and (cargo-at ?c ?a) (plane-at ?p ?a))
		:effect (and (not (cargo-at ?c ?a)) (in ?c ?p))
	)
	(:action unload
		:parameters (?c - cargo ?p - plane ?a - airport)
		:precondition (and (in ?c ?p) (plane-at ?p ?a))
		:effect (and (cargo-at ?c ?a) (not (in ?c ?p)))
	)
)