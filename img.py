import math

from PIL import Image, ImageDraw, ImageFont

from enums import TitleConfig, VertAlignment, HorizontalAlignment
import config
import img_diff


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

    draw.text((final_x, final_y), text, font=font, fill=(100, 150, 150))
    return img


def round_and_clip_image(image):
    """
    Given a dictionary, ensure that the values in the 'pixels' list are all
    integers in the range [0, 255].
    """
    for i,color in enumerate(image['pixels']):
        if type(color) is int:
            image['pixels'][i] = round_image(color)
        elif type(color) is list:
            temp_tuple = []
            for j, color_value in enumerate(color):
                temp_tuple.append(round_image(color_value))
            image['pixels'][i] = tuple(temp_tuple)
        else:
            raise Exception(f'Class is not supported: {color}')
        

def round_image(color: int):
    if color < 0: color = 0
    if color > 255: color = 255
    return round(color)

def apply_vignette(img: Image, mode: str):
    if mode == "L":
        grey = img_diff.load_greyscale_image(img)
    elif mode == "RGB":
        grey = img_diff.load_color_image(img)
    else:
        raise Exception(f'Image mode is not supported')
    height = grey['height']
    width = grey['width']
    kernel_width = width*2
    kernel_height = height*2

    center_x = int((config.VIGNETTE_CENTER[0]-0.5) * width)
    center_y = int((config.VIGNETTE_CENTER[1]-0.5) * height)

    Kx = img_diff.getGaussianKernel(kernel_width, config.VIGNETTE_SCALE[0]/2)
    Ky = img_diff.getGaussianKernel(kernel_height, config.VIGNETTE_SCALE[1]/2)
    K = [k1 * k2 for k1 in Ky for k2 in Kx]
    # K = [math.pow(k, config.VIGNETTE_STR) for k in K]

    # http://mathworld.wolfram.com/FrobeniusNorm.html
    # compute the Frobenius matrix norm
    norm = sum(i ** 2 for i in K)
    norm = math.sqrt(norm)
    K = [i * 255 / norm for i in K]
    min_k = min(K)
    # apply per pixel
    pixels = []
    for y in range(height):
        for x in range(width):
            x_kernel = kernel_width//4 + x - center_x
            y_kernel = kernel_height//4 + y - center_y
            i_kernel = y_kernel*kernel_width + x_kernel
            i_img = y*width + x
            value = grey['pixels'][i_img]

            if x_kernel < 0 or x_kernel > kernel_width \
                or y_kernel < 0 or y_kernel > kernel_height:
                coeff = min_k
            else:
                coeff = K[i_kernel]

            if mode == "L":
                pixels.append(math.pow(coeff, config.VIGNETTE_STR) * value)
            elif mode == "RGB":
                pixels.append([math.pow(coeff, config.VIGNETTE_STR) * value_a for value_a in value])
    im = {'height': height, 'width': width, 'pixels': pixels}
    round_and_clip_image(im)
    out = Image.new(mode=mode, size=(im['width'], im['height']))
    out.putdata(im['pixels'])
    return out


def process(img_paths: [str], font_paths: [str], artist: str, song_title: str,  extract_mode: str, color_mode: int) -> Image:
    color = ["L", "RGB"]
    img = Image.open(img_paths[0])
    img = crop(img)
    img = apply_vignette(img, color[color_mode])
    img = draw_text(img, font_paths[0], f'{artist} - {song_title}', config.TEXT_TITLE)
    return img
