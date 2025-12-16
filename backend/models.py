from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
from enum import Enum

# ==================== ENUMS ====================

class ExecutionPhase(str, Enum):
    BRIEFING = "briefing"
    DRILLS = "drills"
    FIELD_OPERATION = "field_operation"
    DEBRIEF = "debrief"

class SkillLevel(str, Enum):
    NOVICE = "novice"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class TrackLevel(str, Enum):
    FOUNDATION = "foundation"
    ADVANCED = "advanced"
    SPECIALIZED = "specialized"
    LEADERSHIP = "leadership"

class AssistantMode(str, Enum):
    STRATEGIST = "strategist"  # Clear/analytical
    ALLY = "ally"  # Empathetic/supportive
    ORACLE = "oracle"  # Intuitive/poetic

# ==================== USER MODELS ====================

class UserCreate(BaseModel):
    email: str
    name: str
    role: str = "learner"

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    name: str
    role: str = "learner"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    skill_graph: Dict[str, int] = Field(default_factory=dict)
    impact_score: int = 0
    badges: List[str] = Field(default_factory=list)

# ==================== EXECUTION TRACK MODELS ====================

class TrackEnrollment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    track_id: str
    enrolled_at: datetime = Field(default_factory=datetime.utcnow)
    current_day: int = 1
    current_phase: ExecutionPhase = ExecutionPhase.BRIEFING
    progress_percentage: float = 0.0
    completed_projects: int = 0
    skills_unlocked: List[str] = Field(default_factory=list)
    next_logical_step: Optional[str] = None

class ExecutionTrack(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    subtitle: str
    description: str
    level: TrackLevel
    duration_days: int = 90
    skills: List[str]
    phases: Dict[str, Dict[str, Any]] = Field(default_factory=dict)

# ==================== AI ASSISTANT MODELS ====================

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class AssistantRequest(BaseModel):
    user_id: str
    message: str
    mode: AssistantMode = AssistantMode.STRATEGIST
    context: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None

class AssistantResponse(BaseModel):
    response: str
    mode: AssistantMode
    session_id: str
    suggestions: List[str] = Field(default_factory=list)
    next_logical_step: Optional[str] = None

# ==================== LEARNING PATH MODELS ====================

class LearningPathRequest(BaseModel):
    user_id: str
    goals: List[str]
    current_skills: Dict[str, int] = Field(default_factory=dict)
    time_commitment_hours: int = 10  # hours per week
    preferred_tracks: List[str] = Field(default_factory=list)

class LearningPathStep(BaseModel):
    step_number: int
    track_id: str
    track_title: str
    estimated_days: int
    skills_gained: List[str]
    priority_score: float

class LearningPath(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    steps: List[LearningPathStep]
    total_duration_days: int
    alignment_score: float  # 0-100
    rationale: str

# ==================== ANALYTICS MODELS ====================

class AnalyticsEvent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    event_type: str
    event_data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class UserAnalytics(BaseModel):
    user_id: str
    total_time_spent_minutes: int
    tracks_enrolled: int
    tracks_completed: int
    average_completion_rate: float
    skill_growth_rate: float
    engagement_score: float
    impact_metrics: Dict[str, Any]

class PlatformAnalytics(BaseModel):
    total_users: int
    active_users_24h: int
    total_tracks_started: int
    total_tracks_completed: int
    average_completion_rate: float
    total_projects_executed: int
    learner_revenue_generated: float

# ==================== COLLABORATION MODELS ====================

class CrewCreate(BaseModel):
    name: str
    description: str
    track_id: str
    max_members: int = 5

class Crew(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    track_id: str
    max_members: int = 5
    members: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    project_id: Optional[str] = None
    collaboration_score: float = 0.0

class CollaborationRequest(BaseModel):
    crew_id: str
    action: str  # "suggest_roles", "resolve_conflict", "generate_tasks"
    context: Dict[str, Any] = Field(default_factory=dict)

class CollaborationResponse(BaseModel):
    crew_id: str
    action: str
    recommendations: List[Dict[str, Any]]
    insights: str

# ==================== PROJECT MODELS ====================

class ProjectCreate(BaseModel):
    title: str
    description: str
    track_id: str
    user_id: str
    crew_id: Optional[str] = None

class Project(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    track_id: str
    user_id: str
    crew_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "in_progress"
    priority_score: float = 0.0
    impact_score: float = 0.0
    artifacts: List[str] = Field(default_factory=list)
    qc_audit_passed: bool = False

# ==================== EVIDENCE & CREDENTIALS ====================

class Evidence(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    project_id: str
    evidence_type: str  # "document", "code", "video", "outcome"
    title: str
    description: str
    url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    verified: bool = False

class Credential(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    track_id: str
    credential_type: str  # "skill_badge", "track_completion", "nft_credential"
    title: str
    issued_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    blockchain_hash: Optional[str] = None
