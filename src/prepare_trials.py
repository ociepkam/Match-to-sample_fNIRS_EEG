import random
from os.path import join
from psychopy import visual
import math


def calculate_position(r, i, n):
    """
    Calculates the position (x, y) for the i-th figure in a circle with radius r,
    assuming n figures are evenly spaced around the circle.

    :param r: Radius of the circle
    :param i: Index of the figure (0 ≤ i < n)
    :param n: Total number of figures in the circle
    :return: Coordinates (x, y)
    """
    angle = 2 * math.pi * i / n  # Angle for the i-th figure
    y = r * math.cos(angle)  # y-coordinate
    x = r * math.sin(angle)  # x-coordinate
    return x, y


def prepare_trials(trials_description, win, config):
    trials_list = []
    for trial_type in trials_description:
        for _ in range(trial_type["n"]):
            figure_central_shape = random.choice(config["figures_shapes"])
            figure_central_color = random.choice(config["figures_colors"])
            figure_central_file = f"{figure_central_shape}_{figure_central_color}.png"
            figure_central_image = visual.ImageStim(win=win,
                                                    image=join("images", figure_central_file),
                                                    pos=config["figure_central_pos"],
                                                    size=config["figure_central_size"])
            figures = [figure_central_image]
            load = trial_type["load"]
            if trial_type["match"]:
                load -= 1
            for i in load:
                pass
            trial = []
            trials_list.append(trial)

r = 100  # Radius of the circle
i = 0    # Index of the figure (figure number 5)
n = 18   # Total number of figures

position = calculate_position(r, i, n)
print(f"Coordinates of figure {i}: {position}")