extends Area2D

onready var player_camera = get_node("../../PlayerCamera")
onready var animation_camera = get_node("../../AnimationCamera")
onready var tween = animation_camera.get_node("Tween")

var camera_moving = true
var initialized = false
var collision
onready var player = get_parent()

onready var level = get_parent().get_parent()

func _ready():
	tween.connect("tween_completed", self, "tween_completed")
	tween.connect("tween_started", self, "tween_started")
	var error_code = connect("mouse_entered", self, "mouse_entered")
	if error_code != 0:
		print("ERROR: ", error_code)
	var error_code2 = connect("mouse_exited", self, "mouse_exited")
	if error_code2 != 0:
		print("ERROR: ", error_code)
	var error_code3 = connect("area_entered", self, "room_entered")
	if(error_code3 != 0):
		print("ERROR")
func room_entered(area):
	# if an area enters named "RoomCollider" (only the player has this area)
	if("RoomArea" in area.name && Global.playing):
		var topleft = area.get_node("TopLeft")
		var bottomright = area.get_node("BottomRight")
		pan_camera(topleft, bottomright)

func _process(_delta):
	# while the camera isn't in its animation state, set it to the players position
	#print(camera_moving)
	if(!camera_moving):
		player_camera.global_position = player.global_position

func tween_completed(_object, _key):
	# once the animation is completed, set the player's physics back to normal
	player_camera.current = true
	camera_moving = false
	player.set_physics_process(true)
	player.set_process(true)

func tween_started(_object, _key):
	# when the animation starts, pause the player's physics
	camera_moving = true
	player.set_physics_process(false)
	player.set_process(false)

func pan_camera(topleft, bottomright):
	# and set it as the current camera
	animation_camera.current = true
	# defines where initial camera center is
	# bug with godot doesnt define where camera's position is, even if its out of bounds
	player_camera.global_position.x = clamp(player_camera.global_position.x, player_camera.limit_left + ProjectSettings.get_setting("display/window/size/width")/2, player_camera.limit_right - ProjectSettings.get_setting("display/window/size/width")/2)
	player_camera.global_position.y = clamp(player_camera.global_position.y, player_camera.limit_top + ProjectSettings.get_setting("display/window/size/height")/2, player_camera.limit_bottom - ProjectSettings.get_setting("display/window/size/height")/2)
	# set the animation camera's position to the current camera
	animation_camera.global_position = player_camera.global_position
	# then sets the new limits
	player_camera.limit_top = topleft.global_position.y
	player_camera.limit_bottom = bottomright.global_position.y
	player_camera.limit_left = topleft.global_position.x
	player_camera.limit_right = bottomright.global_position.x
	# and determines where the new camera center is (destination)
	player_camera.global_position.x = clamp(player.global_position.x, player_camera.limit_left + ProjectSettings.get_setting("display/window/size/width")/2, player_camera.limit_right - ProjectSettings.get_setting("display/window/size/width")/2)
	player_camera.global_position.y = clamp(player.global_position.y, player_camera.limit_top + ProjectSettings.get_setting("display/window/size/height")/2, player_camera.limit_bottom - ProjectSettings.get_setting("display/window/size/height")/2)
	#yield(get_tree(), "idle_frame")
	# moves animation_camera to player_camera
	tween.interpolate_property(animation_camera, "global_position",
		animation_camera.global_position, player_camera.global_position, .5,
		Tween.TRANS_LINEAR, Tween.EASE_IN_OUT)
	tween.start()
