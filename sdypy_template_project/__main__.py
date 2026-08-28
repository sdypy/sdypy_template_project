'''
The code inside `__main__.py` runs when this module is run from the command line with:

    python -m sdypy_template_project [path/to/video.npy]

If no path is given, the example video shipped with the repository
(`examples/speckle.npy`) is used.
'''

import sys
import os

import numpy as np
from matplotlib import pyplot as plt

from .visualize import animate_video

DEFAULT_VIDEO = os.path.join('examples', 'speckle.npy')

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = DEFAULT_VIDEO

if not os.path.isfile(filename):
    sys.exit(f'Video file not found: {filename}\n'
             f'Usage: python -m sdypy_template_project [path/to/video.npy]')

# Load the video: an array of shape (n_frames, height, width)
images = np.load(filename, mmap_mode='r')

# Show the animation
ani = animate_video(images, fps=30, bit_depth=12)
plt.show()
