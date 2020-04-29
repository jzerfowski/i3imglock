# Automatic locking in i3 with i3imglock

This is an alternative script to [blurlock](https://github.com/manjaro/packages-community/blob/master/i3/i3exit/blurlock) (default in [manjaro](https://manjaro.org/) with [i3wm](https://i3wm.org/)), written in python, that randomly chooses an image file from folder './images/' and displays it as the background of [i3lock](https://i3wm.org/i3lock/).
The [i3imglock.service](i3imglock.service) file can be used as an example to be executed automatically at suspend.

It can take several command-line arguments for configuration:
- `--images_directory` to choose the directory of the images
- `--logging_level` to set a loglevel
- `--filetypes` to choose which filetypes we sample from
- `--i3lock_options` to set options that are passed to on to `i3lock`
- `--i3lock_fallback_command` to set which command should be executed in case of an error

All arguments can be shown by `i3imglock --help`

#### Disclaimer
You're using this at your own risk! I cannot be held responsible when you lock yourself out, your computer explodes or anything else happens. 

## Requirements
- [i3lock](https://github.com/i3/i3lock)
- [NumPy](https://numpy.org/)
- [Pillow](https://pypi.org/project/Pillow/)
- [screeninfo](https://pypi.org/project/screeninfo/)


## Example usage
Source of the [example image](readme_example_image.png): [Jan Zerfowski](https://janzerfowski.de), Bolivia, Madidi National Park

![i3imglock in action](readme_example_image.png "Example usage")

## What it can do
- Display random image from folder
- Check file endings and only display specific filetypes
- Process all filetypes that pillow (https://pillow.readthedocs.io/en/3.1.x/reference/Image.html) understands
- Define fallback locker when file conversion fails

## Installation
- Copy image files in a compatible format to [./images/](./images/) (or any other directory)
- Make i3imglock.py executable
    - `chmod u+x i3imglock.py`
- Create a symbolic link in your $PATH
    - `ln -s <directory of i3imglock.py>/i3imglock.py /usr/local/bin/i3imglock`
- Copy the [i3imglock.service](/i3imglock.service) file to a folder which systemd cares about
    - `cp i3imglock.service /etc/systemd/system/i3imglock.service`
- Set your username in the User variable in the i3imglock.service file (otherwise the numpy import throws an error)
- Enable the service
    - `systemctl enable i3imglock.service`
- Set the appropriate keybindings in your `~/.i3/config`-file
    - `bindsym $mod+9 exec --no-startup-id i3imglock`
    - `exec --no-startup-id xautolock -time 10 -locker i3imglock`
- The `$mod+0` keybinding executes i3exit. Change i3exit by replacing blurlock with a function that executes i3imglock
    - A working version of i3exit can be found [here](/i3exit)
- To apply custom settings, use the possible arguments 
    - `i3imglock.py -h` 

## Issues
- Needs images in exactly 16:9 ratio (or whatever implicit ratio is given by `settings['screen_resolution']`)
