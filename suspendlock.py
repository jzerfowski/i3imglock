#! /home/jan/miniconda3/bin/python

import os
import numpy as np
import subprocess
import logging
import screeninfo
from PIL import Image

# Set our configuration
settings = {'script_dir': os.path.dirname(os.path.realpath(__file__)),
            'backgrounds_relative_dir': 'backgrounds/',
            'filetypes': ['.png'],
            'i3lock_options': ['--show-failed-attempts'],
            'i3lock_fallback_command': ['i3lock'],
            'logging_level': logging.DEBUG
            }


def filetype_filter(filename, filetypes):
    # Return if the filetype of filename is contained filetypes
    return os.path.splitext(filename)[1] in filetypes


def get_images(image_directory, filetype_filter, filetypes):
    # Get all images that are in image_directory and filter them by using function filetype_filter
    images = [image.path for image in os.scandir(image_directory) if filetype_filter(image.path, filetypes)]
    images = [os.path.join(image_directory, image) for image in images]

    return images


logging.basicConfig(level=settings['logging_level'])
logging.debug(f"Script directory: {settings['script_dir']}")

# The backgrounds should be put relative to the directory of the script in settings['backgrounds_relative_dir']
images_directory = os.path.join(settings['script_dir'], settings['backgrounds_relative_dir'])
logging.debug(f"Localizing backgrounds in {images_directory}")

# Get images from background images directory
image_paths = get_images(images_directory, filetype_filter=filetype_filter, filetypes=settings['filetypes'])

# Figure out the total resolution of the screen
monitors = screeninfo.get_monitors()

height = max(monitor.y + monitor.height for monitor in monitors)
width = max(monitor.x + monitor.width for monitor in monitors)

# Set the command for the locking
i3lock_command = ['i3lock'] + settings['i3lock_options'] + ['--raw', f"{width}x{height}" + ':rgb', '--image',
                                                            '/dev/stdin']

# Create an empty canvas the size of the entire screen
# Some black borders might be left black, if the screens are not the same sizes
canvas = Image.new(mode='RGB', size=(width, height))

# Choose an independent image for each monitor and paste them onto the canvas at the position of the monitor
# If size ratios do not match the monitor's ratio, the might currently still get squeezed against their ratio
for monitor in monitors:
    # Choose a random image from available images
    image_path = np.random.choice(image_paths)
    image = Image.open(image_path)
    image = image.resize(size=(monitor.width, monitor.height))
    canvas.paste(image, box=(monitor.x, monitor.y, monitor.x + monitor.width, monitor.y + monitor.height))

try:
    logging.debug(f"Calling locker: {' '.join(i3lock_command)} with our canvas as input")
    i3lock_subprocess = subprocess.Popen(i3lock_command, stdin=subprocess.PIPE)
    i3lock_communicate = i3lock_subprocess.communicate(input=canvas.tobytes())

    logging.debug(f"i3lock_subprocess.communicate(): {i3lock_communicate}")
    logging.debug(f"i3lock_subprocess stdout: {i3lock_subprocess.stdout}")

except Exception as e:
    logging.error("Error occured in lockscript. Locking with default i3lock")
    logging.error(e)

    logging.warning(f"Calling i3lock default: {' '.join(settings['i3lock_fallback_command'])}")
    subprocess.call(settings['i3lock_fallback_command'])
