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

# ------------- Configuration -------------

subject_id = "01"

accommodation_time = 1.0    # Final experiment : 15.0
stimulus_time = 1.0         # Final experiment : 2.5
stimulus_size = 20          # in [px]

n_blocks = 2                # Final experiment : 5
grid_rows = 3
grid_columns = 4

screen_width = 53           # in [cm]
viewing_distance = 58       # in [cm]
screen_res = (1500,960)     # in [pixel]
screen_margin = 40

# ------------- Paths -------------
project_dir = Path(__file__).resolve().parent.parent
output_dir = project_dir / "Data" /"Output" / "1_exp"
output_dir.mkdir(exist_ok=True)


# ------------- Helper functions -------------
def check_escape() -> None:
    """ Stops experiment when ESCAPE is pressed. """
    if 'escape' in event.getKeys():
        window.close()
        core.quit()

def show_text(text:str) -> None:
    """ Display text until SPACE is pressed or abort on ESCAPE. """
    stim = visual.TextStim(
        win=window,
        text=text,
        color='white',
        height=stimulus_size
    )

    stim.draw()
    window.flip()

    event.clearEvents(eventType="keyboard")
    keys = event.waitKeys(keyList=['space','escape'])

    if 'escape' in keys:
        window.close()
        core.quit()


# ------------- Monitor and window -------------
monitor = monitors.Monitor("test_monitor")
monitor.setWidth(screen_width)
monitor.setDistance(viewing_distance)
monitor.setSizePix(screen_res)

window = visual.Window(
    size = screen_res,
    fullscr = True,
    color='grey',
    monitor = monitor,
    units="pix"
)
window_width, window_height = window.size

# ------------- Prepare stimuli -------------

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
log_pos = []

fixation = visual.TextStim(
    win=window,
    text='+',
    color='white',
    height=30
)



intro_text = '''
Welcome to the gaze angle task,

You will see fixation points appearing at different positions.

Please follow each point with your eyes.

Each block begins with a central fixation.

Press SPACE to begin.'''

show_text(intro_text)
clock = core.Clock()



for block in range(n_blocks):
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
    for pos in trial_pos:
        fixation.pos = pos
        clock.reset()

        while clock.getTime() < stimulus_time:
            fixation.draw()
            window.flip()
            check_escape()


    # Break
    if block < (n_blocks-1):
        show_text("Pause\n\nPress SPACE to continue.")
    log_pos.append(trial_pos)



# Also log the positions of the fixation points.
file_path = output_dir / f"{subject_id}_positions.csv"
with file_path.open('w', newline='', encoding= "utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(log_pos)

# Add exit screen
show_text("Thank you for participating.\n\nPress SPACE to exit.")


window.close()
core.quit()
