#!/usr/bin/env python

import sys
import re
import datetime
from contextlib import closing
import cStringIO
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, make_response


sys.path.append('/global/homes/a/apratap/dev/eclipse_workspace/python_scripts/lib')
import jgi_qaqc_plots
from db_access import plot_sequencing_summary, get_lib_query_results



SECRET_KEY = 'ACAH6737AGHAC'

app = Flask(__name__)
app.config.from_object(__name__)



@app.before_request
def before_request():
    pass

@app.teardown_request
def teardown_request(exception):
    pass


@app.route('/')
def index():
    return render_template('index.html')


def plot():
    pass


@app.route('/seq_summary_plot',methods=['GET','POST'])
def plot_seq_summary():
    #print ('you entered &s \t %s ' % request.form['startDate'], request.form['endDate'])
    
    user_entered_startDate = request.form['startDate']
    user_entered_endDate = request.form['endDate']
    
    output_plot = plot_sequencing_summary(user_entered_startDate,user_entered_endDate)
    response = make_response(output_plot.getvalue())
    response.mimetype = 'image/png'
    return response

    #return render_template('plot.html',dates=dates)



@app.route('/check_plot')
def check_plot():
    
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(range(100))
    
    canvas = FigureCanvas(fig)
    output = cStringIO.StringIO()
    canvas.print_png(output)
    
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response
    



@app.route('/libs_summary_plots',methods=['GET','POST'])
def get_libs_summary_plots():
    user_entered_libs = request.form['lib_names']
    
    libs = re.sub(r'(\s+)|(\r+)',',',user_entered_libs)
    libs = [ str(lib) for lib in libs.split(',') if lib != '' ]
    
    #get the lib dbquery results
    plot_buffer=jgi_qaqc_plots.get_libs_qaqc_plots(library_names=tuple(libs))
    
    response = make_response(plot_buffer.getvalue())
    response.mimetype = 'image/png'
    
    return response
    #return response
    #return redirect(url_for('check_plot'))
    #return render_template('libs_report.html')
    

@app.route('/plot')
def plot1():
  
    fig = plt.figure()
    plt.plot(range(100))
    
    canvas = FigureCanvas(fig)
    output = cStringIO.StringIO()
    canvas.print_png(output)
    
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    
    return response







#@app.route('/login', methods=['GET', 'POST'])
#def login():
#    error = None
#    if request.method == 'POST':
#        if request.form['username'] != app.config['USERNAME']:
#            error = 'Invalid username'
#        elif request.form['password'] != app.config['PASSWORD']:
#            error = 'Invalid password'
#        else:
#            session['logged_in'] = True
#            flash('You were logged in')
#            return redirect(url_for('show_entries'))
#    return render_template('login.html', error=error)
#
#
#@app.route('/logout')
#def logout():
#    session.pop('logged_in', None)
#    flash('You were logged out')
#    return redirect(url_for('show_entries'))



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
