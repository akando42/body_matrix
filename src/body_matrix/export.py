import av

# Generate Video from PIL Image Arrays
def generate_video_from_pil_images(pil_images, output, width, height):
    container = av.open(output, mode="w")

    stream = container.add_stream('mpeg4', rate=30)
    stream.width = width
    stream.height = height

    def encode(pil_image):
        frame = av.VideoFrame.from_image(pil_image)
        for packet in stream.encode(frame):
            container.mux(packet)
        
    for pil_image in pil_images:
        encode(pil_image)
    
    container.close()