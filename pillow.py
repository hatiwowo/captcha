from io import BytesIO
import re
import base64
from PIL import Image
from PIL import ImageChops
from numpy import array
import numpy as np

def txt_to_str(path):
    f = open(path, 'r')
    str = f.read()
    f.close()
    return str

bg = txt_to_str("data/bg.txt")
full_bg = txt_to_str("data/full_bg.txt")
slice = txt_to_str("data/slice.txt")

def base64_to_img(base64_str):
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    image = base64.b64decode(base64_data)
    image_data = BytesIO(image)
    return Image.open(image_data).convert('RGB')


# image_file_bg = base64_to_bytes(bg)
# image_file_full_bg = base64_to_bytes(full_bg)
im_bg = base64_to_img(bg)
im_full_bg = base64_to_img(full_bg)

# captcha_bg = Image.new('RGB', (260, 160))
# captcha_full_bg = Image.new('RGB', (260, 160))

def get_offset(diff):
    im = array(diff)
    width, height = diff.size
    print(width, height)
    diff = []
    for i in range(height):
        for j in range(width):
            if im[i, j, 0] > 30 or im[i, j, 1] > 30:
                diff.append(j)
                break
    return min(diff)

diff = ImageChops.difference(im_bg, im_full_bg)
# print(diff)
aa = get_offset(diff)
print(aa)








# bg_data = re.sub('^data:image/.+;base64,', '', bg)
# image_bg = base64.b64decode(bg_data)
# image_file_bg = BytesIO(image_bg)
