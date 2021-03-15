(define (domain set_table)
  (:requirements :typing)
  (:types location object)
  (:constants
    table small_shelf big_shelf - location
    cup_green plate_blue - object
  )
  (:predicates
    (agent-at ?l - location)
    (human-at ?l - location)
    (on ?x - object ?l - location)
    (agent-free)
    (agent-avoid-human)
    (agent-carry ?x - object)
    (human-carry ?x - object)
  )
  (:functions (move-time ?l - location))

  (:durative-action move
      :parameters (?l - location)
      :duration (= ?duration 240)
      :precondition (at end (not (human-at ?l)))
      :effect (and (at end (not (agent-at ?*))) (at end (agent-at ?l)))
  )
  (:durative-action pick
      :parameters (?x - object ?l - location)
      :duration (= ?duration 20)
      :precondition (and (at start (agent-at ?l)) (at start (on ?x ?l)) (at start (agent-free)) (at start (not (human-carry ?x)))) 
      :effect (and (at end (not (on ?x ?l))) (at end (not (agent-free))) (at end (agent-carry ?x)))
  )
  (:durative-action place
      :parameters (?x - object ?l - location)
      :duration (= ?duration 20)
      :precondition (and (at start (agent-at ?l)) (at start (agent-carry ?x)))  
      :effect (and (at end (not (agent-carry ?x))) (at end (on ?x ?l)) (at end (agent-free)))
  )
)