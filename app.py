from flask import Flask, g, render_template, request
import sqlite3


app = Flask(__name__)


# create the table with name: messages
def get_message_db():
    try:
        return g.message_db
    except:
        g.message_db = sqlite3.connect("messages_db.sqlite")
        cmd = \
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT,
            handle TEXT)
            """
        cursor = g.message_db.cursor()
        cursor.execute(cmd)
        return g.message_db



#insert the submitted handle and message into the messages table 
def insert_message(request):
    db = get_message_db()
    message = request.form['message']
    handle = request.form['handle']
    cursor = db.cursor()
    cursor.execute("SELECT * FROM messages")
    idn=len(cursor.fetchall())+1
    cursor.execute("INSERT INTO messages (id, handle, message) VALUES (?, ?, ?)",(idn, handle, message))
    db.commit()
    db.close()
    
def random_messages(n):
    con = get_message_db()
    cursor = con.cursor()
    cmd=\
    f"""
    SELECT handle,message FROM messages ORDER BY RANDOM() LIMIT {n}
    """
    cursor.execute(cmd)
    ran = cursor.fetchall()
    con.close()
    
    return ran
   


@app.route("/")
def main():
    return render_template("base.html")


@app.route("/submit/", methods=['POST', 'GET'])
def submit():
    if request.method == "GET":
        return render_template("submit.html")
    else:
        insert_message(request)
        return render_template("submit.html")

    
@app.route("/view/")
def view():
    return render_template("view.html", ran = random_messages(5))

    
    


