# this program make JPG thumbnail for images in current directory

from PIL import Image
import os

images = os.listdir()

for image in images:
  if image.endswith(('jpg', 'jpeg', 'png', 'webp')):
    with Image.open(image) as img:
      fn_thumb = ''.join([image.rsplit('.')[0], '_thumb.', image.rsplit('.')[1]])
      if not img.mode == 'RGB':
        img.convert('RGB')
      img.thumbnail((200,200))
      img.save(fn_thumb, format='JPEG', quality=85)

