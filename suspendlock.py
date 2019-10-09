#! /home/jan/miniconda3/bin/python

import os
import numpy as np
import subprocess
import logging

logging.basicConfig(level=logging.INFO)


def filetype_filter(filename, filetypes):
    return any([filename.endswith(filetype) for filetype in filetypes])


def get_images(background_directory, filetype_filter, filetypes):
    images = [image.path for image in os.scandir(background_directory) if filetype_filter(image.path, filetypes)]
    images = [os.path.join(background_directory, image) for image in images]

    return images


settings = {}
settings['script_dir'] = os.path.dirname(os.path.realpath(__file__))
settings['backgrounds_relative_dir'] = 'backgrounds/'
settings['filetypes'] = ['png']
settings['screen_resolution'] = '1920x1080'
settings['i3lock_options'] = ['--show-failed-attempts', '-t']
settings['i3lock_fallback_command'] = ['i3lock']

background_directory = os.path.join(settings['script_dir'], settings['backgrounds_relative_dir'])

# Get images from background images directory
images = get_images(background_directory, filetype_filter=filetype_filter, filetypes=settings['filetypes'])

# Choose a random image from available images
imagepath = np.random.choice(images)

# Preconfigure the commands for image conversion to a raw format
convert_command = ['convert', '-resize', settings['screen_resolution'], imagepath, 'RGB:-']
i3lock_command = ['i3lock'] + settings['i3lock_options'] + ['--raw', settings['screen_resolution'] + ':rgb', '--image',
                                                            '/dev/stdin']

try:
    logging.debug(f"Calling converter: {' '.join(convert_command)}")
    convert_subprocess = subprocess.Popen(convert_command, stdout=subprocess.PIPE)

    logging.debug(f"Calling locker: {' '.join(i3lock_command)} with stdin from converter")
    i3lock_subprocess = subprocess.Popen(i3lock_command, stdin=convert_subprocess.stdout)
    logging.debug(i3lock_subprocess.communicate())
    logging.debug(i3lock_subprocess.stdout())
except Exception as e:
    logging.error("Error occured in lockscript. Locking with default i3lock")
    logging.error(e)

    logging.warning(f"Calling i3lock default: {'.'.join(settings['i3lock_fallback_command'])}")
    subprocess.call(settings['i3lock_fallback_command'])
