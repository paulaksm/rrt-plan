(define (problem FR_1_1)

	(:domain first-response)
	(:objects  
		l1  - location
		f1 - fire_unit
	)

	(:init 
		(water-at l1)
		(fire l1)
		(adjacent l1 l1)
		(fire-unit-at f1 l1)
	)

	(:goal (and  (nfire l1)))
)
