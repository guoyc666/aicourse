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
from models import Question, LearningRecord, QuestionRecord, User, QuestionType, CodeLanguage
from utils.auth import get_current_user, get_current_active_user, check_role

# 创建路由对象
router = APIRouter()

# 代码执行辅助类
class CodeExecutor:
    """编程题代码执行器，支持多语言"""
    
    @staticmethod
    def _execute_python_code(user_code: str, examples: List[Dict[str, Any]]) -> tuple[bool, Optional[str]]:
        """执行Python代码"""
        try:
            # 在受限环境中执行学生代码
            # 约定学生代码中需要实现一个名为 solve(input_str: str) -> str 的函数
            local_env: Dict[str, Any] = {}
            global_env = {
                "__builtins__": {
                    "range": range,
                    "len": len,
                    "print": print,
                    "str": str,
                    "int": int,
                    "float": float,
                    "list": list,
                    "dict": dict,
                    "max": max,
                    "min": min,
                    "sum": sum,
                    "abs": abs,
                    "sorted": sorted,
                    "enumerate": enumerate,
                    "zip": zip
                },
                "__name__": "__main__"
            }
            exec(user_code, global_env, local_env)
            
            solve_func = local_env.get("solve") or global_env.get("solve")
            if not callable(solve_func):
                return False, "未找到 solve(input_str: str) 函数"
            
            # 测试所有用例
            for ex in examples:
                ex_input = str(ex.get("input", ""))
                expected_output = str(ex.get("output", ""))
                try:
                    result = solve_func(ex_input)
                    if result is None:
                        result_str = ""
                    else:
                        result_str = str(result)
                except Exception as e:
                    return False, f"运行测试用例时出错: {str(e)}"
                
                if result_str != expected_output:
                    return False, f"测试用例失败：输入'{ex_input}'，期望输出'{expected_output}'，实际输出'{result_str}'"
            
            return True, None
            
        except Exception as e:
            return False, f"代码执行错误: {str(e)}"
    
    @staticmethod
    def _execute_c_code(user_code: str, examples: List[Dict[str, Any]]) -> tuple[bool, Optional[str]]:
        """执行C代码"""
        import subprocess
        import tempfile
        import os
        import sys
        
        def find_gcc():
            """自动寻找GCC编译器"""
            import subprocess
            
            # 先尝试在PATH中查找
            try:
                result = subprocess.run(['where', 'gcc'], capture_output=True, text=True)
                if result.returncode == 0 and result.stdout.strip():
                    return result.stdout.strip().split('\n')[0]
            except:
                pass
            
            # 常见的GCC安装路径
            common_paths = [
                'E:/msys64/mingw64/bin/x86_64-w64-mingw32-gcc.exe',
                'E:/msys64/mingw32/bin/gcc.exe',
                'C:/mingw64/bin/x86_64-w64-mingw32-gcc.exe',
                'C:/mingw/bin/gcc.exe',
                'C:/TDM-GCC-64/bin/gcc.exe',
                'C:/Program Files/mingw-w64/x86_64-8.1.0-posix-seh-rt_v6-rev0/bin/gcc.exe',
                '/usr/bin/gcc',  # WSL
                '/usr/local/bin/gcc',  # macOS/Linux
            ]
            
            # 检查每个路径是否存在
            for path in common_paths:
                if os.path.exists(path):
                    return path
                    
            return None
        
        try:
            # 自动寻找GCC编译器
            gcc_path = find_gcc()
            if not gcc_path:
                return False, "未找到C编译器，请安装GCC或将其路径添加到系统PATH中"
            
            # 检查用户代码是否包含main函数
            if "int main(" in user_code or "void main(" in user_code:
                # 如果用户代码包含main函数，修改为test_main避免冲突
                modified_user_code = user_code.replace("int main(", "int test_main(").replace("void main(", "void test_main(")
            else:
                modified_user_code = user_code
            
            # 包装用户代码，使其能够调用solve函数
            wrapper_code = f'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 用户代码
{modified_user_code}

