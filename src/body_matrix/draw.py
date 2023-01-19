from PIL import ImageDraw, ImageFont

def keypoint_markers(coordinates, image, label_font):
	marker_font = ImageFont.truetype(label_font, 8)
	sample = image.copy()
	draw = ImageDraw.Draw(sample) 
			
	for index, point in enumerate(coordinates.values()):
		label = str(index) 
		radius = 6

		print(point)

		draw.ellipse(
			[(point[0]-radius, point[1]-radius), (point[0]+radius, point[1]+radius)],
			fill="#40389F",
			outline="#ffffff",
			width=1
		)

		draw.text(
			(point[0]-3, point[1]-6),
			str(label),
			fill="#FAFF00",
			font=marker_font,
			align="center"
		)
	return sample


def circle_label(image, radius, central_point, background_color, label, label_font, label_color):
	point = central_point
	letter_length = len(label)
	label_size = int(radius/letter_length*2)
	marker_font = ImageFont.truetype(label_font, label_size)
	sample = image.copy()

	draw = ImageDraw.Draw(sample)
	draw.ellipse(
		[(point[0]-radius, point[1]-radius), (point[0]+radius, point[1]+radius)],
		fill=background_color,
		outline="#ffffff",
		width=1
	)

	draw.text(
		(point[0]-radius/2, point[1]-radius/1.8),
		str(label),
		fill=label_color,
		font=marker_font,
		align="center"
	) 

	return sample


def fixed_rectangle_label(image, anchor_point, label_text, label_size, label_font, label_color, background_color):
	letter_count = len(label_text)
	label_height = label_size * 2
	label_width = label_size * letter_count
	marker_font = ImageFont.truetype(label_font, label_size)
	sample = image.copy()

	rect_topleft = (
		(anchor_point[0] - label_width/2), 
		(anchor_point[1] - label_height/2)
	)

	rect_bottomright = (
		(anchor_point[0] + label_width/2), 
		(anchor_point[1] + label_height/2)
	)

	draw = ImageDraw.Draw(sample)
	draw.rectangle(
		[rect_topleft, rect_bottomright], 
		fill=background_color, 
		outline=label_color, 
		width=1
	)

	draw.text(
		(anchor_point[0] - label_width/4, anchor_point[1]-label_height/4),
		str(label_text),
		fill=label_color,
		font=marker_font,
		align="ms"
	)

	return sample 


def connecting_line():
	return

def floating_rectangle_label():
	return

