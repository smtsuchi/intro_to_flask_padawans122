from flask import request
from . import api
from ..models import User, Post, db

@api.get('/posts')
def get_all_posts_API():
    posts = Post.query.order_by(Post.date_created.desc()).all()
    return {
        'status': 'ok',
        'results': len(posts),
        'posts': [p.to_dict() for p in posts]
    }, 200

@api.get('/posts/<post_id>')
def get_a_post_API(post_id):
    post = Post.query.get(post_id)
    if post:
        return {
            'status': 'ok',
            'results': 1,
            'post': post.to_dict()
        }, 200
    return {
        'status': 'not ok',
        'message': 'The post you are looking for does not exist.'
    }, 404

@api.post('/posts/create')
def create_post_api():
    try:
        data = request.json
        
        title = data['title']
        img_url = data['img_url']
        caption = data.get('caption', '')
        user_id = data['user_id']

        post = Post(title, caption, img_url, user_id)

        db.session.add(post)
        db.session.commit()
        return {
            'status': 'ok',
            'message': 'Successfully created a post!'
        }, 201
    except:
        return {
            'status': 'not ok',
            'message': "Not enough info provided to create a post."
        }, 400
    
@api.post('/posts/like/<post_id>')
# @login_required
def like_post_API(post_id):
    post = Post.query.get(post_id)
    data = request.json
    user_id = data['user_id']
    current_user = User.query.get(user_id)
    if post:
        current_user.liked_posts2.append(post)
        db.session.commit()
    return {
        "status": 'ok',
        "message": "You have succesfullly liked the post."
    }

@api.post('/posts/unlike/<post_id>')
# @login_required
def unlike_post_API(post_id):
    data = request.json
    user_id = data['user_id']
    current_user = User.query.get(user_id)
    post = current_user.liked_posts2.filter_by(id=post_id).first()
    if post:
        current_user.liked_posts2.remove(post) 
        db.session.commit()
    return {
        "status": 'ok',
        "message": "You have succesfullly unliked the post."
    }

