extends CharacterBody3D

@export var move_speed := 5.0 / 2
@export var jump_velocity := 6.0
@export var gravity := 9.8 * 2
@export var nav_move_speed := 3.0  # Navigation movement speed

@onready var animated_sprite = $AnimatedSprite3D
@onready var elapsed_time := 0.0
@onready var nav_agent = $NavigationAgent3D

# Navigation state
var is_navigating := false
var target_position := Vector3.ZERO

func _ready():
	# Setup navigation agent
	await get_tree().physics_frame
	
	nav_agent.path_desired_distance = 0.5
	nav_agent.target_desired_distance = 0.5
	
	# Connect navigation signals	
	if !nav_agent.navigation_finished.is_connected(_on_navigation_finished):
		nav_agent.navigation_finished.connect(_on_navigation_finished)
		print("Navigation finished signal connected")
		
	#var a = get_node("../Window/TextPanel/HttpHost")  # 替換為 A 實際的節點路徑
	#a.connect("custom_signal", Callable(self, "test_func"))
		#

# Manual movement function
func move_character(input_dir: Vector2) -> void:
	input_dir = input_dir.normalized()
	var direction = (transform.basis.x * input_dir.x + transform.basis.z * input_dir.y)
	direction = direction.normalized()
	velocity.x = direction.x * move_speed / 3.0 * 2.0
	velocity.z = direction.z * move_speed
	
# Set navigation target position
func set_target_location(target_pos: Vector3) -> void:
	is_navigating = true
	target_position = target_pos
	nav_agent.target_position = target_pos
	
## Move to cursor position on space key
#func navigate_to_cursor() -> void:
	## Get mouse position
	#var mouse_pos = get_viewport().get_mouse_position()
	#var camera = get_viewport().get_camera_3d()
	#
	## Cast ray from camera to get target position
	#var from = camera.project_ray_origin(mouse_pos)
	#var to = from + camera.project_ray_normal(mouse_pos) * 1000
	#
	#var space_state = get_world_3d().direct_space_state
	#var query = PhysicsRayQueryParameters3D.create(from, to)
	#var result = space_state.intersect_ray(query)
	#
	#if result:
		## Set navigation target
		#set_target_location(result.position)
		#print("Navigating to: ", result.position)
#
# Move to specific coordinates
func  test_func():
	print("haha")

func navigate_to_position(pos: Vector3) -> void:
	set_target_location(pos)
	print("Navigating to specific position: ", pos)

func _physics_process(delta):
	# Handle navigation or manual movement
	if is_navigating and not nav_agent.is_navigation_finished():
		# Navigation movement
		var next_position = nav_agent.get_next_path_position()
		var direction = (next_position - global_position).normalized()
		
		# Set velocity for navigation
		velocity.x = direction.x * nav_move_speed
		velocity.z = direction.z * nav_move_speed
		
		# Face movement direction
		if direction != Vector3.ZERO:
			look_at(global_position + Vector3(direction.x, 0, direction.z), Vector3.UP)
	else:
		# Manual movement with directional keys
		var input_dir = Vector2.ZERO
		input_dir.x = Input.get_action_strength("ui_right") - Input.get_action_strength("ui_left")
		input_dir.y = Input.get_action_strength("ui_down") - Input.get_action_strength("ui_up")
		move_character(input_dir)  # 呼叫封裝後的移動函式
	
	# Handle space key for navigation OR jumping
	if Input.is_action_just_pressed("ui_accept"):
		if is_on_floor():
			# If on floor, use space for navigation
			#navigate_to_position(Vector3(-5, 0, 2))
			print("navagation")
		else:
			# Otherwise, cancel navigation and just keep jumping behavior
			is_navigating = false
	
	# Animation handling
	update_animation()
	
	# Gravity & jumping physics
	if not is_on_floor():
		velocity.y -= gravity * delta
		
	# Reset position if fallen
	if global_position.y < -5:
		global_position = Vector3(0, 10, 0)
		is_navigating = false
	
	# Apply movement
	move_and_slide()

# Animation logic
func update_animation():
	var input_dir = Vector2(
		Input.get_action_strength("ui_right") - Input.get_action_strength("ui_left"),
		Input.get_action_strength("ui_down") - Input.get_action_strength("ui_up")
	)
	
	# Update idle timer
	if input_dir == Vector2.ZERO and !is_navigating:
		elapsed_time += 1
	else:
		elapsed_time = 0
	
	# Play appropriate animation
	if is_navigating and !nav_agent.is_navigation_finished():
		# Use movement direction for animation when navigating
		var direction = (nav_agent.get_next_path_position() - global_position).normalized()
		
		if abs(direction.x) > abs(direction.z):
			if direction.x < 0:
				animated_sprite.play("left")
			else:
				animated_sprite.play("right")
		else:
			animated_sprite.play("forward")
	elif elapsed_time > 1000:
		animated_sprite.play("sleep")
	elif input_dir.x < 0:
		animated_sprite.play("left")
	elif input_dir.x > 0:
		animated_sprite.play("right")
	elif input_dir.y != 0:
		animated_sprite.play("forward")
	else:
		animated_sprite.play("idle")

# Called when navigation is finished
func _on_navigation_finished():
	is_navigating = false
	print("Reached destination")
	look_at(global_position + Vector3(0, 0, -1), Vector3.UP)
	
	# 或者也可以使用 rotation 直接設定為面向正前方
	# rotation = Vector3(0, 0, 0)  # 這是替代方案
	print("finish!")
	# 確保動畫也切換到正面/閒置狀態
	animated_sprite.play("idle")
