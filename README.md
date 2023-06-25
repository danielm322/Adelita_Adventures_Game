# Adelita Adventures Game
This repository contains source code to the Adelita Adventures game, developed in Python using Kivy.
The game is intended to be played on the phone, using both thumbs to control the buttons and the characters easily, so playing on the PC still needs some adaptation to use the keyboard (contributions are welcome!).

This is an amateur's work so there are plenty of possible improvements, please write on the issues section, or create your own pull requests!

![Gif](https://github.com/danielm322/Baby_Adventures_Game/tree/main/graphics/plpaygame.gif)


## Developing or running in your computer
Create your environment with python 3.8 and install the `requirements.txt`. 

Then simply run 
```python
python main.py
```

To build the app for your phone (most easily for android) you need the buildozer package. Follow instructions [here](https://buildozer.readthedocs.io/en/latest/installation.html).

After you have installed buildozer in your environment, you can build an android installable apk by running:
```commandline
buildozer -v android debug deploy run
```

## Contributions
Feel free to contribute to this game. To do so, fork the repo, and open pull requests when you think they're ready to be merged.

## Credits
All assets, including sprites, backgrounds, fonts, and music, are freely and openly available. 
See the credits section in the game for details.