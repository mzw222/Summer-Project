# backend_local/app/crud_db.py

import uuid
import json
import datetime
from typing import List
from sqlalchemy.orm import Session

from .models_orm import (
    AttractionORM,
    UserORM,
    PostORM,
    CommentORM,
    LikeORM,
    FollowORM,
    UsertoitineraryORM,
    ItinerarydetailORM,
    ItineraryORM,
    ItineraryItemORM,
)

from .models import (
    Attraction,
    User,
    Post,
    Comment,
    Like,
    Follow,
    Usertoitinerary,
    Itinerarydetail,
    ItineraryRecord,
    ItineraryItem,
    ItineraryDetail,
    RecommendRequest,
    Attraction_with_tags,
)

# --------------------
# 景点 CRUD
# --------------------

def list_attractions_db(db: Session, dest: str) -> List[Attraction_with_tags]:
    q = db.query(AttractionORM)
    if dest:
        q = q.filter(AttractionORM.attraction_name.contains(dest))
    result: List[Attraction_with_tags] = []
    for orm in q.all():
        result.append(Attraction_with_tags(
            id=orm.id,
            name=orm.attraction_name,
            images=orm.pic_pre or "",
            tags=orm.tags_ai or ""
        ))
    return result

def get_attraction_db(db: Session, attraction_id: str) -> Attraction | None:
    orm = db.get(AttractionORM, attraction_id)
    if not orm:
        return None
    return Attraction(
        id=orm.id,
        name=orm.name,
        description=orm.description,
        lat=orm.lat,
        lon=orm.lon,
        tags=json.loads(orm.tags or "[]"),
        images=json.loads(orm.images or "[]"),
        address=orm.address,
        pros=[],
        cons=[],
        source_posts=[]
    )

# --------------------
# 用户 CRUD
# --------------------

