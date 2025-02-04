import random
from os.path import join
from psychopy import visual

from src.fugures_position import generate_points


def prepare_trials(trials_description, win, config):
    trials_list = []
    coordinates = generate_points(x0=config["figure_central_pos"][0],
                                  y0=config["figure_central_pos"][1],
                                  r0=config["figure_arc_radius0"],
                                  r1=config["figure_arc_radius1"],
                                  theta=config["figure_arc_angle"],
                                  n=config["maximum_load"])

    for trial_type in trials_description:
        for _ in range(trial_type["n"]):
            random.shuffle(coordinates)
            figures_shapes = config["figures_shapes"][:]
            figures_colors = config["figures_colors"][:]
            random.shuffle(figures_shapes)
            random.shuffle(figures_colors)

            figure_central_file = f"{figures_shapes[0]}_{figures_colors[0]}.png"
            figure_central_image = visual.ImageStim(win=win,
                                                    image=join("images", figure_central_file),
                                                    pos=config["figure_central_pos"],
                                                    size=config["figure_central_size"])
            figures = [figure_central_image]
            figures_description = [{"pos": config["figure_central_pos"], "file": figure_central_file}]
            load = trial_type["load"]
            if trial_type["match"]:
                load -= 1
                coordinate = coordinates[0][:]
                if trial_type["hemifield"] == "left":
                    coordinate[0] *= -1
                figure_file = f"{figures_shapes[0]}_{figures_colors[-1]}.png"
                figure = visual.ImageStim(win=win,
                                          image=join("images", figure_file),
                                          pos=coordinate,
                                          size=config["figure_cluster_size"])
                figures.append(figure)
                figures_description.append({"pos": coordinate, "file": figure_file})

            for i in range(load):
                idx = i
                if trial_type["match"]:
                    idx += 1
                coordinate = coordinates[idx][:]
                if trial_type["hemifield"] == "left":
                    coordinate[0] *= -1
                figure_file = f"{figures_shapes[i+1]}_{figures_colors[i+1]}.png"
                figure = visual.ImageStim(win=win,
                                          image=join("images", figure_file),
                                          pos=coordinate,
                                          size=config["figure_cluster_size"])
                print(figure.pos)
                figures.append(figure)
                figures_description.append({"pos": coordinate, "file": figure_file})
            trial = {"figures": figures,
                     "load": load,
                     "match": trial_type["match"],
                     "hemifield": trial_type["hemifield"],
                     "figures_description": figures_description}
            trials_list.append(trial)

    random.shuffle(trials_list)
    return trials_list
