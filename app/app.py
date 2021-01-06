import requests
import pandas
import simplejson as json
from bokeh.plotting import figure
from bokeh.palettes import Spectral11
from bokeh.embed import components 
from flask import Flask,render_template,request,redirect,session

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

        app.vars['ticker'] = request.form['ticker']
	
        stock_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json?api_key=ues6Mm1_essC2iP-xMx6' % app.vars['ticker']
        session = requests.Session()
        session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
        stock_data = session.get(stock_url)

        data = stock_data.json()

        stock_df = pandas.DataFrame(data['data'], columns=data['column_names'])

        stock_df['Date'] = pandas.to_datetime(stock_df['Date'])

        plot = figure(title='Stock prices for %s' % app.vars['ticker'], x_axis_label='date', x_axis_type='datetime')
        
        if request.form.get('Close'):
            plot.line(x=stock_df['Date'].values, y=stock_df['Close'].values,line_width=2, legend='Close')
        if request.form.get('Adj. Close'):
            plot.line(x=stock_df['Date'].values, y=stock_df['Adj. Close'].values,line_width=2, line_color="green", legend='Adj. Close')
        if request.form.get('Open'):
            plot.line(x=stock_df['Date'].values, y=stock_df['Open'].values,line_width=2, line_color="red", legend='Open')
        if request.form.get('Adj. Open'):
            plot.line(x=stock_df['Date'].values, y=stock_df['Adj. Open'].values,line_width=2, line_color="purple", legend='Adj. Open')
        script, div = components(p)
        return render_template('plots.html', script=script, div=div)

if __name__ == '__main__':
    app.run(port=33507)
