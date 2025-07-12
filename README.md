# Summer-Project
## 快速启动

1. 打开 Codespaces（或本地）
2. 安装依赖：
   ```bash
   pip install --no-cache-dir -r requirements.txt
3. 启动服务：
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
4. 在浏览器访问：
文档： http://localhost:8000/docs
推荐： GET  /attractions?destination=北京&days=2&preferences=文化,美食
详情： GET  /attractions/{id}
行程： POST /itinerary (JSON body)

## 协作开发
1. Fork 或 Clone 仓库
2. 点击 **Code → Open with Codespaces**
3. 等待容器启动并安装依赖
4. 运行 Uvicorn 并联调前端，即可开始协作开发

## 后端接口
| 方法   | 路径                                         | 参数示例／位置                                                                             | 功能说明             | 返回模型                               |                  |
| ---- | ------------------------------------------ | ----------------------------------------------------------------------------------- | ---------------- | ---------------------------------- | ---------------- |
| GET  | `/`                                        | —                                                                                   | 健康检查，返回服务状态      | `{ status, message }`              |                  |
| POST  | `/attractions`                             |` { "destination": "北京", "days": 4, "preferences": ["文化", "历史"]}    `              | 搜索/推荐景点列表        |`List<{id,name,images,tags}>`                |                  |
| GET  | `/attractions/{id}`                        | `id`（Path）                                                                          | 单个景点详情，含优缺点与来源链接 | `Attraction`                       |                  |
| POST | `/itinerary`  (这个暂时没用)                             |`{ "destination": "北京", "days": 4, "preferences": ["文化", "历史"]} `  | 基于选中景点生成行程草稿     | `List<{id,name,images,tags}>` |                  |
| POST | /llm-itinerary | { "destination": "北京", "days": 4, "preferences": ["文化", "历史", "步行友好"], "must_visit": ["故宫"], "must_not_visit": ["长城", "王府井"] }（JSON Body） | 调用大模型 API 生成行程草稿 | { "itinerary": List<{ day, work_flow: [{ name, transport, time_spent, id, images }] }> } | |
| POST | `/users`                                   | `{ "username": "xxx", "password": "yyy" }`<br>（JSON Body）                            | 用户注册             | `User`                             |                  |
| POST | `/login`                                   | `{ "username": "xxx", "password": "yyy" }`<br>（JSON Body）                            | 用户登录             | `User`                             |                  |
| GET  | `/users/{user_id}`                         | `user_id`（Path）                                                                     | 获取用户资料           | `User`                             |                  |
| POST | `/posts`                                   | `{ user_id:"uid", content:"文字", images:["url1","url2"] }`<br>（JSON Body）            | 创建一条用户帖子         | `Post`                             |                  |
| GET  | `/posts`                                   | —                                                                                   | 拉取所有用户帖子列表       | `List<Post>`                       |                  |
| POST | `/posts/{post_id}/comments`                | `{ user_id:"uid", content:"评论内容" }`<br>（JSON Body），`post_id`（Path）                  | 在某贴下添加评论         | `Comment`                          |                  |
| GET  | `/posts/{post_id}/comments`                | `post_id`（Path）                                                                     | 获取某贴的所有评论        | `List<Comment>`                    |                  |
| POST | `/posts/{post_id}/like`                    | `?user_id=uid`<br>（Query） 或 JSON Body                                               | 对帖子点赞／取消点赞       | \`{ result: "added"                | "deleted" }\`    |
| GET  | `/posts/{post_id}/likes`                   | `post_id`（Path）                                                                     | 查询某贴的点赞总数        | `{ count: number }`                |                  |
| POST | `/users/{user_id}/follow/{target_user_id}` | `user_id`、`target_user_id`（Path）                                                    | 关注／取关某用户         | \`{ result: "followed"             | "unfollowed" }\` |
<<<<<<< Updated upstream
| POST | `/users/{user_id}/itineraries`             | `{ selected_ids: [...], days:2, preferences:[...] }`<br>（JSON Body），`user_id`（Path） | 保存当前行程到"我的行程"    | `ItineraryRecord`                  |                  |
=======
| POST  | `/upload_itinerary`                             | `{ "itinerary": List<{ day, work_flow: [{ name, id, images }] }> }  `               | 上传行程数据并获取更新后的数据         |`{ "itinerary": List<{ day, work_flow: [{ name,transport，time_spent,id, images }] }> }`                |                  |
| POST | `/users/{user_id}/itineraries`             | `{ selected_ids: [...], days:2, preferences:[...] }`<br>（JSON Body），`user_id`（Path） | 保存当前行程到“我的行程”    | `ItineraryRecord`                  |                  |
>>>>>>> Stashed changes
| GET  | `/users/{user_id}/itineraries`             | `user_id`（Path）                                                                     | 拉取某用户所有保存的行程     | `List<ItineraryRecord>`            |                  |

---

**字段说明：**

* **Attraction**：`{ id, name, description, lat, lon, tags[], images[], address, pros[], cons[], source_posts[] }`
* **User**：`{ id, username, password, avatar?, bio }`
* **Post**：`{ id, user_id, content, images[], created_at }`
* **Comment**：`{ id, post_id, user_id, content, created_at }`
* **ItineraryRecord**：`{ id, user_id, title?, selected_ids[], days, preferences[], itinerary[], created_at }`

* 搜索页/推荐页：`GET /attractions`
* 详情页：`GET /attractions/{id}`
* 滑卡推荐：`POST /itinerary`
* 大模型API推荐：`POST /llm-itinerary`
* 用户社交：`/users`、`/posts`、`/comments`、`/like`、`/follow`
* 我的行程：`/users/{user_id}/itineraries`、`/users/{user_id}/llm-itineraries`

确保在小程序或网页端，按上表填写正确的 Path、Query 或 JSON Body，就能获得相应的 JSON 数据并渲染 UI。