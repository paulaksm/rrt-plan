;; PDDL Problem File

(define (problem room03)
	
	(:domain robot)
	
	(:objects
		room1 room2 room3 - room
		box1 box2 box3 - box
		left right - arm
	)

	(:init
		(robot-at room1)
		(box-at box1 room1)
		(box-at box2 room1)
		(box-at box3 room1)
		(free left)
		(free right)
	)

	(:goal
		(and
			(box-at box1 room1)
			(box-at box2 room2)
			(box-at box3 room3)
		)
	)
)

