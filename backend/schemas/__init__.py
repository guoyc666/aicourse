from .user import (
    UserBase,
    UserCreate,
    UserLogin,
    UserResponse,
    UserUpdate,
)
from .topic import (
    TopicBase,
    TopicCreate,
    TopicUpdate,
    TopicResponse,
    ReplyBase,
    ReplyCreate,
    ReplyResponse,
)
from .task import (
    TaskBase,
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskSubmissionBase,
    TaskSubmissionCreate,
    TaskSubmissionResponse,
    AssignedTaskResponse,
)
from .role import (
    PermissionResponse,
    RoleResponse,
    RoleCreate,
    RoleUpdate,
)
from .records import (
    LearningRecordCreate,
    LearningRecord,
    StudyTimeOut,
    AverageStudyTimeOut,
    StudyTimeListOut,
)
from .progress import (
    ProgressOut,
    ProgressListOut,
    AverageProgressOut,
)
from .mastery import (
    MasteryOut,
    MasteryListOut,
    AverageMasteryOut,
)
from .graph import (
    BaseNode,
    CourseNode,
    ConceptNode,
    ResourceNode,
    ResourceSimpleInfo,
    GraphNode,
    GraphEdge,
    GraphData,
    GraphDataOut,
    KnowledgeInfo,
    ResourceInfo,
    NodeRef,
    NodeDetail,
)
from .file import (
    FileResourceBase,
    FileResourceCreate,
    FileResourceUpdate,
    FileResourceResponse,
)
from .auth import Token, TokenData
from .ai_assistant import (
    MessageOut,
    ConversationCreate,
    ConversationSummary,
    ConversationOut,
    MessageIn,
)

__all__ = [
    # user
    "UserBase",
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "UserUpdate",
    # topic
    "TopicBase",
    "TopicCreate",
    "TopicUpdate",
    "TopicResponse",
    "ReplyBase",
    "ReplyCreate",
    "ReplyResponse",
    # task
    "TaskBase",
    "TaskCreate",
    "TaskUpdate",
    "TaskResponse",
    "TaskSubmissionBase",
    "TaskSubmissionCreate",
    "TaskSubmissionResponse",
    "AssignedTaskResponse",
    # role
    "PermissionResponse",
    "RoleResponse",
    "RoleCreate",
    "RoleUpdate",
    # records
    "LearningRecordCreate",
    "LearningRecord",
    "StudyTimeOut",
    "AverageStudyTimeOut",
    "StudyTimeListOut",
    # progress
    "ProgressOut",
    "ProgressListOut",
    "AverageProgressOut",
    # mastery
    "MasteryOut",
    "MasteryListOut",
    "AverageMasteryOut",
    # graph
    "BaseNode",
    "CourseNode",
    "ConceptNode",
    "ResourceNode",
    "ResourceSimpleInfo",
    "GraphNode",
    "GraphEdge",
    "GraphData",
    "GraphDataOut",
    "KnowledgeInfo",
    "ResourceInfo",
    "NodeRef",
    "NodeDetail",
    # file
    "FileResourceBase",
    "FileResourceCreate",
    "FileResourceUpdate",
    "FileResourceResponse",
    # auth
    "Token",
    "TokenData",
    # ai_assistant
    "MessageOut",
    "ConversationCreate",
    "ConversationSummary",
    "ConversationOut",
    "MessageIn",
]