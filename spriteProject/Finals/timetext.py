import time
import datetime

from PIL import Image, ImageDraw, ImageFont
from PIL import GifImagePlugin

background = Image.open("fireNiceWeather.gif")
for frame in range(45,85):
    background.seek(frame)
    framebuffer = background.convert('RGB')
bob = framebuffer.convert('RGBA')

time = datetime.datetime.now()
magfestday = datetime.datetime(2019,1,3,0,0,0)
daystillmagfest = (magfestday - time).days
if daystillmagfest < 0:
	magfeststring = "MAGFEST  DAY  "+str(daystillmagfest*-1)
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
d.text((78,7), "34F", font=fnt, fill=(0,0,255,255))

out = Image.alpha_composite(bob, txt).convert('RGB')
out.show()