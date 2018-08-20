(define   (problem parking)
  (:domain self-parking)
  (:objects
     car_0  car_1  car_2  car_3 - car
     curb_0 curb_1 curb_2 - curb
     str_0 str_1 str_2 - street
  )
  (:init
    (at-curb car_3 curb_0)
    (at-curb car_2 curb_1)
    (at-street car_0 str_0)
    (at-street car_1 str_1)
    (curb-clear curb_2)
    (street-clear str_2)
    (parallel curb_0 str_0)
    (parallel curb_1 str_1)
    (parallel curb_2 str_2)
  )
  (:goal
    (and
      (at-curb car_0 curb_0)
      (at-street car_3 str_0)
      (at-curb car_1 curb_1)
      (at-curb car_2 curb_2)
    )
  )
)
; =========== INIT =========== 
;  curb_0: car_3 car_0 
;  curb_1: car_2 car_1 
;  curb_2: 
; ========== /INIT =========== 

; =========== GOAL =========== 
;  curb_0: car_0 car_3 
;  curb_1: car_1 
;  curb_2: car_2 
; =========== /GOAL =========== 
