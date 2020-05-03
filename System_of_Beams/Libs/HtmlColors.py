from enum import Enum, unique
"""
All available and used colors
To check color, insert value at this website:
https://www.w3schools.com/colors/colors_picker.asp
"""


@unique
class HtmlColors(Enum):
    white = "#ffffff"
    BLACK = "#000000"       # x and y axis in input plot
    BLUE_TUM    = "#3070b3" # used for invisible tooltip circles
    ORANGE_TUM  = '#e37222' # used for output plot
    GREEN_TUM   = '#a2ad00' # used for output plot
    accent1 = "#98C6EA"     # light light blue
    accent2 = "#64A0C8"     # light blue
    accent3 = "#DAD7CB"     # ivory
    accent4 = "#E37222"     # orange
    GREEN = "#A2AD00"       # (TUM) used for invisible tooltip circles
    lightgrey = "#f5f5f5"   # grid color in plot
    LIGHTGRAY = "#DCDCDC"   # minor grid color in input plot, beam fill color
    # used separately(!) as backgroundcolor for activated button and element info box
    ORANGE = "#ffa500"      # line loads
    # used separately (!) for message box in styles.css
    RED = "#ff4500"         # used for showing the first selected element for line element in input plot
    # used separately(!) for message box in styles.css
    SIENNA = "#A0522D"

    plot_col4 = "#FF7F50"
    plot_col5 = "#FF1493"
    plot_col6 = "#800000"
    plot_col7 = "#7B68EE"
    plot_col8 = "#708090"
    plot_col9 = "#008080"
    plot_col10 = "#BDB76B"


plot_cols = [HtmlColors.BLUE_TUM, HtmlColors.GREEN_TUM, HtmlColors.ORANGE_TUM]
