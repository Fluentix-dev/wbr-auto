# wbr-auto v0.1

Auto-plays the game [WhatBeatsRock](https://whatbeatsrock.com) with image-detection via of [OpenCV](https://pypi.org/project/opencv-python/) with [word list](https://nglam.dev/resources/wbr/).

## Video Demo

Here is the program in action that filled out 150+ words in 20 minutes:

[![YouTube Video](https://img.youtube.com/vi/b51I9jCYjKU/0.jpg)](https://www.youtube.com/watch?v=b51I9jCYjKU)

## Installation & Usage

Ensure you have those components installed correctly on your system before proceeding:

- [Python](https://www.python.org/)
- `pip` (click [here](https://pip.pypa.io/en/stable/installation/))

Download the source file then unzip it, inside the unzipped directory, launch a terminal/cmd there in the same directory and type the following command:

```
pip install -r requirements.txt
```

This will install all of the needed components so that `wbr-auto` can run correctly, or you can manually install those components yourself:

```
pyautogui
opencv-python
BeautifulSoup4
requests
pillow
```

After this, run the file `main.py` (by typing `python3 main.py` in your terminal/cmd, the term `python3` may differs depending on your Python version) and you will be greeted with this text if you do it correctly:


```
> python3 main.py
------------------------------

WBR-auto v1: automatically plays What Beats Rock for you.
--Made by Fluentix (https://fluentix.dev)--

Get involved: https://contribute.fluentix.dev
Contribute to this project here: https://wbr.fluentix.dev/contribute


Options:
[1] : Start WBR-auto
[2] : Update word list (recommended)
Enter a valid option: 
```

Now it is asking for your input, here is what it will do:

- `1` : start `wbr-auto`, which will start the auto-play using the prepacked 150+ words list inside `wbr/data.txt`,
- `2` : update word list that `wbr-auto` uses to fill, words are updated monthly. ([word bank](https://nglam.dev/resources/wbr/))

## Side notes

When using, please make sure that your browser is clear and visible with **default zoom size** (which is 100% as default). If you tweak those settings it **might not work**.

## Last words

**THIS PROJECT IS MADE FOR EDUCATIONAL PURPOSES ONLY**

And, have fun, we suppose.

Also join our [discord](https://fluentix.dev/discord).





