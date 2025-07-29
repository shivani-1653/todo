from flask import Flask, render_template, request, redirect, flash, url_for, session
import bcrypt
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'P@ssword1'
app.config['MYSQL_DB'] = 'to_dos'
app.config['MYSQL_CHARSET'] = 'utf8mb4'

mysql = MySQL(app)

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users2 WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            session['username'] = user[1]
            session['user_id'] = user[0]  # <-- this is KEY!
            return redirect(url_for('welcome'))


        else:
            return "❌ Incorrect email or password."

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users2 WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            return redirect(url_for('login'))

        cursor.execute("INSERT INTO users2 (username, email, password) VALUES (%s, %s, %s)", 
                       (username, email, hashed_password))
        mysql.connection.commit()
        cursor.execute("SELECT * FROM users2 WHERE email = %s", (email,))
        new_user = cursor.fetchone()
        cursor.close()

        session['username'] = new_user[1]
        session['user_id'] = new_user[0]
        return redirect(url_for('welcome'))
    return render_template('register.html')

@app.route('/welcome')
def welcome():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('welcome.html', username=session['username'])

@app.route('/todo2', methods=['GET', 'POST'])
def todo2():
    if 'username' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        category_name = request.form['category_name']
        cursor = mysql.connection.cursor()

        # Insert only user-defined categories (not static)
        cursor.execute("INSERT INTO categories3 (cname, user_id) VALUES (%s, %s)", (category_name, user_id))

        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('todo2'))

    cursor = mysql.connection.cursor()

    # Static categories for all users (user_id IS NULL)
    cursor.execute("SELECT cname FROM categories3 WHERE user_id IS NULL")
    static_categories = cursor.fetchall()

    # Custom categories for current user
    cursor.execute("SELECT cname FROM categories3 WHERE user_id = %s", (user_id,))
    custom_categories = cursor.fetchall()

    cursor.close()

    return render_template('todo2.html', 
        username=session['username'], 
        static_categories=static_categories, 
        custom_categories=custom_categories
    )



