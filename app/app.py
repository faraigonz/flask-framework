import requests
import pandas
import simplejson as json
import datetime
import dateutil
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
        #session = requests.Session()
        #session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
        
	r = requests.get(stock_url)
	data_df = pd.DataFrame(r.json())['dataset'].apply(pd.Series)
        data = dataset_df.ix['data',:].apply(pd.Series)
        data.columns = dataset_df.ix['column_names',0:12]
        data['Date'] = pd.to_datetime(data['Date'])

        #stock_df = pandas.DataFrame(data['data'], columns=data['column_names'])
	current_date = datetime.date.today()
	month = current_date - dateutil.relativedelta.relativedelta(months=1)
	#stock_df['Date'] = pandas.to_datetime(stock_df['Date'])
	month_data = stock_df[stock_df['Date']>month]

        p = figure(title='%s Stock Information' % app.vars['ticker'], x_axis_label='Date', x_axis_type='datetime',
	x_range = (month, current_date), y_axis_label = "USD")
        
        if request.form.get('Close'):
            p.line(x=month_data['Date'], y=month_data['Close'],line_width=2, legend='Close')
        if request.form.get('Adj. Close'):
            p.line(x=month_data['Date'], y=month_data['Adj. Close'].values,line_width=2, line_color="green", legend='Adj. Close')
        if request.form.get('Open'):
            p.line(x=month_data['Date'], y=month_data['Open'].values,line_width=2, line_color="red", legend='Open')
        if request.form.get('Adj. Open'):
            p.line(x=month_data['Date'], y=month_data['Adj. Open'].values,line_width=2, line_color="purple", legend='Adj. Open')
        script, div = components(p)
        return render_template('plots.html', script=script, div=div)

if __name__ == '__main__':
    app.run(port=33507)
