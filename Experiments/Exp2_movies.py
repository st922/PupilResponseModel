import csv
import numpy as np
from pathlib import Path
from psychopy import visual, event, core, monitors
import random



# ------------- Configuration -------------

subject_id = "01"

accommodation_time = 1.0    # Fianl experiment : 15.0
stimulus_time = 1.0         # Final experiment : 2.5

grid_rows = 3
grid_columns = 4

screen_width = 53           # in [cm]
viewing_distance = 58       # in [cm]
screen_res = (1500,960)     # in [px]
screen_margin = 40          # in [px]

# ------------- Paths -------------
project_dir = Path(__file__).resolve().parent.parent

movie_dir = project_dir / "Data" / "Input" / "Movies"
output_dir = project_dir / "Data" /"Output" / "2_exp"
output_dir.mkdir(exist_ok=True)

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
        height=20
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

fixation_positions = [(x,y) for x in X for y in Y]
random.shuffle(fixation_positions)

movie_list = get_movies(movie_dir)
random.shuffle(movie_list)


fixation = visual.TextStim(
    win=window,
    pos = (0,0),
    text='+',
    color='white',
    height=30
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

show_text("Pause\n\nPress SPACE to continue.")


# Movie presentation
for idx,movie_path in enumerate(movie_list):
    print(movie_path.name)
    movie = visual.MovieStim(
        win=window,
        filename=str(movie_path),
        size=(window_width-2*screen_margin,window_height-2*screen_margin),
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
    output_dir / f"{subject_id}_positions.csv",
    ["x_pix", "y_pix"],
    [[x, y] for x, y in fixation_positions],
)

save_data(
    output_dir / f"{subject_id}_movies.csv",
    ["movie_order"],
    [[movie.name] for movie in movie_list],
)

# Exit screen
show_text("Thank you for participating.\n\nPress SPACE to exit.")

window.close()
core.quit()
