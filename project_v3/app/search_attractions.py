# app/search_attractions_service.py
import sqlite3
import json
import os
from fastapi import HTTPException

def search_attractions_api(
    query: str,
    city: str = None,
    fields: str = None
):
    """
    景点搜索API实现
    """
    # 处理fields参数
    field_list = [ 'attraction_name']  # 默认字段
    if fields:
        field_list = [f.strip() for f in fields.split(',')]
    
    try:
        # 调用搜索函数
        results = search_db(query, city, field_list)
        return json.loads(results)  # 将JSON字符串转换为Python对象
    except Exception as e:
        error_detail = f"景点搜索失败: {str(e)}"
        raise HTTPException(status_code=500, detail=error_detail)

def search_db(query, city=None, fields=None):
    """
    执行景点数据库搜索
    """
    db_path = "scripts/dev.db"  # 数据库路径
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"数据库文件不存在: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 查询表中所有字段
    columns = [
        'id', 'city', 'url', 'area_name', 'attraction_name',
        'comment_score', 'star', 'pic_pre', 'price', 'free',
        'character', 'lat', 'lon', 'hot', 'address', 'tags_ai',
        'advantage_1', 'advantage_2', 'advantage_3',
        'disadvantage_1', 'disadvantage_2', 'disadvantage_3',
        'comment_number'
    ]

    try:
        # 执行基础查询
        cursor.execute(f"SELECT {', '.join(columns)} FROM attractions")
        data = cursor.fetchall()
    except sqlite3.OperationalError as e:
        conn.close()
        raise sqlite3.OperationalError(f"表不存在或查询失败: {e}")
    finally:
        conn.close()

    # 简单匹配：检查指定字段是否包含查询词（忽略大小写）
    query_lower = query.lower()
    results = []
    for item in data:
        item_dict = dict(zip(columns, item))

        # 城市筛选（如果指定了城市）
        if city:
            # 处理可能的None值
            item_city = item_dict.get('city', '').lower() if item_dict.get('city') else ''
            if item_city != city.lower():
                continue

        # 关键词匹配
        match = False
        for field in fields:
            if field in item_dict:
                field_value = str(item_dict[field]).lower() if item_dict[field] else ''
                if query_lower in field_value:
                    match = True
                    break
        if match:
            # 清理None值
            cleaned_item = {k: v for k, v in item_dict.items() if v is not None}
            results.append(cleaned_item)

    # 返回JSON格式的结果
    return json.dumps(results, ensure_ascii=False, indent=2)