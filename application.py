from flask import Flask,request,render_template,jsonify,g,send_file
from flask_cors import CORS
import mysql.connector as mysql
import secrets
from PyPDF2 import PdfReader, PdfWriter
import os
application=Flask(__name__)
CORS(application)

def compress_file(to_compress_path,compressed_path):
    reader = PdfReader(to_compress_path)
    writer = PdfWriter()

    for page in reader.pages:
        page.compress_content_streams()  # This is CPU intensive!
        writer.add_page(page)
    writer.add_metadata(reader.metadata)
    with open(compressed_path, "wb") as f:
        writer.write(f)
    os.remove(to_compress_path)

@application.before_request
def create_conexion():
    g.con =mysql.connect(host='localhost', user= 'root', passwd='', db='compressor_api')

# Cierra la conexión después de cada solicitud
@application.teardown_request
def close_conexion(exception=None):
    con = getattr(g, 'con', None)
    if con is not None:
        con.close()

@application.route("/")
def index():
    return render_template("false_index.html")
@application.post("/compress_pdf")
def pdf_compressor():
    con = getattr(g, 'con', None)
    if con is None:
        return jsonify({"error":"An error occurred while trying to access to the Database"}),500
    file=request.files["file_post"]
    if(file.filename.split(".")[-1].lower()!="pdf"):
        return jsonify({"error":"El archivo ingresado tiene que ser un PDF"}),400
    file.save("original_files/"+file.filename)
    sql="INSERT INTO files(ID, ROUTE, NAME, DATE) VALUES(%s,%s,%s,DEFAULT)"
    token=secrets.token_urlsafe(16)
    route="files/"+token+".pdf"
    compress_file("original_files/"+file.filename,route)
    cur=con.cursor()
    cur.execute(sql,(token,route,file.filename))
    con.commit()
    return jsonify({"token":token}),200
@application.put("/change_pdf/<token>")
def tokenpdf_changer(token):
    con = getattr(g, 'con', None)
    if con is None:
        return jsonify({"error":"An error occurred while trying to access to the Database"}),500
    if not os.path.exists("files/"+token+".pdf"):
        return jsonify({"error":"That provided token hasn't a linked file"}),400
    file=request.files["file_put"]
    if(file.filename.split(".")[-1].lower()!="pdf"):
        return jsonify({"error":"The input file must be a PDF file"}),400
    file.save("original_files/"+file.filename)
    sql="UPDATE files SET ROUTE=%s, NAME=%s, DATE=DEFAULT"
    route="files/"+token+".pdf"
    os.remove(route)
    compress_file("original_files/"+file.filename,route)
    cur=con.cursor()
    cur.execute(sql,(route,file.filename))
    con.commit()
    return jsonify({"token":token}),200
@application.delete("/delete_pdf/<token>")
def pdf_deleter(token):
    con = getattr(g, 'con', None)
    if con is None:
        return jsonify({"error":"An error occurred while trying to access to the Database"}),500
    if not os.path.exists("files/"+token+".pdf"):
        return jsonify({"error":"That provided token hasn't a linked file"}),400
    sql="DELETE FROM files WHERE id=%s"
    os.remove("files/"+token+".pdf")
    cur=con.cursor()
    cur.execute(sql,(token,))
    con.commit()
    return jsonify({"result":"Your Operation has been realized successfully"}),200
@application.get("/get_compressed_pdf/<token>")
def returning_compressed_pdf(token):
    con = getattr(g, 'con', None)
    if con is None:
        return jsonify({"error":"An error occurred while trying to access to the Database"}),500
    sql="SELECT ROUTE FROM files WHERE id=%s"
    cur=con.cursor()
    cur.execute(sql,(token,))
    row=cur.fetchone()
    if row is not None:
        route=row[0]
    else:
        return jsonify({"error":"That provided token hasn't a linked file"}),400
    if not os.path.exists(route):
        return jsonify({"error":"That provided token hasn't a linked file"}),400
    with open(route, 'rb') as f:
        file_content = f.read()
    return send_file(route, as_attachment=True, download_name='compressed_file.pdf'),200