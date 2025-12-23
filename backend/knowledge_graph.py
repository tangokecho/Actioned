# Knowledge Graph for Adaptive Learning Paths
# Graph-based learning path optimization with A* pathfinding

import networkx as nx
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass
from datetime import datetime
import logging
import heapq

logger = logging.getLogger(__name__)

@dataclass
class LearningNode:
    """Node in the knowledge graph"""
    node_id: str
    node_type: str  # 'concept', 'skill', 'track', 'project', 'assessment'
    title: str
    description: str
    difficulty: float  # 0.0 to 1.0
    estimated_hours: int
    prerequisites: List[str]
    unlocks: List[str]
    competencies: List[str]
    track_id: Optional[str] = None
    metadata: Dict[str, Any] = None

    def __hash__(self):
        return hash(self.node_id)

@dataclass
class LearningPath:
    """Optimized learning path"""
    path_id: str
    user_id: str
    start_node: str
    goal_node: str
    nodes: List[LearningNode]
    sequence: List[str]
    total_hours: int
    difficulty_progression: List[float]
    alignment_score: float
    confidence: float
    rationale: str
    alternative_paths: List[Dict[str, Any]]
    generated_at: str

class KnowledgeGraph:
    """Knowledge graph for learning path optimization"""

    def __init__(self):
        self.graph = nx.DiGraph()
        self._initialize_graph()

    def _initialize_graph(self):
        """Initialize knowledge graph with ActionEDx tracks and concepts"""

        # Define learning nodes
        nodes = [
            # Foundation Concepts
            LearningNode(
                node_id="concept_clarity",
                node_type="concept",
                title="Clarity: Define Your Vision",
                description="Master the art of clear problem definition",
                difficulty=0.2,
                estimated_hours=4,
                prerequisites=[],
                unlocks=["concept_speed", "concept_ingenuity"],
                competencies=["strategic_thinking", "problem_definition"],
                metadata={"pillar": "Clarity"}
            ),
            LearningNode(
                node_id="concept_speed",
                node_type="concept",
                title="Speed: Rapid Execution",
                description="Learn to move from idea to action quickly",
                difficulty=0.3,
                estimated_hours=6,
                prerequisites=["concept_clarity"],
                unlocks=["concept_discipline", "skill_mvp"],
                competencies=["rapid_prototyping", "time_management"],
                metadata={"pillar": "Speed"}
            ),
            LearningNode(
                node_id="concept_ingenuity",
                node_type="concept",
                title="Ingenuity: Creative Problem Solving",
                description="Develop innovative solutions to complex problems",
                difficulty=0.4,
                estimated_hours=8,
                prerequisites=["concept_clarity"],
                unlocks=["concept_innovation", "skill_creative_thinking"],
                competencies=["creative_thinking", "innovation"],
                metadata={"pillar": "Ingenuity"}
            ),
            LearningNode(
                node_id="concept_discipline",
                node_type="concept",
                title="Discipline: Consistent Execution",
                description="Build habits for sustained progress",
                difficulty=0.3,
                estimated_hours=6,
                prerequisites=["concept_speed"],
                unlocks=["concept_resilience"],
                competencies=["discipline", "habit_formation"],
                metadata={"pillar": "Discipline"}
            ),

            # Skills
            LearningNode(
                node_id="skill_mvp",
                node_type="skill",
                title="MVP Development",
                description="Build minimum viable products",
                difficulty=0.4,
                estimated_hours=12,
                prerequisites=["concept_speed"],
                unlocks=["project_innovation_foundations"],
                competencies=["mvp_development", "lean_startup"],
                metadata={}
            ),
            LearningNode(
                node_id="skill_9_pillar",
                node_type="skill",
                title="9-Pillar Framework Application",
                description="Apply 9-Pillar Framework to real projects",
                difficulty=0.5,
                estimated_hours=16,
                prerequisites=["concept_clarity", "concept_speed", "concept_ingenuity"],
                unlocks=["track_innovation_foundations"],
                competencies=["framework_application", "strategic_analysis"],
                metadata={}
            ),
            LearningNode(
                node_id="skill_ai_prompting",
                node_type="skill",
                title="AI Prompt Engineering",
                description="Master prompt engineering for AI tools",
                difficulty=0.5,
                estimated_hours=10,
                prerequisites=["skill_9_pillar"],
                unlocks=["track_ai_action_officer"],
                competencies=["prompt_engineering", "ai_integration"],
                metadata={}
            ),

            # Tracks
            LearningNode(
                node_id="track_innovation_foundations",
                node_type="track",
                title="Innovation Execution Foundations",
                description="Master 9-Pillar Framework and Tri-Core Loop",
                difficulty=0.5,
                estimated_hours=200,
                prerequisites=["skill_9_pillar"],
                unlocks=["track_ai_action_officer", "track_house_of_hearts"],
                competencies=["strategic_thinking", "framework_application", "impact_measurement"],
                track_id="innovation-foundations",
                metadata={"duration_days": 90}
            ),
            LearningNode(
                node_id="track_ai_action_officer",
                node_type="track",
                title="AI Action Officer Certification",
                description="Deploy AI-powered strategy tools",
                difficulty=0.7,
                estimated_hours=250,
                prerequisites=["track_innovation_foundations", "skill_ai_prompting"],
                unlocks=["track_greenbid"],
                competencies=["ai_strategy", "prompt_engineering", "automation"],
                track_id="ai-action-officer",
                metadata={"duration_days": 90}
            ),
            LearningNode(
                node_id="track_house_of_hearts",
                node_type="track",
                title="House of Hearts Leadership",
                description="Leadership through Courage, Compassion, Accountability",
                difficulty=0.6,
                estimated_hours=180,
                prerequisites=["track_innovation_foundations"],
                unlocks=[],
                competencies=["emotional_intelligence", "team_leadership", "ethical_decision_making"],
                track_id="house-of-hearts",
                metadata={"duration_days": 90}
            ),
            LearningNode(
                node_id="track_youth_energy",
                node_type="track",
                title="Youth Energy Entrepreneurship",
                description="For entrepreneurs aged 16-24",
                difficulty=0.4,
                estimated_hours=150,
                prerequisites=["concept_clarity", "concept_speed"],
                unlocks=["track_innovation_foundations"],
                competencies=["business_basics", "innovation_mindset", "first_revenue"],
                track_id="youth-energy",
                metadata={"duration_days": 90}
            ),
            LearningNode(
                node_id="track_greenbid",
                node_type="track",
                title="GreenBid Bootcamp",
                description="Government contracting mastery",
                difficulty=0.8,
                estimated_hours=220,
                prerequisites=["track_ai_action_officer"],
                unlocks=[],
                competencies=["proposal_writing", "compliance", "contract_management"],
                track_id="greenbid-bootcamp",
                metadata={"duration_days": 90}
            ),

            # Projects
            LearningNode(
                node_id="project_strategy_audit",
                node_type="project",
                title="9-Pillar Strategy Audit Project",
                description="Conduct comprehensive strategy audit",
                difficulty=0.6,
                estimated_hours=20,
                prerequisites=["skill_9_pillar"],
                unlocks=[],
                competencies=["strategic_analysis", "audit_execution"],
                metadata={}
            ),
            LearningNode(
                node_id="project_ai_integration",
                node_type="project",
                title="AI Integration Project",
                description="Build AI-powered application",
                difficulty=0.7,
                estimated_hours=40,
                prerequisites=["skill_ai_prompting"],
                unlocks=[],
                competencies=["ai_integration", "product_development"],
                metadata={}
            ),
        ]

        # Add nodes to graph
        for node in nodes:
            self.graph.add_node(node.node_id, **node.__dict__)

        # Add edges (prerequisites)
        for node in nodes:
            for prereq in node.prerequisites:
                if prereq in self.graph:
                    self.graph.add_edge(prereq, node.node_id, weight=node.difficulty)

    def get_node(self, node_id: str) -> Optional[LearningNode]:
        """Get node by ID"""
        if node_id not in self.graph:
            return None

        data = self.graph.nodes[node_id]
        return LearningNode(**data)

    def get_prerequisites(self, node_id: str) -> List[str]:
        """Get all prerequisites for a node"""
        if node_id not in self.graph:
            return []
        return list(self.graph.predecessors(node_id))

    def check_prerequisites_met(self, node_id: str, completed_nodes: Set[str]) -> bool:
        """Check if all prerequisites are met"""
        prereqs = self.get_prerequisites(node_id)
        return all(p in completed_nodes for p in prereqs)

    def find_optimal_path(self, start_node: str, goal_node: str,
                         user_profile: Dict[str, Any],
                         completed_nodes: Set[str]) -> Optional[List[str]]:
        """Find optimal learning path using A* algorithm"""

        if start_node not in self.graph or goal_node not in self.graph:
            logger.error(f"Invalid nodes: {start_node} or {goal_node}")
            return None

        # A* pathfinding
        def heuristic(node_a: str, node_b: str) -> float:
            """Heuristic function for A*"""
            # Simple heuristic: use difficulty difference
            node_a_data = self.graph.nodes[node_a]
            node_b_data = self.graph.nodes[node_b]
            return abs(node_a_data["difficulty"] - node_b_data["difficulty"])

        try:
            path = nx.astar_path(
                self.graph,
                start_node,
                goal_node,
                heuristic=heuristic,
                weight='weight'
            )

            # Filter out already completed nodes
            path = [n for n in path if n not in completed_nodes]

            return path

        except nx.NetworkXNoPath:
            logger.warning(f"No path from {start_node} to {goal_node}")
            return None

    def generate_adaptive_path(
        self,
        user_id: str,
        goal_track: str,
        user_profile: Dict[str, Any],
        completed_nodes: Set[str],
    ) -> LearningPath:
        """Generate adaptive learning path based on user profile"""

        # Find entry point based on user's current knowledge
        entry_point = self._find_entry_point(user_profile, completed_nodes)

        # Find goal node
        goal_node = f"track_{goal_track}"
        if goal_node not in self.graph:
            # Fallback to innovation foundations
            goal_node = "track_innovation_foundations"

        # Find optimal path
        sequence = self.find_optimal_path(entry_point, goal_node, user_profile, completed_nodes)
        if not sequence:
            # Fallback: direct path to goal
            sequence = [goal_node]

        # Build path with nodes
        nodes = [self.get_node(node_id) for node_id in sequence]
        nodes = [n for n in nodes if n is not None]

        # Calculate metrics
        total_hours = sum(n.estimated_hours for n in nodes)
        difficulty_progression = [n.difficulty for n in nodes]

        # Calculate alignment score
        alignment_score = self._calculate_alignment(nodes, user_profile)

        # Find alternative paths
        alternatives = self._find_alternative_paths(entry_point, goal_node, sequence, user_profile)

        # Generate rationale
        rationale = self._generate_path_rationale(nodes, user_profile, alignment_score)

        return LearningPath(
            path_id=f"path_{user_id}_{datetime.utcnow().timestamp()}",
            user_id=user_id,
            start_node=entry_point,
            goal_node=goal_node,
            nodes=nodes,
            sequence=sequence,
            total_hours=total_hours,
            difficulty_progression=difficulty_progression,
            alignment_score=alignment_score,
            confidence=0.85,
            rationale=rationale,
            alternative_paths=alternatives,
            generated_at=datetime.utcnow().isoformat()
        )

    def _find_entry_point(self, user_profile: Dict[str, Any], completed: Set[str]) -> str:
        """Find optimal entry point based on user's current knowledge"""

        skill_level = user_profile.get("skill_level", "novice")
        completed_tracks = user_profile.get("completed_tracks", 0)

        if completed_tracks >= 2:
            return "track_ai_action_officer"
        elif completed_tracks >= 1:
            return "track_innovation_foundations"
        elif skill_level in ["advanced", "expert"]:
            return "skill_9_pillar"
        else:
            return "concept_clarity"

    def _calculate_alignment(self, nodes: List[LearningNode], profile: Dict) -> float:
        """Calculate how well path aligns with user profile"""

        if not nodes:
            return 0.0

        score = 70.0  # Base score

        # Check difficulty alignment
        user_level = profile.get("skill_level", "novice")
        avg_difficulty = sum(n.difficulty for n in nodes) / len(nodes)
        target_difficulty = {
            "novice": 0.3,
            "intermediate": 0.5,
            "advanced": 0.7,
            "expert": 0.8
        }.get(user_level, 0.5)
        difficulty_match = 1 - abs(avg_difficulty - target_difficulty)
        score += difficulty_match * 15

        # Check competency alignment
        user_goals = set(profile.get("goals", []))
        path_competencies = set()
        for node in nodes:
            path_competencies.update(node.competencies)

        if user_goals:
            goal_overlap = len(user_goals & path_competencies) / len(user_goals)
            score += goal_overlap * 15

        return min(100.0, score)

    def _find_alternative_paths(
        self,
        start: str,
        goal: str,
        primary_path: List[str],
        profile: Dict
    ) -> List[Dict[str, Any]]:
        """Find alternative learning paths"""

        alternatives: List[Dict[str, Any]] = []
        try:
            # Find all simple paths
            all_paths = list(nx.all_simple_paths(self.graph, start, goal, cutoff=10))

            # Filter and score
            for path in all_paths[:3]:  # Top 3 alternatives
                if path != primary_path:
                    nodes = [self.get_node(n) for n in path]
                    nodes = [n for n in nodes if n is not None]

                    alternatives.append({
                        "sequence": path,
                        "total_hours": sum(n.estimated_hours for n in nodes),
                        "avg_difficulty": sum(n.difficulty for n in nodes) / len(nodes) if nodes else 0,
                        "description": self._describe_path_difference(path, primary_path)
                    })
        except Exception:
            pass

        return alternatives[:2]  # Return max 2 alternatives

    def _describe_path_difference(self, alt_path: List[str], primary: List[str]) -> str:
        """Describe how alternative differs from primary"""

        alt_set = set(alt_path)
        primary_set = set(primary)

        unique_to_alt = alt_set - primary_set
        if len(alt_path) < len(primary):
            return "Faster route with fewer intermediate steps"
        elif len(alt_path) > len(primary):
            return "More comprehensive route with additional concepts"
        elif unique_to_alt:
            return f"Alternative approach focusing on different concepts"
        else:
            return "Similar difficulty, different sequence"

    def _generate_path_rationale(
        self,
        nodes: List[LearningNode],
        profile: Dict,
        alignment: float
    ) -> str:
        """Generate human-readable rationale for path"""

        if not nodes:
            return "Starting from fundamentals"

        rationale_parts = []

        # Alignment
        if alignment >= 90:
            rationale_parts.append("Highly aligned with your goals and skill level")
        elif alignment >= 75:
            rationale_parts.append("Well-suited to your profile")
        else:
            rationale_parts.append("Recommended foundational path")

        # Difficulty progression
        if nodes:
            start_difficulty = nodes[0].difficulty
            end_difficulty = nodes[-1].difficulty

            if end_difficulty - start_difficulty > 0.3:
                rationale_parts.append("Progressive difficulty increase for optimal challenge")
            else:
                rationale_parts.append("Consistent difficulty level for steady progress")

        # Duration
        total_hours = sum(n.estimated_hours for n in nodes)
        if total_hours < 100:
            rationale_parts.append(f"Can be completed in ~{total_hours // 20} weeks with 5 hrs/week")
        else:
            rationale_parts.append(f"Comprehensive path requiring ~{total_hours // 20} weeks")

        return ". ".join(rationale_parts) + "."


# Singleton instance
knowledge_graph = KnowledgeGraph()
