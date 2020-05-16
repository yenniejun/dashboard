import io
import plotly.express as px
from requests import get
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go

date_today = datetime.today().strftime("%Y-%m-%d")
noise_req = get(url=f"https://data.cityofnewyork.us/resource/erm2-nwe9.csv?$query=\
    SELECT *,date_trunc_ymd(created_date) AS DAY\
    WHERE (created_date between '2020-01-01' and '{date_today}' AND complaint_type like '%Noise')\
    LIMIT 18000\
	")
noise_df = pd.read_csv(io.StringIO(noise_req.content.decode('utf-8')), dtype={'incident_zip': object})
noise_df.set_index(pd.DatetimeIndex(noise_df['created_date']), inplace=True);
# grouper_zip = noise_df.groupby([pd.Grouper(freq='1D'), 'incident_zip']).count()
# grouper_bor = noise_df.groupby([pd.Grouper(freq='1D'), 'borough']).count()
# grouper_bor_h = noise_df.groupby([pd.Grouper(freq='1H'), 'borough']).count()
grouper_overall = noise_df.groupby([pd.Grouper(freq='1D')]).count()

limit=3000
req_borough_w = get(f"https://data.cityofnewyork.us/api/id/erm2-nwe9.csv?$query=select%20date_trunc_ymd(%60created_date%60)%20as%20%60created_date%60%2C%20%60complaint_type%60%2C%20%60borough%60%2C%20count(%60unique_key%60)%20as%20%60unique_key%60%20where%20(contains(upper(%60complaint_type%60)%2C%20upper(%27Noise%27)))%20group%20by%20%60created_date%60%2C%20%60complaint_type%60%2C%20%60borough%60%20order%20by%20%60created_date%60%20desc%20limit%20{limit}")
df_borough_w= pd.read_csv(io.StringIO(req_borough_w.content.decode('utf-8')))
boroughs = df_borough_w[df_borough_w.complaint_type.str.contains("Noise")].groupby(['created_date', 'borough']).sum()

limit=3000
req_zip_w = get(f"https://data.cityofnewyork.us/api/id/erm2-nwe9.csv?$query=select%20date_trunc_ymd(%60created_date%60)%20as%20%60created_date%60%2C%20%60complaint_type%60%2C%20%60incident_zip%60%2C%20count(%60unique_key%60)%20as%20%60unique_key%60%20where%20(contains(upper(%60complaint_type%60)%2C%20upper(%27Noise%27)))%20group%20by%20%60created_date%60%2C%20%60complaint_type%60%2C%20%60incident_zip%60%20order%20by%20%60created_date%60%20desc%20limit%20{limit}")
df_zip_w= pd.read_csv(io.StringIO(req_zip_w.content.decode('utf-8')))
zips = df_zip_w[df_zip_w.complaint_type.str.contains("Noise")].groupby(['created_date', 'incident_zip']).sum()


def noise_graph(graph_type):
	
	fig = px.line(grouper_overall, 
                 x=grouper_overall.index, 
                 y=grouper_overall.unique_key, 
                 title='Overall NYC Noise Complaints',
                 labels = {'x':'Date', 'unique_key':'Number of Noise Complaints'})
	
	fig.update_xaxes(
	    rangeslider_visible=True,
	    rangeselector=dict(
	        buttons=list([
	        	dict(count=7, label="1w", step="day", stepmode="backward"),
	            dict(count=1, label="1m", step="month", stepmode="backward"),
	            dict(count=3, label="3m", step="month", stepmode="backward"),
	            dict(count=1, label="YTD", step="year", stepmode="todate"),
	#             dict(count=1, label="1y", step="year", stepmode="backward"),
	            dict(step="all")
	        ])
	    )
    )

	return fig

def noise_graph_borough():
	fig = px.line(boroughs, 
                 x=[a[0] for a in boroughs.index], 
                 y=boroughs.unique_key, 
                 color=[a[1] for a in boroughs.index],
                 title='DAILY NYC Noise Complaints (By Borough)',
                 labels = {'x':'Date', 'y':'Number of Noise Complaints'})

	fig.update_xaxes(
	    rangeslider_visible=True,
	    rangeselector=dict(
	        buttons=list([
	        	dict(count=7, label="1w", step="day", stepmode="backward"),
	            dict(count=1, label="1m", step="month", stepmode="backward"),
	            dict(count=2, label="2m", step="month", stepmode="backward"),
	            # dict(count=1, label="YTD", step="year", stepmode="todate"),
	#             dict(count=1, label="1y", step="year", stepmode="backward"),
	            dict(step="all")
	        ])
	    )
    )

	return fig


def noise_graph_zip():
	
	fig = px.line(zips, 
                 x=[a[0] for a in zips.index], 
                 y=zips.unique_key, 
                 color=[a[1] for a in zips.index],
                 title='DAILY NYC Noise Complaints (By Zip Code)',
                 labels = {'x':'Date', 'y':'Number of Noise Complaints'})

	fig.update_xaxes(
	    rangeslider_visible=True,
	    rangeselector=dict(
	        buttons=list([
	            dict(count=5, label="5d", step="day", stepmode="backward"),
	            dict(count=10, label="10d", step="day", stepmode="backward"),
	            # dict(count=1, label="1m", step="month", stepmode="backward"),
	            dict(step="all")
	        ])
	    )
	)

	return fig


