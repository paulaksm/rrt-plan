(define (problem BLOCKS-4-0)
(:domain blocks)
(:objects 
    D - block 
    B - block 
    A - block 
    C - block 
)
(:init 
    (CLEAR C) 
    (CLEAR A) 
    (CLEAR B) 
    (CLEAR D) 
    (ONTABLE C) 
    (ONTABLE A)
    (ONTABLE B)
    (ONTABLE D)
    (HANDEMPTY)
) 
(:goal 
    (and 
        (ON D C) 
        (ON C B) 
        (ON B A) 
)))
