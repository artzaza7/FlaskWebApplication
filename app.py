from flask import Flask, render_template, request, redirect, url_for
import pymysql
import json

app = Flask(__name__)
# connection Database


def openConnection():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 database='flaskdb_sql',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection
# localhost, username, password, database


@app.route("/")
def index():
    return render_template('login.html')


@app.route("/login", methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    conn = openConnection()
    cur = conn.cursor()
    sql = "SELECT * FROM `user` WHERE user_username = %s AND user_password = %s"
    cur.execute(sql, (username, password))
    result = cur.fetchone()
    # print(result)
    saveResult = result["user_type"]
    conn.close()
    if saveResult == "USER":
        # print(result["user_type"])
        # print(result["user_id"])
        return redirect(url_for('haslogin',  user_type=result["user_type"], user_id=result["user_id"]))
    else:
        return render_template('admin/admin.html')


@app.route("/login/<string:user_type>/<string:user_id>", methods=['GET'])
def haslogin(user_type, user_id):
    conn = openConnection()
    cur = conn.cursor()
    sql = "SELECT * FROM `user` WHERE user_id = %s"
    cur.execute(sql, (user_id))
    result = cur.fetchone()
    conn.close()
    conn = openConnection()
    cur = conn.cursor()
    sql = "SELECT * FROM `product` WHERE product_id NOT IN ( SELECT product_id FROM favoriteproduct WHERE user_id = %s)"
    cur.execute(sql, (user_id))
    result_product = cur.fetchall()
    conn.close()
    return render_template('user/user.html', data=result, product_data=result_product)


@app.route("/addProductToFavorite/<string:user_type>/<string:user_id>/<string:product_id>", methods=['GET'])
def addProductToFavorite(user_type, user_id, product_id):
    conn = openConnection()
    cur = conn.cursor()
    sql = "INSERT INTO `favoriteproduct`(`user_id`, `product_id`) VALUES (%s, %s)"
    cur.execute(sql, (user_id, product_id))
    conn.commit()
    conn.close()
    return redirect(url_for('haslogin',  user_type=user_type, user_id=user_id))

@app.route("/login/<string:user_type>/<string:user_id>/favoriteProduct")
def hasLoginFavoriteProduct(user_type, user_id):
    conn = openConnection()
    cur = conn.cursor()
    sql = "SELECT * FROM `product` WHERE product_id IN ( SELECT product_id FROM favoriteproduct WHERE user_id = %s)"
    cur.execute(sql, (user_id))
    result = cur.fetchall()
    conn.close()
    conn = openConnection()
    cur = conn.cursor()
    sql = "SELECT * FROM `user` WHERE user_id = %s"
    cur.execute(sql, (user_id))
    result_user = cur.fetchone()
    conn.close()
    return render_template('user/userFavorite.html', data=result, data_user = result_user)
    
# @app.route("/login/<string:type>")
# def hasLogin(type):


if __name__ == "__main__":
    app.run(debug=True)
