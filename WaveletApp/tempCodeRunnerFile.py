Wavelet_Function_source = ColumnDataSource(data=dict(t=[],y=[]))
# plot_Wavelet_Function = Figure(x_range=(-10, 10), y_range=(-2, 2),
#                             x_axis_label='t', y_axis_label='psi(t)',
#                             tools ="wheel_zoom,box_zoom,save,reset,help",
#                             title="Wavelet function",  width=650, height=300)
# n=200
# t=np.linspace(-10,10,n)
# y= np.exp(-(t**2)/2) * np.cos(5*t)
# Wavelet_Function_source.data = dict(t=t, y=y)
# plot_Wavelet_Function.line('t', 'y', color='red', source=Wavelet_Function_source, line_width=2)