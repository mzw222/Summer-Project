# backend_local/scripts/import_data.py

import os
import sys
import json
import uuid
import datetime
import pandas as pd

# 将项目根目录（backend_local）加入 sys.path，确保可以导入 app 模块
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(current_dir, "..")))

from app.db import SessionLocal, Base, engine
from app.models_orm import AttractionORM, PostORM, CommentORM

# 确保所有表已创建
Base.metadata.create_all(bind=engine)


def import_attractions(csv_path: str):
    df = pd.read_excel(csv_path, dtype=str)
    df['评论数']=df['评论数'].fillna(0)
    db = SessionLocal()
    for _, row in df.iterrows():
        orm = AttractionORM(
            id=row.get("景区id"),
            city=row.get("城市",''),
            url=row.get("链接",''),
            area_name=row.get('区域名称',''),
            attraction_name= row.get('景区名称',''),
            comment_score= float(row.get('景区评论得分',0)),
            star        = row.get('星级',''),
            pic_pre     = row.get('景区展示图片',''),
            price       = float(row.get('景区门票价格',0)),
            free        = row.get('景区是否免费',''),
            character   = row.get('景区特点描述',''),
            lat         = float(row.get('景区纬度',0)),
            lon         = float(row.get('景区经度',0)),
            hot         = float(row.get('景区热度',0)),
            address     = row.get('景区地址',''),
            tags_ai     = row.get('tags',''),
            advantage_1 = row.get('优点汇总1',''),
            advantage_2 = row.get('优点汇总2',''),
            advantage_3 = row.get('优点汇总3',''),
            disadvantage_1 = row.get('缺点汇总1',''),
            disadvantage_2 = row.get('缺点汇总2',''),
            disadvantage_3 = row.get('缺点汇总3',''),
            comment_number = int(row.get('评论数',0))
        )
        db.merge(orm)
    db.commit()
    db.close()
    print("✅ Attractions imported.")


def import_xhs_posts(xlsx_path: str):
    df = pd.read_excel(xlsx_path).fillna("")
    db = SessionLocal()
    for _, row in df.iterrows():
        pid = str(uuid.uuid4())
        orm = PostORM(
            id=pid,
            user_id=row.get("用户ID", ""),
            content=row.get("内容", ""),
            images=json.dumps(row.get("图片URLs", "").split(","), ensure_ascii=False),
            created_at=datetime.datetime.utcnow()
        )
        db.add(orm)
    db.commit()
    db.close()
    print("✅ 小红书帖子导入完成。")


def import_ctrip_comments(xlsx_path: str):
    df = pd.read_excel(xlsx_path).fillna("")
    db = SessionLocal()
    for _, row in df.iterrows():
        cid = str(uuid.uuid4())
        orm = CommentORM(
            id=cid,
            attraction_id=row.get("关联PostID", ""),
            user_id=row.get("评论用户ID", ""),
            content1=row.get("评论内容", ""),
            created_at=datetime.datetime.utcnow()
        )
        db.add(orm)
    db.commit()
    db.close()
    print("✅ 携程评论导入完成。")


if __name__ == "__main__":
    base = os.path.abspath(os.path.join(current_dir, "..", "data"))
    import_attractions(os.path.join(base, "D:/desktop/项目/code/Summer-Project-3/project_v3/data/北京景点数据.xlsx"))
    import_xhs_posts(os.path.join(base, "xiaohongshu_posts.xlsx"))
    import_ctrip_comments(os.path.join(base, "ctrip_comments.xlsx"))
    print("✅ 数据导入完成。")
