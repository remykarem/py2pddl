(define
	(problem someproblem)
	(:domain somedomain)
	(:objects
		SFO JFK - airport
		C1 C2 - cargo
		P1 P2 - plane
	)
	(:init (at C1 SFO) (at C2 JFK) (at P1 SFO))
	(:goal (and (at C1 JFK) (at C2 SFO)))
)
