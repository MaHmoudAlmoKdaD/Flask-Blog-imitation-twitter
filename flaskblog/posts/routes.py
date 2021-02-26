from flask import (render_template, url_for, flash, 
                    redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
# @login_required : to creating new post will be a route that requires user to be login
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Post has been created!', 'sucess')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legand='New Post')

@posts.route('/post/<int:post_id>')
@login_required
def post(post_id):
    # give me the post with this id, id doesn't exist then return 404 (it mean the page doesn't exist)
    # but it that post does exist then _simply render a template_ (ببساطة يعرض النوذج) that return that post
    post = Post.query.get_or_404(post_id) # 404 (page not found )
    return render_template('post.html', title=post.title, post=post)

@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403) #abort : اجهاض , that return in the page on browser (Forbidden /ممنوع|محظور/ You don't have the permission to access the requested resource. It is either read-protected or not readable by the server.)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your Post Has Been Updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content    
    return render_template('create_post.html', title='Update post', form=form, legand='Update Post')
    
@posts.route('/delete_post<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)  #404 (not found)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
