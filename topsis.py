from flask import Flask, request, jsonify, flash, redirect, url_for
from flask import render_template
import numpy as np
import requests
import os
from werkzeug.utils import secure_filename
import csv
from asynchat import simple_producer
from numpy import *
import matplotlib.pyplot as plt


UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = {'csv'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route("/")
@app.route("/index")
def index():
	return render_template('dashboard.html',landing=1,title='Topsis')
@app.route("/topsis",methods=['GET','POST'])

def topsis():    


    if request.method == 'GET':
        return render_template('dashboard.html',form=1,title='HitungTopsis')
    elif request.method == 'POST':
        
        if 'matrix' not in request.files:
            flash('No file part')
            return redirect(request.url)
        csvmatrix = request.files['matrix']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if csvmatrix.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if csvmatrix and allowed_file(csvmatrix.filename):
            mfilename = secure_filename(csvmatrix.filename)
            csvmatrix.save(os.path.join(app.config['UPLOAD_FOLDER'], mfilename))
            
        if 'bobot' not in request.files:
            flash('No file part')
            return redirect(request.url)
        csvbobot = request.files['bobot']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if csvbobot.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if csvbobot and allowed_file(csvbobot.filename):
            bfilename = secure_filename(csvbobot.filename)
            csvbobot.save(os.path.join(app.config['UPLOAD_FOLDER'], bfilename))
        

        
        x = np.loadtxt(os.path.join(app.config['UPLOAD_FOLDER'], mfilename), delimiter=',')
        weights = np.loadtxt(os.path.join(app.config['UPLOAD_FOLDER'], bfilename), delimiter=',')



        
        
        # csvmatrix = request.files['matrix']
        # csvbobot = request.files['bobot']
        

        
        n1 = int(request.form['benefit'])
        n2 = int(request.form['cost'])
        
        
        
        def cumsqrt(bobot):
            k = np.array(cumsum(pow(bobot,2), 0))
            z = np.array([[bobot[i, j] / sqrt(k[bobot.shape[0] - 1,j]) for j in range(bobot.shape[1])] for i in range(bobot.shape[0])])
           # print(f"z adalah {z}")
            return z

        def kalibobot(y):
            y = (y*weights)
           # print(f"\n\n\n\n\n bobot kali pembagi{y}")
            return y

        cum = cumsqrt(x)

        kb = kalibobot(cum)

        #shape 0 row baris 4
        #shape 1 col kolom 10
      #  for index in range(kb.shape[1]):
       #     print(f"\n\n\n{np.array([kb[i,j+index] for j in range(kb.shape[1]-(kb.shape[1]-1)) for i in range(kb.shape[0])])}")
        #for sign in range(tanda.shape[0]):
            #for index in range(kb.shape[1]):
            
        #       print(f"\n\n\n{amax(np.array([kb[i,j] for j in range(kb.shape[1]-(kb.shape[1]-1)) for i in range(kb.shape[0])]))}")

        #       print(tanda[sign])

        siplistp = []
        siplistn = []
        #n1 = int(input(f"Silakan masukan jarak benefit, contoh jika benefit sampai index 4, maka ketik 4:"))
        #n2 = int(input(f"Silakan masukan jarak cost, contoh jika cost sampai index 10, maka ketik 10:"))

        def fsip(benefit,cost):
            
            for index in range(0,benefit):
                #print(f"benefit{amax(np.array([kb[i,j+index] for j in range(kb.shape[1]-(kb.shape[1]-1)) for i in range(kb.shape[0])]))}")

                siplistp.append(amax(np.array([kb[i,j+index] for j in range(kb.shape[1]-(kb.shape[1]-1)) for i in range(kb.shape[0])])))
                index = index+1
            for index in range(benefit,cost):

                #print(f"cost{amin(np.array([kb[i,j+index] for j in range(kb.shape[1]-(kb.shape[1]-1)) for i in range(kb.shape[0])]))}")
                siplistp.append(amin(np.array([kb[i,j+index] for j in range(kb.shape[1]-(kb.shape[1]-1)) for i in range(kb.shape[0])])))
                index = index+1

            for index in range(0,benefit):
                    
                #print(f"benefit{amax(np.array([kb[i,j+index] for j in range(kb.shape[1]-(kb.shape[1]-1)) for i in range(kb.shape[0])]))}")

                siplistn.append(amin(np.array([kb[i,j+index] for j in range(kb.shape[1]-(kb.shape[1]-1)) for i in range(kb.shape[0])])))
                index = index+1
            for index in range(benefit,cost):
           #     print(index)
                #print(f"cost{amin(np.array([kb[i,j+index] for j in range(kb.shape[1]-(kb.shape[1]-1)) for i in range(kb.shape[0])]))}")
                siplistn.append(amax(np.array([kb[i,j+index] for j in range(kb.shape[1]-(kb.shape[1]-1)) for i in range(kb.shape[0])])))
                index = index+1
            #print(siplistn)



        fsip(n1,n2)
        #fsip(benefit,cost)

        #print(f"d+{np.array([siplistp[n]-kb[i,j] for j in range(kb.shape[1]) for i in range(kb.shape[0]-(kb.shape[0]-1)) for n in range(len(siplistp))])}")
        sip = np.array([siplistp[n] for n in range(len(siplistp))])
        kalib = np.array([kb[i,j] for j in range(kb.shape[1]) for i in range(kb.shape[0]-(kb.shape[0]-1))])
   #     print(f"kb+{kalib}")
  #      print(f"sip+{sip}")
        dplus=[]
        for index in range(0,4):
            hitung = np.array(np.sqrt([sum(np.subtract(np.array([siplistp[n] for n in range(len(siplistp))]),np.array([kb[i+index,j] for j in range(kb.shape[1]) for i in range(kb.shape[0]-(kb.shape[0]-1))]))**2)]))
            dplus.append(hitung)
            
     #       print(f"hasil distance+ ke-{index} adalah {hitung}")

            
  #      print(dplus)
        dmin=[]
        for index in range(0,4):
            hitung = np.array(np.sqrt([sum(np.subtract(np.array([kb[i+index,j] for j in range(kb.shape[1]) for i in range(kb.shape[0]-(kb.shape[0]-1))]),np.array([siplistn[n] for n in range(len(siplistn))]))**2)]))
        # hitung2 = np.array([np.sqrt(sum(np.subtract(np.array(kb),np.array(siplistn)))**2)])
            dmin.append(hitung)
            #print(f"hasil distance -ke-{index} adalah {hitung}")

            #print(hitung2)

        #cj = np.array([np.array([dmin[n] for n in range(len(dmin))])/(np.array([dplus[j] for j in range(len(dplus))])+np.array(dmin[n] for n in range(len(dmin))))])
        cj = np.array(np.array(dmin)/(np.array(dplus)+np.array(dmin)))
        
        #df = pd.DataFrame(cj, "CJ", "CJ")
        #dft = df.to_html()
        q = [i + 1 for i in range(x.shape[0])]
        dispp = render_template('dashboard.html',submit=1,form=1,title='Hitung Topsis Hermano Diazo',fq=q,fn1=n1, fn2=n2, fweight=weights, fx=x, fdplus=dplus, fdmin=dmin, fcj=cj)
        return dispp

                
if __name__ == '__main__':
#    port = int(os.environ.get('PORT', 9111))
    app.secret_key = 'DPTE0909@#$'
    app.run(host='0.0.0.0')
    #app.run(, debug=True)
    
  #  app.run(port=port, debug=True)