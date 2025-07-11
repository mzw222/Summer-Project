import appbuilder
import os
import re
import json
from .models import LLMIteraryRequest, LLMIteraryResponse, ItineraryStep 
from .db import SessionLocal  
from .models_orm import AttractionORM 

# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = 'Bearer bce-v3/ALTAK-acJ0DM86Ly28qeK89yA74/f5ec5af120f5d8efc28948e54314b33205595368'
app_id = 'f7424d75-3523-454c-87af-d50f455729c6'

# 初始化智能体
builder = appbuilder.AppBuilderClient(app_id)

def extract_json_from_text(text):
    """从文本中提取JSON内容"""
    # 定义JSON可能的开始和结束标记
    json_start = None
    json_end = None

    # 查找JSON数组或对象的开始标记
    array_start = text.find('[')
    object_start = text.find('{')

    # 确定实际的开始位置
    if array_start >= 0 and (array_start < object_start or object_start < 0):
        json_start = array_start
    elif object_start >= 0:
        json_start = object_start

    if json_start is None:
        return None

    # 查找对应的结束标记
    brace_count = 0
    bracket_count = 0
    in_quote = False
    escape_char = False

    for i in range(json_start, len(text)):
        char = text[i]

        # 处理转义字符
        if char == '\\' and not escape_char:
            escape_char = True
            continue
        else:
            escape_char = False

        # 处理引号
        if char == '"' and not escape_char:
            in_quote = not in_quote
            continue

        # 如果在引号内，忽略括号
        if in_quote:
            continue

        # 计算括号数量
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
        elif char == '[':
            bracket_count += 1
        elif char == ']':
            bracket_count -= 1

        # 检查是否找到匹配的结束标记
        if (json_start == object_start and brace_count == 0) or \
                (json_start == array_start and bracket_count == 0):
            json_end = i
            break

    if json_end is not None:
        return text[json_start:json_end + 1]
    return None

def fix_json_format(json_str):
    """修复JSON格式问题"""
    # 修复URL格式
    json_str = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'"\1：\2"', json_str)

    # 尝试解析并验证
    try:
        json_obj = json.loads(json_str)
        return json.dumps(json_obj, ensure_ascii=False, indent=2)
    except json.JSONDecodeError as e:
        print(f"JSON格式修复失败: {e}")
        return json_str

def get_attraction_info(name):
    """从数据库中获取景点的id和图片信息"""
    db = SessionLocal()
    try:
        # 使用 like 方法进行模糊查询
        attractions = db.query(AttractionORM).filter(AttractionORM.attraction_name.like(f"%{name}%")).all()
        if attractions:
            # 选择第一个匹配的景点
            attraction = attractions[0]
            attraction_id = attraction.id
            image = attraction.pic_pre
            actual_name = attraction.attraction_name  # 获取实际的景点名称
            return attraction_id, image, actual_name
        return None, None, None
    except Exception as e:
        print(f"Error querying database for attraction {name}: {e}")
        return None, None, None
    finally:
        db.close()

def generate_llm_itinerary(req: LLMIteraryRequest):
    # 构建请求文本
    request_text = f"我要去{req.目的地}旅游{req.天数}天，必去的景点有{','.join(req.必去的景点)}，必不去的景点有{','.join(req.必不去的景点)}，偏好是{','.join(req.preferences)}，给个攻略"
    # 创建会话
    conversation_id = builder.create_conversation()
    # 运行对话
    out = builder.run(conversation_id, request_text)
    answer = out.content.answer
    # 提取回答中的JSON内容
    json_content = extract_json_from_text(answer)
    if json_content:
        fixed_json = fix_json_format(json_content)
        try:
            itinerary = json.loads(fixed_json)
            # 处理字段名和 time_spent 字段
            for day in itinerary:
                if 'work_flow' in day:
                    new_work_flow = []
                    for step in day['work_flow']:
                        time_spent = step.get('time_spent')
                        if time_spent is None:
                            time_spent = "未指定" 
                        name = step.get('name')
                        print(f"Searching for attraction: {name}")  # 添加日志检查 name 字段
                        attraction_id, image, actual_name = get_attraction_info(name)
                        if actual_name:
                            name = actual_name  # 使用实际的景点名称
                        new_step = ItineraryStep(
                            name=name,
                            transport=step.get('transport'),
                            time_spent=time_spent
                        )
                        step_dict = new_step.dict()
                        step_dict['id'] = attraction_id if attraction_id else ""
                        step_dict['images'] = image if image else ""
                        new_work_flow.append(step_dict)
                    day['work_flow'] = new_work_flow
            return LLMIteraryResponse(itinerary=itinerary)
        except json.JSONDecodeError:
            return None
    return None