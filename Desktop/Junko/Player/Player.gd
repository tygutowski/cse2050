extends KinematicBody2D

onready var animation_player = get_node("AnimationPlayer")
#onready var slide_particles = get_node("SlideParticles")
#onready var jump_particles = get_node("JumpParticles")
onready var sprite = get_node("Sprite")

const DEATH_TYPE = ["generic", "laser"]

var velocity = Vector2.ZERO
export(int) var max_run = 100
export(int) var run_accel = 800
export(int) var gravity = 1000
export(int) var max_fall = 160
export(int) var jump_force = -160
export(int) var jump_hold_time = 0.2
export(int) var wall_jump_outwards_force = 120
var local_hold_time = 0
var can_coyote_jump = false
var time_in_air = 0
var coyote_frame_timer = 0
var previous_positions = []
var previous_directions = []
var previous_animations = []
var previous_velocities = []
var direction = 0
var recalling = false
var jumping = false
export(int) var dash_force = 300
var dashing = false
var long_jumping = false
var last_direction = 1
var dash_frame_timer = 0
var jumps_remaining = 0
var initial_position
var dying = false
var health = 100
var taking_damage = 0
var max_health = 100

onready var death_camera_sweep = get_node("../CanvasLayer/ColorRect")
func _ready():
	initial_position = position

func _process(delta):
	get_inputs()
	if(Global.playing && !dying):
		manage_jump(delta)
		manage_velocity(delta)
		manage_animations()
		dash_frame_timer -= 1
		coyote_frame_timer -= 1
		taking_damage -= 1

func manage_animations():
	if(direction > 0):
		sprite.flip_h = false
	elif(direction < 0):
		sprite.flip_h = true
	
	if(is_on_floor()):
		$AnimationTree.set("parameters/in_air/current", 0)
	else:
		$AnimationTree.set("parameters/in_air/current", 1)
	if(velocity.y > 0):
		$AnimationTree.set("parameters/is_falling/current", 1)
	else:
		$AnimationTree.set("parameters/is_falling/current", 0)
	if(velocity.x == 0):
		$AnimationTree.set("parameters/is_running/current", 0)
	else:
		$AnimationTree.set("parameters/is_running/current", 1)
func get_inputs():
	# Movement inputs
	if(Input.is_action_just_pressed("ui_close")):
		get_tree().quit()
	if(Input.is_action_just_pressed("ui_pause")):
		Global.playing = !Global.playing
	jumping = Input.is_action_just_pressed("ui_select")
	long_jumping = Input.is_action_pressed("ui_select")
	dashing = Input.is_action_just_pressed("ui_dash")
	direction = (Input.get_action_strength("ui_right") - Input.get_action_strength("ui_left"))
	# UI inputs
func manage_jump(delta):
	# no longer emit sliding particles
	if(is_on_floor()):
		jumps_remaining = 2
	#slide_particles.emitting = false
	if is_on_floor(): #if youre on the ground, you cant coyote jump
		coyote_frame_timer = 3
	if is_on_floor() && dashing && dash_frame_timer <= 0:
		velocity.x = last_direction * dash_force
		dash_frame_timer = 15
	#elif !is_on_floor() && is_on_wall() && dashing && direction != 0:
	#	velocity.y = -400
		
		
	if jumping && (coyote_frame_timer >= 0 || jumps_remaining >= 1): #if youre on the ground and try to jump, you will
		velocity.y = jump_force
		local_hold_time = jump_hold_time
		coyote_frame_timer = 3
		#jump_particles.restart()
		#jump_particles.emitting = true
		jumps_remaining -= 1
		
		
	#elif(is_on_wall() && !is_on_floor() && velocity.y > 10 && direction < 0): # wall slide left
		#slide_particles.emitting = true
	#	velocity.y /= 1.2
	#elif(is_on_wall() && !is_on_floor() && velocity.y > 10 && direction > 0): # wall slide right
		#slide_particles.emitting = true
	#	velocity.y /= 1.2
	if local_hold_time > 0: #if you hold jump, you will fly further (even if you are coyote jumping)
		if long_jumping:
			#slide_particles.emitting = true
			velocity.y = jump_force
		else:
			#slide_particles.emitting = false
			local_hold_time = 0
	local_hold_time -= delta

func manage_velocity(delta):
	velocity.x = move_toward(velocity.x, max_run * direction, run_accel)
	velocity.y = move_toward(velocity.y, max_fall, gravity*delta)	
	velocity = move_and_slide(velocity, Vector2.UP)
	position.x = round(position.x)
	position.y = round(position.y)

func die(death_type):
	if(!dying):
		$AnimationTree.set("parameters/alive/current", 1)
		$AnimationTree.set("parameters/death_type/current", death_type)
		dying = true
		$DeathTimer.start()
		
func _on_Area2D_mouse_entered():
	pass # Replace with function body.

func _on_Area2D_mouse_exited():
	pass # Replace with function body.

func deathtimer_timeout():
	var dying_tween = death_camera_sweep.get_node("DyingTween")
	dying_tween.interpolate_property(death_camera_sweep.get_material(), "shader_param/progress", 0, 1, 1, Tween.TRANS_LINEAR, Tween.EASE_OUT)
	dying_tween.start()

func take_damage(number, damage_type):
	if(taking_damage <= 0):
		print("took damage")
		taking_damage = 5
		health -= number
		if(health < 0):
			health = 0
			die(damage_type)
		$AnimationTree.set("parameters/taking_damage/current", 0)
	else:
		print("between frames")

func _on_death_tween_completed(object, key):
	position = initial_position
	$AnimationTree.set("parameters/alive/current", 0)
	$AnimationTree.set("parameters/taking_damage/current", 1)
	$AnimationTree.set("parameters/in_air/current", 0)
	$AnimationTree.set("parameters/is_running/current", 0)
	var respawn_tween = death_camera_sweep.get_node("RespawnTween")
	respawn_tween.interpolate_property(death_camera_sweep.get_material(), "shader_param/progress", 1, 0, 1, Tween.TRANS_LINEAR, Tween.EASE_OUT)
	velocity = Vector2.ZERO
	respawn_tween.start()

func respawn_tween_completed(object, key):
	health = max_health
	dying = false
