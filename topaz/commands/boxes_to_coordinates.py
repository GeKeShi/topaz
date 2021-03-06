from __future__ import print_function,division

import sys
import os
import pandas as pd
from PIL import Image

name = 'boxes_to_coordinates'
help = 'convert .box format coordinates to tab delimited coordinates table'

def add_arguments(parser):
    parser.add_argument('files', nargs='+', help='path to input box files')
    parser.add_argument('--imagedir', help='directory of images, eman2 inverts the y-axis')
    parser.add_argument('--image-ext', default='tiff', help='image format extension (default: tiff)')
    parser.add_argument('-o', '--output', help='destination file (default: stdout)')

def main(args):
    from topaz.utils.conversions import boxes_to_coordinates

    tables = []

    for path in args.files:
        if os.path.getsize(path) == 0:
            continue

        image_name = os.path.splitext(os.path.basename(path))[0]
        im = Image.open(args.imagedir + '/' + image_name + '.' + args.image_ext)
        shape = (im.height,im.width)
        box = pd.read_csv(path, sep='\t', header=None).values

        coords = boxes_to_coordinates(box, shape, image_name=image_name)

        tables.append(coords)

    table = pd.concat(tables, axis=0)

    output = sys.stdout
    if args.output is not None:
        output = args.output
    table.to_csv(output, sep='\t', index=False)




