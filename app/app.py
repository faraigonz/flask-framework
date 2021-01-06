import requests
import pandas as pd
from datetime import datetime, date
import dateutil
import simplejson as json
from bokeh.plotting import figure
from bokeh.embed import components 
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

app.vars={}


@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')
    
@app.route('/plots', methods=['POST'])
def plots():
#   
        app.vars['ticker'] = request.form['ticker']
        
        stock_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json?api_key=ues6Mm1_essC2iP-xMx6' % app.vars['ticker']
    
        stock_data = requests.get(stock_url)
	
        stock_df = pd.DataFrame(stock_data.json()['data'], columns=stock_data.json()['column_names'])

        stock_df['Date'] = pd.to_datetime(stock_df['Date'])

        p = figure(title='Stock prices for %s' % app.vars['ticker'], x_axis_label='Date', y_axis_label='USD', x_axis_type='datetime')
        
        if request.form.get('Close'):
            p.line(x=stock_df['Date'].values, y=stock_df['Close'].values,line_width=2, legend='Close')
        
	if request.form.get('Adj. Close'):
            p.line(x=stock_df['Date'].values, y=stock_df['Adj. Close'].values,line_width=2, line_color="green", legend='Adj. Close')
        
	if request.form.get('Open'):
            p.line(x=stock_df['Date'].values, y=stock_df['Open'].values,line_width=2, line_color="red", legend='Open')
        
	if request.form.get('Adj. Open'):
            p.line(x=stock_df['Date'].values, y=stock_df['Adj. Open'].values,line_width=2, line_color="purple", legend='Adj. Open')
        
	script, div = components(p)
        
	return render_template('plots.html', script=script, div=div)

if __name__ == '__main__':
    app.run(port=33507)
