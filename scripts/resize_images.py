import argparse,os
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--images_path", help = "path to the folder containing images", required = True, type = str)
parser.add_argument("-s", "--image_scale", help = "denominator to scale image by: 1/(your number)", default = 9, type = int)
args = parser.parse_args()

path = args.images_path
image_scale = args.image_scale

i = 0

for file in os.listdir(path):
    print(file)
    with Image.open(path + "/" + file) as img:
        resized = img.resize((img.size[0]//image_scale, img.size[1]//image_scale))
        resized.save(path + '/_' + file)
        i += 1
