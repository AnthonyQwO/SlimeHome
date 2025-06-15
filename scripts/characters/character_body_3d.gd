# 角色控制腳本：附加在 CharacterBody3D 上
extends CharacterBody3D

@export var move_speed := 5.0 / 2
@export var jump_velocity := 6.0
@export var gravity := 9.8 * 2

@onready var animated_sprite = $AnimatedSprite3D
@onready var elapsed_time := 0.0

func move_character(input_dir: Vector2) -> void:
	input_dir = input_dir.normalized()
	var direction = (transform.basis.x * input_dir.x + transform.basis.z * input_dir.y)
	direction = direction.normalized()

	velocity.x = direction.x * move_speed / 3 * 2
	velocity.z = direction.z * move_speed

	move_and_slide()

func _physics_process(delta):
	var input_dir = Vector2.ZERO
	input_dir.x = Input.get_action_strength("ui_right") - Input.get_action_strength("ui_left")
	input_dir.y = Input.get_action_strength("ui_down") - Input.get_action_strength("ui_up")

	move_character(input_dir)  # 呼叫封裝後的移動函式

	# idle 計算與動畫
	if input_dir == Vector2.ZERO:
		elapsed_time += 1
	else:
		elapsed_time = 0
	
	if elapsed_time > 1000:
		animated_sprite.play("sleep")
	elif input_dir.x < 0:
		animated_sprite.play("left")
	elif input_dir.x > 0:
		animated_sprite.play("right")
	elif input_dir.y != 0:
		animated_sprite.play("forward")
	else:
		animated_sprite.play("idle")
	
	# 重力與跳躍
	if not is_on_floor():
		velocity.y -= gravity * delta
	else:
		if Input.is_action_just_pressed("ui_accept"):
			velocity.y = jump_velocity

	# 掉下去的重置
	if global_position.y < -5:
		global_position = Vector3(0, 10, 0)

	move_and_slide()  # 別忘了實際應用 velocity
