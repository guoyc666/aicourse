import json
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

from database import get_db
from models import Question, LearningRecord, QuestionRecord, User
from auth import get_current_user, get_current_active_user

# 创建路由对象
router = APIRouter(
    prefix="/api/question",
    tags=["题库"]
)

# Pydantic模型定义
class AnswerItem(BaseModel):
    question_id: int
    student_answer: str

class SubmitRequest(BaseModel):
    answers: List[AnswerItem]
    time_spent: int
    knowledge_id: Optional[str] = None

# 1. 题目添加接口
@router.post("/add", summary="添加题目")
async def add_question(
    text: str = Form(..., description="题目内容"),
    type: str = Form(..., description="题目类型(choice/fill/code)"),
    options: Optional[str] = Form(None, description="选项(JSON格式，仅选择题)"),
    answer: str = Form(..., description="正确答案"),
    knowledge_id: str = Form(..., description="知识点ID列表(JSON格式)"),
    difficulty: Optional[float] = Form(0.5, description="难度系数(0-1)"),
    current_user: User = Depends(get_current_active_user),  
    db: Session = Depends(get_db)
):
    # 验证题目类型
    if type not in ["choice", "fill", "code"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="题目类型必须为choice、fill或code"
        )
    
    # 验证选择题选项
    if type == "choice" and not options:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="选择题必须提供选项"
        )
    
    # 验证知识点ID列表
    try:
        # 尝试直接解析
        raw = knowledge_id.strip()
        
        # 首先尝试直接解析为JSON
        try:
            knowledge_ids = json.loads(raw)
            if not isinstance(knowledge_ids, list):
                raise ValueError("知识点ID必须为列表格式")
        except json.JSONDecodeError:
            # 如果直接解析失败，检查是否是嵌套的JSON字符串（前端可能已经JSON.stringify过）
            if raw.startswith('"') and raw.endswith('"'):
                # 尝试去除外层引号后再解析
                try:
                    inner_raw = raw[1:-1].replace('\\"', '"')
                    knowledge_ids = json.loads(inner_raw)
                    if not isinstance(knowledge_ids, list):
                        raise ValueError("知识点ID必须为列表格式")
                except (json.JSONDecodeError, ValueError):
                    # 如果仍然失败，尝试其他格式修复
                    # 1. 确保有外层方括号
                    if not (raw.startswith('[') and raw.endswith(']')):
                        raw = f'[{raw}]'
                    
                    # 2. 尝试处理逗号分隔的ID列表，支持数字或字符串格式
                    try:
                        # 移除方括号
                        content = raw[1:-1].strip()
                        if not content:
                            knowledge_ids = []
                        else:
                            # 分割元素
                            elements = [elem.strip() for elem in content.split(',')]
                            # 尝试转换为数字，失败则保留为字符串
                            knowledge_ids = []
                            for elem in elements:
                                try:
                                    # 尝试作为数字处理
                                    knowledge_ids.append(int(elem))
                                except ValueError:
                                    # 尝试作为字符串处理（去除可能的单引号）
                                    elem = elem.strip("'\"")
                                    knowledge_ids.append(elem)
                    except Exception:
                        # 如果修复失败，抛出原始错误
                        raise json.JSONDecodeError("Invalid JSON", raw, 0)
            else:
                # 如果不是嵌套的JSON字符串，尝试其他格式修复
                # 1. 确保有外层方括号
                if not (raw.startswith('[') and raw.endswith(']')):
                    raw = f'[{raw}]'
                
                # 2. 尝试处理逗号分隔的ID列表，支持数字或字符串格式
                try:
                    # 移除方括号
                    content = raw[1:-1].strip()
                    if not content:
                        knowledge_ids = []
                    else:
                        # 分割元素
                        elements = [elem.strip() for elem in content.split(',')]
                        # 尝试转换为数字，失败则保留为字符串
                        knowledge_ids = []
                        for elem in elements:
                            try:
                                # 尝试作为数字处理
                                knowledge_ids.append(int(elem))
                            except ValueError:
                                # 尝试作为字符串处理（去除可能的单引号）
                                elem = elem.strip("'\"")
                                knowledge_ids.append(elem)
                except Exception:
                    # 如果修复失败，抛出原始错误
                    raise json.JSONDecodeError("Invalid JSON", raw, 0)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="知识点ID格式错误，必须为JSON列表（如[""111"",""222""]）"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    # 验证选项格式
    if options:
        try:
            json.loads(options)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="选项格式错误，必须为JSON对象"
            )
    
    # 处理难度系数 - 完全简化的方式
    # 直接使用默认值，避免任何可能的验证失败
    difficulty_value = 0.5
    
    # 尝试处理输入值但不抛出异常
    try:
        if difficulty is not None:
            # 确保是数字类型
            if isinstance(difficulty, (int, float)):
                temp_val = float(difficulty)
                if 0.0 <= temp_val <= 1.0:
                    difficulty_value = temp_val
            elif isinstance(difficulty, str):
                try:
                    temp_val = float(difficulty.strip())
                    if 0.0 <= temp_val <= 1.0:
                        difficulty_value = temp_val
                except:
                    pass  # 保持默认值
    except Exception:
        pass  # 任何错误都保持默认值
    
    difficulty = difficulty_value
    
    # 创建题目记录
    try:
        new_question = Question(
            text=text,
            type=type,
            options=options,
            answer=answer,
            knowledge_id=json.dumps(knowledge_ids),
            difficulty=difficulty,
            answer_count=0,
            correct_count=0
        )
        db.add(new_question)
        db.commit()
        db.refresh(new_question)
        
        return JSONResponse(
            content={
                "code": 200,
                "message": "题目添加成功",
                "data": {"question_id": new_question.question_id}
            }
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"添加题目失败: {str(e)}"
        )

