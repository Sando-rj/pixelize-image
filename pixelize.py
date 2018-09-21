import sys
import imghdr
from PIL import Image
import argparse
import operator


# Get arguments, use argparse to form a good commandline tool
def ProcessArgs():
    argParser = argparse.ArgumentParser(description="Tool to convert regular images to pixelized images")
    argParser.add_argument('imagePath', help="File path of the source image")
    argParser.add_argument('-ps', '--pixel-size', nargs='?', default=2, type=int, help="Size of pixelated image pixel, in pixels")
    argParser.add_argument('-m', '--mode', nargs='?', default=1, type=str, choices=['first','average'], help="Processing mode for pixels, first to apply first pixel to the zone, average to make an average of it")
    argParser.add_argument('outputPath', help="File path for output image", nargs='?', default="output")
    args = vars(argParser.parse_args())
    
    imgType = str(imghdr.what(args['imagePath']))

    # catch if not an image
    if imgType == 'None':
        raise ValueError('Incorrect image type')

    return args


# Match a pixel color value with a pixel color value from input color palette
def matchingColor(colorArray, pixColor):
    bestValue = 2000

    if(len(pixColor)==3):
        pixColor.append(255)
    elif(len(pixColor)==4):
        if(int(pixColor[3]/128)==0):
            return (0,0,0,0) 

    for val in colorArray:
        diff = abs(val[0]-pixColor[0])+abs(val[1]-pixColor[1])+abs(val[2]-pixColor[2])+abs(val[3]-pixColor[3])
        if diff < bestValue:
            bestValue = diff
            newValue = val

    return tuple(newValue)


# Main function to pixelize the input image
def pixelizeImg(args):
    img = Image.open(args['imagePath'], 'r')
    img = img.convert('RGBA')
    outputImg = Image.new(img.mode, img.size)
    pixelSize = args['pixel_size']

    # Create megadrive color palette
    cs = [0, 52, 87, 116, 144, 172, 206, 255]
    megadriveColors = [[cs[i], cs[j], cs[k], 255] for i in range(len(cs)) for j in range(len(cs)) for k in range(len(cs))]
    
    width, height = img.size
    pixelData = list(img.getdata())

    if width % pixelSize != 0 or height % pixelSize != 0:
        raise ValueError('image dimension does not allow for complete pixelization of image')

    for i in range(0, height, pixelSize):
        for j in range(0, width, pixelSize):
            # Take a block of pixels to convert it into the same color
            color = (0,0,0,0)
            for k in range(pixelSize):
                for l in range(pixelSize):
                    # Unify color to average of pixels colors
                    if(args['mode']=='average'):
                        color = tuple(map(sum, zip(color, pixelData[((i+k)*width + j + l)]))) 
                    # Unify color to first top left color
                    else:
                        color = tuple(map(sum, zip(color, pixelData[(i*width + j)])))
            color = tuple(c/(pixelSize*pixelSize) for c in color)

            if len(color)==3: 
                color += (255,)

            color = matchingColor(megadriveColors, color)
            for k in range(pixelSize):
                for l in range(pixelSize):
                    pixelData[((i+k)*width +j + l)] = color

    # Save Image
    outputImg.putdata(pixelData)
    if(img.format == None):
        outputImg.save(args['outputPath'], 'png')
    else:
        outputImg.save(args['outputPath'], img.format)


if __name__ =="__main__":
    args = ProcessArgs()
    pixelizeImg(args)
