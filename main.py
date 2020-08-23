from flask import Flask, flash, render_template, request, redirect
# from db_config import MySQL
# from app import app
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()
app.secret_key = "secret key"

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
app.config['MYSQL_DATABASE_DB'] = 'twitter'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def home():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        sql = "SELECT Username, URL, status, id FROM twitter_data"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        urls = cursor.fetchall()
        conn.commit()
        flash('User added successfully!')
        return render_template("base.html", urls=urls)
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()
    return 'Error while adding url'

@app.route('/add', methods=['POST'])
def add():
    conn = mysql.connect()
    cursor = conn.cursor()
    try: 
        username = request.form['username']
        url = request.form['url']
        if username and url and request.method == 'POST':
            sql = "INSERT INTO twitter_data(Username, URL, status) VALUES (%s, %s, 'False')"
            data = (username, url)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            flash('User added successfully!')
            return redirect('/')
        else:
            return 'Error while adding url'
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()
    return 'Error while adding url'

@app.route('/update/<int:id>')
def update(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        sql_str = "SELECT id, status from twitter_data where id=%s"
        data = (id)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql_str, data)
        status = cursor.fetchall()
        if status[0][1] == 'False':
            sql = "UPDATE twitter_data SET status='True' where id=%s"
        else:
            sql = "UPDATE twitter_data SET status='False' where id=%s"
        data = (id)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        flash('User updated successfully!')
        return redirect('/')
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()
    return 'Error while updating user'

if __name__ == "__main__":
    app.run(port = 5004, debug = True)