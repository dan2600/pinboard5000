#!/usr/bin/env python
from time import sleep
import datetime
import serial 
from samplebase import SampleBase
from PIL import Image, ImageDraw, ImageFont
from PIL import GifImagePlugin
import pyowm

owm = pyowm.OWM('ae761e0f412e4f82e90ed207ca6163fe')
observation = owm.weather_at_place('New York,US')

ser = serial.Serial('/dev/ttyUSB0', 9600)
ser2 = serial.Serial('/dev/ttyUSB1', 9600)
sleep(5)

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

		def showtemp():
			w = observation.get_weather()
			background = Image.open("fireNiceWeather.gif")
			ser.write("HIGH "+str(int(w.get_temperature('fahrenheit')["temp_max"]))+"F\n")
			ser2.write("LOW "+str(int(w.get_temperature('fahrenheit')["temp_min"]))+"F\n")
			for f in range(0,78):
				background.seek(f)
				self.framebuffer = background
				double_buffer.SetImage(self.framebuffer.convert('RGB'))   
				self.matrix.SwapOnVSync(double_buffer)
				sleep(.06)			
			framebuffer = background.convert('RGB')
			bob = framebuffer.convert('RGBA')

			time = datetime.datetime.now()
			magfestday = datetime.datetime(2019,1,3,0,0,0)
			daystillmagfest = (magfestday - time).days
			if daystillmagfest <= 0:
				magfeststring = "MAGFEST  DAY  "+str(daystillmagfest*-1+1)
			else:
				magfeststring = str(daystillmagfest)+"  DAYS  TILL  MAGFEST"

			thetime = time.strftime("%I:%M %p")

			txt = Image.new('RGBA', background.size, (255,255,255,0))
			fnt = ImageFont.truetype('atari.ttf', 16)
			fnt2 = ImageFont.truetype('pixelated.ttf', 8)
			d = ImageDraw.Draw(txt)
			d.text((1,-1), "TIME", font=fnt2, fill=(255,255,255,255))
			d.text((71,-1), "TEMP", font=fnt2, fill=(255,255,255,255))
			pos = 128 - d.multiline_textsize(magfeststring, font=fnt2, spacing=0)[0]
			d.multiline_text((pos,24), magfeststring, fill=(255,255,255,255), font=fnt2)
			d.text((1,7), thetime, font=fnt, fill=(0,255,0,255))
			d.text((78,7), str(int(w.get_temperature('fahrenheit')["temp"]))+"F", font=fnt, fill=(0,0,255,255))
			double_buffer.SetImage(Image.alpha_composite(bob, txt).convert('RGB'))   
			self.matrix.SwapOnVSync(double_buffer)
			sleep(10)
			if int(w.get_temperature('fahrenheit')["temp"]) < 32:
				for f in range(78,background.n_frames):
					background.seek(f)
					self.framebuffer = background		
					double_buffer.SetImage(Image.alpha_composite(self.framebuffer.convert('RGBA'), txt).convert('RGB'))   
					self.matrix.SwapOnVSync(double_buffer)
					sleep(.03)
			sleep(5)
		def pinballScore(imageFile, logoLoopIn, logoLoopOut, loops, speed):
			self.image = Image.open(imageFile)
			for f in range(0,logoLoopIn):
				self.image.seek(f)
				double_buffer.SetImage(self.image.convert('RGB'))   
				self.matrix.SwapOnVSync(double_buffer)
				sleep(speed)
			for l in range(0, loops):
				self.image.seek(logoLoopIn)	
				for f in range(logoLoopIn,logoLoopOut):
					self.image.seek(f)	
					double_buffer.SetImage(self.image.convert('RGB'))   
					self.matrix.SwapOnVSync(double_buffer)
					sleep(speed)			
			for f in range(logoLoopOut,self.image.n_frames):
				self.image.seek(f)
				double_buffer.SetImage(self.image.convert('RGB'))   
				self.matrix.SwapOnVSync(double_buffer)
				sleep(speed)
			double_buffer.SetImage(Image.new('RGB',(128,32), (0,0,0)))
			self.matrix.SwapOnVSync(double_buffer)
			sleep(.001)

		def oneShot(imageFile, speed=.016, hold=0):
			self.image = Image.open(imageFile)
			for f in range(0,self.image.n_frames):
				self.image.seek(f)
				double_buffer.SetImage(self.image.convert('RGB'))   
				self.matrix.SwapOnVSync(double_buffer)
				sleep(speed)
			sleep(hold)
		# let's scroll
		while True:
			pinballScore("getawayii.gif", 23, 5, 250, .016)
			pinballScore("t2.gif", 136, 375, 1, .016)
			pinballScore("metallica.gif", 330, 331, 100, .016)
			oneShot("zeldaTemp.gif")
			oneShot("metroidtimetemp.gif")
			pinballScore("monsterbash.gif", 10, 12, 0, .016)
			pinballScore("startrek.gif", 10, 12, 0, .016)
			
			oneShot("mvc.gif", .016, 10)
			oneShot("StreetFighterTitle.gif", .016, 10)
			oneShot("MortalKombat.gif", .016, 10)
			showtemp()
			oneShot("ChronoTriggerFinal.gif")
			oneShot("noDrugs2.gif", .016, 15)
			ser.write("PLEASE TIP YOUR\n")
			ser2.write("DRUG DEALER\n")
		


# Main function
# e.g. call with
#  sudo ./image-scroller.py --chain=4
# if you have a chain of four
if __name__ == "__main__":
	image_scroller = ImageScroller()
	if (not image_scroller.process()):
		image_scroller.print_help()
