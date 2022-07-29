from PIL import Image
from PIL import ImageChops

image_bg = Image.open('img/bg.png').convert('RGB')
image_full_bg = Image.open('img/full_bg.png').convert('RGB')

diff = ImageChops.difference(image_bg, image_full_bg).getbbox()
print(diff)
