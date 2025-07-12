# backend_local/app/models_orm.py

import datetime
from sqlalchemy import Column, String, Float, Text, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .db import Base
from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AttractionORM(Base):  # 注意这里使用Base，而非BaseModel
    __tablename__ = "attractions"
    
    id = Column(String, primary_key=True)
    city = Column(String)
    url = Column(String, nullable=True)
    area_name = Column(String, nullable=True)
    attraction_name = Column(String)
    comment_score = Column(Float)
    star = Column(String, nullable=True)
    pic_pre = Column(String, nullable=True)
    price = Column(Float)
    free = Column(String, nullable=True)
    character = Column(String, nullable=True)
    lat = Column(Float)
    lon = Column(Float)
    hot = Column(Float)
    address = Column(String, nullable=True)
    tags_ai = Column(String, nullable=True)
    advantage_1 = Column(String, nullable=True)
    advantage_2 = Column(String, nullable=True)
    advantage_3 = Column(String, nullable=True)
    disadvantage_1 = Column(String, nullable=True)
    disadvantage_2 = Column(String, nullable=True)
    disadvantage_3 = Column(String, nullable=True)

class UserORM(Base):
    __tablename__ = "users"
    id       = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    avatar   = Column(String)
    bio      = Column(Text)

class UsertoitineraryORM(Base):
    __tablename__ = "usertoitinerary"
    itineraries_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    created_time = Column(String)

class ItinerarydetailORM(Base):
    __tablename__ = "itinerarydetail"
    attraction_detail_id = Column(Integer, primary_key=True)
    itineraries_id = Column(Integer, ForeignKey("usertoitinerary.itineraries_id"))
    name = Column(String)
    transport = Column(String)
    time_spent = Column(String)
    image = Column(String)

class PostORM(Base):
    __tablename__ = "posts"
    id = Column(String, primary_key=True)
    title = Column(String)
    text = Column(Text)
    great = Column(Integer)
    comments_num = Column(Integer)
    post_url = Column(String)
    tag_1 = Column(String)
    tag_2 = Column(String)
    tag_3 = Column(String)
    tag_4 = Column(String)
    tag_5 = Column(String)
    tag_6 = Column(String)
    tag_7 = Column(String)
    tag_8 = Column(String)
    tag_9 = Column(String)
    tag_10 = Column(String)
    comment_1 = Column(Text)
    comment_2 = Column(Text)
    comment_3 = Column(Text)
    comment_4 = Column(Text)
    comment_5 = Column(Text)
    comment_6 = Column(Text)
    comment_7 = Column(Text)
    comment_8 = Column(Text)
    comment_9 = Column(Text)
    comment_10 = Column(Text)
    comment_11 = Column(Text)
    comment_12 = Column(Text)
    comment_13 = Column(Text)
    comment_14 = Column(Text)
    comment_15 = Column(Text)
    comment_16 = Column(Text)
    comment_17 = Column(Text)
    comment_18 = Column(Text)
    comment_19 = Column(Text)
    comment_20 = Column(Text)
    pic_url_1 = Column(String)
    pic_url_2 = Column(String)
    pic_url_3 = Column(String)


class CommentORM(Base):
    __tablename__ = "comments"
    id         = Column(String, primary_key=True, index=True)
    attraction_id    = Column(String, ForeignKey("attractions.id"))
    user_id    = Column(String, ForeignKey("users.id"))
    content1    = Column(Text)
    content2    = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class LikeORM(Base):
    __tablename__ = "likes"
    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    post_id = Column(String, ForeignKey("posts.id"), primary_key=True)

class FollowORM(Base):
    __tablename__ = "follows"
    user_id        = Column(String, ForeignKey("users.id"), primary_key=True)
    target_user_id = Column(String, ForeignKey("users.id"), primary_key=True)

class ItineraryORM(Base):
    __tablename__ = "itineraries"
    id           = Column(String, primary_key=True, index=True)
    user_id      = Column(String, ForeignKey("users.id"))
    title        = Column(String)
    selected_ids = Column(Text)      # JSON 列表
    days         = Column(String)
    preferences  = Column(Text)      # JSON 列表
    itinerary    = Column(Text)      # JSON
    created_at   = Column(DateTime, default=datetime.datetime.utcnow)
    # 可选：添加关系以便级联查询
    items        = relationship("ItineraryItemORM", back_populates="itinerary")

class ItineraryItemORM(Base):
    __tablename__ = "itinerary_items"
    id            = Column(String, primary_key=True, index=True)
    itinerary_id  = Column(String, ForeignKey("itineraries.id"), index=True)
    day           = Column(Integer, index=True)
    position      = Column(Integer, index=True)
    attraction_id = Column(String, index=True)

    # 与主表建立双向关系
    itinerary     = relationship("ItineraryORM", back_populates="items")
