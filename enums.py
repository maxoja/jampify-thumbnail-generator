from enum import Enum


class TitleConfig(Enum):
    DRAW_AREA = 'coord'
    H_ALIGN = 'h_align'
    V_ALIGN = 'v-align'
    OFFSET = 'offset'


class VertAlignment(Enum):
    TOP = 'top'
    CENTER = 'center'
    BOTTOM = 'bottom'


class HorizontalAlignment(Enum):
    LEFT = 'left'
    CENTER = 'center'
    RIGHT = 'right'

# Usage
# current_status = Status.PENDING
# print(current_status)  # Output: Status.PENDING

# Convert enum to string
# status_string = current_status.value
# print(status_string)  # Output: 'pending'

# Convert string to enum
# new_status = Status(status_string)
# print(new_status)  # Output: Status.PENDING
