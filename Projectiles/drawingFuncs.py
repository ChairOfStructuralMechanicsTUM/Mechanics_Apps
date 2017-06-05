import os.path
from drawable import Drawable


def monkeyLetGo(monkey, space=False):
    print "monkeyLetGo"
    assert isinstance(monkey, Drawable)
    if space:
        filename = "Images/spaceMonkeyLetGo.png"
    else:
        filename = "Images/monkeyLetGo.png"
    print "calling monkey.replace_image"
    monkey.replace_image(filename)


def monkeyGrab(monkey, space = False):
    print "monkeyGrab"
    assert isinstance(monkey, Drawable)
    if (space):
        filename = "Images/spaceMonkey.png"
    else:
        filename = "Images/monkey.png"
    print "calling monkey.replace_image"
    monkey.replace_image(filename)