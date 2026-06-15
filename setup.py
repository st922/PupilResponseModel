"""
Created on Tue Jun 09 13:21:14 2026

@author: Kyle Stock

Settings:
Shared configuration and helper functions for the pupil experiments.

"""
from pathlib import Path


# ---------------- Paths ----------------

PROJECT_DIR = Path(__file__).resolve().parent
PATHS = {
    "data_dir": PROJECT_DIR / "data",
    "movie_dir": PROJECT_DIR / "data" / "stimuli" / "movies",
    "exp1_output_dir": PROJECT_DIR / "data" / "raw" / "exp1",
    "exp2_output_dir": PROJECT_DIR / "data" / "raw" / "exp2",
    "exp1_intermediate_dir": PROJECT_DIR / "data" / "intermediate" / "exp1",
    "exp1_processed_dir": PROJECT_DIR / "data" / "processed" / "exp1",

}

# ---------------- Setup classes ----------------
class Setup:
    """Physical properties of the experimental setup."""

    # Monitor
    monitor_name = "test_monitor"

    screen_width_cm = 59.5
    viewing_distance_cm = 65.0
    screen_resolution_px = (1536,960)

    full_screen = True

    # Gaze Angle
    accommodation_time_s = 1.0   # Final experiment: 15.0
    fixation_time_s = 1.0        # Final experiment: 2.5
    break_time_s = 10.0          # Final experiment: 10.0

    n_blocks = 2                   # Final experiment: 5
    grid_rows = 3
    grid_columns = 4

    fixation_symbol = "+"
    fixation_color = "white"
    fixation_size_px = 30

    # Margins
    screen_margin_px = 40
    movie_margin_px = 0


    # Tobii camera properties
    center_shift = True
    @classmethod
    def get_recording_interval(cls):
        start_time = cls.accommodation_time_s
        end_time = start_time + cls.fixation_time_s * cls.grid_rows * cls.grid_columns
        return start_time,end_time
