from motion import df
from bokeh.plotting import figure,show,output_file
from bokeh.models import HoverTool,ColumnDataSource

df["start_string"]=df["Start"].dt.strftime("%Y-%m-%d,%H:%M:%S")
df["end_string"]=df["End"].dt.strftime("%Y-%m-%d,%H:%M:%S")

cds=ColumnDataSource(df)

p=figure(x_axis_type="datetime",height=200,width=500,title="motion graph",sizing_mode="scale_width")
p.yaxis.minor_tick_line_color=None

hover=HoverTool(tooltips=[("Start","@start_string"),("End","@end_string")])
p.add_tools(hover)

q=p.quad(left="Start",right="End",bottom=0,top=1,color="blue",source=cds)

output_file("graph.html")

show(p)