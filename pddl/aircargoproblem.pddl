(define
	(problem someproblem)
	(:domain somedomain)
	(:objects
		sfo jfk - airport
		c1 c2 - cargo
		p1 p2 - plane
	)
	(:init (cargo-at c1 sfo) (cargo-at c2 jfk) (plane-at p1 sfo) (plane-at p2 jfk))
	(:goal (and (cargo-at c1 jfk) (cargo-at c2 sfo)))
)
