(define (domain self-parking)
 (:requirements :typing :equality :strips)
 (:types car curb street)
 (:predicates 
    (at-curb ?car - car ?curb - curb) 
    (at-street ?car - car ?street - street)
    (curb-clear ?curb - curb)
    (street-clear ?street - street)
    (parallel ?curb - curb ?street - street)
 )
 
    (:action move-curb-to-curb
		:parameters (?car - car ?curbsrc ?curbdest - curb ?strsrc ?strdest - street)
		:precondition (and 
			(curb-clear ?curbdest)
			(street-clear ?strdest)
			(street-clear ?strsrc)
			(at-curb ?car ?curbsrc)
			(parallel ?curbsrc ?strsrc)
			(parallel ?curbdest ?strdest)
			(not (= ?strsrc ?strdest))
		)
		:effect (and 
			(not (curb-clear ?curbdest))
			(curb-clear ?curbsrc)
			(at-curb ?car ?curbdest)
			(not (at-curb ?car ?curbsrc))
		)
	)
	
    (:action move-street-to-street
		:parameters (?car - car ?strsrc ?strdest - street)
		:precondition (and 
			(street-clear ?strdest)
			(at-street ?car ?strsrc)
		)
		:effect (and 
			(not (street-clear ?strdest))
			(street-clear ?strsrc)
			(at-street ?car ?strdest)
			(not (at-street ?car ?strsrc))
		)
	)

    (:action move-street-to-curb
		:parameters (?car - car ?strsrc ?strdest - street ?curbdest - curb)
		:precondition (and 
			(curb-clear ?curbdest)
			(at-street ?car ?strsrc)
			(street-clear ?strdest)
			(parallel ?curbdest ?strdest)
		)
		:effect (and 
			(not (curb-clear ?curbdest))
			(street-clear ?strsrc)
			(at-curb ?car ?curbdest)
			(not (at-street ?car ?strsrc))
		)
	)
	
    (:action move-same-street-to-curb
		:parameters (?car - car ?strsrc - street ?curbdest - curb)
		:precondition (and 
			(curb-clear ?curbdest)
			(at-street ?car ?strsrc)
			(parallel ?curbdest ?strsrc)
		)
		:effect (and 
			(not (curb-clear ?curbdest))
			(street-clear ?strsrc)
			(at-curb ?car ?curbdest)
			(not (at-street ?car ?strsrc))
		)
	)
	
    (:action move-curb-to-street
		:parameters (?car - car ?curbsrc - curb ?strsrc ?strdest - street)
		:precondition (and 
			(street-clear ?strdest)
			(street-clear ?strsrc)
			(at-curb ?car ?curbsrc)
		    (parallel ?curbsrc ?strsrc)
			;(parallel ?curbdest ?strdest)
			;(not (= ?strsrc ?strdest))
		)
		:effect (and 
			(not (street-clear ?strdest))
			(curb-clear ?curbsrc)
			(not (at-curb ?car ?curbsrc))
			(at-street ?car ?strdest)
		)
	)
)

