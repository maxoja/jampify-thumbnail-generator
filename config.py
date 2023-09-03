import os
from enums import TitleConfig, VertAlignment, HorizontalAlignment

IN_DIR = os.getcwd() + "/input"
OUT_DIR = os.getcwd() + "/output"

ARTIST = "Paramore"
SONG = "Last Hope (Live)"
EXTRACT_MODE = "Instrumental Non Vocal"
# Vocal Only
# Instrumental Non Vocal

IMG_TYPES = ["png"]
FONT_TYPES = ["ttf"]

CROP_RATIO_TUPLE = (16, 9)
CROP_RATIO = 16/9
CROP_SCALE = 0.9
CROP_OFFSET = (0.1, 0.22)

VIGNETTE_STR = 0.2
# VIGNETTE_CENTER = (0.25, 0.75)
VIGNETTE_CENTER = (0.25, 0.675)
VIGNETTE_SCALE = (0.15, 0.2)

TEXT_TITLE = {
    TitleConfig.DRAW_AREA: (0.1, 0, 0.9, 0.25),
    TitleConfig.H_ALIGN: HorizontalAlignment.CENTER,
    TitleConfig.V_ALIGN: VertAlignment.CENTER
}

TEXT_EXTRACT = {
    TitleConfig.DRAW_AREA: (0.55, 0.55, 0.9, 0.8),
    TitleConfig.H_ALIGN: HorizontalAlignment.CENTER,
    TitleConfig.V_ALIGN: VertAlignment.TOP
}
