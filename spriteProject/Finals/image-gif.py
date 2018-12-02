#!/usr/bin/env python
import time
from samplebase import SampleBase
from PIL import Image
from PIL import GifImagePlugin



class ImageScroller(SampleBase):
    def __init__(self, *args, **kwargs):
        super(ImageScroller, self).__init__(*args, **kwargs)
        self.parser.add_argument("-i", "--image", help="The image to display", default="../../../examples-api-use/runtext.ppm")

    def run(self):
        if not 'image' in self.__dict__:
            self.image = Image.open(self.args.image)
        print(self.image.is_animated)
	print(self.image.n_frames)
	self.framebuffer = self.image
        double_buffer = self.matrix.CreateFrameCanvas()
	

        img_width, img_height = self.image.size
      


        # let's scroll
        frame = 0
        while True:
	    self.image.seek(frame)
	    self.framebuffer = self.image
	    double_buffer.SetImage(self.framebuffer.convert('RGB'))   
            self.matrix.SwapOnVSync(double_buffer)
	    frame += 1
	    if frame >= self.image.n_frames:
	        frame = 0
	    time.sleep(.06)
	  


# Main function
# e.g. call with
#  sudo ./image-scroller.py --chain=4
# if you have a chain of four
if __name__ == "__main__":
    image_scroller = ImageScroller()
    if (not image_scroller.process()):
        image_scroller.print_help()
