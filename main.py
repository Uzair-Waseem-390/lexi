"""
Lexi - AI Assistant with Tools
Main Entry Point

Created by Uzair Waseem

Run with: chainlit run main.py
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import Chainlit app (this registers all the handlers)
from config.chainlit_app import *

# ============================================================
# 🚀 STARTUP
# ============================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🤖 LEXI - AI ASSISTANT")
    print("="*60)
    print("Created by: Uzair Waseem")
    print("Model: Google Gemini 2.5 Flash")
    print("Framework: Chainlit + Agents SDK")
    print("="*60)
    print("\n🚀 Starting Chainlit server...")
    print("📝 Use: chainlit run main.py")
    print("\n" + "="*60 + "\n")
    
    # Chainlit will automatically use the handlers from chainlit_app.py
    # The actual server is started by the 'chainlit run' command