"""
初始化数据库数据
创建默认的角色和权限
"""
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Role, Permission, RolePermission, User, UserRole, Task, AssignedTask, TaskSubmission, Topic, Reply
from utils.auth import get_password_hash

def create_tables():
    """创建数据库表"""
    Base.metadata.create_all(bind=engine)

def init_permissions():
    """初始化权限"""
    db = SessionLocal()
    
    permissions = [
        # 用户管理权限
        {"name": "user:read", "description": "查看用户信息", "resource": "user"},
        {"name": "user:create", "description": "创建用户", "resource": "user"},
        {"name": "user:update", "description": "更新用户信息", "resource": "user"},
        {"name": "user:delete", "description": "删除用户", "resource": "user"},
        {"name": "user:assign_role", "description": "分配用户角色", "resource": "user"},
        {"name": "user:remove_role", "description": "移除用户角色", "resource": "user"},
        
        # 角色权限管理
        {"name": "role:read", "description": "查看角色", "resource": "role"},
        {"name": "role:create", "description": "创建角色", "resource": "role"},
        {"name": "role:update", "description": "更新角色", "resource": "role"},
        {"name": "role:delete", "description": "删除角色", "resource": "role"},
        
        # 权限管理
        {"name": "permission:read", "description": "查看权限", "resource": "permission"},
    ]
    
    for perm_data in permissions:
        existing = db.query(Permission).filter(Permission.name == perm_data["name"]).first()
        if not existing:
            permission = Permission(
                name=perm_data["name"],
                description=perm_data["description"],
                resource=perm_data["resource"]
            )
            db.add(permission)
    
    db.commit()
    db.close()

def init_roles():
    """初始化角色"""
    db = SessionLocal()
    
    # 学生角色
    student_role = db.query(Role).filter(Role.name == "student").first()
    if not student_role:
        student_role = Role(
            name="student",
            description="学生角色，可以学习课程内容、答题、使用AI助教"
        )
        db.add(student_role)
        db.commit()
        db.refresh(student_role)
    
    # 教师角色
    teacher_role = db.query(Role).filter(Role.name == "teacher").first()
    if not teacher_role:
        teacher_role = Role(
            name="teacher",
            description="教师角色，可以上传资源、创建题目、查看学生学习情况"
        )
        db.add(teacher_role)
        db.commit()
        db.refresh(teacher_role)
    
    # 管理员角色
    admin_role = db.query(Role).filter(Role.name == "admin").first()
    if not admin_role:
        admin_role = Role(
            name="admin",
            description="管理员角色，拥有系统所有权限"
        )
        db.add(admin_role)
        db.commit()
        db.refresh(admin_role)
    
    # 分配权限
    assign_role_permissions(db, student_role, [
        "user:read"
    ])
    
    assign_role_permissions(db, teacher_role, [
        "user:read", "role:read"
    ])
    
    # 管理员拥有所有权限
    all_permissions = db.query(Permission).all()
    assign_role_permissions(db, admin_role, [p.name for p in all_permissions])
    
    db.commit()
    db.close()

def assign_role_permissions(db: Session, role: Role, permission_names: list):
    """为角色分配权限"""
    for perm_name in permission_names:
        permission = db.query(Permission).filter(Permission.name == perm_name).first()
        if permission:
            existing = db.query(RolePermission).filter(
                RolePermission.role_id == role.id,
                RolePermission.permission_id == permission.id
            ).first()
            if not existing:
                role_permission = RolePermission(
                    role_id=role.id,
                    permission_id=permission.id
                )
                db.add(role_permission)

def create_default_admin():
    """创建默认管理员用户"""
    db = SessionLocal()
    
    # 检查是否已存在管理员
    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        admin_user = User(
            username="admin",
            full_name="系统管理员",
            hashed_password=get_password_hash("admin123"),
            is_active=True
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        # 分配管理员角色
        admin_role = db.query(Role).filter(Role.name == "admin").first()
        if admin_role:
            user_role = UserRole(user_id=admin_user.id, role_id=admin_role.id)
            db.add(user_role)
            db.commit()
    
    db.close()

def init_topics_data():
    """初始化讨论区数据"""
    db = SessionLocal()
    
    # 获取管理员用户来创建示例主题和回复
    admin_user = db.query(User).filter(User.username == "admin").first()
    
    # 创建示例主题
    topics_data = [
        {
            "title": "欢迎来到学习系统讨论区",
            "content": "大家好！欢迎使用我们的学习系统。在这里，您可以提问、分享学习心得、讨论课程内容。请遵守讨论区规则，文明发言！",
            "user": admin_user
        }
    ]
    
    created_topics = []
    for topic_data in topics_data:
        existing_topic = db.query(Topic).filter(Topic.title == topic_data["title"]).first()
        if not existing_topic:
            topic = Topic(
                title=topic_data["title"],
                content=topic_data["content"],
                created_by_id=topic_data["user"].id
            )
            db.add(topic)
            db.commit()
            db.refresh(topic)
            created_topics.append(topic)
    
    # 为第一个主题添加回复
    if created_topics:
        replies_data = [
            {
                "content": "在此鸣谢开发组的所有成员",
                "topic": created_topics[0],
                "user": admin_user
            }
        ]
        
        for reply_data in replies_data:
            reply = Reply(
                topic_id=reply_data["topic"].id,
                content=reply_data["content"],
                created_by_id=reply_data["user"].id
            )
            db.add(reply)
    
    db.commit()
    db.close()
    print("讨论区数据初始化完成！")

def init_knowledge_graph():
    from neo4j import get_graph
    graph = get_graph()
    # 如果没有节点，则初始化知识图谱
    if not graph.nodes.match().first():
        from utils.graph_api_utils import nodes, edges
        from crud.graph import save_knowledge_graph
        save_knowledge_graph(nodes, edges)
        print("知识图谱初始化完成！")

def init_all():
    """初始化所有数据"""
    print("创建数据库表...")
    create_tables()
    
    print("初始化权限...")
    init_permissions()
    
    print("初始化角色...")
    init_roles()
    
    print("创建默认管理员...")
    create_default_admin()
    
    print("初始化讨论区数据...")
    init_topics_data()

    print("初始化知识图谱...")
    init_knowledge_graph()  
    
    print("初始化完成！")
    print("默认管理员账号：admin")
    print("默认管理员密码：admin123")
    

if __name__ == "__main__":
    init_all()
