from flask import Flask, request, render_template, redirect, url_for, make_response
import matplotlib.pyplot as plt 
import time,os
import datetime as dt
import numpy as np
import pandas as pd

app = Flask(__name__)

def plotgraph(filepath,imagefolder):
	p1=filepath.split('/')
	p2=p1[-1]
	iname= p2.strip('.txt')
	plt.plotfile(filepath, delimiter=',', cols=(0, 1), names=('YYYY-MM', 'Total Hits'), marker='o')
	new_graph_name = iname + str(time.time()) + ".png"
	for filename in os.listdir(imagefolder):
		if filename.startswith(iname):  # not to remove other images
			os.remove(imagefolder+filename)
	plt.savefig(imagefolder + new_graph_name)
	imagename = imagefolder + new_graph_name
	return imagename
	
def monthlyhits(filepath):
	hits = [line.rstrip('\n') for line in open(filepath)]
	a = hits[1].split(',')
	total_hits=a[-1]
	a = hits[2].split(',')
	avg_hits=a[-1]
	a = hits[3].split(',')
	peak_hits=a[-1]
	return total_hits,avg_hits,peak_hits
		
@app.route('/',methods = ['POST','GET'])
def index():
	m1=(pd.Period(dt.datetime.now(), 'M') - 1).strftime('%B %Y')
	m2=(pd.Period(dt.datetime.now(), 'M') - 2).strftime('%B %Y')
	m3=(pd.Period(dt.datetime.now(), 'M') - 3).strftime('%B %Y')
	return render_template('index.html',m1=m1,m2=m2,m3=m3)
	
@app.route('/home',methods = ['POST','GET'])
def home():
	mstring=request.form['mstring']
	arr=mstring.split(' ')
	month=arr[0]
	year=arr[1]
	resp = make_response(render_template('home.html',mstring=mstring,month=month,year=year))
	resp.set_cookie('month',month)
	resp.set_cookie('year',year)
	resp.set_cookie('mstring',mstring)
	return resp
	
@app.route('/ssointernet',methods = ['POST','GET'])
def ssointernet():
	mstring = request.cookies.get('mstring')
	month = request.cookies.get('month')
	year = request.cookies.get('year')
	#Monthly hits Web
	filename='static/files/'+month+'-'+year+'/sso_internet/internet_monthly_web_hits.txt'
	web_total_hits,web_avg_hits,web_peak_hits = monthlyhits(filename)
	#Monthly hits App
	filename='static/files/'+month+'-'+year+'/sso_internet/internet_monthly_app_hits.txt'
	app_total_hits,app_avg_hits,app_peak_hits = monthlyhits(filename)
	#Monthly hits Policy
	filename='static/files/'+month+'-'+year+'/sso_internet/internet_monthly_policy_hits.txt'
	policy_total_hits,policy_avg_hits,policy_peak_hits = monthlyhits(filename)
	#Monthly hits DSS
	filename='static/files/'+month+'-'+year+'/sso_internet/internet_monthly_dss_hits.txt'
	dss_total_hits,dss_avg_hits,dss_peak_hits = monthlyhits(filename)
	
	

	#For SSO Internet Top Hitting Apps
	top_apps = [line.rstrip('\n') for line in open('static/files/'+month+'-'+year+'/sso_internet/internet_top_hitting_apps.txt')]
	#For Internet Web Hit Trend
	filepath = 'static/files/'+month+'-'+year+'/sso_internet/internet_web_hit_trend.txt'
	imagefolder = 'static/images/'
	internet_web_hit_trend = plotgraph(filepath,imagefolder)
	#For Internet App Hit Trend
	filepath = 'static/files/'+month+'-'+year+'/sso_internet/internet_app_hit_trend.txt'
	imagefolder = 'static/images/'
	internet_app_hit_trend = plotgraph(filepath,imagefolder)
	#For Internet Policy Hit Trend
	filepath = 'static/files/'+month+'-'+year+'/sso_internet/internet_policy_hit_trend.txt'
	imagefolder = 'static/images/'
	internet_policy_hit_trend = plotgraph(filepath,imagefolder)
	#For Internet DSS Hit Trend
	filepath = 'static/files/'+month+'-'+year+'/sso_internet/internet_dss_hit_trend.txt'
	imagefolder = 'static/images/'
	internet_dss_hit_trend = plotgraph(filepath,imagefolder)	
	return render_template('ssointernet.html',web_total_hits=web_total_hits,web_avg_hits=web_avg_hits,web_peak_hits=web_peak_hits,app_total_hits=app_total_hits,app_avg_hits=app_avg_hits,app_peak_hits=app_peak_hits,policy_total_hits=policy_total_hits,policy_avg_hits=policy_avg_hits,policy_peak_hits=policy_peak_hits,dss_total_hits=dss_total_hits,dss_avg_hits=dss_avg_hits,dss_peak_hits=dss_peak_hits,lines=top_apps,internet_web_hit_trend =internet_web_hit_trend,internet_app_hit_trend =internet_app_hit_trend,internet_policy_hit_trend =internet_policy_hit_trend,internet_dss_hit_trend =internet_dss_hit_trend,mstring=mstring,month=month,year=year)
	
