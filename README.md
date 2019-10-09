# Automatic locking in i3

This is an alternative script to [blurlock](https://github.com/manjaro/packages-community/blob/master/i3/i3exit/blurlock) (default in manjaro with i3), written in python, that randomly chooses an image file from folder './backgrounds/' and displays it as the background of i3lock.
The [suspendlock.service](./suspendlock.service) file can be used as an example to be executed automatically at suspend.

Source of the [example image](./backgrounds/example.png): Jan Zerfowski, Bolivia, Madidi National Park

## What it can do
- Display random image from folder
- Check file endings and only display settings['filetypes']
- Do all filetypes that [convert](https://imagemagick.org/script/convert.php) can process
- Define fallback locker when file conversion fails

## Installation
- Copy image files in a compatible format to [./backgrounds/](./backgrounds)
- Make suspendlock.py executable
    - `chmod u+x suspendlock.py`
- Create a symbolic link in your $PATH
    - `ln -s <directory of suspendlock.py> /usr/local/bin/suspendlock`
- Copy the [suspendlock.service](./suspendlock.service) file to a folder which systemd cares about
    - `cp suspendlock.service /etc/systemd/system/suspendlock.service`
- To execute the script manually, edit all necessary references in the i3 config files

## Issues
- Needs images in exactly 16:9 ratio (or whatever implicit ratio is given by settings['screen_resolution'])
