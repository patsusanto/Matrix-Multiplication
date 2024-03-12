from flask import Flask, render_template, url_for, request, redirect, session, g
import numpy as np

#creates instance of flask web app
app = Flask(__name__, static_url_path='/static')

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

col = 0
row = 0
col1 = 0
row1 = 0

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/addition', methods=["GET","POST"])
def addition(): 
    if request.method == "POST":
        try:
            global col
            col = int(request.form.get("col"))
            global row 
            row = int(request.form.get("row"))
            return render_template("added.html", col=col, row=row)
        except ValueError:
            return render_template("add_error_miss.html", row=row, col=col, row1=row1, col1=col1)
    return render_template("addition.html")

@app.route('/added', methods=["GET", "POST"])
def added():
    if request.method == "POST":
        try:
            #receive data from form
            og_mat1 = request.form.getlist("matrix1")
            og_mat2 = request.form.getlist("matrix2")
            
            matrix1 = np.array(og_mat1).reshape(row,col)
            matrix2 = np.array(og_mat2).reshape(row,col)
            result = [[0 for _ in range(col)] for _ in range(row)]

            operation = request.form.get("operation")

            if operation == '+':
                for i in range(row):
                    for j in range(col):
                        result[i][j] = int(matrix1[i][j]) + int(matrix2[i][j])
            else:
                for i in range(row):
                    for j in range(col):
                        result[i][j] = int(matrix1[i][j]) - int(matrix2[i][j])
            
            return render_template("add_end.html", col=col, row=row, length=len(matrix1), matrix1=matrix1, matrix2=matrix2, result=result)
        except ValueError:
            return render_template("added_error_miss.html", row=row, col=col)
    return render_template("added.html", col=col, row=row)
    
@app.route('/multiplication', methods=["GET","POST"])
def multiplication():
    if request.method == "POST":
        try:
            global row
            global col
            global row1
            global col1
            row = int(request.form.get("row"))
            col = int(request.form.get("col"))
            row1 = int(request.form.get("row1"))
            col1 = int(request.form.get("col1"))

            if col != row1:
                return render_template("error.html")
            return render_template("multiplied.html", row=row, col=col, row1=row1, col1=col1)
        except ValueError:
            return render_template("multiplication_err.html")
    return render_template("multiplication.html")

@app.route('/multiplied', methods=["GET", "POST"])
def multiplied():
    if request.method == "POST":
        try:
            #receive data from form
            og_mat1 = request.form.getlist("matrix1")
            og_mat2 = request.form.getlist("matrix2")
                
            matrix1 = np.array(og_mat1, dtype=int).reshape(row,col)
            matrix2 = np.array(og_mat2, dtype=int).reshape(row1,col1)
                
            result = np.matmul(matrix1, matrix2)

            row_length = len(result)
            col_length = len(result[0])

            return render_template("mult_end.html", row=row, col=col, row1=row1, col1=col1, matrix1=matrix1, matrix2=matrix2, result=result, row_length=row_length, col_length=col_length)
        except ValueError:
            return render_template("error_missing.html", row=row, col=col, row1=row1, col1=col1)
    return render_template("multiplied.html", row=row, col=col, row1=row1, col1=col1)

#prevents unnecesarry execution of programs
if __name__ == "__main__":
    app.run(debug=True)