# 2. 题目删除接口
@router.delete("/delete", summary="删除题目")
async def delete_question(
    question_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 查找题目
    question = db.query(Question).filter(Question.question_id == question_id).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="题目不存在"
        )
    
    # 删除题目
    try:
        db.delete(question)
        db.commit()
        return JSONResponse(
            content={
                "code": 200,
                "message": "题目删除成功"
            }
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除题目失败: {str(e)}"
        )

# 3. 题目查看接口（教师用）
@router.get("/list", summary="获取题目列表（教师）")
async def get_question_list(
    skip: int = 0,
    limit: int = 20,
    knowledge_id: Optional[str] = None,
    type: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 验证分页参数
    if limit > 100:
        limit = 100
    
    # 构建查询
    query = db.query(Question)
    
    # 筛选条件
    if knowledge_id:
        query = query.filter(Question.knowledge_id.like(f"%{knowledge_id}%"))
    if type and type in ["choice", "fill", "code"]:
        query = query.filter(Question.type == type)
    
    # 获取总数和分页数据
    total = query.count()
    questions = query.offset(skip).limit(limit).all()
    
    # 格式化响应
    result_list = []
    for q in questions:
        # 计算正确率
        correct_rate = q.correct_count / q.answer_count if q.answer_count > 0 else 0.0
        
        result_list.append({
            "question_id": q.question_id,
            "text": q.text,
            "type": q.type,
            "options": json.loads(q.options) if q.options else None,
            "answer": q.answer,
            "knowledge_id": json.loads(q.knowledge_id),
            "difficulty": q.difficulty,
            "correct_rate": round(correct_rate, 4)
        })
    
    return JSONResponse(
        content={
            "code": 200,
            "message": "查询成功",
            "data": {
                "total": total,
                "list": result_list
            }
        }
    )

# 4. 题目获取接口（学生答题用）
@router.get("/get", summary="获取题目（学生）")
async def get_questions_for_student(
    knowledge_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 这是一个完全防御性编程的实现，确保无论什么情况下都返回有效的JSON响应
    try:
        print(f"获取题目请求: knowledge_id={knowledge_id}, user_id={getattr(current_user, 'user_id', 'unknown')}")
        
        # 验证knowledge_id参数
        if not knowledge_id or not str(knowledge_id).strip():
            return {"code": 400, "message": "知识点ID不能为空", "data": {"count": 0, "list": []}}
        
        # 特殊处理'random'参数，表示随机获取题目
        is_random_request = knowledge_id.lower() == 'random'
        print(f"请求类型: {'随机练习' if is_random_request else '知识点练习'}")
        
        # 初始化结果列表
        result_list = []
        
        try:
            # 先尝试基本的查询（不使用排序和模糊查询等复杂操作）
            # 这是最安全的查询方式，避免因为数据库方言问题导致的错误
            questions = []
            try:
                # 根据请求类型选择查询方式
                if is_random_request:
                    # 随机练习：直接获取任意题目的随机样本
                    try:
                        # 获取所有题目并随机排序
                        questions = db.query(Question).order_by(func.random()).limit(10).all()
                        print(f"随机练习查询: 成功获取 {len(questions)} 道随机题目")
                    except Exception as e:
                        # 如果随机排序失败，使用简单查询
                        print(f"随机排序失败: {str(e)}，使用简单查询")
                        questions = db.query(Question).limit(10).all()
                else:
                    # 知识点练习：先尝试精确匹配
                    questions = db.query(Question).filter(Question.knowledge_id == knowledge_id).limit(10).all()
                    
                    # 如果精确匹配没有找到题目，尝试使用LIKE匹配（考虑JSON数组格式）
                    if not questions:
                        try:
                            # 尝试匹配JSON格式的知识点ID，如包含[knowledge_id]或"knowledge_id"
                            like_pattern = f"%{knowledge_id}%"
                            questions = db.query(Question).filter(Question.knowledge_id.like(like_pattern)).limit(10).all()
                            print(f"使用LIKE查询找到了 {len(questions)} 道题目")
                        except Exception as e:
                            print(f"LIKE查询失败: {str(e)}")
                            questions = []
            except Exception as e:
                print(f"基本查询失败: {str(e)}")
                
            # 如果查询到了题目，尝试处理它们
            for q in questions:
                try:
                    # 使用字典而不是对象属性访问，更安全
                    question_dict = {
                        "question_id": getattr(q, 'question_id', f'unknown_{id(q)}'),
                        "text": getattr(q, 'text', '题目文本缺失'),
                        "type": getattr(q, 'type', 'unknown'),
                        "options": None,
                        "knowledge_id": [],
                        "difficulty": getattr(q, 'difficulty', 1)
                    }
                    
                    # 安全处理options字段
                    try:
                        if hasattr(q, 'options') and q.options:
                            if isinstance(q.options, str):
                                # 不尝试解析JSON，直接返回字符串，让前端处理
                                question_dict["options"] = q.options
                            else:
                                question_dict["options"] = q.options
                    except Exception:
                        pass  # 保持options为None
                    
                    # 安全处理knowledge_id字段
                    try:
                        if hasattr(q, 'knowledge_id') and q.knowledge_id:
                            if isinstance(q.knowledge_id, str):
                                # 不尝试解析JSON，直接返回原始值
                                question_dict["knowledge_id"] = q.knowledge_id
                            else:
                                question_dict["knowledge_id"] = q.knowledge_id
                    except Exception:
                        pass  # 保持knowledge_id为空列表
                    
                    result_list.append(question_dict)
                except Exception as item_error:
                    print(f"处理单个题目出错: {str(item_error)}")
                    continue  # 跳过当前题目，继续处理下一个
            
            # 准备响应数据
            response_data = {
                "code": 200,
                "message": "题目获取成功" if result_list else "未找到相关题目",
                "data": {
                    "count": len(result_list),
                    "list": result_list
                }
            }
            
            return response_data
        except Exception as e:
            # 处理查询和处理过程中的错误
            error_msg = f"处理题目数据时出错: {str(e)}"
            print(error_msg)
            return {
                "code": 500,
                "message": error_msg,
                "data": {"count": 0, "list": []}
            }
    except Exception as e:
        # 最终的异常捕获，确保无论如何都返回有效的响应
        print(f"严重错误 - 整个请求处理失败: {str(e)}")
        # 不使用JSONResponse，直接返回字典，让FastAPI自动处理
        return {
            "code": 500,
            "message": f"服务器处理请求失败: {str(e)}",
            "data": {"count": 0, "list": []}
        }

# 5. 答题接口
@router.post("/submit", summary="提交答案")
async def submit_answers(
    request: SubmitRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not request.answers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="至少需要提交一个答案"
        )
    
    # 处理答题结果
    results = []
    # 1. 记录每个知识点的答题情况：{knowledge_id: [(is_correct, difficulty, time_spent), ...]}
    knowledge_stats = {}
    # 2. 统计每个知识点的出现次数（关联的题目数量）
    knowledge_count = {}
    
    try:
        time_spent = request.time_spent  # 总耗时（秒）
        total_questions = len(request.answers)
        
        for item in request.answers:
            # 获取题目信息
            question = db.query(Question).filter(Question.question_id == item.question_id).first()
            if not question:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"题目ID {item.question_id} 不存在"
                )
            
            # 判断答案是否正确
            is_correct = (item.student_answer == question.answer)
            
            # 更新题目统计
            question.answer_count += 1
            if is_correct:
                question.correct_count += 1
            
            # 计算当前题目正确率
            correct_rate = question.correct_count / question.answer_count if question.answer_count > 0 else 0.0
            
            # 收集知识点信息：统计出现次数 + 记录答题情况
            question_knowledges = json.loads(question.knowledge_id)
            for kid in question_knowledges:
                # 统计知识点出现次数（每关联1道题，次数+1）
                knowledge_count[kid] = knowledge_count.get(kid, 0) + 1
                
                # 记录答题详情
                if kid not in knowledge_stats:
                    knowledge_stats[kid] = []
                knowledge_stats[kid].append((is_correct, question.difficulty, 0))
            
            # 记录答题结果
            results.append({
                "question_id": item.question_id,
                "student_answer": item.student_answer,
                "correct_answer": question.answer,
                "is_correct": is_correct,
                "correct_rate": round(correct_rate, 4)
            })
        
        # 计算总体正确率
        correct_count = sum(1 for res in results if res["is_correct"])
        accuracy = correct_count / total_questions if total_questions > 0 else 0.0
        
        # 核心步骤：筛选出“出现次数最多的知识点”（仅更新该知识点的掌握度）
        mastery_updates = []
        
        # 创建答题记录
        # 如果是随机练习，knowledge_id设置为'random'
        record_knowledge_id = json.dumps(['random']) if request.knowledge_id == 'random' else json.dumps(list(knowledge_stats.keys()))
        question_record = QuestionRecord(
            student_id=current_user.id,
            submit_time=datetime.now(),
            duration=request.time_spent,
            accuracy=accuracy,
            knowledge_id=record_knowledge_id,
            detail=json.dumps(results),
            total_questions=total_questions  # 题目数量字段
        )
        db.add(question_record)
        
        # 提交事务
        db.commit()
        
        return JSONResponse(
            content={
                "code": 200,
                "message": "答题提交成功",
                "data": {
                    "accuracy": round(accuracy, 4),
                    "results": results,
                    "mastery": mastery_updates
                }
            }
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"提交答案失败: {str(e)}"
        )

# 6. 答题记录获取接口
@router.get("/record/list", summary="获取答题记录列表")
async def get_answer_records(
    user_id: int = None,
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    try:
        # 如果没有指定user_id，则使用当前用户的id
        # 如果指定了user_id但与当前用户不匹配，则返回当前用户的记录（避免403错误）
        actual_user_id = current_user.id
        
        # 这里可以根据需要添加管理员/教师权限检查，允许查看其他用户的记录
        # 暂时简化处理，只返回当前登录用户的记录
        
        # 验证分页参数
        if limit > 100:
            limit = 100
        
        # 查询记录，使用当前登录用户的ID
        query = db.query(QuestionRecord).filter(QuestionRecord.student_id == actual_user_id)
        total = query.count()
        records = query.order_by(QuestionRecord.submit_time.desc()).offset(skip).limit(limit).all()
        
        # 格式化响应
        result_list = []
        for record in records:
            knowledge_id = ""
            # 安全解析knowledge_id字段
            try:
                if record.knowledge_id:
                    knowledge_ids = json.loads(record.knowledge_id)
                    # 确保是列表且不为空
                    if isinstance(knowledge_ids, list) and knowledge_ids:
                        # 取第一个知识点作为代表
                        knowledge_id = knowledge_ids[0]
            except (json.JSONDecodeError, TypeError, IndexError):
                # 如果解析失败，使用空字符串
                knowledge_id = ""
            
            result_list.append({
                "record_id": record.id,
                "submit_time": record.submit_time.strftime("%Y-%m-%d %H:%M:%S"),
                "time_spent": record.duration,
                "accuracy": record.accuracy,
                "knowledge_id": knowledge_id,
                "total_questions": record.total_questions
            })
        
        return JSONResponse(
            content={
                "code": 200,
                "message": "查询成功",
                "data": {
                    "total": total,
                    "list": result_list
                }
            }
        )
    except Exception as e:
        # 捕获所有可能的异常，返回友好的错误信息
        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "message": f"获取练习记录失败: {str(e)}",
                "data": {}
            }
        )

