(define
	(problem grid_world)
	(:domain grid_world)
	(:objects
		agent1 - agent
		x0 x1 - x
		y0 y1 - y
	)
	(:init (at agent1 x0 y0) (occupied x0 y1))
	(:goal (at agent1 x1 y1))
)
