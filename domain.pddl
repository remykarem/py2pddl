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
		(is_occupied ?x - x ?y - y)
	)
	(:action forward
		:parameters ()
		:precondition (at ?agent ?x_old ?y) (not (is_occupied ?x_new ?y)))
		:effect (not (at ?agent ?x_old ?y)) (at ?agent ?x_new ?y))
	)
	(:action up
		:parameters ()
		:precondition (at ?agent ?x_old ?y_old) (not (is_occupied ?x_new ?y_new)))
		:effect (not (at ?agent ?x_old ?y_old)) (at ?agent ?x_new ?y_new))
	)
)