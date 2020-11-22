(define
	(problem blocks)
	(:domain blocks)
	(:objects
		a b c d - block
	)
	(:init (clear a) (clear b) (ontable a) (clear b))
	(:goal (on a b))
)
