import csv
import numpy as np
import random

from pathlib import Path
import sys
from psychopy import visual, event, core, monitors


project_dir = Path(__file__).resolve().parent.parent
if str(project_dir) not in sys.path:
    sys.path.append(str(project_dir))
from setup import PATHS, Setup


# ------------- Configuration -------------
subject_id = "00"

accommodation_time=Setup.accommodation_time_s

stimulus_time=Setup.fixation_time_s
stimulus_size=Setup.fixation_size_px

stimulus_symbol = Setup.fixation_symbol
stimulus_color = Setup.fixation_color

grid_rows=Setup.grid_rows
grid_columns=Setup.grid_columns

screen_margin=Setup.screen_margin_px
movie_margin = Setup.movie_margin_px


# ------------- Paths -------------
movie_dir = PATHS["movie_dir"]
output_dir = PATHS["exp2_output_dir"] / f"subject_{subject_id}"
calibration_dir = output_dir / "calibration"
output_dir.mkdir(parents=True, exist_ok=True)
calibration_dir.mkdir(parents=True,exist_ok=True)


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

def get_movies(movie_dir:Path)->list[Path]:
    """Return all .mp4 movie paths """
    movie_list = sorted(movie_dir.glob("*.mp4"))

    if not movie_list:
        raise FileNotFoundError(f"Could not find movies in: {movie_dir}")

    return movie_list

def save_data(file_path:Path, header:list[str], data:list[list[object]]) -> None:
    """ Write rows to a CSV file. """
    with file_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)


# ------------- Monitor and window -------------
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

fixation_positions = [(x,y) for x in X for y in Y]
random.shuffle(fixation_positions)
#print(list(fixation_positions))

movie_list = get_movies(movie_dir)[:2]
random.shuffle(movie_list)
#print(movie_list)

fixation = visual.TextStim(
    win=window,
    pos = (0,0),
    text=stimulus_symbol,
    color=stimulus_color,
    height=stimulus_size
)

intro_text = '''
Welcome to the second experiment,

This session begins with a short calibration task.
Please follow the fixation cross.

Afterwards, you will watch several short films,
during which you may look freely at any part of the screen.

Press SPACE to begin.'''


show_text(intro_text)
clock = core.Clock()

# Accomodation
clock.reset()

while clock.getTime() < accommodation_time:
    fixation.draw()
    window.flip()
    check_escape()

# Fixation points -------------
for pos in fixation_positions:
    fixation.pos = pos
    clock.reset()

    while clock.getTime() < stimulus_time:
        fixation.draw()
        window.flip()
        check_escape()

show_text("Calibration complete\n\nPress SPACE to continue to movies.")



# ------------- Movie presentation -------------
for idx,movie_path in enumerate(movie_list):
    print(movie_path.name)
    movie = visual.MovieStim(
        win=window,
        filename=str(movie_path),
        size=(window_width-2*movie_margin,window_height-2*movie_margin),
        pos=(0, 0),
        loop=False,
        volume = 0.0,
        noAudio=True,
        autoStart=False)

    movie.play()

    while not movie.isFinished:
        movie.draw()
        window.flip()

        if 'escape' in event.getKeys():
            movie.stop()
            window.close()
            core.quit()

    movie.stop()
    movie.unload()
    del movie

    window.flip()
    # Break
    if idx < len(movie_list) - 1:
        # Add accomodation phase here two
        show_text("Pause\n\nPress SPACE to continue.")


# ------------- Save data -------------
save_data(
    output_dir /"calibration"/ f"fixation_positions.csv",
    ["x_pix", "y_pix"],
    [[x, y] for x, y in fixation_positions],
)

save_data(
    output_dir / f"movie_order.csv",
    ["movie_order"],
    [[movie_path.stem] for movie_path in movie_list],
)

# Exit screen
show_text("Thank you for participating.\n\nPress SPACE to exit.")

window.close()
core.quit()