@app.route('/work',methods=['GET', 'POST']) 
def work():
    if 'username' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        task=request.form.get('task')
        if task:
            cursor = mysql.connection.cursor()

            cursor.execute("INSERT INTO task3 (title, user_id, category) VALUES (%s, %s, %s)", (task, user_id, 'work'))

            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('work'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT task_id, title, status FROM task3 WHERE user_id = %s AND category = %s ORDER BY created_at DESC", (user_id, 'work'))

    tasks = cursor.fetchall()
    cursor.close()
    
    return render_template('work.html', username=session['username'], tasks=tasks)
    
@app.route('/personal',methods=['GET', 'POST'])
def personal():
    if 'username' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        task=request.form.get('task')
        if task:
            cursor = mysql.connection.cursor()

            cursor.execute("INSERT INTO task3 (title, user_id, category) VALUES (%s, %s, %s)", (task, user_id, 'personal'))

            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('personal'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT task_id, title, status FROM task3 WHERE user_id = %s AND category = %s ORDER BY created_at DESC", (user_id, 'personal'))

    tasks = cursor.fetchall()
    cursor.close()
    
    return render_template('personal.html', username=session['username'], tasks=tasks)
    

@app.route('/travel',methods=['GET', 'POST'])
def travel():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']

    if request.method == 'POST':
        task=request.form.get('task')
        if task:
            cursor = mysql.connection.cursor()

            cursor.execute("INSERT INTO task3 (title, user_id, category) VALUES (%s, %s, %s)", (task, user_id, 'travel'))

            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('travel'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT task_id, title, status FROM task3 WHERE user_id = %s AND category = %s ORDER BY created_at DESC", (user_id, 'travel'))

    tasks = cursor.fetchall()
    cursor.close()
    
    return render_template('travel.html', username=session['username'], tasks=tasks)
    
    
@app.route('/shopping',methods=['GET', 'POST'])
def shopping():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']

    if request.method == 'POST':
        task=request.form.get('task')
        if task:
            cursor = mysql.connection.cursor()

            cursor.execute("INSERT INTO task3 (title, user_id, category) VALUES (%s, %s, %s)", (task, user_id, 'shopping'))

            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('shopping'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT task_id, title, status FROM task3 WHERE user_id = %s AND category = %s ORDER BY created_at DESC", (user_id, 'shopping'))

    tasks = cursor.fetchall()
    cursor.close()
    
    return render_template('shopping.html', username=session['username'], tasks=tasks)
    
@app.route('/delete__category', methods=['POST'])
def delete_category():
    category_name = request.form['category_name']
    user_id = session['user_id']

    cursor = mysql.connection.cursor()
    # Only delete if this user created it (i.e., user_id is not NULL)
    cursor.execute("""
        DELETE FROM categories3 
        WHERE cname = %s AND user_id = %s
    """, (category_name, user_id))
    mysql.connection.commit()

    cursor.close()

    return redirect(url_for('todo2'))


  # redirect to last visited page

@app.route('/complete_task', methods=['POST'])
def complete_task():
    task_id = request.form.get('task_id')
    category = request.form.get('category')
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE task3 SET status = 'completed' WHERE task_id = %s", (task_id,))
    mysql.connection.commit()
    cursor.close()
    flash('Task marked as completed!', 'success')
    if category in ['work', 'personal', 'travel', 'shopping']:
        return redirect(url_for(category))
    else:
        return redirect(url_for('category_page', category_name=category))
   
    return redirect(url_for('category_page', category_name=category))

@app.route('/delete_task', methods=['POST'])
def delete_task():
    task_id = request.form['task_id']
    category = request.form.get('category')
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM task3 WHERE task_id = %s", (task_id,))

    mysql.connection.commit()
    cursor.close()
    flash("Task deleted!", "danger")
    if category in ['work', 'personal', 'travel', 'shopping']:
        return redirect(url_for(category))  # <-- redirect to /work, /personal
    else:
        return redirect(url_for('category_page', category_name=category))
   
    return redirect(url_for('category_page', category_name=category))

@app.route('/category/<category_name>', methods=['GET', 'POST'])
def category_page(category_name):
    if 'username' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    # Check if static
    static_categories = ['work', 'personal', 'travel', 'shopping']

    # Validate if category exists for this user (for dynamic)
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT cname FROM categories3 WHERE cname = %s AND user_id = %s", (category_name, user_id))
    custom_category = cursor.fetchone()
    cursor.close()

    # Handle POST (Add Task)
    if request.method == 'POST':
        task = request.form.get('task')
        if task:
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO task3 (title, user_id, category) VALUES (%s, %s, %s)",
                           (task, user_id, category_name))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('category_page', category_name=category_name))

    # Fetch tasks
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT task_id, title, status FROM task3 WHERE user_id = %s AND category = %s ORDER BY created_at DESC",
                   (user_id, category_name))
    tasks = cursor.fetchall()
    cursor.close()

    # Render correct template
    if category_name in static_categories:
        return render_template(f'{category_name}.html', username=session['username'], tasks=tasks)
    elif custom_category:
        return render_template('category.html', username=session['username'], tasks=tasks, category_name=category_name)
    else:
        flash("Invalid category!", "danger")
        return redirect(url_for('todo2'))


@app.route("/clear_category/<category>", methods=["POST"])
def clear_category(category):
    if 'username' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    # Delete all tasks
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM task3 WHERE category = %s AND user_id = %s", (category, user_id))
    mysql.connection.commit()
    cursor.close()
    flash(f"✅ All tasks in {category.title()} cleared!", "success")

    # ✅ If it's a static category, redirect to its route
    if category in ['work', 'personal', 'travel', 'shopping']:
        return redirect(url_for(category))  # /work, /personal, etc.
    else:
        return redirect(url_for('category_page', category_name=category))



if __name__ == '__main__':
    app.run(debug=True)
