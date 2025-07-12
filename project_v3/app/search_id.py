# app/search_id.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from .models_orm import AttractionORM  # 导入SQLAlchemy模型

def search_id_in_db(db: Session, query: str, fuzzy: bool = False):
    try:
        if fuzzy:
            # 模糊匹配
            query_expr = AttractionORM.id.ilike(f'%{query}%')
        else:
            # 精确匹配
            query_expr = AttractionORM.id == query
            
        results = db.query(AttractionORM).filter(query_expr).all()
        
        # 将ORM对象转换为字典列表
        return [
            {
                'id': attraction.id,
                'city': attraction.city,
                'url': attraction.url,
                'area_name': attraction.area_name,
                'attraction_name': attraction.attraction_name,
                'comment_score': attraction.comment_score,
                'star': attraction.star,
                'pic_pre': attraction.pic_pre,
                'price': attraction.price,
                'free': attraction.free,
                'character': attraction.character,
                'lat': attraction.lat,
                'lon': attraction.lon,
                'hot': attraction.hot,
                'address': attraction.address,
                'tags_ai': attraction.tags_ai,
                'advantage_1': attraction.advantage_1,
                'advantage_2': attraction.advantage_2,
                'advantage_3': attraction.advantage_3,
                'disadvantage_1': attraction.disadvantage_1,
                'disadvantage_2': attraction.disadvantage_2,
                'disadvantage_3': attraction.disadvantage_3,
                'comment_number': attraction.comment_number  # 注意字段名匹配
            }
            for attraction in results
        ]
        
    except Exception as e:
        import traceback
        print(f"数据库查询错误: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"查询数据库时出错: {str(e)}")