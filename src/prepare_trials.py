import random
from os.path import join
from psychopy import visual
import numpy as np
import math


def calculate_arc_dots(x0, y0, r, theta_max, n):
    """
    Calculates the coordinates of dots evenly spaced along an arc.

    :param x0: X-coordinate of the red dot (arc center)
    :param y0: Y-coordinate of the red dot (arc center)
    :param r: Radius of the arc (distance to the closest point on the arc)
    :param theta_max: Total angle of the arc in radians (curvature)
    :param n: Number of dots to place along the arc
    :return: List of (x, y) coordinates of the dots
    """

    if n is None or n < 2:
        raise ValueError("Either 'width' or 'n >= 2' must be provided.")

    # Calculate angular spacing between dots
    theta_start = -theta_max / 2  # Start angle of the arc
    theta_end = theta_max / 2  # End angle of the arc
    angles = np.linspace(theta_start, theta_end, n)  # Evenly spaced angles

    # Calculate coordinates of the dots
    coordinates = [
        (x0 + r * np.cos(theta), y0 + r * np.sin(theta))
        for theta in angles
    ]
    return coordinates


def prepare_trials(trials_description, win, config):
    trials_list = []
    coordinates = calculate_arc_dots(config["figure_central_pos"][0], config["figure_central_pos"][1], config["figure_cluster_radius"],
                                     config["cluster_angle"], config["maximum_load"])

    for trial_type in trials_description:
        for _ in range(trial_type["n"]):
            random.shuffle(coordinates)
            figure_central_shape = random.choice(config["figures_shapes"])
            figure_central_color = random.choice(config["figures_colors"])
            figure_central_file = f"{figure_central_shape}_{figure_central_color}.png"
            figure_central_image = visual.ImageStim(win=win,
                                                    image=join("images", figure_central_file),
                                                    pos=config["figure_central_pos"],
                                                    size=config["figure_central_size"])
            figures = [figure_central_image]
            load = trial_type["load"]
            # if trial_type["match"]:
            #     load -= 1
            #     pass
            for i in load:
                figure = visual.ImageStim(win=win,
                                          image=join("images", figure_central_file),
                                          pos=coordinates[i],
                                          size=config["figure_cluster_size"])
                figures.append(figure)
            trial = {"figures": figures, "load": load, "match": trial_type["match"], "hemifield": trial_type["hemifield"]}
            trials_list.append(trial)

print(calculate_arc_dots(0, 0, 100, 180, 8))
