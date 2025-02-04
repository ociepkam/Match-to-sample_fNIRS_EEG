import atexit
from psychopy import visual, event, core
from os.path import join
import random
import datetime
import csv

from src.screen_misc import get_screen_res
from src.check_exit import check_exit
from src.load_data import load_config
from src.show_info import show_info, part_info
from src.prepare_trials import prepare_trials

PART_ID = ""
RESULTS = []
LSL_OUTLET = None
SEND_TRIGGERS = False

@atexit.register
def save_results():
    current_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = f'{PART_ID}_{current_datetime}.csv'
    with open(join('results', file_name), 'w', newline='') as beh_file:
        dict_writer = csv.DictWriter(beh_file, RESULTS[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(RESULTS)


def draw_stimulus(stimulus, clock, win, stimulus_time, idx):
    stimulus.setAutoDraw(True)
    win.callOnFlip(clock.reset)
    if SEND_TRIGGERS:
        win.callOnFlip(LSL_OUTLET.push_sample, x=[int("1" + str(idx))])
    win.flip()
    while clock.getTime() < stimulus_time:
        check_exit()
    stimulus.setAutoDraw(False)

def run_block(trials, win, config, clock, fixation, block_type):
    for idx, trial in enumerate(trials):
        acc = None
        reaction_time = None
        key = None
        # fixation
        if config["first_fixation"] and idx == 0 and block_type == "experiment":
            fixation_time = config["first_fixation_time"]
        else:
            fixation_time = random.uniform(config[f"{block_type}_fixation_time"][0],
                                           config[f"{block_type}_fixation_time"][1])
        draw_stimulus(stimulus=fixation, clock=clock, win=win, stimulus_time=fixation_time, idx=idx)

        # stimulus
        win.callOnFlip(event.clearEvents)
        win.callOnFlip(clock.reset)
        for figure in trial["figures"]:
            figure.setAutoDraw(True)
        if SEND_TRIGGERS:
            win.callOnFlip(LSL_OUTLET.push_sample, x=[int("2" + str(idx))])
        win.flip()
        while clock.getTime() < config[f"{block_type}_time"]:
            key = event.getKeys(keyList=config["reaction_keys"].values())
            if key:
                reaction_time = clock.getTime()
                if SEND_TRIGGERS:
                    LSL_OUTLET.push_sample(x=[int("3" + str(idx))])
                key = key[0]
                break
            check_exit()

        for figure in trial["figures"]:
            figure.setAutoDraw(False)

        # results
        if key:
            if (key == config["reaction_keys"]["match"] and trial["match"]) or \
               (key == config["reaction_keys"]["no match"] and not trial["match"]):
                acc = 1
            else:
                acc = 0

        trial_results = {"idx": idx,
                         "block_type": block_type,
                         "acc": acc,
                         "rt": reaction_time,
                         "load": trial["load"],
                         "hemifield": trial["hemifield"],
                         "match": trial["match"],
                         "figures": trial["figures_description"]}
        RESULTS.append(trial_results)
        # feedback
        if block_type == "training" and config["feedback"]:
            if acc == 1:
                feedback_text = config["feedback_correct"]
            elif acc == 0:
                feedback_text = config["feedback_incorrect"]
            else:
                feedback_text = config["feedback_no_ans"]

            feedback = visual.TextStim(win, text=feedback_text, color=config["feedback_color"],
                                       height=config["feedback_size"])
            draw_stimulus(feedback, clock, win, config["feedback_time"])

        # wait
        wait_time = random.uniform(config[f"{block_type}_wait_time"][0],
                                   config[f"{block_type}_wait_time"][1])
        while clock.getTime() < wait_time:
            check_exit()
            win.flip()

def main():
    global PART_ID, LSL_OUTLET, SEND_TRIGGERS
    config = load_config()
    info, PART_ID = part_info()

    screen_res = dict(get_screen_res())
    win = visual.Window(list(screen_res.values()), fullscr=True, monitor='testMonitor', units='pix', screen=0,
                        color=config["screen_color"])
    event.Mouse(visible=False)
    clock = core.Clock()
    fixation = visual.TextStim(win, color=config["fixation_color"], text=config["fixation_text"], height=config["fixation_size"])

    SEND_TRIGGERS = config["send_lsl_triggers"]
    if SEND_TRIGGERS:
        from pylsl import StreamInfo, StreamOutlet
        lsl_info = StreamInfo(name="TriggerStream", type="Triggers", channel_count=1, nominal_srate=0,
                              channel_format="int32", source_id="Match_to_sample")
        LSL_OUTLET = StreamOutlet(info=lsl_info)

    # --------------------------------------- procedure ---------------------------------------
    # training
    if config["training"]:
        trials = prepare_trials(trials_description=config["training_trials"], win=win, config=config)
        show_info(win=win, file_name=join("messages", f"training.txt"), text_size=config["text_size"],
                  text_color=config["text_color"], screen_res=screen_res)
        run_block(trials=trials, win=win, config=config, clock=clock, fixation=fixation, block_type="training")
    # experiment
    trials = prepare_trials(trials_description=config["experiment_trials"], win=win, config=config)
    show_info(win=win, file_name=join("messages", f"experiment.txt"), text_size=config["text_size"],
              text_color=config["text_color"], screen_res=screen_res)
    run_block(trials=trials, win=win, config=config, clock=clock, fixation=fixation, block_type="experiment")

    # end screen
    show_info(win=win, file_name=join("messages", "end.txt"), text_size=config["text_size"], text_color=config["text_color"], screen_res=screen_res)


if __name__ == "__main__":
    main()
