
# stuck => stuck to track
# if stuck=True then sum normal forces = 0
# if stuck=False then sum normal forces >= 0
def getNormalForce(normal,drag,grav,stuck):
    #normGrav=normal\cdot grav
    normGrav=normal[0]*grav[0]+normal[1]*grav[1]
    normDrag=normal[0]*drag[0]+normal[1]*drag[1]
    N=-normGrav-normDrag
    if (stuck or N<0):
        return [normal[0]*N, normal[1]*N]
    else:
        return [0, 0]
