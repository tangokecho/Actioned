# Advanced Learning Analytics Engine
# ML-powered behavioral analysis and predictions

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging
from enum import Enum

logger = logging.getLogger(__name__)

class LearningPattern(str, Enum):
    """Identified learning patterns"""
    RAPID_PROTOTYPER = "rapid_prototyper"
    DEEP_THINKER = "deep_thinker"
    SOCIAL_LEARNER = "social_learner"
    NEEDS_SUPPORT = "needs_support"
    CONSISTENT_ACHIEVER = "consistent_achiever"
    EXPLORER = "explorer"
    PERFECTIONIST = "perfectionist"

@dataclass
class PatternSignature:
    """Pattern detection signature"""
    pattern: LearningPattern
    confidence: float
    characteristics: Dict[str, Any]
    recommendations: List[str]
    intervention_priority: int  # 1-5, 5 being highest
    predicted_outcomes: Dict[str, float]

@dataclass
class LearningAnalytics:
    """Comprehensive learning analytics"""
    user_id: str
    analysis_timestamp: str
    
    # Summary metrics
    total_time_minutes: int
    tracks_enrolled: int
    tracks_completed: int
    completion_rate: float
    engagement_score: float
    skill_growth_rate: float
    
    # Patterns
    detected_patterns: List[PatternSignature]
    dominant_pattern: Optional[LearningPattern]
    learning_style: str
    
    # Predictions
    dropout_risk: float  # 0-1
    completion_probability: float  # 0-1
    time_to_completion_days: int
    next_action_prediction: str
    
    # Recommendations
    personalized_recommendations: List[str]
    intervention_needed: bool
    suggested_tracks: List[str]
    optimal_session_length_minutes: int
    
    # Risk factors
    risk_factors: List[str]
    opportunity_areas: List[str]

