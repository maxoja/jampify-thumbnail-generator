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
    input_files = utils.get_absolute_file_paths(config.IN_DIR)
    img_paths = get_input_file_paths(input_files, config.IMG_TYPES)
    font_paths = get_input_file_paths(input_files, config.FONT_TYPES)
    print('input images', img_paths)
    print('input fonts', font_paths)

    out_img = img.process(img_paths, font_paths, config.ARTIST, config.SONG, config.EXTRACT_MODE)
    if not out_img.mode.startswith('RGB'):
        out_img = out_img.convert('RGB')
    out_img.save(config.OUT_DIR + "/img.png")
    out_img.show()

