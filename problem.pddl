(define
	(problem grid_world)
	(:domain somedomain)
	(:objects
		agent1 - agent
		x0 x1 - x
	)
	(:init (and (at agent1 x0 y0) (is_occupied x0 y1)))
	(:goal (at agent1 x1 y1))
)
