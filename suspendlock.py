#! /home/jan/miniconda3/bin/python

import os
import numpy as np
import subprocess
import logging

settings = {'script_dir': os.path.dirname(os.path.realpath(__file__)),
            'backgrounds_relative_dir': 'backgrounds/',
            'filetypes': ['.png'],
            'screen_resolution': '1920x1080',
            'i3lock_options': ['--show-failed-attempts', '-t'],
            'i3lock_fallback_command': ['i3lock'],
            'logging_level': logging.DEBUG
            }


def filetype_filter(filename, filetypes):
    return os.path.splitext(filename)[1] in filetypes


def get_images(background_directory, filetype_filter, filetypes):
    images = [image.path for image in os.scandir(background_directory) if filetype_filter(image.path, filetypes)]
    images = [os.path.join(background_directory, image) for image in images]

    return images


logging.basicConfig(level=settings['logging_level'])

logging.debug(f"Script directory: {settings['script_dir']}")

background_directory = os.path.join(settings['script_dir'], settings['backgrounds_relative_dir'])
logging.debug(f"Localizing backgrounds in {background_directory}")

# Get images from background images directory
images = get_images(background_directory, filetype_filter=filetype_filter, filetypes=settings['filetypes'])

# Choose a random image from available images
imagepath = np.random.choice(images)
logging.debug(f"Random image path: {imagepath}")

# Preconfigure the commands for image conversion to a raw format
convert_command = ['convert', '-resize', settings['screen_resolution'], imagepath, 'RGB:-']
i3lock_command = ['i3lock'] + settings['i3lock_options'] + ['--raw', settings['screen_resolution'] + ':rgb', '--image',
                                                            '/dev/stdin']

try:
    logging.debug(f"Calling converter: {' '.join(convert_command)}")
    convert_subprocess = subprocess.Popen(convert_command, stdout=subprocess.PIPE)

    logging.debug(f"Calling locker: {' '.join(i3lock_command)} with stdin from converter")
    i3lock_subprocess = subprocess.Popen(i3lock_command, stdin=convert_subprocess.stdout)
    logging.debug(f"i3lock_subprocess.communicate(): {i3lock_subprocess.communicate()}")
    logging.debug(f"i3lock_subprocess stdout: {i3lock_subprocess.stdout}")

except Exception as e:
    logging.error("Error occured in lockscript. Locking with default i3lock")
    logging.error(e)

    logging.warning(f"Calling i3lock default: {'.'.join(settings['i3lock_fallback_command'])}")
    subprocess.call(settings['i3lock_fallback_command'])
