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

def circle_label():
	return


def rectangle_label():
	return


def connecting_line():
	return
