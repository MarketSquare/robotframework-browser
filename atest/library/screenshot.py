from PIL import Image
from typing import Tuple


def get_image_size(img_path: str) -> Tuple[int]:
    im: Image.Image = Image.open(img_path)
    return im.size


def get_pixel_color(img_path: str, x: int, y: int) -> Tuple[int, int]:
    """Returns the color as (r,g,b,a) Tuple[int]"""
    im: Image.Image = Image.open(img_path)
    pix = im.load()
    return pix[x,y]