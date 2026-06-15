'''
Created on Wed Mar 18 09:33:24 2026

@author: Kyle Stock

Gaze_angle:
Presentation of fixation points across screen positions
to measure gaze angle.
'''
from psychopy import core, visual, event, monitors
import numpy as np
import random
import csv
from pathlib import Path
import sys

project_dir = Path(__file__).resolve().parent.parent
if str(project_dir) not in sys.path:
    sys.path.append(str(project_dir))
from setup import PATHS, Setup

subject_id = "01"

# ----------- Import Setup --------------
accommodation_time=Setup.accommodation_time_s

stimulus_time=Setup.fixation_time_s
stimulus_size=Setup.fixation_size_px
stimulus_symbol = Setup.fixation_symbol
stimulus_color = Setup.fixation_color

n_blocks = Setup.n_blocks
grid_rows=Setup.grid_rows
grid_columns=Setup.grid_columns

screen_margin=Setup.screen_margin_px


# ------------- Paths -------------
output_dir = PATHS["exp1_output_dir"] / f"subject_{subject_id}"
output_dir.mkdir(parents=True, exist_ok=True)


# ------------- Helper functions -------------
def check_escape() -> None:
    """ Stops experiment when ESCAPE is pressed. """
    if 'escape' in event.getKeys(keyList=["escape"]):
        window.close()
        core.quit()

def show_text(text:str) -> None:
    """ Display text until SPACE is pressed or abort on ESCAPE. """
    stim = visual.TextStim(
        win=window,
        text=text,
        color='white',
        height=30
    )

    stim.draw()
    window.flip()

    event.clearEvents(eventType="keyboard")
    keys = event.waitKeys(keyList=['space','escape'])

    if 'escape' in keys:
        window.close()
        core.quit()


# ------------- Prepare stimuli -------------
monitor = monitors.Monitor(Setup.monitor_name)
monitor.setWidth(Setup.screen_width_cm)
monitor.setDistance(Setup.viewing_distance_cm)
monitor.setSizePix(Setup.screen_resolution_px)

window = visual.Window(
    size = Setup.screen_resolution_px,
    fullscr = Setup.full_screen,
    color="grey",
    monitor = monitor,
    units= "pix"
)

window_width, window_height = window.size

X = np.linspace(
    -(window_width/2 -screen_margin),
    +(window_width/2 -screen_margin),
    grid_columns
)
Y = np.linspace(
    -(window_height/2 -screen_margin),
    +(window_height/2 -screen_margin),
    grid_rows
)
positions = [(x,y) for x in X for y in Y]
fixation_log = []

fixation = visual.TextStim(
    win=window,
    text=stimulus_symbol,
    color=stimulus_color,
    height=stimulus_size
)



intro_text = '''
Welcome to the gaze angle task,

You will see fixation points appearing at different positions.

Please follow each point with your eyes.

Each block begins with a central fixation.

Press SPACE to begin.'''

show_text(intro_text)
clock = core.Clock()



for block_idx in range(n_blocks):
    trial_pos = positions.copy()
    random.shuffle(trial_pos)

    # Accommodation Phase
    fixation.pos = (0,0)
    clock.reset()

    while clock.getTime() < accommodation_time:
        fixation.draw()
        window.flip()
        check_escape()

    # Trial Loop
    for trial_idx, pos in enumerate(trial_pos):
        fixation.pos = pos

        onset_time = round(core.getTime(),2)
        clock.reset()

        while clock.getTime() < stimulus_time:
            fixation.draw()
            window.flip()
            check_escape()

        fixation_log.append([
            subject_id,
            block_idx +1,
            trial_idx +1,
            float(pos[0]),
            float(pos[1]),
            onset_time,
            stimulus_time
        ])

    # Break
    if block_idx < (n_blocks-1):
        show_text("Pause\n\nPress SPACE to continue.")




# Log the positions of the fixation points.
file_path = output_dir / f"fixation_positions.csv"
with file_path.open('w', newline='', encoding= "utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(fixation_log)

# Add exit screen
show_text("Thank you for participating.\n\nPress SPACE to exit.")


window.close()
core.quit()
