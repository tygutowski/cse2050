extends RayCast2D

var is_casting := true setget set_is_casting

func ready() -> void:
	set_physics_process(false)
	$Line2D.points[1] = Vector2.ZERO
 
func _physics_process(delta):
	var cast_point := cast_to
	force_raycast_update()
	
	if is_colliding():
		cast_point = to_local(get_collision_point())
		if(get_collider().name == "Player"):
			#get_collider().die(1)
			get_collider().take_damage(10, 1)
	cast_point += Vector2(1,1)
	$Line2D.points[1] = cast_point
	
	
func set_is_casting(cast: bool) -> void:
	is_casting = cast
	if(is_casting):
		appear()
	else:
		disappear()
	set_physics_process(is_casting)
func appear() -> void:
	$Tween.stop_all()
	$Tween.interpolate_property($Line2D, "width", 0, 5.0, 0.2)
	$Tween.start()

func disappear() -> void:
	$Tween.stop_all()
	$Tween.interpolate_property($Line2D, "width", 5.0, 0.0, 0.1)
	$Tween.start()