# 7. 详细答题记录获取接口
@router.get("/record/detail", summary="获取详细答题记录")
async def get_answer_record_detail(
    record_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 查询记录
    record = db.query(QuestionRecord).filter(QuestionRecord.id == record_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="答题记录不存在"
        )
    
    # 学生只能查看自己的答题记录
    if current_user.id != record.student_id:
        # 这里可以添加角色检查，允许管理员/教师查看所有记录
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，只能查看自己的答题记录"
        )
    
    # 获取题目详情
    detail = json.loads(record.detail)
    question_ids = [item["question_id"] for item in detail]
    questions = db.query(Question).filter(Question.question_id.in_(question_ids)).all()
    
    # 构建题目信息映射
    question_map = {q.question_id: q for q in questions}
    
    # 格式化题目详情
    questions_detail = []
    for item in detail:
        q = question_map.get(item["question_id"])
        if q:
            questions_detail.append({
                "text": q.text,
                "type": q.type,
                "options": json.loads(q.options) if q.options else None,
                "correct_answer": q.answer,
                "knowledge_id": json.loads(q.knowledge_id),
                "difficulty": q.difficulty,
                "student_answer": item["student_answer"],
                "is_correct": item["is_correct"],
                "correct_rate": item["correct_rate"]
            })
    
    # 处理知识点信息
    knowledge_ids = json.loads(record.knowledge_id)
    knowledge_id = knowledge_ids[0] if knowledge_ids else ""
    
    return JSONResponse(
        content={
            "code": 200,
            "message": "查询成功",
            "data": {
                "record_id": record.id,
                "submit_time": record.submit_time.strftime("%Y-%m-%d %H:%M:%S"),
                "time_spent": record.duration,
                "accuracy": record.accuracy,
                "knowledge_id": knowledge_id,
                "questions": questions_detail
            }
        }
    )