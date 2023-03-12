from flask import Flask,request,render_template,jsonify
from flask_cors import CORS
import mysql.connector as mysql
import secrets
application=Flask(__name__)
CORS(application)
con=mysql.connect(host='localhost', user= 'root', passwd='', db='compressor_api')

@application.route("/")
def index():
    return render_template("false_index.html")
@application.post("/compress_pdf")
def pdf_compressor():
    file=request.files["file_post"]
    sql="INSERT INTO files(ID, ROUTE, NAME, DATE) VALUES(%s,%s,%s,DEFAULT)"
    token=secrets.token_urlsafe(16)
    route="files/"+token+"."+file.filename.split(".")[-1]#Por si acaso
    cur=con.cursor()
    cur.execute(sql,(token,route,file.filename))
    con.commit()
    con.close()
    file.save(route)
    return jsonify({"token":token})