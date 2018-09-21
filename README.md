# pixelize-image

Piece of code to create a pixelized looking version of an image.

## Use

```pixelize.py [-h] [-ps [PIXEL_SIZE]] [-m [{first,average}]] imagePath [outputPath]```

-h : get the man for pixelize.py

-ps [PIXEL_SIZE] : Size of virtual pixel, in number of pixel

-m : Mode for virtual pixel creation, either first to apply top-right pixel to a block, or average to find average color of the block

imagePath : source image

outputPath : output image path, "output" if not precised 

*The pixelated image will be created only if the pixel size is valid, meaning if width and height can be divided with the pixel size*
