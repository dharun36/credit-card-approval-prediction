"""
Pytest configuration and fixtures for tests
"""
import sys
import os

# Add the parent directory to Python path so tests can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
