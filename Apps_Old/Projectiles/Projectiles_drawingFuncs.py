from Projectiles_drawable import Projectiles_Drawable


def monkeyLetGo(monkey, space=False):
    print("monkeyLetGo")
    assert isinstance(monkey, Projectiles_Drawable)
    if space:
        filename = "static/images/spaceMonkeyLetGo.png"
    else:
        filename = "static/images/monkeyLetGo.png"
    print("calling monkey.replace_image")
    monkey.replace_image(filename)


def monkeyGrab(monkey, space = False):
    print("monkeyGrab")
    assert isinstance(monkey, Projectiles_Drawable)
    if (space):
        filename = "static/images/spaceMonkey.png"
    else:
        filename = "static/images/monkey.png"
    print("calling monkey.replace_image")
    monkey.replace_image(filename)