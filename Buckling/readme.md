# Buckling Application
https://en.wikipedia.org/wiki/Buckling
http://www.bu.edu/moss/mechanics-of-materials-beam-buckling/
http://www.continuummechanics.org/columnbuckling.html

## Possible enhancement:
All values can be precomputed and read into the CDS at startup. This would increase performance.

## Animation Description:

There are 4 beams. Each beam has different boundary conditions:
	1. Beam is free at top end, fixed at bottom end.
	2. Beam is pinned at both ends. One pin is free to move vertically as force is applied.
	3. Beam is pinned at top end, fixed at bottom end. Pinned end moves with increase in force.
	4. Beam is fixed at both ends.

Force reaches critica
F = pi^{2}*(E*I) / (K*L)^{2})
