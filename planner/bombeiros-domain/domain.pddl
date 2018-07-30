(define (domain first-response)
	(:requirements :strips :equality :typing)
  
	(:types location fire_unit)
 
	(:predicates 
		(fire ?l - location)
		(water-at ?l - location)
		(adjacent ?l1 ?l2 - location)
		(fire-unit-at ?u - fire_unit ?l - location)
		(have-water ?u - fire_unit)
		(nfire ?l - location)
	)

	(:action drive-fire-unit
		:parameters (?u - fire_unit ?from ?to - location)
		:precondition (and (fire-unit-at ?u ?from) (adjacent ?to ?from) (not (= ?to ?from)) (not (fire ?to)) )
		:effect (and (fire-unit-at ?u ?to) (not (fire-unit-at ?u ?from)))
	)

	(:action load-fire-unit
		:parameters (?u - fire_unit ?l - location)
		:precondition (and (fire-unit-at ?u ?l) (water-at ?l))
		:effect (have-water ?u)
	)

	(:action unload-fire-unit
		:parameters (?u - fire_unit ?l ?l1 - location)
		:precondition (and (fire-unit-at ?u ?l) (adjacent ?l1 ?l) (have-water ?u) (fire ?l1))
		:effect (and (not (have-water ?u)) (nfire ?l1) (not (fire ?l1)))
	)
  
)
