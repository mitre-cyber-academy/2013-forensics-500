import numpy as np
import scipy.misc
import argparse
from PIL import Image, ImageFont, ImageDraw

def main():
	parser = argparse.ArgumentParser(
		description = 'This program will generate a bmp of Gaussian Noise')
	parser.add_argument('width', help='The width of the image', 
		type=int)
	parser.add_argument('height', help='The height of the image',
		type=int)
	parser.add_argument('inFile', help='The input text, including the flag',
		type=argparse.FileType('r'))
	parser.add_argument('outFName', help='The name of the output image',
		nargs='?', default='noiseImg.png')
	args = parser.parse_args()

	#Set up a numpy array to hold our image data (for mathy stuff):
	imgArr = np.zeros((args.width, args.height, 3))

	#First, make a background gradient, from 0,0 to N, N
	for i in range(args.width):
		for j in range(args.height):
			greenVal = np.sin(np.radians((10 * i) % 360)) * 127 + 127
			redVal = np.cos(np.radians((10 * j) % 360)) * 127 + 127
			blueVal = (np.cos(np.radians((j * 360)/args.height
				% 360)) * 127 + 127)
			imgArr[i, j, 0] = redVal
			imgArr[i, j, 1] = greenVal
			imgArr[i,j,2] = blueVal
	#Next, corrupt the image with red/green gaussian noise
	cov = np.eye(3,3) * 0.01
	cov[2][2] = 0
	mean = np.zeros(3)
	noiseArr = np.random.multivariate_normal(mean, cov, 
		(args.width, args.height))
	noiseArr = noiseArr * 127 + 127
	#data = np.random.normal(0, 0.01, (args.height, args.width))

	imgArr += noiseArr
	imgArr /= 2

	imgArr = np.uint8(imgArr)

	img = Image.fromarray(imgArr).convert('RGB')

	font = ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSansMono.ttf', 20)
	width, height = font.getsize('O') # Get width of monospace character
	flagText = args.inFile.read()
	#flagText = flagText.replace('\n','')
	numUnits = args.width / width -1 

	writeText = encode(flagText)
	#For viciousness, pad to the closest 8 bytes (with 0)
	writeText += (len(writeText) % 8) * 'O'

	draw = ImageDraw.Draw(img)

	xCounter = 0
	yCounter = 0
	for char in writeText:
		draw.text((xCounter * width, yCounter * height), char, 
			font=font)
		xCounter += 1
		if xCounter > numUnits:
			xCounter = 0
			yCounter += 1

	#draw.text((0,0), writeText, font=font)
	img.show()
	img.save(args.outFName)

	#'Arbitrarily' selected:
	#data = np.random.normal(0, 0.01, (args.height, args.width))
	#scipy.misc.imsave(args.outFName, imgArr)

#This will encode the input character string into a list of 0/O based
# in seven bit ASCII. O is 0, 1 is 0
def encode(text):
	#Define the output string:
	retStr = ''
	#Iterate  through each character in the string:
	for char in text:
		#Convert to a binary string:
		binChar = '%07d' % int(bin(ord(char))[2:])
		#replace all of the 0's with O
		binChar = binChar.replace('0', 'O').replace('1', '0')
		retStr += binChar
	return retStr

def decode(ohStr):
	#First, change to 0's and 1's:
	ohStr = ohStr.replace('0', '1').replace('O', '0')
	retStr = ''
	#Next, go through each chunk of 7 bits:
	count = 0
	for i in range(len(ohStr)):
		if(i % 7 == 0):
			retStr += chr(int(ohStr[i: i + 7], 2))
			count += 1
	return retStr

if __name__ == '__main__':
	main()
