#       linegraph.py
#
#   Plot a line graph, which depicts pauses versus no pauses.
#   Because data collected is only on paused times, not running times,
#   Adds points at (time, 0) to depict running time, before and after each pause
#
#   Ellis Brown, 6/29/2021

#  TODO: plot with rectangles rather than just lines, use opacity as well to make sure that the colors can be seen through each other.

import random
from src.graphing.__generic_mapping import __generic_plotting

#       plot_paused_and_running_line
#
#   Create a 2d line plot, with highs for programming running, and lows for the programming waiting.
#   higher bars and thicker bar widths both mean longer pause time.
#
def plot_paused_and_running_line(
    time_seconds=[], pauses_miliseconds=[], axs=None, color="", label="", const_bar_width=False
):
    # Parameters:
    # time_seconds: list of floats representing timestamps of events
    # pauses_miliseconds: list of floats representing event duration
    # axs: plot to draw on
    # color: string color. Must be included in matplotlib colors
    # label: string used to describe the dataset. Typically filename
    # const_bar_width: If true, all bars have the same width. Recommended only for specially formatted data.
    if not axs:
        print("No axes supplied. Create one using\nf, axs = matplotlib.pyplot.subplots()")
        return
    if not label:
        label = "No label provided"
    if not color:
        r = random.random()
        b = random.random()
        g = random.random()
        color = (r, g, b)
    x_data = []
    y_data = []
    ###### Create X-Y Data. bumps for height based on pause duration #####
    if not const_bar_width:  # outside loop for runtime purposes

        for x, y in zip(time_seconds, pauses_miliseconds):
            # convert y from ms to seconds
            y_scaled = y / 1000
            # first, create a point at time before pause
            x_data.append(x)
            y_data.append(0)
            # next, create a point of y height, at that initial time
            x_data.append(x)
            y_data.append(y)  # CHANGED PLEASE FIX BACK TO 'y'
            # last point in pause duration high
            x_data.append(x + y_scaled)
            y_data.append(y)  # CHANGED PLEASE FIX BACK TO 'y'
            # end pause duration high
            x_data.append(x + y_scaled)
            y_data.append(0)
    else:  # Create buckets of the same size, placed uniformly over time.
        pt_uniform = time_seconds[0] * 0.7  # 0.7 constant for bar width
        # 1 means bars indistinguishable
        # 0 means no bars
        for x, y in zip(time_seconds, pauses_miliseconds):
            x_data.append(x)
            y_data.append(0)
            x_data.append(x)
            y_data.append(y)
            x_data.append(x + pt_uniform)
            y_data.append(y)
            x_data.append(x + pt_uniform)
            y_data.append(0)

    axs.plot(x_data, y_data, color=color, label=label, alpha=0.6)
    axs.grid()
    axs.set_ylabel("Pause duration (miliseconds)")
    axs.set_xlabel("Time from program start (seconds)")
    axs.set_title("Pauses during runtime, running line graph")
    axs.legend()


#       compare_paused_running_line
#
#   Given a set of data to turn into running_line plots, creates a plot and puts them all on the
#   same figure.
#
#   Implementation note: __generic_plotting checks parameter correctness. then calls plot_paused_and_running_line
#
def compare_paused_running_line(xdata_list, ydata_list, axs=None, colors=[], labels=[], const_bar_width=False):
    return __generic_plotting(
        xdata_list, ydata_list, axs, colors, labels, plot_paused_and_running_line, const_bar_width
    )
