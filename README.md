# Automatic locking in i3 with i3imglock

This is an alternative script to [blurlock](https://github.com/manjaro/packages-community/blob/master/i3/i3exit/blurlock) (default in manjaro with i3), written in python, that randomly chooses an image file from folder './images/' and displays it as the background of i3lock.
The [i3imglock.service](i3imglock.service) file can be used as an example to be executed automatically at suspend.

It can take several command-line arguments for configuration:
- `--images_directory` to choose the directory of the images
- `--logging_level` to set a loglevel
- `--filetypes` to choose which filetypes we sample from
- `--i3lock_options` to set options that are passed to on to `i3lock`
- `--i3lock_fallback_command` to set which command should be executed in case of an error

All arguments can be shown by `i3imglock --help`

## Requirements
- [NumPy](https://numpy.org/)
- [PIL](https://pypi.org/project/Pillow/)
- [screeninfo](https://pypi.org/project/screeninfo/)

Source of the [example image](./images/example.jpg): Jan Zerfowski, Bolivia, Madidi National Park

#### Example
![i3imglock in action](images/example.jpg "Example usage")

## What it can do
- Display random image from folder
- Check file endings and only display settings.filetypes
- Process all filetypes that pillow (https://pillow.readthedocs.io/en/3.1.x/reference/Image.html) understands
- Define fallback locker when file conversion fails

## Installation
- Copy image files in a compatible format to [./images/](./images/) (or any other directory)
- Make i3imglock.py executable
    - `chmod u+x i3imglock.py`
- Create a symbolic link in your $PATH
    - `ln -s <directory of i3imglock.py> /usr/local/bin/i3imglock`
- Copy the [i3imglock.service](./i3imglock.service) file to a folder which systemd cares about
    - `cp i3imglock.service /etc/systemd/system/i3imglock.service`
- To apply custom settings, use arguments when calling
    - `i3imglock.py -h` 

## Issues
- Needs images in exactly 16:9 ratio (or whatever implicit ratio is given by settings['screen_resolution'])
