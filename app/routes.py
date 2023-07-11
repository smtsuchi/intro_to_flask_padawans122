from flask import render_template, request, redirect, url_for, flash
from app import app
from .forms import LoginForm, SignUpForm, PostForm
from .models import User, Post , db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/contact')
def contact_page():
    return render_template('contact.html')

## AUTHENTICATION

@app.route('/login', methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            password = form.password.data
            
            # find user from the db
            user = User.query.filter_by(username=username).first()

            if user:
                if user.password == password:
                    login_user(user)
                    flash('Successfully logged in.', 'success')
                    return redirect(url_for('home_page'))
                else:
                    flash('Incorrect username/password.', 'danger')
            else:
                flash('Incorrect username.', 'danger')
        else:
            flash('An error has occurred. Please submit a valid form', 'danger')           
            
    return render_template('login.html', form=form)

@app.route('/signup', methods=["GET", "POST"])
def signup_page():
    form = SignUpForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            
            #add user to database
            user = User(username, email, password)

            db.session.add(user)
            db.session.commit()
            flash('Successfully created user.', 'success')
            return redirect(url_for('login_page'))
        flash('An error has occurred. Please submit a valid form', 'danger')

    return render_template('signup.html', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login_page'))

## POSTS

@app.route('/posts/create', methods = ["GET", "POST"])
@login_required
def create_post_page():
    form = PostForm()
    if request.method == "POST":
        if form.validate():
            title = form.title.data
            caption = form.caption.data
            img_url = form.img_url.data

            my_post = Post(title, caption, img_url, current_user.id)

            db.session.add(my_post)
            db.session.commit()
            
            return redirect(url_for('home_page'))

    return render_template('createpost.html', form = form)

@app.route('/')
@app.route('/posts')
def home_page():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/posts/<post_id>')
def single_post_page(post_id):
    post = Post.query.filter_by(id = post_id).first()   # these lines are indetical 
    post = Post.query.get(post_id)                      # these lines are indetical 
    if post:
        return render_template('singlepost.html', post=post, like_count = len(post.likers2))
    else:
        return redirect(url_for('home_page'))
    
@app.route('/posts/update/<post_id>', methods=["GET", "POST"])
@login_required
def update_post_page(post_id):
    post = Post.query.get(post_id)
    if current_user.id != post.user_id:
        return redirect(url_for('home_page'))
    form = PostForm()
    if request.method == "POST":
        if form.validate():
            title = form.title.data
            caption = form.caption.data
            img_url = form.img_url.data

            post.title = title
            post.caption = caption
            post.img_url = img_url

            db.session.commit()
            return redirect(url_for('single_post_page', post_id = post.id))
    
    return render_template('updatepost.html', post=post, form=form)
    
@app.route('/posts/delete/<post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if current_user.id != post.user_id:
        return redirect(url_for('home_page'))
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home_page'))

# @app.route('/posts/like/<post_id>')
# @login_required
# def like_post(post_id):
#     like = Like.query.filter_by(post_id=post_id).filter_by(user_id=current_user.id).first()
#     if like:
#         return redirect(url_for('home_page'))
#     like = Like(current_user.id, post_id)
#     db.session.add(like)
#     db.session.commit()
#     return redirect(url_for('home_page'))

@app.route('/posts/like/<post_id>')
@login_required
def like_post2(post_id):
    post = Post.query.get(post_id)
    if post:
        current_user.liked_posts2.append(post)
        db.session.commit()
    return redirect(url_for('home_page'))

# @app.route('/posts/unlike/<post_id>')
# @login_required
# def unlike_post(post_id):
#     like = Like.query.filter_by(post_id=post_id).filter_by(user_id=current_user.id).first()
#     if like:
#         db.session.delete(like)
#         db.session.commit()
#     return redirect(url_for('home_page'))

@app.route('/posts/unlike/<post_id>')
@login_required
def unlike_post2(post_id):
    post = current_user.liked_posts2.filter_by(id=post_id).first()
    if post:
        current_user.liked_posts2.remove(post) 
        db.session.commit()
    return redirect(url_for('home_page'))

@app.route('/users')
def users_page():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/follow/<user_id>')
@login_required
def follow(user_id):
    user = User.query.get(user_id)
    current_user.followed.append(user)
    db.session.commit()
    return redirect(url_for('users_page'))

@app.route('/unfollow/<user_id>')
@login_required
def unfollow(user_id):
    user = current_user.followed.filter_by(id=user_id).first()
    if user:
        current_user.followed.remove(user)
        db.session.commit()
    return redirect(url_for('users_page'))