# app/search_id.py
import sqlite3
import json
import os
from fastapi import HTTPException

def search_id_api(query: str, fuzzy: bool = False):
    """仅通过id字段匹配数据"""
    db_path = "scripts/dev.db"
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"数据库文件不存在: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 定义需要返回的字段（可根据需求调整）
    columns = [
      'id', 'city', 'url', 'area_name', 'attraction_name',
        'comment_score', 'star', 'pic_pre', 'price', 'free',
        'character', 'lat', 'lon', 'hot', 'address', 'tags_ai',
        'advantage_1', 'advantage_2', 'advantage_3',
        'disadvantage_1', 'disadvantage_2', 'disadvantage_3',
        'comment_number'
    ]

    try:
        if fuzzy:
            # 模糊匹配：id中包含query（忽略大小写）
            cursor.execute(
                f"SELECT {', '.join(columns)} FROM attractions WHERE LOWER(id) LIKE ?",
                (f'%{query.lower()}%',)  # SQL模糊查询语法
            )
        else:
            # 精确匹配：id完全等于query
            cursor.execute(
                f"SELECT {', '.join(columns)} FROM attractions WHERE id = ?",
                (query,)
            )
        
        data = cursor.fetchall()
        # 转换为字典列表
        results = [dict(zip(columns, row)) for row in data]

    except sqlite3.OperationalError as e:
        raise HTTPException(
            status_code=500,
            detail=f"数据库错误: 表或字段不存在 - {str(e)}"
        )
    finally:
        conn.close()

    return json.dumps(results, ensure_ascii=False)