class AdvancedLearningAnalytics:
    """ML-powered learning analytics engine"""
    
    def __init__(self):
        self.pattern_detectors = self._initialize_pattern_detectors()
        self.prediction_models = self._initialize_prediction_models()
    
    def _initialize_pattern_detectors(self) -> Dict:
        """Initialize pattern detection rules"""
        return {
            LearningPattern.RAPID_PROTOTYPER: {
                "indicators": [
                    ("avg_time_to_first_submission", "<", 24),  # hours
                    ("iteration_count", ">", 5),
                    ("projects_started", ">", 3)
                ],
                "weight": 1.0,
                "recommendations": [
                    "Channel experimentation into structured validation experiments",
                    "Document learnings from each iteration in Evidence Locker",
                    "Schedule weekly reflection sessions to consolidate learning",
                    "Consider mentoring others to deepen your understanding"
                ],
                "intervention_priority": 2
            },
            LearningPattern.DEEP_THINKER: {
                "indicators": [
                    ("avg_research_time_hours", ">", 10),
                    ("planning_to_execution_ratio", ">", 0.7),
                    ("completion_time_vs_estimate", ">", 1.5)
                ],
                "weight": 1.0,
                "recommendations": [
                    "Set time-bound planning phases (2 hours max before action)",
                    "Implement 'minimum viable action' approach: start small, iterate",
                    "Schedule weekly execution sprints with clear deliverables",
                    "Use Tri-Core Loop: Strategy (1 day) → Build (3 days) → Deploy (1 day)"
                ],
                "intervention_priority": 3
            },
            LearningPattern.SOCIAL_LEARNER: {
                "indicators": [
                    ("peer_interaction_rate", ">", 0.5),
                    ("collaboration_score", ">", 0.7),
                    ("forum_posts", ">", 10)
                ],
                "weight": 1.0,
                "recommendations": [
                    "Lead peer review sessions using House of Hearts framework",
                    "Document collaborative learnings for the community",
                    "Mentor newer learners in your track",
                    "Organize weekly crew sync sessions"
                ],
                "intervention_priority": 1
            },
            LearningPattern.NEEDS_SUPPORT: {
                "indicators": [
                    ("abandonment_rate", ">", 0.3),
                    ("help_request_frequency", ">", 0.5),
                    ("progress_rate", "<", 0.3)
                ],
                "weight": 2.0,  # Higher weight for at-risk
                "recommendations": [
                    "🚨 PRIORITY: Schedule 1:1 coaching session this week",
                    "Simplify current objectives: break into smaller milestones",
                    "Celebrate small wins: track daily progress",
                    "Join a supportive crew for accountability and encouragement",
                    "Consider switching to a foundation-level track first"
                ],
                "intervention_priority": 5  # Highest
            },
            LearningPattern.CONSISTENT_ACHIEVER: {
                "indicators": [
                    ("completion_rate", ">", 0.8),
                    ("session_regularity_score", ">", 0.8),
                    ("quality_score_avg", ">", 0.8)
                ],
                "weight": 1.0,
                "recommendations": [
                    "You're excelling! Consider advanced certification tracks",
                    "Share your success strategies in community forums",
                    "Mentor others struggling with concepts you've mastered",
                    "Challenge yourself with cross-disciplinary projects"
                ],
                "intervention_priority": 1
            },
            LearningPattern.EXPLORER: {
                "indicators": [
                    ("tracks_started", ">", 3),
                    ("completion_rate", "<", 0.4),
                    ("topic_diversity_score", ">", 0.7)
                ],
                "weight": 1.0,
                "recommendations": [
                    "Focus energy: commit to completing ONE track before starting another",
                    "Create a learning roadmap with clear milestones",
                    "Use exploration time as 'research phase' before deep dive",
                    "Set a 30-day sprint challenge: one track to completion"
                ],
                "intervention_priority": 3
            },
            LearningPattern.PERFECTIONIST: {
                "indicators": [
                    ("revision_count", ">", 10),
                    ("submission_delay_hours", ">", 48),
                    ("self_reported_confidence", "<", 0.5)
                ],
                "weight": 1.0,
                "recommendations": [
                    "Embrace 'good enough': ship at 80% completion, iterate from feedback",
                    "Set hard deadlines: 24 hours max per assignment",
                    "Practice 'imperfect action': value progress over perfection",
                    "Remember: Done is better than perfect. Iterate based on real feedback."
                ],
                "intervention_priority": 3
            }
        }
    
    def _initialize_prediction_models(self) -> Dict:
        """Initialize prediction models (simple heuristics for now)"""
        return {
            "dropout_risk": self._predict_dropout_risk,
            "completion_probability": self._predict_completion,
            "time_to_completion": self._predict_time_to_completion
        }
    
    async def analyze_learner(self, user_id: str, events: List[Dict[str, Any]],
                             enrollments: List[Dict[str, Any]]) -> LearningAnalytics:
        """Comprehensive learner analysis"""
        
        # Extract features
        features = self._extract_features(events, enrollments)
        
        # Detect patterns
        patterns = self._detect_patterns(features)
        
        # Generate predictions
        predictions = self._generate_predictions(features, patterns)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(features, patterns, predictions)
        
        # Identify risks and opportunities
        risks = self._identify_risks(features, patterns, predictions)
        opportunities = self._identify_opportunities(features, patterns)
        
        # Determine intervention need
        intervention_needed = any(p.intervention_priority >= 4 for p in patterns)
        
        return LearningAnalytics(
            user_id=user_id,
            analysis_timestamp=datetime.utcnow().isoformat(),
            total_time_minutes=features["total_time_minutes"],
            tracks_enrolled=features["tracks_enrolled"],
            tracks_completed=features["tracks_completed"],
            completion_rate=features["completion_rate"],
            engagement_score=features["engagement_score"],
            skill_growth_rate=features["skill_growth_rate"],
            detected_patterns=patterns,
            dominant_pattern=patterns[0].pattern if patterns else None,
            learning_style=self._determine_learning_style(features, patterns),
            dropout_risk=predictions["dropout_risk"],
            completion_probability=predictions["completion_probability"],
            time_to_completion_days=predictions["time_to_completion_days"],
            next_action_prediction=predictions["next_action"],
            personalized_recommendations=recommendations,
            intervention_needed=intervention_needed,
            suggested_tracks=self._suggest_tracks(features, patterns),
            optimal_session_length_minutes=self._calculate_optimal_session(features),
            risk_factors=risks,
            opportunity_areas=opportunities
        )
    
    def _extract_features(self, events: List[Dict], enrollments: List[Dict]) -> Dict[str, Any]:
        """Extract behavioral features from events"""
        
        if not events:
            return self._default_features()
        
        # Time-based features
        total_time = sum(e.get("duration_minutes", 0) for e in events)
        session_count = len([e for e in events if e.get("event_type") == "session_start"])
        avg_session_duration = total_time / session_count if session_count > 0 else 0
        
        # Completion features
        tracks_enrolled = len(enrollments)
        tracks_completed = len([e for e in enrollments if e.get("progress_percentage", 0) >= 100])
        completion_rate = tracks_completed / tracks_enrolled if tracks_enrolled > 0 else 0
        
        # Engagement features
        submissions = len([e for e in events if e.get("event_type") == "project_submit"])
        iterations = len([e for e in events if e.get("event_type") == "project_update"])
        forum_posts = len([e for e in events if "forum" in e.get("event_type", "")])
        
        # Behavioral patterns
        collaboration_events = len([e for e in events if "collaboration" in e.get("event_type", "")])
        help_requests = len([e for e in events if "help" in e.get("event_type", "")])
        
        # Calculate derived metrics
        engagement_score = min(100, (total_time / 60) + (submissions * 10) + (forum_posts * 2))
        skill_growth_rate = min(100, tracks_completed * 20 + total_time / 30)
        
        return {
            "total_time_minutes": total_time,
            "session_count": session_count,
            "avg_session_duration": avg_session_duration,
            "tracks_enrolled": tracks_enrolled,
            "tracks_completed": tracks_completed,
            "completion_rate": completion_rate,
            "projects_started": submissions + iterations,
            "iteration_count": iterations,
            "forum_posts": forum_posts,
            "collaboration_score": collaboration_events / len(events) if events else 0,
            "help_request_frequency": help_requests / len(events) if events else 0,
            "engagement_score": engagement_score,
            "skill_growth_rate": skill_growth_rate,
            "avg_time_to_first_submission": 48,  # Placeholder
            "planning_to_execution_ratio": 0.5,  # Placeholder
            "abandonment_rate": 1 - completion_rate,
            "peer_interaction_rate": collaboration_events / len(events) if events else 0,
            "progress_rate": completion_rate
        }
    
    def _default_features(self) -> Dict[str, Any]:
        """Default features for new users"""
        return {
            "total_time_minutes": 0,
            "session_count": 0,
            "avg_session_duration": 0,
            "tracks_enrolled": 0,
            "tracks_completed": 0,
            "completion_rate": 0,
            "projects_started": 0,
            "iteration_count": 0,
            "forum_posts": 0,
            "collaboration_score": 0,
            "help_request_frequency": 0,
            "engagement_score": 0,
            "skill_growth_rate": 0,
            "avg_time_to_first_submission": 0,
            "planning_to_execution_ratio": 0,
            "abandonment_rate": 0,
            "peer_interaction_rate": 0,
            "progress_rate": 0
        }
    
    def _detect_patterns(self, features: Dict[str, Any]) -> List[PatternSignature]:
        """Detect learning patterns using rule-based ML"""
        
        detected = []
        
        for pattern, config in self.pattern_detectors.items():
            # Check if pattern matches
            matches = 0
            total_indicators = len(config["indicators"])
            
            for feature_name, operator, threshold in config["indicators"]:
                value = features.get(feature_name, 0)
                
                if operator == ">" and value > threshold:
                    matches += 1
                elif operator == "<" and value < threshold:
                    matches += 1
                elif operator == ">=" and value >= threshold:
                    matches += 1
                elif operator == "<=" and value <= threshold:
                    matches += 1
            
            # Calculate confidence
            confidence = (matches / total_indicators) * config["weight"]
            
            if confidence >= 0.5:  # Threshold for detection
                detected.append(PatternSignature(
                    pattern=pattern,
                    confidence=min(1.0, confidence),
                    characteristics={
                        "matches": matches,
                        "total_indicators": total_indicators,
                        "key_features": [ind[0] for ind in config["indicators"][:3]]
                    },
                    recommendations=config["recommendations"],
                    intervention_priority=config["intervention_priority"],
                    predicted_outcomes=self._predict_pattern_outcomes(pattern, features)
                ))
        
        # Sort by confidence
        detected.sort(key=lambda x: x.confidence, reverse=True)
        
        return detected
    
    def _predict_pattern_outcomes(self, pattern: LearningPattern, features: Dict) -> Dict[str, float]:
        """Predict outcomes based on pattern"""
        
        base_outcomes = {
            LearningPattern.RAPID_PROTOTYPER: {
                "speed_score": 0.9,
                "depth_score": 0.6,
                "completion_probability": 0.75
            },
            LearningPattern.DEEP_THINKER: {
                "quality_score": 0.9,
                "speed_score": 0.4,
                "completion_probability": 0.65
            },
            LearningPattern.SOCIAL_LEARNER: {
                "engagement_score": 0.95,
                "network_growth": 0.8,
                "completion_probability": 0.85
            },
            LearningPattern.NEEDS_SUPPORT: {
                "dropout_risk": 0.6,
                "intervention_effectiveness": 0.9,
                "recovery_probability": 0.7
            },
            LearningPattern.CONSISTENT_ACHIEVER: {
                "completion_probability": 0.95,
                "quality_score": 0.85,
                "leadership_potential": 0.8
            },
            LearningPattern.EXPLORER: {
                "curiosity_score": 0.9,
                "completion_probability": 0.4,
                "breadth_score": 0.85
            },
            LearningPattern.PERFECTIONIST: {
                "quality_score": 0.95,
                "speed_score": 0.3,
                "stress_level": 0.7
            }
        }
        
        return base_outcomes.get(pattern, {"completion_probability": 0.5})
    
    def _generate_predictions(self, features: Dict, patterns: List[PatternSignature]) -> Dict[str, Any]:
        """Generate predictive analytics"""
        
        dropout_risk = self._predict_dropout_risk(features, patterns)
        completion_prob = self._predict_completion(features, patterns)
        time_to_complete = self._predict_time_to_completion(features, patterns)
        next_action = self._predict_next_action(features, patterns)
        
        return {
            "dropout_risk": dropout_risk,
            "completion_probability": completion_prob,
            "time_to_completion_days": time_to_complete,
            "next_action": next_action
        }
    
    def _predict_dropout_risk(self, features: Dict, patterns: List[PatternSignature]) -> float:
        """Predict dropout risk (0-1)"""
        
        # Base risk from features
        base_risk = 0.2  # Default 20%
        
        # Adjust based on engagement
        if features["engagement_score"] < 30:
            base_risk += 0.3
        elif features["engagement_score"] < 50:
            base_risk += 0.1
        
        # Adjust based on completion rate
        if features["completion_rate"] < 0.2:
            base_risk += 0.2
        
        # Adjust based on patterns
        if any(p.pattern == LearningPattern.NEEDS_SUPPORT for p in patterns):
            base_risk += 0.3
        
        if any(p.pattern == LearningPattern.CONSISTENT_ACHIEVER for p in patterns):
            base_risk -= 0.3
        
        return max(0.0, min(1.0, base_risk))
    
    def _predict_completion(self, features: Dict, patterns: List[PatternSignature]) -> float:
        """Predict completion probability"""
        
        base_prob = 0.5
        
        # Adjust based on current progress
        base_prob += features["completion_rate"] * 0.3
        
        # Adjust based on engagement
        base_prob += (features["engagement_score"] / 100) * 0.2
        
        # Pattern adjustments
        if patterns:
            pattern_prob = patterns[0].predicted_outcomes.get("completion_probability", 0.5)
            base_prob = (base_prob + pattern_prob) / 2
        
        return max(0.0, min(1.0, base_prob))
    
    def _predict_time_to_completion(self, features: Dict, patterns: List[PatternSignature]) -> int:
        """Predict days to completion"""
        
        if features["completion_rate"] >= 0.9:
            return 7  # Nearly done
        elif features["completion_rate"] >= 0.5:
            return 30
        elif features["completion_rate"] >= 0.2:
            return 60
        else:
            return 90
    
    def _predict_next_action(self, features: Dict, patterns: List[PatternSignature]) -> str:
        """Predict optimal next action"""
        
        if any(p.pattern == LearningPattern.NEEDS_SUPPORT for p in patterns):
            return "Schedule 1:1 coaching session"
        
        if features["completion_rate"] < 0.1:
            return "Complete Day 1 Briefing and set first milestone"
        
        if features["completion_rate"] < 0.5:
            return "Continue current track: aim for 50% completion milestone"
        
        if features["completion_rate"] >= 0.8:
            return "Final push: complete remaining assignments and request review"
        
        return "Maintain momentum: complete next module"
    
    def _generate_recommendations(self, features: Dict, patterns: List[PatternSignature],
                                 predictions: Dict) -> List[str]:
        """Generate personalized recommendations"""
        
        recommendations = []
        
        # Add pattern-based recommendations
        for pattern in patterns[:2]:  # Top 2 patterns
            recommendations.extend(pattern.recommendations[:2])
        
        # Add risk-based recommendations
        if predictions["dropout_risk"] > 0.5:
            recommendations.insert(0, "🚨 HIGH PRIORITY: Connect with support team this week")
        
        # Add engagement recommendations
        if features["engagement_score"] < 40:
            recommendations.append("Join weekly Community Showcase to stay motivated")
        
        # Add time management
        if features["avg_session_duration"] > 180:
            recommendations.append("Break sessions into 90-minute focused blocks with breaks")
        
        return recommendations[:5]  # Top 5
    
    def _identify_risks(self, features: Dict, patterns: List[PatternSignature],
                       predictions: Dict) -> List[str]:
        """Identify risk factors"""
        
        risks = []
        
        if predictions["dropout_risk"] > 0.5:
            risks.append("High dropout risk detected")
        
        if features["engagement_score"] < 30:
            risks.append("Low engagement - needs immediate attention")
        
        if features["completion_rate"] < 0.2 and features["tracks_enrolled"] > 0:
            risks.append("Low progress rate - potential blocker")
        
        if any(p.pattern == LearningPattern.NEEDS_SUPPORT for p in patterns):
            risks.append("Learner showing distress signals")
        
        return risks
    
    def _identify_opportunities(self, features: Dict, patterns: List[PatternSignature]) -> List[str]:
        """Identify growth opportunities"""
        
        opportunities = []
        
        if features["completion_rate"] > 0.8:
            opportunities.append("Ready for advanced certification tracks")
        
        if features["collaboration_score"] > 0.6:
            opportunities.append("Strong collaborator - consider crew leadership role")
        
        if any(p.pattern == LearningPattern.CONSISTENT_ACHIEVER for p in patterns):
            opportunities.append("Mentor potential - help newer learners")
        
        if features["skill_growth_rate"] > 70:
            opportunities.append("Fast learner - explore cross-disciplinary tracks")
        
        return opportunities
    
    def _determine_learning_style(self, features: Dict, patterns: List[PatternSignature]) -> str:
        """Determine optimal learning style"""
        
        if any(p.pattern == LearningPattern.RAPID_PROTOTYPER for p in patterns):
            return "project_based"
        
        if any(p.pattern == LearningPattern.DEEP_THINKER for p in patterns):
            return "sequential"
        
        if any(p.pattern == LearningPattern.SOCIAL_LEARNER for p in patterns):
            return "collaborative"
        
        return "adaptive"
    
    def _suggest_tracks(self, features: Dict, patterns: List[PatternSignature]) -> List[str]:
        """Suggest next tracks based on profile"""
        
        if any(p.pattern == LearningPattern.CONSISTENT_ACHIEVER for p in patterns):
            return ["ai-action-officer", "house-of-hearts"]
        
        if any(p.pattern == LearningPattern.NEEDS_SUPPORT for p in patterns):
            return ["innovation-foundations", "youth-energy"]
        
        return ["innovation-foundations", "ai-action-officer"]
    
    def _calculate_optimal_session(self, features: Dict) -> int:
        """Calculate optimal session length in minutes"""
        
        avg_duration = features["avg_session_duration"]
        
        if avg_duration > 180:
            return 90  # Reduce to prevent burnout
        elif avg_duration < 30:
            return 60  # Increase for better progress
        else:
            return int(avg_duration)


# Singleton instance
advanced_analytics = AdvancedLearningAnalytics()
