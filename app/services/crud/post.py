import datetime

from schemas.post import PostCreate, PostFeedback
from models.post import Post


def insert_post(post: PostCreate, db):
    generated_post = Post(**post)
    db.add(generated_post)
    db.commit()
    db.refresh(generated_post)
    return generated_post


def get_number_posts_per_day(chat_id: int, db):
    posts = db.query(Post).filter(
        (Post.chat_id == chat_id) & (Post.created_at == datetime.date.today())).all()
    return len(posts)


def insert_feedback(post_feedback: PostFeedback, db):
    post = db.query(Post).filter(
        (Post.chat_id == post_feedback.chat_id) & (Post.generate == post_feedback.post)).first()

    post.feedback = post_feedback.feedback
    db.add(post)
    db.commit()
