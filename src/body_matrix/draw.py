from PIL import Image, ImageDraw, ImageFont
from . import measure

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
		outline=background_color,
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


def connecting_line(image, pointA, pointB, line_color, line_width):
	sample = image.copy()
	draw = ImageDraw.Draw(sample)
	draw.line(
		[pointA[0], pointA[1],  pointB[0], pointB[1]], 
		fill=line_color, 
		width=line_width
	)

	return sample


def floating_rectangle_label(image, longitude_coordinate, point, label_text, label_size, label_color, label_font, background_color):
	sample = image.copy()
	draw = ImageDraw.Draw(sample)
	radius = 6
	
	### Draw a Dot at anchor point
	draw.ellipse(
		[(point[0]-radius, point[1]-radius), (point[0]+radius, point[1]+radius)],
		fill=label_color,
		outline="#ffffff",
		width=1
	)

	### Draw a Label 60 degree North East or North West basing on anchor location
	marker_font = ImageFont.truetype(label_font, label_size)
	letter_count = len(label_text)
	label_height = label_size * 2
	label_width = label_size * letter_count

	if point[0] < longitude_coordinate:
		anchor_point = [point[0] - 100, point[1] - 100]
	else:
		anchor_point = [point[0] + 100, point[1] - 100]

	rect_topleft = (
		(anchor_point[0] - label_width/2), 
		(anchor_point[1] - label_height/2)
	)

	rect_bottomright = (
		(anchor_point[0] + label_width/2), 
		(anchor_point[1] + label_height/2)
	)

	rect_bottomleft = (
		rect_topleft[0], 
		rect_bottomright[1]
	)

	rect_topright = (
		rect_topleft[1],
		rect_bottomright[0]
	)

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

	### Draw a Line connecting Anchor Dot and the Label
	line_color = label_color
	line_width = int(radius/3)

	draw.line(
		[point[0], point[1],  anchor_point[0], (anchor_point[1]+label_height/2)], 
		fill=line_color, 
		width=line_width
	)

	return sample 


def segmentation_contour(contour_pixels, contour_color, contour_size, font,  image):
	contoured = image.copy()
	for contour in contour_pixels:
	    contoured = circle_label(
	        contoured, 
	        contour_size, 
	        contour,
	        background_color=contour_color,
	        label=" ", 
	        label_font=font,
	        label_color=contour_color,   
	    )

	return contoured


def add_crown(score, le, re, top_head,frame, crown_image, font_file):
	middle_ear = measure.find_middle_point(le, re)
	head_width = measure.two_points_distance(le, re)
	crown_width = int(head_width * 1.6)
	crown_height = int(head_width * 0.8)
	crown_size = (crown_width,crown_height)
	crown = Image.open(crown_image)
	crown = crown.resize(crown_size)
	draw = ImageDraw.Draw(crown)
	font_size = int(crown_width/5)
	font = ImageFont.truetype(font_file, font_size)
	draw.text(
	    (crown_width/4,crown_height/2), 
	    str(score),
	    fill="#FF0000",
	    font=font,
	    align="center"
	)

	crown_position = (
	    int(top_head[0] - crown_width/2), 
	    int(top_head[1] - crown_height)
	)

	crowned = frame.copy()
	crowned.paste(crown, crown_position, crown)

	return crowned


# def add_thong(score, lh, rh, frame):
# 	return




