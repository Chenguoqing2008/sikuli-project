#! /usr/bin/env python

# -*- encoding:utf-8 -*¡ª

from PIL import Image, ImageDraw, ImageFont
import sys


def create_png(filename):
    name = filename.split(".")[0]
    image_name = name + ".png"
    font = ImageFont.truetype('segoeui.ttf', 13)
    img = Image.new('RGBA', (160, 20), color=(255, 255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((5, -2), filename, font=font, fill='black')
    img.save('{}'.format(image_name))


def main():
    create_png(sys.argv[1])


if __name__ == "__main__":
    main()
