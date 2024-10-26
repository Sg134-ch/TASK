from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('task_manager.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        description TEXT,
                        status TEXT DEFAULT 'Pending')''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks')
def tasks():
    conn = sqlite3.connect('task_manager.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return render_template('tasks.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form.get('description')
    conn = sqlite3.connect('task_manager.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, description) VALUES (?, ?)", (title, description))
    conn.commit()
    conn.close()
    return redirect(url_for('tasks'))

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    conn = sqlite3.connect('task_manager.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('tasks'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
