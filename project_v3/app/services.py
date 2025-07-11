# project_v3/app/services.py

from typing import List
import json

from .crud_db import list_attractions_db, get_attraction_db
from .crud import get_posts_for
from .ai_services import generate_llm_itinerary
from .models import RecommendRequest, ItineraryRequest, Attraction
from .db import SessionLocal

def recommend(req: RecommendRequest) -> List[Attraction]:
    """
    查询候选景点，并可根据偏好进行二次过滤或排序（TODO）。
    """
    db = SessionLocal()
    try:
        # 从数据库中拉取所有符合目的地的景点
        cands = list_attractions_db(db, req.destination)
        # TODO: 按 req.preferences 做打分或二次筛选
        return cands
    finally:
        db.close()

def build_itinerary(req: ItineraryRequest) -> List[dict]:
    """
    根据用户选中的景点与偏好，调用 AI 生成结构化行程方案。
    """
    # 先从数据库读取所有景点
    db = SessionLocal()
    try:
        all_attractions = list_attractions_db(db, "")
    finally:
        db.close()

    # 过滤出用户已选的景点对象
    selected = [a for a in all_attractions if a.id in req.selected_ids]
    if not selected:
        return []

    # 构建 LLMIteraryRequest 对象
    llm_req = LLMIteraryRequest(
        目的地="北京",  # 根据实际情况设置目的地
        天数=req.days,
        必去的景点=[attraction.name for attraction in selected],
        必不去的景点=[],  # 根据实际情况设置
        preferences=req.preferences,
        selected=selected
    )

    # 调用 AI 生成行程
    llm_itinerary = generate_llm_itinerary(llm_req)
    if llm_itinerary:
        # 将 LLMIteraryResponse 对象转换为 List[dict]
        itinerary_list = []
        for day in llm_itinerary.itinerary:
            day_dict = day.dict()
            work_flow_list = []
            for step in day_dict["work_flow"]:
                step_dict = step.dict()
                work_flow_list.append(step_dict)
            day_dict["work_flow"] = work_flow_list
            itinerary_list.append(day_dict)
        return itinerary_list
    return []