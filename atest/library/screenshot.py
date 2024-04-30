import base64
from enum import Enum, auto
from io import BytesIO
from PIL import Image, ImageChops
from typing import Tuple
from robot.api import logger


class ExpectFailure(Enum):
    yes = auto()
    no = auto()


def get_image_size(img_path: str) -> Tuple[int]:
    im: Image.Image = Image.open(img_path)
    return im.size


def get_pixel_color(img_path: str, x: int, y: int) -> Tuple[int, int]:
    """Returns the color as (r,g,b,a) Tuple[int]"""
    im: Image.Image = Image.open(img_path)
    pix = im.load()
    return pix[x,y]


def compare_images(img1_path: str, img2_bytes: bytes, expect_failure: ExpectFailure = ExpectFailure.no):
    """Returns True if the images are the same, False otherwise"""
    im1: Image.Image = Image.open(img1_path).convert('RGB')
    im2: Image.Image = Image.open(BytesIO(img2_bytes)).convert('RGB')
    diff: Image.Image = ImageChops.difference(im1, im2)
    buffered = BytesIO()
    diff.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    logger.info(
            '</td></tr><tr><td colspan="3">'
            '<img alt="screenshot" class="robot-seleniumlibrary-screenshot" '
            f'src="data:image/png;base64,{img_str}" width="900px">',
            html=True,
        )
    box = diff.getbbox()
    if box and expect_failure == ExpectFailure.no:
        logger.info(f"box: {box}, type({type(box)}), but no idea why this fails.")
        error_sum = 0
        for pixel1, pixel2 in zip(im1.getdata(), im2.getdata()):
            error_sum = error_sum + abs(pixel1[0] - pixel2[0])
            error_sum = error_sum + abs(pixel1[1] - pixel2[1])
            error_sum = error_sum + abs(pixel1[2] - pixel2[2])
        logger.info(f"Difference between pixes is {error_sum}")
        if error_sum > 10:
            raise ValueError(f"Box {box} has difference of {error_sum}")
    elif box and expect_failure == ExpectFailure.yes:
        logger.info(f"box: {box}, type({type(box)})")
    assert box is None
