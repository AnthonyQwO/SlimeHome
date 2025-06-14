extends Window
@onready var speed := 5
@onready var move := 0

func _process(delta):
	# Apply movement based on the move direction
	position.x += speed * move * 0.2
			
func left():
	print("Left")
	move = -1
	
func right():
	print("Right")
	move = 1
	
func stop():
	print("Stop")
	move = 0