// 测试主函数
int main() {{
    char input[1000];
    
    // 从标准输入读取测试用例
    if (fgets(input, sizeof(input), stdin)) {{
        // 去除换行符
        input[strcspn(input, "\\r\\n")] = 0;
        
        // 调用solve函数
        char* result = solve(input);
        
        if (result != NULL) {{
            printf("%s", result);
            free(result);
        }} else {{
            printf("");
        }}
    }}
    
    return 0;
}}
'''
            
            # 创建临时C文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False, encoding='utf-8') as f:
                f.write(wrapper_code)
                c_file = f.name
            
            # 编译C代码
            exe_file = c_file.replace('.c', '.exe')
            compile_cmd = [gcc_path, c_file, '-o', exe_file]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=30)
            
            if compile_result.returncode != 0:
                return False, f"C代码编译失败: {compile_result.stderr}"
            
            # 测试所有用例
            for ex in examples:
                input_data = str(ex.get("input", ""))
                expected_output = str(ex.get("output", ""))
                
                try:
                    run_result = subprocess.run([exe_file], 
                                              input=input_data, 
                                              capture_output=True, 
                                              text=True, 
                                              timeout=10)
                    actual_output = run_result.stdout.strip()
                except subprocess.TimeoutExpired:
                    return False, f"C代码执行超时：输入'{input_data}'"
                except Exception as e:
                    return False, f"C代码执行错误：输入'{input_data}', 错误: {str(e)}"
                
                if actual_output != expected_output:
                    return False, f"测试用例失败：输入'{input_data}'，期望输出'{expected_output}'，实际输出'{actual_output}'"
            
            return True, None
            
        except Exception as e:
            return False, f"C代码评测异常: {str(e)}"
        finally:
            # 清理临时文件
            try:
                if 'c_file' in locals():
                    os.unlink(c_file)
                if 'exe_file' in locals():
                    if os.path.exists(exe_file):
                        os.unlink(exe_file)
            except:
                pass
    
    @staticmethod
    def _execute_cpp_code(user_code: str, examples: List[Dict[str, Any]]) -> tuple[bool, Optional[str]]:
        """执行C++代码"""
        import subprocess
        import tempfile
        import os
        
        def find_gpp():
            """自动寻找G++编译器"""
            import subprocess
            
            # 先尝试在PATH中查找
            try:
                result = subprocess.run(['where', 'g++'], capture_output=True, text=True)
                if result.returncode == 0 and result.stdout.strip():
                    return result.stdout.strip().split('\n')[0]
            except:
                pass
            
            # 常见的G++安装路径
            common_paths = [
                'E:/msys64/mingw64/bin/x86_64-w64-mingw32-g++.exe',
                'E:/msys64/mingw32/bin/g++.exe',
                'C:/mingw64/bin/x86_64-w64-mingw32-g++.exe',
                'C:/mingw/bin/g++.exe',
                'C:/TDM-GCC-64/bin/g++.exe',
                'C:/Program Files/mingw-w64/x86_64-8.1.0-posix-seh-rt_v6-rev0/bin/g++.exe',
                '/usr/bin/g++',  # WSL
                '/usr/local/bin/g++',  # macOS/Linux
            ]
            
            # 检查每个路径是否存在
            for path in common_paths:
                if os.path.exists(path):
                    return path
                    
            return None
        
        try:
            # 自动寻找G++编译器
            gpp_path = find_gpp()
            if not gpp_path:
                return False, "未找到C++编译器，请安装G++或将其路径添加到系统PATH中"
            
            # 检查用户代码是否包含main函数
            if "int main(" in user_code or "void main(" in user_code or "int main (" in user_code or "void main (" in user_code:
                # 如果用户代码包含main函数，修改为test_main避免冲突
                modified_user_code = user_code.replace("int main(", "int test_main(").replace("void main(", "void test_main(")
                modified_user_code = modified_user_code.replace("int main (", "int test_main (").replace("void main (", "void test_main (")
            else:
                modified_user_code = user_code
            
            # 包装用户代码，使其能够调用solve函数
            wrapper_code = f'''
#include <iostream>
#include <string>
#include <cstring>
#include <cstdlib>

using namespace std;

// 用户代码
{modified_user_code}

