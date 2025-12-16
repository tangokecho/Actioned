from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
from enum import Enum

# ==================== AI MODEL ENUMS ====================

class AIModel(str, Enum):
    """Supported AI models with specific capabilities"""
    GPT_4O = "gpt-4o"
    GPT_4_TURBO = "gpt-4-turbo-preview"
    CLAUDE_3_SONNET = "claude-3-sonnet-20240229"
    CLAUDE_3_OPUS = "claude-3-opus-20240229"
    GEMINI_PRO = "gemini-pro"
    GEMINI_FLASH = "gemini-2.0-flash"

class TaskType(str, Enum):
    """AI task types for routing"""
    STRATEGY_AUDIT = "strategy_audit"
    CODE_REVIEW = "code_review"
    CREATIVE_IDEATION = "creative_ideation"
    ETHICAL_ASSESSMENT = "ethical_assessment"
    FRAMEWORK_ALIGNMENT = "framework_alignment"
    REAL_TIME_TUTORING = "real_time_tutoring"
    COLLABORATION_FACILITATION = "collaboration_facilitation"
    DOCUMENT_SYNTHESIS = "document_synthesis"

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
    STRATEGIST = "strategist"
    ALLY = "ally"
    ORACLE = "oracle"

class LearningPattern(str, Enum):
    RAPID_PROTOTYPER = "rapid_prototyper"
    DEEP_THINKER = "deep_thinker"
    SOCIAL_LEARNER = "social_learner"
    NEEDS_SUPPORT = "needs_support"
    CONSISTENT_ACHIEVER = "consistent_achiever"

# ==================== MODEL CAPABILITY ====================

class ModelCapability(BaseModel):
    """AI model capability definitions"""
    model: AIModel
    strategy_planning: bool = False
    code_generation: bool = False
    creative_writing: bool = False
    analysis_synthesis: bool = False
    framework_alignment: bool = False
    ethical_guidance: bool = False
    cost_per_1k_tokens: float = 0.0
    max_tokens: int = 4096
    latency_ms: int = 1000

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
    learning_style: str = "sequential"
    detected_patterns: List[str] = Field(default_factory=list)

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
    ai_recommendations: List[str] = Field(default_factory=list)

# ==================== AI ASSISTANT MODELS ====================

class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    model_used: Optional[str] = None
    tokens_used: Optional[int] = None

class AssistantRequest(BaseModel):
    user_id: str
    message: str
    mode: AssistantMode = AssistantMode.STRATEGIST
    task_type: TaskType = TaskType.REAL_TIME_TUTORING
    context: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None
    prefer_model: Optional[AIModel] = None

class AssistantResponse(BaseModel):
    response: str
    mode: AssistantMode
    session_id: str
    model_used: str
    suggestions: List[str] = Field(default_factory=list)
    next_logical_step: Optional[str] = None
    latency_ms: int = 0
    tokens_used: int = 0

# ==================== STRATEGY AUDIT MODELS ====================

class PillarScore(BaseModel):
    pillar: str
    score: int  # 1-10
    strengths: List[str]
    improvements: List[str]
    recommendations: List[str]

class StrategyAuditRequest(BaseModel):
    user_id: str
    project_data: Dict[str, Any]
    focus_pillars: Optional[List[str]] = None

class StrategyAuditResponse(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    project_id: Optional[str] = None
    pillar_scores: List[PillarScore]
    overall_score: float
    priority_improvement: str
    next_logical_step: str
    full_report: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

# ==================== LEARNING PATH MODELS ====================

class LearningPathRequest(BaseModel):
    user_id: str
    goals: List[str]
    current_skills: Dict[str, int] = Field(default_factory=dict)
    time_commitment_hours: int = 10
    preferred_tracks: List[str] = Field(default_factory=list)
    learning_style: str = "sequential"
    constraints: Dict[str, Any] = Field(default_factory=dict)

class LearningPathStep(BaseModel):
    step_number: int
    track_id: str
    track_title: str
    estimated_days: int
    skills_gained: List[str]
    priority_score: float
    prerequisites_met: bool = True
    node_type: str = "track"

class LearningPath(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    steps: List[LearningPathStep]
    total_duration_days: int
    alignment_score: float
    rationale: str
    adjustments_needed: List[str] = Field(default_factory=list)
    confidence_score: float = 0.85

# ==================== ANALYTICS MODELS ====================

class AnalyticsEvent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    event_type: str
    event_data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    duration_minutes: int = 0

class DetectedPattern(BaseModel):
    pattern_type: LearningPattern
    confidence: float
    characteristics: Dict[str, Any]
    recommendations: List[str]
    predicted_outcomes: Dict[str, float]

class UserAnalytics(BaseModel):
    user_id: str
    analysis_timestamp: datetime = Field(default_factory=datetime.utcnow)
    total_time_spent_minutes: int
    tracks_enrolled: int
    tracks_completed: int
    average_completion_rate: float
    skill_growth_rate: float
    engagement_score: float
    detected_patterns: List[DetectedPattern]
    predictions: Dict[str, float]
    recommendations: List[str]
    risk_factors: List[str]
    opportunity_areas: List[str]
    ai_insights: Dict[str, Any]

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

class CollaborationSession(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    crew_id: str
    participants: List[str]
    focus_area: str
    artifacts: List[Dict[str, Any]] = Field(default_factory=list)
    ai_suggestions: List[Dict[str, Any]] = Field(default_factory=list)
    started_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    status: str = "active"

class CollaborationRequest(BaseModel):
    crew_id: str
    action: str  # "suggest_roles", "resolve_conflict", "generate_tasks", "synthesize"
    context: Dict[str, Any] = Field(default_factory=dict)

class CollaborationResponse(BaseModel):
    crew_id: str
    action: str
    recommendations: List[Dict[str, Any]]
    insights: str
    session_summary: Optional[str] = None

# ==================== HOUSE OF HEARTS MODELS ====================

class HouseOfHeartsReview(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    submission_id: str
    reviewer_id: str
    courage_score: int  # 1-10
    courage_feedback: str
    compassion_score: int  # 1-10
    compassion_feedback: str
    accountability_score: int  # 1-10
    accountability_feedback: str
    overall_impression: str
    actionable_suggestions: List[str]
    question_for_creator: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

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
    tricore_plan: Optional[Dict[str, Any]] = None

# ==================== EVIDENCE & CREDENTIALS ====================

class Evidence(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    project_id: str
    evidence_type: str
    title: str
    description: str
    url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    verified: bool = False
    ai_analysis: Optional[Dict[str, Any]] = None

class Credential(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    track_id: str
    credential_type: str
    title: str
    issued_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    blockchain_hash: Optional[str] = None

# ==================== MONITORING MODELS ====================

class AIRequestMetrics(BaseModel):
    model: str
    task_type: str
    latency_ms: int
    tokens_used: int
    cost_usd: float
    success: bool
    quality_score: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
