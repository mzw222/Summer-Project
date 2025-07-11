import sys
import os

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from typing import List
import json

from .crud_db import list_attractions_db, get_attraction_db
from .crud import get_posts_for
from .ai_services import generate_llm_itinerary
from .models import RecommendRequest, ItineraryRequest, Attraction, Attraction_with_tags
from .db import SessionLocal

def recommend(req: RecommendRequest) -> List[Attraction_with_tags]:
    """
    查询候选景点，并根据偏好进行二次过滤或排序。
    """
    db = SessionLocal()
    try:
        # 从数据库中拉取所有符合目的地的景点
        cands = list_attractions_db(db, req.destination)

        # 计算每个景点的preference词语匹配个数和hot值
        scored_cands = []
        for cand in cands:
            # 将 tags 字符串转换为列表
            tags = cand.tags.split(',') if cand.tags else []
            match_count = len(set(tags).intersection(set(req.preferences)))
            # 假设 Attraction_with_tags 有 hot 属性，如果没有需要调整
            hot = getattr(cand, 'hot', 0)  # 如果没有 hot 属性，默认为 0
            scored_cands.append((cand, match_count, hot))

        # 按照preference词语匹配个数和hot值排序
        scored_cands.sort(key=lambda x: (-x[1], -x[2]))

        # 取前十个结果
        top_ten = scored_cands[:10]

        # 提取景点信息
        result = []
        for cand, _, _ in top_ten:
            result.append({
                "id": cand.id,
                "name": cand.name,
                "images": cand.images,
                "tags": cand.tags
            })

        return result
    finally:
        db.close()
    """
    查询候选景点，并根据偏好进行二次过滤或排序。
    """
    db = SessionLocal()
    try:
        # 从数据库中拉取所有符合目的地的景点
        cands = list_attractions_db(db, req.destination)

        # 计算每个景点的preference词语匹配个数和hot值
        scored_cands = []
        for cand in cands:
            # 假设tags_ai是一个字符串，需要先将其转换为列表
            tags_ai = cand.tags_ai.split(',') if cand.tags_ai else []
            match_count = len(set(tags_ai).intersection(set(req.preferences)))
            scored_cands.append((cand, match_count, cand.hot))

        # 按照preference词语匹配个数和hot值排序
        scored_cands.sort(key=lambda x: (-x[1], -x[2]))

        # 取前十个结果
        top_ten = scored_cands[:10]

        # 提取景点信息
        result = []
        for cand, _, _ in top_ten:
            result.append({
                "id": cand.id,
                "name": cand.name,
                "images": cand.images[0] if cand.images else "",
                "tags": str(cand.tags)
            })

        return result
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