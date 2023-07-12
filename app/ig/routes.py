from flask import render_template, request, redirect, url_for, flash
from . import ig
from .forms import PostForm
from ..models import User, Post , db
from flask_login import login_required, current_user

@ig.route('/posts/create', methods = ["GET", "POST"])
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
            flash('Succesfully made a post!', 'success')
            return redirect(url_for('ig.home_page'))

    return render_template('createpost.html', form = form)

@ig.route('/')
@ig.route('/posts')
def home_page():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@ig.route('/posts/<post_id>')
def single_post_page(post_id):
    post = Post.query.filter_by(id = post_id).first()   # these lines are indetical 
    post = Post.query.get(post_id)                      # these lines are indetical 
    if post:
        return render_template('singlepost.html', post=post, like_count = len(post.likers2))
    else:
        return redirect(url_for('ig.home_page'))
    
@ig.route('/posts/update/<post_id>', methods=["GET", "POST"])
@login_required
def update_post_page(post_id):
    post = Post.query.get(post_id)
    if current_user.id != post.user_id:
        return redirect(url_for('ig.home_page'))
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
            return redirect(url_for('ig.single_post_page', post_id = post.id))
    
    return render_template('updatepost.html', post=post, form=form)
    
@ig.route('/posts/delete/<post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if current_user.id != post.user_id:
        return redirect(url_for('ig.home_page'))
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('ig.home_page'))

# @ig.route('/posts/like/<post_id>')
# @login_required
# def like_post(post_id):
#     like = Like.query.filter_by(post_id=post_id).filter_by(user_id=current_user.id).first()
#     if like:
#         return redirect(url_for('ig.home_page'))
#     like = Like(current_user.id, post_id)
#     db.session.add(like)
#     db.session.commit()
#     return redirect(url_for('ig.home_page'))

@ig.route('/posts/like/<post_id>')
@login_required
def like_post2(post_id):
    post = Post.query.get(post_id)
    if post:
        current_user.liked_posts2.append(post)
        db.session.commit()
    return redirect(url_for('ig.home_page'))

# @ig.route('/posts/unlike/<post_id>')
# @login_required
# def unlike_post(post_id):
#     like = Like.query.filter_by(post_id=post_id).filter_by(user_id=current_user.id).first()
#     if like:
#         db.session.delete(like)
#         db.session.commit()
#     return redirect(url_for('ig.home_page'))

@ig.route('/posts/unlike/<post_id>')
@login_required
def unlike_post2(post_id):
    post = current_user.liked_posts2.filter_by(id=post_id).first()
    if post:
        current_user.liked_posts2.remove(post) 
        db.session.commit()
    return redirect(url_for('ig.home_page'))

@ig.route('/users')
def users_page():
    users = User.query.all()
    return render_template('users.html', users=users)

@ig.route('/follow/<user_id>')
@login_required
def follow(user_id):
    user = User.query.get(user_id)
    current_user.followed.append(user)
    db.session.commit()
    return redirect(url_for('ig.users_page'))

@ig.route('/unfollow/<user_id>')
@login_required
def unfollow(user_id):
    user = current_user.followed.filter_by(id=user_id).first()
    if user:
        current_user.followed.remove(user)
        db.session.commit()
    return redirect(url_for('ig.users_page'))
