To Do:
[X]change axis so that plot is not cut off
[X]fix what happens when both supports are equal (becomes a cantilever on a wall)
	[X]add rectangle
	[X}add segments/rays
	[X]modify moment/shear
	[X]modify arrows
[X]turn axis off CHECK
[X]Fix the biegelinie-variation (bending shape)
[ ]add the schub effects (shear effects) with length-to-height ratio as interactive
[X]add length to height slider
[X]add the checkboxes
[X]add reset button
[X]add length-height interactive slider
[X]Columndatasource error
[ ]Add Multiple concentrated load capability
[X]LAST: change colors to TUM colors



Translations:
-Biegemoment: Bending Moment
-Querkraft: Lateral Force? Shear
-Doppeltgelagerter Balken und Einzellast: Double bearing beam and single cell
-Lagerposition: Position of b
-Laenge zu Hoehe: Length to Height ratio. This has been added. make a change

-Biegelinie: Buffer-line?
-Mit Schub: Shear effects

There is a beam: side A is fixed. Side B location can be changed by the slider. The animation takes the following inputs:
	-Location of side B
	-Magnitude of Force F
	-Location of Force F

The outputs of the animation:
	-Magnitude of Force at B
	-Magniture of Force at A
	-Bending moment
	-Lateral Force?	==> shear?

function for:
	-Magnitude of Force at B
	-Magnitude of Force at A
	-Shear
	-Moment
