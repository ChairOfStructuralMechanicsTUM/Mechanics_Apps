import matplotlib.pyplot as plt
from bokeh.models import ColumnDataSource

def get_contour_data(X, Y, Z):
    cs = plt.contour(X, Y, Z)
    xs = []
    ys = []
    xt = []
    yt = []
    col = []
    text = []
    isolevelid = 0
    for isolevel in cs.collections:
        isocol = isolevel.get_color()[0]
        thecol = 3 * [None]
        theiso = str(cs.get_array()[isolevelid])
        isolevelid += 1
        for i in range(3):
            thecol[i] = int(255 * isocol[i])
        thecol = '#%02x%02x%02x' % (thecol[0], thecol[1], thecol[2])

        for path in isolevel.get_paths():
            v = path.vertices
            x = v[:, 0]
            y = v[:, 1]
            xs.append(x.tolist())
            ys.append(y.tolist())
            xt.append(x[int( len(x) / 2 )])
            yt.append(y[int( len(y) / 2 )])
            text.append(theiso)
            col.append(thecol)

    source = ColumnDataSource(data={'xs': xs, 'ys': ys, 'line_color': col,'xt':xt,'yt':yt,'text':text})
    return source
    
def get_index( position, Xgrid, Ygrid ):
    # finding the x position index
    counter = 0
    for i in Xgrid[0,:]:
        if i == Xgrid[0,-1]:
            pass
        elif position[0] >= i and position[0] < (i+1):
            xPosIndex = counter
        else:
            pass
        counter += 1
        
    # finding the y position index
    counter = 0
    for i in Ygrid[:,0]:
        if i == Ygrid[-1,0]:
            pass
        elif position[1] >= i and position[1] < (i+1):
            yPosIndex = counter
        else:
            pass
        counter += 1
        
    return xPosIndex, yPosIndex
    
def get_pressure_grad( position, Xgrid, Ygrid, presGrad ):
    
    xPosIndex, yPosIndex = get_index( position, Xgrid, Ygrid )
    
    return presGrad[ xPosIndex, yPosIndex ]