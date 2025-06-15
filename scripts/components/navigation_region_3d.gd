# navigation_setup.gd
extends NavigationRegion3D

func _ready():
	# Generate navigation mesh when the scene starts
	bake_navigation_mesh()
