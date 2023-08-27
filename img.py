from PIL import Image, ImageDraw, ImageFont
from enums import TitleConfig, VertAlignment, HorizontalAlignment
import config


def crop_box_from_pins(size: tuple, scale_based_crop: tuple) -> tuple:
    w, h = size
    cx1, cy1, cx2, cy2 = scale_based_crop
    x1, x2 = w*cx1, w*cx2
    y1, y2 = h*cy1, w*cy2
    # might need to change to x1, y1, w, h
    return x1, y1, x2, y2


def crop(img: Image) -> Image:
    o_w, o_h = img.size
    o_ratio = o_w/o_h

    if config.CROP_RATIO > o_ratio:
        max_w = o_w
        max_h = max_w / config.CROP_RATIO
    else:
        max_h = o_h
        max_w = max_h * config.CROP_RATIO

    x = o_w * config.CROP_OFFSET[0]
    y = o_h * config.CROP_OFFSET[1]
    w = max_w * config.CROP_SCALE
    h = max_h * config.CROP_SCALE
    x2 = x + w
    y2 = y + h
    crop_area = (x, y, x2, y2)
    return img.crop(crop_area)


def draw_text(img: Image, font_path: str, text: str, text_config) -> Image:
    img = img.copy()
    bx1, by1, bx2, by2 = crop_box_from_pins(img.size, text_config[TitleConfig.DRAW_AREA])
    bw, bh = bx2 - bx1, by2 - by1

    best_font_size = 1
    while True:
        font = ImageFont.truetype(font_path, best_font_size)
        draw = ImageDraw.Draw(img)
        print(text, font, best_font_size)
        _, _, w, h = draw.textbbox((0, 0), text, font=font)
        maxed_out = w > bw or h > bh
        best_font_size += -1 if maxed_out else 1
        if maxed_out:
            break

    if text_config[TitleConfig.H_ALIGN] is HorizontalAlignment.CENTER:
        final_x = (bx1 + bx2)/2 - w/2
    else:
        raise Exception(f'{text_config[TitleConfig.H_ALIGN]} is not supported')

    if text_config[TitleConfig.V_ALIGN] is VertAlignment.TOP:
        final_y = by1
    else:
        raise Exception(f'{text_config[TitleConfig.V_ALIGN]} is not supported')

    draw.text((final_x, final_y), text, font=font, fill=255)
    return img


def round_and_clip_image(image):
    """
    Given a dictionary, ensure that the values in the 'pixels' list are all
    integers in the range [0, 255].
    """
    for i,color in enumerate(image['pixels']):
        if color < 0: color = 0
        if color > 255: color = 255
        image['pixels'][i] = round(color)


# HELPER FUNCTIONS FOR LOADING AND SAVING COLOR IMAGES
def load_greyscale_image(img: Image):
    """
    Loads an image from the given file and returns a dictionary
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_image('test_images/cat.png')
    """
    img_data = img.getdata()
    if img.mode.startswith('RGB'):
        pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2])
                  for p in img_data]
    elif img.mode == 'LA':
        pixels = [p[0] for p in img_data]
    elif img.mode == 'L':
        pixels = list(img_data)
    else:
        raise ValueError('Unsupported image mode: %r' % img.mode)
    w, h = img.size
    return {'height': h, 'width': w, 'pixels': pixels}


def apply_vignette(img: Image):
    grey = load_greyscale_image(img)
    height = grey['height']
    width = grey['width']
    import math
    # first, compute the Gaussian Kernel
    # https://docs.opencv.org/2.4/modules/imgproc/doc/filtering.html#Mat%20getGaussianKernel(int%20ksize,%20double%20sigma,%20int%20ktype)
    def getGaussianKernel(ksize):
        sigma = 0.4 * ((ksize - 1) * 0.5 - 1) + 0.8
        kernel = []
        scale_factor = 0
        for i in range(ksize):
            coeff = math.e ** (-((i - (ksize - 1) / 2) ** 2) / (2 * sigma ** 2))
            kernel.append(coeff)
            scale_factor += coeff
        for i in range(ksize): kernel[i] /= scale_factor
        return kernel

    Kx = getGaussianKernel(width)
    Ky = getGaussianKernel(height)
    K = [k1 * k2 for k1 in Ky for k2 in Kx]
    # http://mathworld.wolfram.com/FrobeniusNorm.html
    # compute the Frobenius matrix norm
    norm = sum(i ** 2 for i in K)
    norm = math.sqrt(norm)
    K = [i * 255 / norm for i in K]
    # apply per pixel
    pixels = []
    for coeff, value in zip(K, grey['pixels']):
        pixels.append(coeff * value)
    im = {'height': height, 'width': width, 'pixels': pixels}
    round_and_clip_image(im)
    out = Image.new(mode='L', size=(im['width'], im['height']))
    out.putdata(im['pixels'])
    return out


def process(img_paths: [str], font_paths: [str], artist: str, song_title: str,  extract_mode: str) -> Image:
    img = Image.open(img_paths[0])
    img = crop(img)
    img = apply_vignette(img)
    img = draw_text(img, font_paths[0], f'{artist} - {song_title}', config.TEXT_TITLE)
    return img
