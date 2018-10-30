#BLOGS - MAIN.PY

from flask import Flask, request, redirect, render_template,flash
import os


from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:Aishatwin82!@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
app.secret_key = 'creamofthenile29'


class Blogz (db.Model):

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    

    def __init__(self,title,body):
        self.title = title
        self.body = body

class User (db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))  
    blogs = db.relationship('Blogs', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password



@app.route('/newpost', methods=['POST','GET'])
def newpost():
    
    if request.method == 'POST':
        
        blog_body = request.form['blog_body']
        blog_title = request.form['blog_title']
        title_error = ''
        body_error = ''
        
        
        if len (blog_body) < 1:
            body_error = 'Need content'
        if len (blog_title) < 1:
            title_error = 'Need content'

        if not body_error and not title_error:
            
            
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            url = '/blog?id=' + str(new_blog.id)
            return redirect(url)

        else:
            
            return render_template('newpost.html', body_error=body_error,title_error=title_error)

    else:
        
         return render_template('newpost.html')   



@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

    #TODO - validate user data

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/')

        else:
        #TODO - user better response messaging
            return "<h1> Duplicate user</h1>"        


    return  render_template('register.html')


@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        #1. User enters username that is stored in database with the correct password and redirectd to /newposy with their username being stored in a session
        #if username 

    #     if user and user.password == password:
    #         session['username']= username
    #         #flash("Logged in")
    #         return redirect('/newpost')
    #     #2. User enters a username that is stored in the database w/an incorrect password and is redirected to the /login page w/a message thst their password is incorrect    
    #         if username
    #             flash("User paswword incorrect")
    #             return ('/login')
    #     #else:
    #         #flash('User password incorrect, or user does not exist', 'error')

    #     #3. User tries to login w/a username that is not stored in the database and is redirected to the /login page with a message username does not exist    
    #     if username not 
    #        flash("Username does not exist")
    #        return ('/login')    
           
    # return render_template('login.html')

@app.route('/', methods = ['POST', 'GET'])
def index():

    owner = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        task_name = request.form['task']
        
        new_task = Task(task_name, owner)
        db.session.add(new_task)
        db.session.commit()
        
        #tasks.append(task)
        

    tasks = Task.query.filter_by(completed=False,owner=owner).all()
    completed_tasks = Task.query.filter_by(completed=True,owner=owner).all()
    return render_template('todos.html', title ="Get It Done!", 
        tasks = tasks, completed_tasks=completed_tasks)


@app.route('/logout', methods=['POST'])
def logout():
    del session['username']
    return redirect('/blog')    



















     

@app.route('/blog', methods=['POST', 'GET'])
def blog():

    if request.args:
        blog_id = request.args.get("id")
        blog = Blog.query.get(blog_id)

        return render_template('single_post.html',blog=blog)

    else:
        blog_list = Blog.query.all()
        return render_template('blog.html', blog_list=blog_list)




if __name__ == '__main__':
    
    app.run()