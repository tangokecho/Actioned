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
            return None\n    
    def generate_adaptive_path(self, user_id: str, goal_track: str,\n                             user_profile: Dict[str, Any],\n                             completed_nodes: Set[str]) -> LearningPath:\n        \"\"\"Generate adaptive learning path based on user profile\"\"\"\n        \n        # Find entry point based on user's current knowledge\n        entry_point = self._find_entry_point(user_profile, completed_nodes)\n        \n        # Find goal node\n        goal_node = f\"track_{goal_track}\"\n        \n        if goal_node not in self.graph:\n            # Fallback to innovation foundations\n            goal_node = \"track_innovation_foundations\"\n        \n        # Find optimal path\n        sequence = self.find_optimal_path(entry_point, goal_node, user_profile, completed_nodes)\n        \n        if not sequence:\n            # Fallback: direct path to goal\n            sequence = [goal_node]\n        \n        # Build path with nodes\n        nodes = [self.get_node(node_id) for node_id in sequence]\n        nodes = [n for n in nodes if n is not None]\n        \n        # Calculate metrics\n        total_hours = sum(n.estimated_hours for n in nodes)\n        difficulty_progression = [n.difficulty for n in nodes]\n        \n        # Calculate alignment score\n        alignment_score = self._calculate_alignment(nodes, user_profile)\n        \n        # Find alternative paths\n        alternatives = self._find_alternative_paths(entry_point, goal_node, sequence, user_profile)\n        \n        # Generate rationale\n        rationale = self._generate_path_rationale(nodes, user_profile, alignment_score)\n        \n        return LearningPath(\n            path_id=f\"path_{user_id}_{datetime.utcnow().timestamp()}\",\n            user_id=user_id,\n            start_node=entry_point,\n            goal_node=goal_node,\n            nodes=nodes,\n            sequence=sequence,\n            total_hours=total_hours,\n            difficulty_progression=difficulty_progression,\n            alignment_score=alignment_score,\n            confidence=0.85,\n            rationale=rationale,\n            alternative_paths=alternatives,\n            generated_at=datetime.utcnow().isoformat()\n        )\n    
    def _find_entry_point(self, user_profile: Dict[str, Any], completed: Set[str]) -> str:\n        \"\"\"Find optimal entry point based on user's current knowledge\"\"\"\n        \n        skill_level = user_profile.get(\"skill_level\", \"novice\")\n        completed_tracks = user_profile.get(\"completed_tracks\", 0)\n        \n        if completed_tracks >= 2:\n            return \"track_ai_action_officer\"\n        elif completed_tracks >= 1:\n            return \"track_innovation_foundations\"\n        elif skill_level in [\"advanced\", \"expert\"]:\n            return \"skill_9_pillar\"\n        else:\n            return \"concept_clarity\"\n    
    def _calculate_alignment(self, nodes: List[LearningNode], profile: Dict) -> float:\n        \"\"\"Calculate how well path aligns with user profile\"\"\"\n        \n        if not nodes:\n            return 0.0\n        \n        score = 70.0  # Base score\n        \n        # Check difficulty alignment\n        user_level = profile.get(\"skill_level\", \"novice\")\n        avg_difficulty = sum(n.difficulty for n in nodes) / len(nodes)\n        \n        target_difficulty = {\n            \"novice\": 0.3,\n            \"intermediate\": 0.5,\n            \"advanced\": 0.7,\n            \"expert\": 0.8\n        }.get(user_level, 0.5)\n        \n        difficulty_match = 1 - abs(avg_difficulty - target_difficulty)\n        score += difficulty_match * 15\n        \n        # Check competency alignment\n        user_goals = set(profile.get(\"goals\", []))\n        path_competencies = set()\n        for node in nodes:\n            path_competencies.update(node.competencies)\n        \n        if user_goals:\n            goal_overlap = len(user_goals & path_competencies) / len(user_goals)\n            score += goal_overlap * 15\n        \n        return min(100.0, score)\n    
    def _find_alternative_paths(self, start: str, goal: str,\n                              primary_path: List[str],\n                              profile: Dict) -> List[Dict[str, Any]]:\n        \"\"\"Find alternative learning paths\"\"\"\n        \n        alternatives = []\n        \n        try:\n            # Find all simple paths\n            all_paths = list(nx.all_simple_paths(self.graph, start, goal, cutoff=10))\n            \n            # Filter and score\n            for path in all_paths[:3]:  # Top 3 alternatives\n                if path != primary_path:\n                    nodes = [self.get_node(n) for n in path]\n                    nodes = [n for n in nodes if n is not None]\n                    \n                    alternatives.append({\n                        \"sequence\": path,\n                        \"total_hours\": sum(n.estimated_hours for n in nodes),\n                        \"avg_difficulty\": sum(n.difficulty for n in nodes) / len(nodes) if nodes else 0,\n                        \"description\": self._describe_path_difference(path, primary_path)\n                    })\n        \n        except:\n            pass\n        \n        return alternatives[:2]  # Return max 2 alternatives\n    
    def _describe_path_difference(self, alt_path: List[str], primary: List[str]) -> str:\n        \"\"\"Describe how alternative differs from primary\"\"\"\n        \n        alt_set = set(alt_path)\n        primary_set = set(primary)\n        \n        unique_to_alt = alt_set - primary_set\n        \n        if len(alt_path) < len(primary):\n            return \"Faster route with fewer intermediate steps\"\n        elif len(alt_path) > len(primary):\n            return \"More comprehensive route with additional concepts\"\n        elif unique_to_alt:\n            return f\"Alternative approach focusing on different concepts\"\n        else:\n            return \"Similar difficulty, different sequence\"\n    
    def _generate_path_rationale(self, nodes: List[LearningNode],\n                                profile: Dict, alignment: float) -> str:\n        \"\"\"Generate human-readable rationale for path\"\"\"\n        \n        if not nodes:\n            return \"Starting from fundamentals\"\n        \n        rationale_parts = []\n        \n        # Alignment\n        if alignment >= 90:\n            rationale_parts.append(\"Highly aligned with your goals and skill level\")\n        elif alignment >= 75:\n            rationale_parts.append(\"Well-suited to your profile\")\n        else:\n            rationale_parts.append(\"Recommended foundational path\")\n        \n        # Difficulty progression\n        if nodes:\n            start_difficulty = nodes[0].difficulty\n            end_difficulty = nodes[-1].difficulty\n            \n            if end_difficulty - start_difficulty > 0.3:\n                rationale_parts.append(\"Progressive difficulty increase for optimal challenge\")\n            else:\n                rationale_parts.append(\"Consistent difficulty level for steady progress\")\n        \n        # Duration\n        total_hours = sum(n.estimated_hours for n in nodes)\n        if total_hours < 100:\n            rationale_parts.append(f\"Can be completed in ~{total_hours // 20} weeks with 5 hrs/week\")\n        else:\n            rationale_parts.append(f\"Comprehensive path requiring ~{total_hours // 20} weeks\")\n        \n        return \". \".join(rationale_parts) + \".\"\n\n\n# Singleton instance\nknowledge_graph = KnowledgeGraph()\n