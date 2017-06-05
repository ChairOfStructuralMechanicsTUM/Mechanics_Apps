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


def modifyHeight(h, cannon, base, banana):
    assert isinstance(cannon, Drawable) and isinstance(base, Drawable) and isinstance(banana, Drawable)

    base.move_to((None, h))
    cannon.move_to((None, h+0.5))
    banana.move_to((None, 10+h))