@app.route('/ssointranet',methods = ['POST','GET'])
def ssointranet():
	mstring = request.cookies.get('mstring')
	month = request.cookies.get('month')
	year = request.cookies.get('year')
	#Monthly hits Web
	filename='static/files/'+month+'-'+year+'/sso_intranet/intranet_monthly_web_hits.txt'
	web_total_hits,web_avg_hits,web_peak_hits = monthlyhits(filename)
	#Monthly hits App
	filename='static/files/'+month+'-'+year+'/sso_intranet/intranet_monthly_app_hits.txt'
	app_total_hits,app_avg_hits,app_peak_hits = monthlyhits(filename)
	#Monthly hits Policy
	filename='static/files/'+month+'-'+year+'/sso_intranet/intranet_monthly_policy_hits.txt'
	policy_total_hits,policy_avg_hits,policy_peak_hits = monthlyhits(filename)

	#For SSO Intranet Top Hitting Apps
	top_apps = [line.rstrip('\n') for line in open('static/files/'+month+'-'+year+'/sso_intranet/intranet_top_hitting_apps.txt')]
	#For Intranet Web Hit Trend
	filepath = 'static/files/'+month+'-'+year+'/sso_intranet/intranet_web_hit_trend.txt'
	imagefolder = 'static/images/'
	intranet_web_hit_trend = plotgraph(filepath,imagefolder)
	#For Intranet App Hit Trend
	filepath = 'static/files/'+month+'-'+year+'/sso_intranet/intranet_app_hit_trend.txt'
	imagefolder = 'static/images/'
	intranet_app_hit_trend = plotgraph(filepath,imagefolder)
	#For Intranet Policy Hit Trend
	filepath = 'static/files/'+month+'-'+year+'/sso_intranet/intranet_policy_hit_trend.txt'
	imagefolder = 'static/images/'
	intranet_policy_hit_trend = plotgraph(filepath,imagefolder)

	return render_template('ssointranet.html',web_total_hits=web_total_hits,web_avg_hits=web_avg_hits,web_peak_hits=web_peak_hits,app_total_hits=app_total_hits,app_avg_hits=app_avg_hits,app_peak_hits=app_peak_hits,policy_total_hits=policy_total_hits,policy_avg_hits=policy_avg_hits,policy_peak_hits=policy_peak_hits,lines=top_apps,intranet_web_hit_trend =intranet_web_hit_trend,intranet_app_hit_trend =intranet_app_hit_trend,intranet_policy_hit_trend =intranet_policy_hit_trend,mstring=mstring,month=month,year=year)	
	
@app.route('/inauthinternet',methods = ['POST','GET'])
def inauthinternet():
	mstring = request.cookies.get('mstring')
	month = request.cookies.get('month')
	year = request.cookies.get('year')
	#Monthly hits Web
	filename='static/files/'+month+'-'+year+'/inauth_internet/inauth_internet_monthly_hits.txt'
	inauth_internet_total_hits,inauth_internet_avg_hits,inauth_internet_peak_hits = monthlyhits(filename)


	#For Internet Web Hit Trend
	filepath = 'static/files/'+month+'-'+year+'/inauth_internet/inauth_internet_hit_trend.txt'
	imagefolder = 'static/images/'
	inauth_internet_hit_trend = plotgraph(filepath,imagefolder)

	return render_template('inauthinternet.html',inauth_internet_total_hits=inauth_internet_total_hits,inauth_internet_avg_hits=inauth_internet_avg_hits,inauth_internet_peak_hits=inauth_internet_peak_hits,inauth_internet_hit_trend =inauth_internet_hit_trend,mstring=mstring,month=month,year=year)

