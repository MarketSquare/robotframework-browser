import base64
from io import BytesIO
from PIL import Image, ImageChops
from typing import Tuple
from robot.api import logger


def get_image_size(img_path: str) -> Tuple[int]:
    im: Image.Image = Image.open(img_path)
    return im.size


def get_pixel_color(img_path: str, x: int, y: int) -> Tuple[int, int]:
    """Returns the color as (r,g,b,a) Tuple[int]"""
    im: Image.Image = Image.open(img_path)
    pix = im.load()
    return pix[x,y]


def compare_images(img1_path: str, img2_bytes: bytes):
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
    if isinstance(box, tuple):
        logger.warn(f"box: {box}, type({type(box)}), but no idea why this fails.")
        raise ValueError(f"Diff is not correct.")    
    elif box is None:
        logger.info("No diff found, all good")
        return True
    raise ValueError(f"Diff is not correct.")


def compare_images_2(img1_path: str, img2_path: str):
    """Returns True if the images are the same, False otherwise"""
    im1: Image.Image = Image.open(img1_path).convert('RGB')
    im2: Image.Image = Image.open(img2_path).convert('RGB')
    for im1_pix, im2_pix in zip(im1.getdata(), im2.getdata()):
        if im1_pix != im2_pix:
            logger.info(im1_pix)
            logger.info(im2_pix)
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
    assert box is None, f"diff is not None"