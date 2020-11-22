(define
	(domain somedomain)
	(:requirements :strips :typing)
	(:types
		city physobj place - object
		package vehicle - physobj
		airplane truck - vehicle
		airport location - place
	)
	(:predicates
		(at ?physobj - physobj ?place - place)
		(in ?pkg - package ?veh - vehicle)
		(in-city ?place - place ?city - city)
	)
	(:action drive-truck
		:parameters (?truck - truck ?loc_from - place ?loc_to - place ?city - city)
		:precondition (and (at ?truck ?loc-from) (in-city ?loc-from ?city) (in-city ?loc-to ?city))
		:effect (and (not (at ?truck ?loc-from)) (at ?truck ?loc-to))
	)
	(:action fly-airplane
		:parameters (?airplane - airplane ?loc_from - airport ?loc_to - airport)
		:precondition (at ?airplane ?loc-from)
		:effect (and (not (at ?airplane ?loc-from)) (at ?airplane ?loc-to))
	)
	(:action load-airplane
		:parameters (?pkg - package ?airplane - airplane ?loc - place)
		:precondition (and (at ?pkg ?loc) (at ?airplane ?loc))
		:effect (and (not (at ?pkg ?loc)) (in ?pkg ?airplane))
	)
	(:action load-truck
		:parameters (?pkg - package ?truck - truck ?loc - place)
		:precondition (and (at ?truck ?loc) (at ?pkg ?loc))
		:effect (and (not (at ?pkg ?loc)) (in ?pkg ?truck))
	)
	(:action unload-airplane
		:parameters (?pkg - package ?airplane - airplane ?loc - place)
		:precondition (and (in ?pkg ?airplane) (at ?airplane ?loc))
		:effect (and (not (in ?pkg ?airplane)) (at ?pkg ?loc))
	)
	(:action unload-truck
		:parameters (?pkg - package ?truck - truck ?loc - place)
		:precondition (and (at ?truck ?loc) (in ?pkg ?truck))
		:effect (and (not (in ?pkg ?truck)) (at ?pkg ?loc))
	)
)