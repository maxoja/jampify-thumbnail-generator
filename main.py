# This is a sample Python script.
import os

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import config
import utils
import img


def filter_extension(path: str, extensions: [str]) -> bool:
    return path.split('.')[-1].lower() in extensions


def get_input_file_paths(file_paths: [str], extensions: [str]) -> [str]:
    return list(filter(lambda p: filter_extension(p, extensions), file_paths))


if __name__ == '__main__':
    current_working_dir = os.getcwd()
    input_files = utils.get_absolute_file_paths(current_working_dir + "/input")
    img_paths = get_input_file_paths(input_files, config.IMG_TYPES)
    font_paths = get_input_file_paths(input_files, config.FONT_TYPES)
    print('input images', img_paths)
    print('input fonts', font_paths)

    #out_img = img.process(img_paths, font_paths, config.ARTIST, config.SONG, config.EXTRACT_MODE, config.COLOR_MODE[1])
    out_img = img.process(img_paths, font_paths, config.ARTIST, config.SONG, config.EXTRACT_MODE)
    out_img.show()

    w_dpi = 1200
    h_dpi = 700
    img.save_image(out_img, os.path.join(os.path.dirname(img_paths[0]), "output.png"), w_dpi, h_dpi)

