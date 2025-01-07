import atexit
from psychopy import visual, event, core
from os.path import join
import random
import datetime

from src.screen_misc import get_screen_res
from src.check_exit import check_exit
from src.load_data import load_config
from src.show_info import show_info, part_info
from src.prepare_trials import prepare_trials

PART_ID = ""


@atexit.register
def save_results():
    current_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = f'{PART_ID}_{current_datetime}.txt'
    with open(join('results', file_name), 'w', newline='') as file:
        pass  # TODO


def main():
    global PART_ID
    config = load_config()
    info, PART_ID = part_info()

    screen_res = dict(get_screen_res())
    win = visual.Window(list(screen_res.values()), fullscr=True, monitor='testMonitor', units='pix', screen=0,
                        color=config["screen_color"])
    event.Mouse(visible=False)
    clock = core.Clock()
    fixation = visual.TextStim(win, color=config["fixation_color"], text=config["fixation_text"], height=config["fixation_size"])

    # --------------------------------------- procedure ---------------------------------------
    # training
    if config["training"]:
        trials = prepare_trials(trials_description=config["training_trials"], win=win, config=config)

    # experiment
    trials = prepare_trials(trials_description=config["experiment_trials"], win=win, config=config)

    # end screen
    show_info(win=win, file_name=join("messages", "end.txt"), text_size=config["text_size"], text_color=config["text_color"], screen_res=screen_res)


if __name__ == "__main__":
    main()
