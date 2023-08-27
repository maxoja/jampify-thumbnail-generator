from PIL import Image, ImageDraw, ImageFont
import config


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


def add_text(img: Image, font_path: str, artist: str, song_title: str, extract_mode: str) -> Image:
    img = img.copy()
    text_title = f'{artist} - {song_title}'
    text_extract = f'{extract_mode}'
    title_font_size = 70
    title_extract_size = 50
    text_position = (50, 50)  # (x, y)
    # text_clr = (255, 255, 255)
    text_clr = 255

    font = ImageFont.truetype(font_path, title_font_size)
    draw = ImageDraw.Draw(img)

    # Calculate the position to place the text
    text_width, text_height = draw.textsize(text_title, font=font)
    x, y = text_position
    draw.text((x, y), text_title, fill=text_clr, font=font)

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
    img = add_text(img, font_paths[0], artist, song_title, extract_mode)
    return img