@app.route('/inauthintranet',methods = ['POST','GET'])
def inauthintranet():
	mstring = request.cookies.get('mstring')
	month = request.cookies.get('month')
	year = request.cookies.get('year')
	#Monthly hits Web
	filename='static/files/'+month+'-'+year+'/inauth_intranet/inauth_intranet_monthly_hits.txt'
	inauth_intranet_total_hits,inauth_intranet_avg_hits,inauth_intranet_peak_hits = monthlyhits(filename)


	#For Intranet Web Hit Trend
	filepath = 'static/files/'+month+'-'+year+'/inauth_intranet/inauth_intranet_hit_trend.txt'
	imagefolder = 'static/images/'
	inauth_intranet_hit_trend = plotgraph(filepath,imagefolder)

	return render_template('inauthintranet.html',inauth_intranet_total_hits=inauth_intranet_total_hits,inauth_intranet_avg_hits=inauth_intranet_avg_hits,inauth_intranet_peak_hits=inauth_intranet_peak_hits,inauth_intranet_hit_trend =inauth_intranet_hit_trend,mstring=mstring,month=month,year=year)	
	
@app.route('/epassinternet',methods = ['POST','GET'])
def epassinternet():
	mstring = request.cookies.get('mstring')
	month = request.cookies.get('month')
	year = request.cookies.get('year')
	#Monthly hits 
	filename='static/files/'+month+'-'+year+'/epass_internet/epass_internet_monthly_hits.txt'
	epass_internet_total_hits,epass_internet_avg_hits,epass_internet_peak_hits = monthlyhits(filename)


	#For Epass Internet Web Hit Trend
	filepath = 'static/files/'+month+'-'+year+'/epass_internet/epass_internet_hit_trend.txt'
	imagefolder = 'static/images/'
	epass_internet_hit_trend = plotgraph(filepath,imagefolder)
	
	#For Epass Internet Top Hitting Apps
	top_apps = [line.rstrip('\n') for line in open('static/files/'+month+'-'+year+'/epass_internet/epass_internet_top_hitting_apps.txt')]

	return render_template('epassinternet.html',epass_internet_total_hits=epass_internet_total_hits,epass_internet_avg_hits=epass_internet_avg_hits,epass_internet_peak_hits=epass_internet_peak_hits,epass_internet_hit_trend =epass_internet_hit_trend,lines=top_apps,mstring=mstring,month=month,year=year)
	
@app.route('/epassintranet',methods = ['POST','GET'])
def epassintranet():
	mstring = request.cookies.get('mstring')
	month = request.cookies.get('month')
	year = request.cookies.get('year')
	#Monthly hits 
	filename='static/files/'+month+'-'+year+'/epass_intranet/epass_intranet_monthly_hits.txt'
	epass_intranet_total_hits,epass_intranet_avg_hits,epass_intranet_peak_hits = monthlyhits(filename)

	#For Epass Intranet Web Hit Trend
	filepath = 'static/files/'+month+'-'+year+'/epass_intranet/epass_intranet_hit_trend.txt'
	imagefolder = 'static/images/'
	epass_intranet_hit_trend = plotgraph(filepath,imagefolder)
	
	#For Epass Intranet Top Hitting Apps
	top_apps = [line.rstrip('\n') for line in open('static/files/'+month+'-'+year+'/epass_intranet/epass_intranet_top_hitting_apps.txt')]

	return render_template('epassintranet.html',epass_intranet_total_hits=epass_intranet_total_hits,epass_intranet_avg_hits=epass_intranet_avg_hits,epass_intranet_peak_hits=epass_intranet_peak_hits,epass_intranet_hit_trend =epass_intranet_hit_trend,lines=top_apps,mstring=mstring,month=month,year=year)	
	
@app.route('/oauth',methods = ['POST','GET'])
def oauth():
	mstring = request.cookies.get('mstring')
	month = request.cookies.get('month')
	year = request.cookies.get('year')
	#Monthly hits 
	filename='static/files/'+month+'-'+year+'/oauth/oauth_monthly_hits.txt'
	oauth_total_hits,oauth_avg_hits,oauth_peak_hits = monthlyhits(filename)

	#For oauth Hit Trend
	filepath = 'static/files/'+month+'-'+year+'/oauth/oauth_hit_trend.txt'
	imagefolder = 'static/images/'
	oauth_hit_trend = plotgraph(filepath,imagefolder)

	return render_template('oauth.html',oauth_total_hits=oauth_total_hits,oauth_avg_hits=oauth_avg_hits,oauth_peak_hits=oauth_peak_hits,oauth_hit_trend =oauth_hit_trend,mstring=mstring,month=month,year=year)
	
'''For Heroku'''

if __name__ == "__main__":
	app.run(debug=True)


'''For Localhost'''
'''
if __name__ == '__main__':
	app.run(port=5000, host='localhost', debug=True)
'''	

