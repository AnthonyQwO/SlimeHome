extends RichTextLabel

const MAX_HEIGHT := 300
var bg_color := Color(0, 0, 0, 0.5) # Half-transparent black
var stylebox := StyleBoxFlat.new()

func _ready() -> void:
	# Setup rounded semi-transparent background
	stylebox.bg_color = bg_color
	stylebox.set_corner_radius_all(8)
	stylebox.set_border_width_all(0)
	
	# Apply the stylebox to the theme
	add_theme_stylebox_override("normal", stylebox)
	
	text = ""
	scroll_active = true
	fit_height_to_text()

func _add_text(str: String) -> void:
	text += "\n" + str + "\n--------------------------------"
	fit_height_to_text()
	scroll_to_line(get_line_count())

func fit_height_to_text() -> void:
	var font := get_theme_font("normal_font")
	var font_size := get_theme_font_size("normal_font_size")
	var line_spacing := 4
	var line_count := get_line_count()
	var content_height := line_count * (font.get_height(font_size) + line_spacing) + 8
	size.y = min(content_height, MAX_HEIGHT)

# Remove the _draw() method as we're using theme styling instead
