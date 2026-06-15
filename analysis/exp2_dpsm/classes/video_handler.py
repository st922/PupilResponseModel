# -*- coding: utf-8 -*-
"""
Created on Tue May 19 15:28:38 2026

@author: stock
"""
from typing import Optional
import numpy as np
from scipy.interpolate import PchipInterpolator
from matplotlib import pyplot as plt
import pickle
from dataclasses import dataclass
from pathlib import Path
#from moviepy.video.io import *
#import moviepy.video.io
import cv2


@dataclass
class VisualFieldMask:
    """
    Reusable visual-field mask template.

    The template depends on the experimental geometry and regional
    weighting configuration, but not on the subject or gaze trajectory.
    """
    map_type: str

    final_width_px: int
    final_height_px: int

    # Scale factor used by the original Open-DPSM implementation
    scale_factor: float

    # Only used for circular masks
    region_label_map: Optional[np.ndarray] = None
    region_masks_flat: Optional[np.ndarray] = None
    pixels_per_region: Optional[np.ndarray] = None

    # Only used for square masks
    square_width_px: Optional[int] = None
    square_height_px: Optional[int] = None
