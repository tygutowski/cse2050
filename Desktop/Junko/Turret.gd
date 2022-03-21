extends Node2D

var toggle = false

func shoot():
	toggle = !toggle
	$RayCast2D.set_is_casting(toggle)
