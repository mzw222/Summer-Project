# app/search_service.py
import sqlite3
import json
from fastapi import HTTPException

def search_posts_api(
    query: str,
    city: str = None,
    fields: str = None
):
    """
    搜索帖子的API实现
    """
    # 处理fields参数
    field_list = None
    if fields:
        field_list = [f.strip() for f in fields.split(',')]
    
    try:
        # 调用搜索函数
        results = search_db(query, city, field_list)
        return json.loads(results)  # 将JSON字符串转换为Python对象
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail=f"数据库查询失败: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")

def search_db(query, city=None, fields=None):
    """
    执行数据库搜索
    """
    # 设置默认的搜索字段
    if fields is None:
        fields = ['title', 'text', 'tag_1', 'tag_2', 'tag_3',
                  'tag_4', 'tag_5', 'tag_6', 'tag_7', 'tag_8', 'tag_9', 'tag_10']

    # 连接数据库 - 确保数据库文件路径正确
    conn = sqlite3.connect("scripts/dev.db")
    cursor = conn.cursor()

    # 查询表中所有字段
    columns = [
        'id', 'title', 'text', 'great', 'comments_num', 'post_url',
        'tag_1', 'tag_2', 'tag_3', 'tag_4', 'tag_5',
        'tag_6', 'tag_7', 'tag_8', 'tag_9', 'tag_10',
        'comment_1', 'comment_2', 'comment_3', 'comment_4', 'comment_5',
        'comment_6', 'comment_7', 'comment_8', 'comment_9', 'comment_10',
        'comment_11', 'comment_12', 'comment_13', 'comment_14', 'comment_15',
        'comment_16', 'comment_17', 'comment_18', 'comment_19', 'comment_20',
        'pic_url_1', 'pic_url_2', 'pic_url_3'
    ]

    try:
        # 执行查询
        cursor.execute(f"SELECT {', '.join(columns)} FROM posts")
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

        # 城市筛选
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