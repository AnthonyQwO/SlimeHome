#!/usr/bin/env python3
# main.py - Entry point for the Slime Simulation Backend

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.api.app import start

if __name__ == "__main__":
    start()