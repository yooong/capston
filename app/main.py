from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from bokeh.models import ColumnDataSource
from bokeh.layouts import row, column, gridplot

df=pd.read_csv('C:/Users/yong/Desktop/kang.csv')
df=df.set_index('measure_date')
df.index=pd.to_datetime(df.index)
df.index.name='Datetime'
df.sort_index(inplace=True)

app=Flask(__name__)

@app.route('/') 
@app.route('/bokeh', methods=['post'])
def bokeh(condition=None, feature=None):
    if request.method=='post':
        condition=request.form['condition']
        feature=request.form['feature']
    source=ColumnDataSource(df)
    fig_lst=[]
    for i in ['temperature', 'humidity', 'lighting']:
        fig=figure(x_axis_type='datetime')
        fig.line('Datetime', i, source=source)
        fig.title.text='{}'.format(i.upper())
        fig.xaxis.axis_label='TimeStamp'
        fig.yaxis.axis_label='Values'
        fig_lst.append(fig)

    print(fig_lst)
    grid=gridplot(fig_lst, ncols=1, plot_width=1200, plot_height=250)
    fig=grid
    
    js_resources=INLINE.render_js()
    css_resources=INLINE.render_css()

    script, div=components(fig)
    html=render_template(
        'index.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return encode_utf8(html)
if __name__=='__main__':
    app.run()
