from PIL import Image
import math


# https://docs.opencv.org/2.4/modules/imgproc/doc/filtering.html#Mat%20getGaussianKernel(int%20ksize,%20double%20sigma,%20int%20ktype)
def getGaussianKernel(ksize, radius_scale=0.5):
    sigma = 0.4 * ((ksize - 1) * radius_scale - 1) + 0.8
    kernel = []
    scale_factor = 0
    for i in range(ksize):
        coeff = math.e ** (-((i - (ksize - 1) / 2) ** 2) / (2 * sigma ** 2))
        kernel.append(coeff)
        scale_factor += coeff
    for i in range(ksize): kernel[i] /= scale_factor
    return kernel


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


def load_color_image(img: Image):
    """ works like load_greyscale_image but not convert to greyscale"""
    img_data = img.getdata()
    if img.mode.startswith('RGB'):
        pixels = [[ p[0], p[1], p[2] ] for p in img_data]
    elif img.mode == 'LA':
        pixels = [[ p[0], p[0], p[0] ] for p in img_data]
    elif img.mode == 'L':
        pixels = [[p, p, p ] for p in img_data]
    else:
        raise ValueError('Unsupported image mode: %r' % img.mode)
    w, h = img.size
    return {'height': h, 'width': w, 'pixels': pixels}