def create_user_db(db: Session, username: str, password: str) -> User:
    new_user = UserORM(
        id=str(uuid.uuid4()),
        username=username,
        password=password,
        avatar=None,
        bio=""
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return User(
        id=new_user.id,
        username=new_user.username,
        password=new_user.password,
        avatar=new_user.avatar,
        bio=new_user.bio
    )


def get_user_db(db: Session, user_id: str) -> User | None:
    orm = db.get(UserORM, user_id)
    if not orm:
        return None
    return User(**orm.__dict__)


def update_user_bio_db(db: Session, user_id: str, new_bio: str) -> User:
    """更新用戶的個人簡介

    Args:
        db (Session): 數據庫會話
        user_id (str): 用戶ID
        new_bio (str): 新的個人簡介

    Returns:
        User: 更新後的用戶資料

    Raises:
        HTTPException: 當用戶不存在時拋出404錯誤
    """
    user = db.get(UserORM, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用戶不存在")
    
    user.bio = new_bio
    db.commit()
    db.refresh(user)
    
    return User(**user.__dict__)

# --------------------
# 帖子 CRUD
# --------------------

def create_post_db(db: Session, user_id: str, content: str, images: List[str]) -> Post:
    new_post = PostORM(
        id=str(uuid.uuid4()),
        user_id=user_id,
        content=content,
        images=json.dumps(images, ensure_ascii=False),
        created_at=datetime.datetime.utcnow()
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return Post(
        id=new_post.id,
        user_id=new_post.user_id,
        content=new_post.content,
        images=json.loads(new_post.images),
        created_at=new_post.created_at.isoformat()
    )


def list_posts_db(db: Session) -> List[Post]:
    result: List[Post] = []
    for orm in db.query(PostORM).order_by(PostORM.created_at.desc()).all():
        result.append(Post(
            id=orm.id,
            user_id=orm.user_id,
            content=orm.content,
            images=json.loads(orm.images or "[]"),
            created_at=orm.created_at.isoformat()
        ))
    return result

# --------------------
# 评论 CRUD
# --------------------

def add_comment_db(db: Session, post_id: str, user_id: str, content: str) -> Comment:
    new_comment = CommentORM(
        id=str(uuid.uuid4()),
        post_id=post_id,
        user_id=user_id,
        content=content,
        created_at=datetime.datetime.utcnow()
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return Comment(
        id=new_comment.id,
        post_id=new_comment.post_id,
        user_id=new_comment.user_id,
        content=new_comment.content,
        created_at=new_comment.created_at.isoformat()
    )


def list_comments_db(db: Session, post_id: str) -> List[Comment]:
    result: List[Comment] = []
    for orm in db.query(CommentORM).filter(CommentORM.post_id == post_id).order_by(CommentORM.created_at).all():
        result.append(Comment(
            id=orm.id,
            post_id=orm.post_id,
            user_id=orm.user_id,
            content=orm.content,
            created_at=orm.created_at.isoformat()
        ))
    return result

# --------------------
# 点赞 CRUD
# --------------------

def toggle_like_db(db: Session, user_id: str, post_id: str) -> dict:
    existing = db.query(LikeORM).filter(
        LikeORM.user_id == user_id,
        LikeORM.post_id == post_id
    ).first()
    if existing:
        db.delete(existing)
        action = "deleted"
    else:
        new_like = LikeORM(user_id=user_id, post_id=post_id)
        db.add(new_like)
        action = "added"
    db.commit()
    return {"result": action}


def count_likes_db(db: Session, post_id: str) -> int:
    return db.query(LikeORM).filter(LikeORM.post_id == post_id).count()

# --------------------
# 关注 CRUD
# --------------------

def toggle_follow_db(db: Session, user_id: str, target_user_id: str) -> dict:
    existing = db.query(FollowORM).filter(
        FollowORM.user_id == user_id,
        FollowORM.target_user_id == target_user_id
    ).first()
    if existing:
        db.delete(existing)
        action = "unfollowed"
    else:
        new_follow = FollowORM(user_id=user_id, target_user_id=target_user_id)
        db.add(new_follow)
        action = "followed"
    db.commit()
    return {"result": action}

# --------------------
# 行程主表 CRUD
# --------------------

def save_itinerary_db(
    db: Session,
    user_id: str,
    title: str,
    selected_ids: List[str],
    days: int,
    preferences: List[str],
    itinerary: List[dict]
) -> ItineraryRecord:
    record = ItineraryORM(
        id=str(uuid.uuid4()),
        user_id=user_id,
        title=title,
        selected_ids=json.dumps(selected_ids, ensure_ascii=False),
        days=str(days),
        preferences=json.dumps(preferences, ensure_ascii=False),
        itinerary=json.dumps(itinerary, ensure_ascii=False),
        created_at=datetime.datetime.utcnow()
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return ItineraryRecord(
        id=record.id,
        user_id=record.user_id,
        title=record.title,
        selected_ids=json.loads(record.selected_ids),
        days=int(record.days),
        preferences=json.loads(record.preferences),
        itinerary=json.loads(record.itinerary),
        created_at=record.created_at.isoformat()
    )


def list_user_itineraries_db(db: Session, user_id: str) -> List[ItineraryRecord]:
    result: List[ItineraryRecord] = []
    for orm in db.query(ItineraryORM).filter(ItineraryORM.user_id == user_id).order_by(ItineraryORM.created_at.desc()).all():
        result.append(ItineraryRecord(
            id=orm.id,
            user_id=orm.user_id,
            title=orm.title,
            selected_ids=json.loads(orm.selected_ids),
            days=int(orm.days),
            preferences=json.loads(orm.preferences),
            itinerary=json.loads(orm.itinerary),
            created_at=orm.created_at.isoformat()
        ))
    return result

# --------------------
# 行程明细 CRUD (Itinerary Items)
# --------------------

def list_itinerary_items(db: Session, itinerary_id: str) -> ItineraryDetail:
    rows = (
        db.query(ItineraryItemORM)
          .filter(ItineraryItemORM.itinerary_id == itinerary_id)
          .order_by(ItineraryItemORM.day, ItineraryItemORM.position)
          .all()
    )
    items: List[ItineraryItem] = [
        ItineraryItem(
            id=r.id,
            itinerary_id=r.itinerary_id,
            day=r.day,
            position=r.position,
            attraction_id=r.attraction_id
        ) for r in rows
    ]
    return ItineraryDetail(itinerary_id=itinerary_id, items=items)


def update_item_positions(db: Session, updates: List[dict]) -> dict:
    for u in updates:
        itm = db.get(ItineraryItemORM, u.get("id"))
        if itm and "new_position" in u:
            itm.position = u["new_position"]
    db.commit()
    return {"updated": len(updates)}


def add_itinerary_item(db: Session, itinerary_id: str, day: int, position: int, attraction_id: str) -> ItineraryItem:
    new = ItineraryItemORM(
        id=str(uuid.uuid4()),
        itinerary_id=itinerary_id,
        day=day,
        position=position,
        attraction_id=attraction_id
    )
    db.add(new)
    db.commit()
    db.refresh(new)
    return ItineraryItem(
        id=new.id,
        itinerary_id=new.itinerary_id,
        day=new.day,
        position=new.position,
        attraction_id=new.attraction_id
    )


def delete_itinerary_item(db: Session, item_id: str) -> dict:
    itm = db.get(ItineraryItemORM, item_id)
    if itm:
        db.delete(itm)
        db.commit()
        return {"deleted": True}
    return {"deleted": False}

#usertoitinerary表的插入和查找、删除
def insert_usertoitinenary(db:Session, _user_id: str, _created_time: str):
    orm = UsertoitineraryORM(
        itineraries_id = _user_id + _created_time,
        user_id = _user_id,
        created_time = _created_time
        )
    db.merge(orm)
    return Usertoitinerary(
        itineraries_id = _user_id + _created_time,
        user_id = _user_id,
        created_time = _created_time
        )

def get_usertoitinenary_via_itineraries_id(db:Session, _itineraries_id: str) -> Usertoitinerary:
    orm = db.get(UsertoitineraryORM, _itineraries_id)
    if not orm:
        return None
    return Usertoitinerary(
        **orm.__dict__
        )

def get_usertoitinerary_via_user(db: Session, user_id: str) -> List[Usertoitinerary]:
    results = db.query(UsertoitineraryORM).filter(
        UsertoitineraryORM.userid == user_id
    ).all()
    
    return [Itinerarydetail(**item.__dict__) for item in results] if results else []

def delete_usertoitinerary_via_itineraries_id(db:Session, _itineraries_id: str) -> dict:
        itm = db.get(UsertoitineraryORM, _itineraries_id)
        if itm:
            db.delete(itm)
            db.commit()
            return {"deleted": True}
        return {"deleted": False}

#itinerarydetail表的插入、查找和删除
def insert_itinerarydetail(db: Session, 
                          _itineraries_id: int, 
                          _name: str, 
                          _transport: str, 
                          _time_spent: str, 
                          _image: str):
    orm = ItinerarydetailORM(
        itineraries_id=_itineraries_id,
        name=_name,
        transport=_transport,
        time_spent=_time_spent,
        image=_image
    )
    db.merge(orm)  
    return Itinerarydetail(
        attraction_detail_id=orm.attraction_detail_id,
        itineraries_id=_itineraries_id,
        name=_name,
        transport=_transport,
        time_spent=_time_spent,
        image=_image
    )

def get_itinerarydetails_by_itinerary(db: Session, _itinerary_id: int) -> List[Itinerarydetail]:
    orm_list = db.query(ItinerarydetailORM).filter(
        ItinerarydetailORM.itineraries_id == _itinerary_id
    ).all()
    return [Itinerarydetail(**item.__dict__) for item in orm_list] if orm_list else []

def delete_itinerarydetail_by_detail_id(db: Session, _detail_id: int) -> dict:
    orm = db.get(ItinerarydetailORM, _detail_id)
    if orm:
        db.delete(orm)
        db.commit()
        return {"deleted": True}
    return {"deleted": False}