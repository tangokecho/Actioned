#!/usr/bin/env python3
# Load Testing Script for ActionEDx API
# Uses locust for distributed load testing

from locust import HttpUser, task, between
import json
import random

class ActionEDxUser(HttpUser):
    wait_time = between(1, 3)  # Wait 1-3 seconds between requests
    
    def on_start(self):
        """Called when a user starts"""
        self.user_id = f"load-test-user-{random.randint(1000, 9999)}"
    
    @task(10)
    def health_check(self):
        """Test health endpoint (high frequency)"""
        self.client.get("/api/health")
    
    @task(5)
    def get_tracks(self):
        """Test get tracks endpoint"""
        self.client.get("/api/tracks")
    
    @task(5)
    def get_analytics_patterns(self):
        """Test analytics patterns endpoint"""
        self.client.get("/api/analytics/patterns")
    
    @task(3)
    def get_user_analytics(self):
        """Test user analytics"""
        self.client.get(f"/api/analytics/user/{self.user_id}")
    
    @task(3)
    def generate_learning_path(self):
        """Test adaptive path generation"""
        self.client.post(
            f"/api/paths/generate-adaptive?user_id={self.user_id}&goal_track=innovation-foundations",
            json={"skill_level": "intermediate"},
            headers={"Content-Type": "application/json"}
        )
    
    @task(2)
    def chat_with_assistant(self):
        """Test AI assistant chat"""
        messages = [
            "Help me with strategy",
            "What are the 9 pillars?",
            "Generate a plan",
            "How do I start?"
        ]
        self.client.post(
            "/api/assistant/chat",
            json={
                "user_id": self.user_id,
                "message": random.choice(messages),
                "mode": "strategist"
            },
            headers={"Content-Type": "application/json"}
        )
    
    @task(1)
    def get_rate_limit_quota(self):
        """Test rate limit endpoint"""
        self.client.get(f"/api/rate-limit/quota/{self.user_id}?tier=free")
    
    @task(1)
    def get_circuit_breakers(self):
        """Test circuit breaker status"""
        self.client.get("/api/circuit-breakers")
    
    @task(1)
    def get_cache_stats(self):
        """Test cache statistics"""
        self.client.get("/api/cache/stats")

# Run with:
# locust -f load_test.py --host=https://actionedx-ai.preview.emergentagent.com
