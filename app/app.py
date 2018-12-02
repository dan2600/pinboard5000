#!/usr/bin/env python
from __future__ import print_function
from time import sleep
import datetime, serial, os, sys, sqlite3
from PIL import Image, ImageDraw, ImageFont
from PIL import GifImagePlugin

# load the database
# os.chdir(os.path.dirname(sys.argv[0]))
dir_path = os.path.dirname(os.path.realpath(__file__))
db_path = dir_path+'/../backEnd/db/pinboard.db'
print(db_path)


#load the matrix library
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))
from rgbmatrix import RGBMatrix, RGBMatrixOptions


# attempt to add serial devices
try:
	ser = serial.Serial('/dev/ttyUSB0', 9600)
except:
	print("error no serial 1")
	ser = False

try:
	ser2 = serial.Serial('/dev/ttyUSB1', 9600)
except:
	print("error no serial 2")
	ser2 = False

print("attempting to load RGBMatrix")

# load the matrix
options = RGBMatrixOptions()
options.hardware_mapping = 'adafruit-hat-pwm'
options.rows = 32
options.cols = 64
options.chain_length = 2
options.parallel = 1
options.row_address_type = 0
options.multiplexing = 0
options.pwm_bits = 11
options.brightness = 10
options.pwm_lsb_nanoseconds = 130
options.led_rgb_sequence = "RBG"
options.pixel_mapper_config = ""
options.gpio_slowdown = 2
matrix = RGBMatrix(options = options)

def getPlaylist():
	c.execute('SELECT * FROM playlist ORDER BY id')
	all_rows = c.fetchall()
	return all_rows

def getScene(sceneName):
	c.execute('SELECT * FROM scenes WHERE name = "{tn}" LIMIT 1'.\
        format(tn=sceneName))
	all_rows = c.fetchall()
	return(all_rows)

def getSegments(segmentName):
	c.execute('SELECT * FROM segmentdisp WHERE name = "{tn}" LIMIT 1'.\
        format(tn=segmentName))
	all_rows = c.fetchall()
	return(all_rows)

def setSegments(segments):
    print("Setting Segments")

def playOneShot(scene):
	print("Playing "+scene[1])
	playbackImage = Image.open(dir_path+"/../backEnd/public/images/"+scene[3])
	frameRate = (1.0/scene[4])
	holdTime = (scene[5])
	if playbackImage.is_animated:
		for f in range(0,playbackImage.n_frames):
			playbackImage.seek(f)
			framebuffer = playbackImage
			double_buffer = matrix.CreateFrameCanvas()
			double_buffer.SetImage(framebuffer.convert('RGB'))
			matrix.SwapOnVSync(double_buffer)
			complete = int(float(f)/float(playbackImage.n_frames)*10.0)
			bar = ""
			for b in range(0, complete):
				bar = bar + "="
			for b in range(0, 10 - complete):
				bar = bar + " "
			bar = "["+bar+"]"
			print(bar, end='\r')
			sys.stdout.flush()
			sleep(frameRate)
	else:
		print("oneFrame")
	print("[==========]")
	print("Holding last frame for "+str(holdTime))
	sleep(holdTime)


def playItem(playlistItem):
    sceneInfo = getScene(playlistItem[1])[0]
    if ser != False:
    	print("serial Shit")
    	segmentInfo = getSegments(playlistItem[1])[0]
    # setSegments(segmentInfo)
    if sceneInfo[2] == 'oneShot':
    	playOneShot(sceneInfo)

print(db_path)
while True:
	print(db_path)
	conn = sqlite3.connect(db_path)
	c = conn.cursor()	
	playList = getPlaylist()
	for i in range(len(playList)):
		playItem(playList[i])
	conn.close()