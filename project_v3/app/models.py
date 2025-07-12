# app/models.py

from pydantic import BaseModel
from typing import List, Optional

# --------------------
# 景点与外部爬取帖子模型
# --------------------

class Attraction(BaseModel):
    id: str
    city: str
    url: Optional[str]
    area_name: Optional[str]
    attraction_name: str
    comment_score: float 
    star: Optional[str] 
    pic_pre: Optional[str]
    price: float 
    free: Optional[str] 
    character: Optional[str]
    lat: float
    lon: float
    hot: float
    address: Optional[str] 
    tags_ai: Optional[str]
    advantage_1: Optional[str]
    advantage_2: Optional[str]
    advantage_3: Optional[str]
    disadvantage_1: Optional[str]
    disadvantage_2: Optional[str]
    disadvantage_3: Optional[str]
    comment_num: int
    
class SourcePost(BaseModel):
    """
    用于存储爬虫抓取的小红书/携程等点评内容
    """
    post_id: str
    attraction_id: str
    content: str
    url: Optional[str]
    tags: List[str]
    likes: int
    sentiment: float

# --------------------
# 请求与行程模型
# --------------------

class RecommendRequest(BaseModel):
    destination: str
    days: int
    preferences: List[str]

class Attraction_with_tags(BaseModel):
    id: str
    name: str
    images: str
    tags: str

class ItineraryRequest(BaseModel):
    selected_ids: List[str]
    days: int
    preferences: List[str]

# --------------------
# 社交化用户与互动模型
# --------------------

class User(BaseModel):
    id: str                # UUID
    username: str          # 登录账号
    password: str          # 密码
    avatar: Optional[str] = None
    bio: Optional[str]    = ""

class Usertoitinerary(BaseModel):
    itineraries_id: str
    user_id: str
    created_time: str
    
class Itinerarydetail(BaseModel):
    attraction_detail_i: int
    itineraries_id: int
    name: str
    transport: str
    time_spent: str
    image: str

class Post(BaseModel):
    """
    社交平台上的用户帖子（UGC）
    """
    id: str
    user_id: str
    content: str
    images: List[str] = []  # 可为空
    created_at: str         # ISO 时间字符串

class Comment(BaseModel):
    id: str
    post_id: str
    user_id: str
    content: str
    created_at: str

class Like(BaseModel):
    user_id: str
    post_id: str

class Follow(BaseModel):
    user_id: str
    target_user_id: str

class ItineraryRecord(BaseModel):
    id: str
    user_id: str
    title: Optional[str]
    selected_ids: List[str]
    days: int
    preferences: List[str]
    itinerary: List[dict]
    created_at: str

# app/models.py

class ItineraryItem(BaseModel):
    id: str
    itinerary_id: str
    day: int
    position: int
    attraction_id: str

class ItineraryDetail(BaseModel):
    itinerary_id: str
    items: List[ItineraryItem]  # 按 day, position 排序

class LLMIteraryRequest(BaseModel):
    目的地: str
    必去的景点: List[str]
    必不去的景点: List[str]
    天数: str
    preferences: List[str]

class ItineraryStep(BaseModel):
    name: str
    transport: str
    time_spent: str
    id: Optional[str] = None  # 添加景区 ID 字段
    images: Optional[str] = None  # 添加景区展示图片字段

class LLMIteraryDay(BaseModel):
    day: int
    work_flow: List[ItineraryStep]

class LLMIteraryResponse(BaseModel):
    itinerary: List[LLMIteraryDay]

class ItineraryWorkFlowStep(BaseModel):
    name: str
    id: str
    images: str

class ItineraryDay(BaseModel):
    day: int
    work_flow: List[ItineraryWorkFlowStep]

class ItineraryWorkFlowStep(BaseModel):
    name: str
    id: str
    images: str

class ItineraryDay(BaseModel):
    day: int
    work_flow: List[ItineraryWorkFlowStep]

class UserUploadItineraryRequest(BaseModel):
    itinerary: List[ItineraryDay]

class UpdatedItineraryWorkFlowStep(BaseModel):
    name: str
    transport: str
    time_spent: str
    id: str
    images: str

class UpdatedItineraryDay(BaseModel):
    day: int
    work_flow: List[UpdatedItineraryWorkFlowStep]

class UserUploadItineraryResponse(BaseModel):
    itinerary: List[UpdatedItineraryDay]