#! /usr/bin/python

import os
import numpy as np
import subprocess
import logging
import argparse
import screeninfo
from PIL import Image

logging_levels = {'debug': logging.DEBUG, 'warning': logging.WARNING, 'error': logging.ERROR}
images_directory_default = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images/')
filetypes_default = ['png']
i3lock_options_default = "--show-failed-attempts"
i3lock_fallback_command_default = "i3lock"

parser = argparse.ArgumentParser(
    description='suspendlock.py to call i3lock with custom images and options. Requires numpy, PIL and screeninfo')

parser.add_argument('--images_directory', type=str, default=images_directory_default, required=False,
                    help=f"Absolute directory to images which can be used for i3lock "
                         f"(default: {str(images_directory_default)})")

parser.add_argument('--logging_level', type=str, default='warning', required=False, choices=logging_levels,
                    help=f"Logging level "
                         f"(default: warning)")

parser.add_argument('--filetypes', nargs='+', required=False, default=filetypes_default,
                    help=f"Set filetypes "
                         f"(default: {filetypes_default})")

parser.add_argument('--i3lock_options', type=str, default=i3lock_options_default,
                    help=f'Arguments which are passed on to i3lock '
                         f'(default: --i3lock_options="{i3lock_options_default}")')

parser.add_argument('--i3lock_fallback_command', type=str, default=i3lock_fallback_command_default,
                    help=f'Fallback command if any of the custom script throws an exception. '
                         f'(default: --i3lock_fallback_command="{i3lock_fallback_command_default}")')

settings = parser.parse_args()


def filetype_filter(filename, filetypes):
    # Return if the filetype of filename is contained filetypes
    return os.path.splitext(filename)[1].endswith(tuple(filetypes))


def get_images(image_directory, filetype_filter, filetypes):
    # Get all images that are in image_directory and filter them by using function filetype_filter
    images = [image.path for image in os.scandir(image_directory) if filetype_filter(image.path, filetypes)]
    images = [os.path.join(image_directory, image) for image in images]

    return images


logging.basicConfig(level=logging_levels[settings.logging_level])

# images_directory = os.path.join(settings['script_dir'], settings['backgrounds_relative_dir'])
images_directory = settings.images_directory

# Get images from background images directory
image_paths = get_images(images_directory, filetype_filter=filetype_filter, filetypes=settings.filetypes)
logging.debug(f"Found {len(image_paths)} images in {images_directory}")

# Figure out the total resolution of the screen
monitors = screeninfo.get_monitors()

height = max(monitor.y + monitor.height for monitor in monitors)
width = max(monitor.x + monitor.width for monitor in monitors)

# Set the command for the locking
i3lock_command = ['i3lock'] + settings.i3lock_options.split(' ') + ['--raw', f"{width}x{height}" + ':rgb', '--image',
                                                                    '/dev/stdin']

# Create an empty canvas the size of the entire screen
# Some areas might be left empty (i.e., black), if the screens are not the same sizes
canvas = Image.new(mode='RGB', size=(width, height))
logging.debug(f"Creating canvas with {width}x{height}")

# Choose an independent image for each monitor and paste them onto the canvas at the position of the monitor
image_paths_selected = np.random.choice(image_paths, size=len(monitors), replace=False)
logging.debug(f"Selected {len(image_paths_selected)} image: {image_paths_selected}")

# If size ratios do not match the monitor's ratio, the might currently still get squeezed against their ratio
for monitor, image_path in zip(monitors, image_paths_selected):
    # Choose a random image from available images
    # image_path = np.random.choice(image_paths)
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

    logging.warning(f"Calling i3lock default: {' '.join(settings.i3lock_fallback_command)}")
    subprocess.call(settings.i3lock_fallback_command)
