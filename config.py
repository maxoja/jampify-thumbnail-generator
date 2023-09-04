from enums import TitleConfig, VertAlignment, HorizontalAlignment

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

COLOR_MODE = ("L", "RGB")

TEXT_TITLE = {
    TitleConfig.DRAW_AREA: (0.1, 0.125, 0.9, 1),
    TitleConfig.H_ALIGN: HorizontalAlignment.CENTER,
    TitleConfig.V_ALIGN: VertAlignment.TOP
}

TEXT_EXTRACT = {
    TitleConfig.DRAW_AREA: (0.5, 0.5, 0.8, 0.8),
    TitleConfig.H_ALIGN: HorizontalAlignment.RIGHT,
    TitleConfig.V_ALIGN: VertAlignment.TOP
}