// 测试主函数
int main() {{
    string input;
    
    // 从标准输入读取测试用例
    if (getline(cin, input)) {{
        // 移除换行符
        if (!input.empty() && (input.back() == '\\n' || input.back() == '\\r')) {{
            input.pop_back();
        }}
        if (!input.empty() && (input.back() == '\\n' || input.back() == '\\r')) {{
            input.pop_back();
        }}
        
        // 调用solve函数
        char* result = solve(input.c_str());
        
        if (result != nullptr) {{
            cout << result;
            free(result);
        }}
    }}
    
    return 0;
}}
'''
            
            # 创建临时C++文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False, encoding='utf-8') as f:
                f.write(wrapper_code)
                cpp_file = f.name
            
            # 编译C++代码
            exe_file = cpp_file.replace('.cpp', '.exe')
            compile_cmd = [gpp_path, cpp_file, '-o', exe_file]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=30)
            
            if compile_result.returncode != 0:
                return False, f"C++代码编译失败: {compile_result.stderr}"
            
            # 测试所有用例
            for ex in examples:
                input_data = str(ex.get("input", ""))
                expected_output = str(ex.get("output", ""))
                
                try:
                    run_result = subprocess.run([exe_file], 
                                              input=input_data, 
                                              capture_output=True, 
                                              text=True, 
                                              timeout=10)
                    actual_output = run_result.stdout.strip()
                except subprocess.TimeoutExpired:
                    return False, f"C++代码执行超时：输入'{input_data}'"
                except Exception as e:
                    return False, f"C++代码执行错误：输入'{input_data}', 错误: {str(e)}"
                
                if actual_output != expected_output:
                    return False, f"测试用例失败：输入'{input_data}'，期望输出'{expected_output}'，实际输出'{actual_output}'"
            
            return True, None
            
        except Exception as e:
            return False, f"C++代码评测异常: {str(e)}"
        finally:
            # 清理临时文件
            try:
                if 'cpp_file' in locals():
                    os.unlink(cpp_file)
                if 'exe_file' in locals():
                    if os.path.exists(exe_file):
                        os.unlink(exe_file)
            except:
                pass
    
    @staticmethod
    def _execute_java_code(user_code: str, examples: List[Dict[str, Any]]) -> tuple[bool, Optional[str]]:
        """执行Java代码"""
        import subprocess
        import tempfile
        import os
        import re
        
        try:
            # 创建临时Java文件，使用UTF-8编码
            with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False, encoding='utf-8') as f:
                f.write(user_code)
                java_file = f.name
            
            # 从文件路径中获取文件名（不包含扩展名）作为类名
            class_name = os.path.splitext(os.path.basename(java_file))[0]
            
            # 从Java代码中检查是否有public class声明，如果没有则添加
            public_class_match = re.search(r'public\s+class\s+(\w+)', user_code)
            if public_class_match:
                # 如果有public class，但类名与文件名不匹配，需要修改代码中的类名
                original_class = public_class_match.group(1)
                if original_class != class_name:
                    # 替换类名声明
                    modified_code = re.sub(
                        r'public\s+class\s+' + re.escape(original_class),
                        f'public class {class_name}',
                        user_code
                    )
                    
                    # 重新写入文件
                    with open(java_file, 'w', encoding='utf-8') as f:
                        f.write(modified_code)
            
            # 编译Java代码，指定UTF-8编码
            compile_cmd = ['javac', '-encoding', 'UTF-8', java_file]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=30)
            
            if compile_result.returncode != 0:
                return False, f"Java代码编译失败: {compile_result.stderr}"
            
            # 测试所有用例
            for ex in examples:
                input_data = str(ex.get("input", ""))
                expected_output = str(ex.get("output", ""))
                
                try:
                    run_result = subprocess.run(['java', '-cp', os.path.dirname(java_file), class_name], 
                                              input=input_data, 
                                              capture_output=True, 
                                              text=True, 
                                              timeout=10)
                    actual_output = run_result.stdout.strip()
                except subprocess.TimeoutExpired:
                    return False, f"Java代码执行超时：输入'{input_data}'"
                except Exception as e:
                    return False, f"Java代码执行错误：输入'{input_data}', 错误: {str(e)}"
                
                if actual_output != expected_output:
                    return False, f"测试用例失败：输入'{input_data}'，期望输出'{expected_output}'，实际输出'{actual_output}'"
            
            return True, None
            
        except Exception as e:
            return False, f"Java代码评测异常: {str(e)}"
        finally:
            # 清理临时文件
            try:
                if 'java_file' in locals():
                    os.unlink(java_file)
                    # 删除对应的.class文件
                    class_file = java_file.replace('.java', '.class')
                    if os.path.exists(class_file):
                        os.unlink(class_file)
            except:
                pass

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
    answer: str = Form(..., description="正确答案（编程题可填写参考说明）"),
    code_examples: Optional[str] = Form(
        None,
        description="编程题测试用例(JSON数组，每项包含input和output字段，仅编程题必填)"
    ),
    code_language: Optional[str] = Form("python", description="编程语言类型(python/c/cpp/java，仅编程题有效)"),
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
    
    # 验证编程语言类型
    if type == "code":
        if code_language not in ["python", "c", "cpp", "java"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="编程语言类型必须为python、c、cpp或java"
            )
    else:
        # 非编程题忽略编程语言字段
        code_language = "python"
    
    # 验证选择题选项
    if type == "choice" and not options:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="选择题必须提供选项"
        )
    
    # 验证编程题测试用例
    if type == "code":
        if not code_examples:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="编程题必须提供测试用例"
            )
        try:
            examples_data = json.loads(code_examples)
            if not isinstance(examples_data, list) or not examples_data:
                raise ValueError("测试用例必须为非空列表")
            for ex in examples_data:
                if not isinstance(ex, dict) or "input" not in ex or "output" not in ex:
                    raise ValueError("每个测试用例必须包含input和output字段")
        except (json.JSONDecodeError, ValueError) as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"测试用例格式错误: {str(e)}"
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
            code_examples=code_examples,
            code_language=code_language,
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
            "correct_rate": round(correct_rate, 4),
            "code_examples": q.code_examples,  # 添加编程题测试用例字段
            "code_language": getattr(q, 'code_language', 'python')  # 添加编程语言字段
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

@router.get("/knowledge/list", summary="获取知识点列表")
async def get_knowledge_nodes(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    try:
        questions = db.query(Question).all()
        knowledge_map: Dict[str, Dict[str, Any]] = {}
        
        for question in questions:
            raw_value = getattr(question, "knowledge_id", None)
            if not raw_value:
                continue
            
            knowledge_ids = []
            if isinstance(raw_value, list):
                knowledge_ids = raw_value
            else:
                try:
                    parsed_value = json.loads(raw_value)
                    if isinstance(parsed_value, list):
                        knowledge_ids = parsed_value
                    else:
                        knowledge_ids = [parsed_value]
                except (json.JSONDecodeError, TypeError):
                    knowledge_ids = [raw_value]
            
            for knowledge in knowledge_ids:
                if knowledge is None:
                    continue
                
                # 过滤掉无效的知识点ID（包括0、空字符串、无效值）
                try:
                    knowledge_str = str(knowledge).strip()
                    if not knowledge_str or knowledge_str == "0" or knowledge_str.lower() == "null":
                        continue
                except (ValueError, TypeError):
                    continue
                
                key = knowledge_str
                if key not in knowledge_map:
                    knowledge_map[key] = {
                        "id": key,
                        "name": key,
                        "description": "",
                        "node_type": "concept",
                        "level": 1,
                        "question_count": 0
                    }
                knowledge_map[key]["question_count"] += 1
        
        # 过滤掉无效的知识节点，确保所有返回的数据都是有效的
        valid_knowledge_list = [
            item for item in knowledge_map.values()
            if item["id"] and item["id"] != "0" and item["name"].strip()
        ]
        
        knowledge_list = sorted(
            valid_knowledge_list,
            key=lambda item: item["question_count"],
            reverse=True
        )
        
        return JSONResponse(
            content={
                "code": 200,
                "message": "查询成功",
                "data": knowledge_list
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "message": f"获取知识点列表失败: {str(e)}",
                "data": []
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
                    
                    # 添加编程语言字段 - 对于编程题必须添加
                    q_type = getattr(q, 'type', 'unknown')
                    print(f"题目类型检查: {q_type} (原始值: {getattr(q, 'type', 'unknown')})")
                    
                    # 检查是否为编程题 - 支持字符串和枚举类型
                    is_code_question = False
                    if hasattr(q_type, 'value'):
                        # 枚举类型
                        is_code_question = str(q_type.value).lower() == 'code'
                    else:
                        # 字符串类型
                        is_code_question = str(q_type).lower() == 'code'
                    
                    print(f"是否为编程题: {is_code_question}")
                    
                    if is_code_question:
                        # 只返回数据库中实际存储的值，不设置默认值
                        code_lang = getattr(q, 'code_language', None)
                        if code_lang is not None:
                            question_dict["code_language"] = str(code_lang)
                            print(f"编程题添加语言字段: {question_dict['question_id']} -> {question_dict['code_language']}")
                        else:
                            print(f"编程题无语言字段: {question_dict['question_id']}")
                    
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
                    
                    print(f"处理完成的题目: {question_dict}")
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
            is_correct = False
            code_runtime_error = None
            
            # DEBUG: 添加调试信息
            print(f"DEBUG: question_id={item.question_id}")
            print(f"DEBUG: question.type={question.type}")
            print(f"DEBUG: str(question.type)='{str(question.type)}'")
            print(f"DEBUG: question.type == QuestionType.code: {question.type == 'code'}")
            print(f"DEBUG: student_answer='{item.student_answer}'")
            print(f"DEBUG: question.answer='{question.answer}'")
            
            # 编程题：根据测试用例运行学生代码判定
            if question.type == QuestionType.code or question.type == "code":
                try:
                    # 解析测试用例
                    examples = []
                    if question.code_examples:
                        try:
                            examples = json.loads(question.code_examples)
                            print(f"DEBUG: parsed examples={examples}")
                        except json.JSONDecodeError as e:
                            print(f"DEBUG: JSON decode error: {e}")
                            examples = []
                    else:
                        print(f"DEBUG: question.code_examples is None or empty")
                    
                    if not examples:
                        # 没有配置测试用例则认为无法判分，默认错误
                        print(f"DEBUG: No examples found, setting is_correct=False")
                        is_correct = False
                    else:
                        # 获取编程语言
                        code_language = getattr(question, 'code_language', 'python')
                        user_code = item.student_answer or ""
                        print(f"DEBUG: code_language={code_language}")
                        print(f"DEBUG: user_code=\"{user_code}\"")
                        
                        if code_language == "python":
                            # Python代码执行
                            is_correct, code_runtime_error = CodeExecutor._execute_python_code(user_code, examples)
                        elif code_language == "c":
                            # C代码执行
                            is_correct, code_runtime_error = CodeExecutor._execute_c_code(user_code, examples)
                        elif code_language == "cpp":
                            # C++代码执行
                            is_correct, code_runtime_error = CodeExecutor._execute_cpp_code(user_code, examples)
                        elif code_language == "java":
                            # Java代码执行
                            is_correct, code_runtime_error = CodeExecutor._execute_java_code(user_code, examples)
                        else:
                            code_runtime_error = f"不支持的编程语言: {code_language}"
                            is_correct = False
                            
                except Exception as e:
                    code_runtime_error = f"评测过程异常: {str(e)}"
                    is_correct = False
            else:
                # 非编程题：直接比对答案
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
            result_item: Dict[str, Any] = {
                "question_id": item.question_id,
                "student_answer": item.student_answer,
                "correct_answer": question.answer,
                "is_correct": is_correct,
                "correct_rate": round(correct_rate, 4)
            }
            if (question.type == QuestionType.code or question.type == "code") and code_runtime_error:
                result_item["code_error"] = code_runtime_error
            results.append(result_item)
        
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

        from crud.mastery import calc_mastery
        # 计算并更新掌握度
        calc_mastery(current_user.id, db)
        
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
        # 默认查询当前用户
        target_user_id = current_user.id
        
        # 如果显式指定了user_id，检查是否有权限查看
        if user_id is not None:
            try:
                user_id = int(user_id)
            except (TypeError, ValueError):
                return JSONResponse(
                    status_code=400,
                    content={
                        "code": 400,
                        "message": "user_id必须为整数",
                        "data": {}
                    }
                )
            
            if user_id != current_user.id:
                has_teacher_privilege = check_role(db, current_user.id, "teacher")
                has_admin_privilege = check_role(db, current_user.id, "admin")
                
                if has_teacher_privilege or has_admin_privilege:
                    target_user_id = user_id
                else:
                    # 学生尝试查看他人记录时强制回退到自身数据
                    target_user_id = current_user.id
            else:
                target_user_id = user_id
        
        # 验证分页参数
        if limit > 100:
            limit = 100
        
        # 查询记录
        query = db.query(QuestionRecord).filter(QuestionRecord.student_id == target_user_id)
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
                "student_id": record.student_id,
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
            # 构建基础题目信息
            question_info = {
                "text": q.text,
                "type": q.type,
                "options": json.loads(q.options) if q.options else None,
                "correct_answer": q.answer,
                "knowledge_id": json.loads(q.knowledge_id),
                "difficulty": q.difficulty,
                "student_answer": item["student_answer"],
                "is_correct": item["is_correct"],
                "correct_rate": item["correct_rate"]
            }
            
            # 编程题需要包含code_language字段
            if q.type == "code" and hasattr(q, "code_language"):
                question_info["code_language"] = q.code_language
                # 如果有code_error或error_details，也包含进来
                if "code_error" in item:
                    question_info["code_error"] = item["code_error"]
                if "error_details" in item:
                    question_info["error_details"] = item["error_details"]
            
            questions_detail.append(question_info)
    
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