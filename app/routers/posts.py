from fastapi import APIRouter, HTTPException, status, Response
from .. import schemas, database

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/")
def get_posts():
    database.cursor.execute("""SELECT * FROM posts""")
    posts = database.cursor.fetchall()
    return {"data": posts}


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.Post):
    database.cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
        (post.title, post.content, post.published),
    )
    new_post = database.cursor.fetchone()
    database.conn.commit()
    return {"data": new_post}


@router.get("/{id}")
def get_post(id: int):
    database.cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = database.cursor.fetchone()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"post_detail": post}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    database.cursor.execute(
        """DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),)
    )
    deleted_post = database.cursor.fetchone()
    database.conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_post(id: int, post: schemas.Post):
    database.cursor.execute(
        """UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",
        (post.title, post.content, post.published, str(id)),
    )
    updated_post = database.cursor.fetchone()
    database.conn.commit()
    if not updated_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"data": updated_post}
