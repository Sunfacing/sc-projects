"""
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.

This file will draw a plot chart of searched names with the rank in each year from
1900 to 2010
"""

import tkinter
import babynames
import babygraphicsgui as gui

FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt'
]
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
GRAPH_MARGIN_SIZE = 20
COLORS = ['red', 'purple', 'green', 'blue']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index of the current year in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                              with the specified year.
    """
    interval = (width - 2 * GRAPH_MARGIN_SIZE) / len(YEARS)
    return interval * year_index + GRAPH_MARGIN_SIZE


def draw_fixed_lines(canvas):
    """
    Erases all existing information on the given canvas and then
    draws the fixed background lines on it.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.

    Returns:
        This function does not return any value.
    """
    canvas.delete('all')            # delete all existing lines from the canvas

    # Write your code below this line
    #################################
    canvas.create_line(GRAPH_MARGIN_SIZE, 0, GRAPH_MARGIN_SIZE, CANVAS_HEIGHT, width=LINE_WIDTH)  # left_line
    canvas.create_line(GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE, CANVAS_WIDTH - GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE, width=LINE_WIDTH)  # top_line
    canvas.create_line(GRAPH_MARGIN_SIZE, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE, CANVAS_WIDTH - GRAPH_MARGIN_SIZE, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE, width=LINE_WIDTH)  # bottom_line
    for i in range(len(YEARS)):
        x_position = get_x_coordinate(CANVAS_WIDTH, i)
        canvas.create_line(x_position, 0, x_position, CANVAS_HEIGHT, width=LINE_WIDTH)
        canvas.create_text(x_position + TEXT_DX, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE, text=YEARS[i], anchor=tkinter.NW, font='helvetica 10')



def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)        # draw the fixed background grid

    # Write your code below this line
    #################################
    color_index = 0
    for name in lookup_names:
        color_index %= len(COLORS)
        if name in name_data.keys():
            for i in range(len(YEARS)):
                x2_position = get_x_coordinate(CANVAS_WIDTH, i)
                if i == 0:
                    if str(YEARS[i]) in name_data[name].keys():
                        rank = name + ' ' + name_data[name][str(YEARS[i])]
                        y1_position = (int(name_data[name][str(YEARS[i])]) / 1000) * 600 + GRAPH_MARGIN_SIZE
                    else:
                        rank = name + ' *'
                        y1_position = CANVAS_HEIGHT - GRAPH_MARGIN_SIZE
                    canvas.create_text(x2_position + TEXT_DX, y1_position, text=rank, anchor=tkinter.SW,
                                       font='helvetica 10', fill=COLORS[color_index])
                else:
                    x1_position = get_x_coordinate(CANVAS_WIDTH, i - 1)
                    if str(YEARS[i - 1]) in name_data[name].keys():
                        y1_position = (int(name_data[name][str(YEARS[i - 1])]) / 1000) * (600 - 2 * GRAPH_MARGIN_SIZE) + GRAPH_MARGIN_SIZE
                    else:
                        y1_position = CANVAS_HEIGHT - GRAPH_MARGIN_SIZE

                    if str(YEARS[i]) in name_data[name].keys():
                        y2_position = (int(name_data[name][str(YEARS[i])]) / 1000) * (600 - 2 * GRAPH_MARGIN_SIZE) + GRAPH_MARGIN_SIZE
                        rank = name + ' ' + name_data[name][str(YEARS[i])]
                    else:
                        y2_position = CANVAS_HEIGHT - GRAPH_MARGIN_SIZE
                        rank = name + ' *'

                    canvas.create_line(x1_position, y1_position, x2_position, y2_position, width=LINE_WIDTH, fill=COLORS[color_index])
                    canvas.create_text(x2_position + TEXT_DX, y2_position, text=rank, anchor=tkinter.SW, font='helvetica 10', fill=COLORS[color_index])
            color_index += 1

# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
