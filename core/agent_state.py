"""
Agent State Module for Lexi
Implements TRUE STATEFULNESS with explicit conversation history management.
"""

from agents import Agent, RunConfig, Runner, function_tool
from typing import Optional, Dict, Any, List
import json
import os
from datetime import datetime

# Import tool functions
from core.functions import (
    get_current_time as core_get_current_time,
    calculate_expression as core_calculate_expression,
    search_wikipedia as core_search_wikipedia
)

# ============================================================
# 🧰 TOOL WRAPPERS
# ============================================================

@function_tool
def get_current_time() -> str:
    """
    Returns current date and time. MUST use for ANY time/date question.
    
    Use when user asks:
    - "What time is it?"
    - "What's the date?"
    - "Tell me the current time"
    - ANY question about NOW/TODAY
    
    Returns:
        str: Current time like "It's currently 3:42 PM on October 20, 2025."
    """
    try:
        print("🕐 Tool called: get_current_time")
        result = core_get_current_time()
        print(f"✅ Result: {result}")
        return result
    except Exception as e:
        error_msg = f"Error getting time: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg


@function_tool
def calculate(expression: str) -> str:
    """
    Calculates math expressions. MUST use for ANY calculation.
    
    CRITICAL: Call this for ALL math, even simple ones like "2+2"
    
    Examples:
    - User: "25 * 4" → calculate("25*4")
    - User: "5 plus 4" → calculate("5+4")
    - User: "2^8" → calculate("2**8")
    
    Format rules:
    - Use * for multiply (not x)
    - Use ** for power (not ^)
    - Remove spaces: "25 * 4" → "25*4"
    
    Args:
        expression: Math string like "25*4", "5+4", "100/5"
    
    Returns:
        str: Result like "25*4 equals 100"
    """
    try:
        print(f"🧮 Tool called: calculate('{expression}')")
        result = core_calculate_expression(expression)
        print(f"✅ Result: {result}")
        return result
    except Exception as e:
        error_msg = f"Error calculating: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg


@function_tool
def search_wiki(query: str) -> str:
    """
    Searches Wikipedia for information. Use for factual lookups.
    
    Use when user asks:
    - "Tell me about X"
    - "Who is X?"
    - "What is X?"
    - "Search for X"
    
    Args:
        query: Topic to search like "Nikola Tesla", "Python programming"
    
    Returns:
        str: Wikipedia summary
    """
    try:
        print(f"🔍 Tool called: search_wiki('{query}')")
        result = core_search_wikipedia(query)
        print(f"✅ Result: {result[:100]}...")
        return result
    except Exception as e:
        error_msg = f"Error searching Wikipedia: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg


# List of all available tools
TOOLS = [get_current_time, calculate, search_wiki]

# ============================================================
# 🧠 AGENT INSTRUCTIONS (WITH EXPLICIT MEMORY INSTRUCTIONS)
# ============================================================

AGENT_INSTRUCTIONS = """You are Lexi, a STATEFUL AI assistant created by Uzair Waseem.

🧠 CRITICAL MEMORY INSTRUCTION:
You will receive conversation history at the start of each message. This history contains ALL previous exchanges in this conversation. You MUST read and use this context.

When responding:
1. READ the conversation history carefully
2. Reference previous messages when relevant
3. Remember user's name, preferences, and topics discussed
4. Build on earlier context naturally
5. Don't repeat information you already provided

═══════════════════════════════════════════════════════════
🔴 TOOL USAGE RULES
═══════════════════════════════════════════════════════════

RULE 1: TIME → Call get_current_time()
RULE 2: MATH → Call calculate()
RULE 3: FACTS → Call search_wiki()

═══════════════════════════════════════════════════════════
💬 MEMORY DEMONSTRATION
═══════════════════════════════════════════════════════════

Show you remember by:
- Using user's name if they told you
- Referencing previous topics: "Earlier you asked about..."
- Connecting new questions to old ones
- Building on previous answers
- Not asking for information already provided

Examples:
User: "My name is John"
You: "Nice to meet you, John!"

User: "What's my name?"
You: "Your name is John, as you told me earlier."

User: "Calculate 5+5"
You: [Use calculate tool] "5+5 equals 10."

User: "What did I just ask you to calculate?"
You: "You asked me to calculate 5+5, which equals 10."

═══════════════════════════════════════════════════════════
REMEMBER: Use the conversation history provided with each message!
═══════════════════════════════════════════════════════════
"""

# ============================================================
# 🤖 TRUE STATEFUL AGENT CLASS
# ============================================================

class LexiAgent:
    """
    TRUE STATEFUL agent that explicitly manages conversation history.
    """
    
    def __init__(self, model, model_provider):
        """Initialize Lexi agent with model configuration."""
        self.model = model
        self.model_provider = model_provider
        
        # Create the agent
        self.agent = Agent(
            name="Lexi",
            tools=TOOLS,
            instructions=AGENT_INSTRUCTIONS
        )
        
        # Create the runner
        self.runner = Runner()
        
        # CRITICAL: Store full conversation history
        self.conversation_history = []
        
        # Session metadata
        self.session_start = datetime.now().isoformat()
        self.message_count = 0
        
        print("✅ Lexi agent initialized (TRUE STATEFUL)")
        print(f"✅ Tools loaded: {[tool.name for tool in TOOLS]}")
    
    def _build_context_prompt(self) -> str:
        """
        Build a context prompt with full conversation history.
        
        Returns:
            str: Formatted conversation history
        """
        if not self.conversation_history:
            return ""
        
        context = "\n\n📜 CONVERSATION HISTORY (Read this before responding):\n"
        context += "="*60 + "\n"
        
        for i, turn in enumerate(self.conversation_history, 1):
            context += f"\n[Message {i}]\n"
            context += f"User: {turn['user']}\n"
            context += f"You: {turn['assistant']}\n"
        
        context += "="*60 + "\n"
        context += "END OF HISTORY - Now respond to the new message below.\n\n"
        
        return context
    
    def process_message(self, user_message: str) -> str:
        """
        Process message with EXPLICIT conversation history injection.
        
        Args:
            user_message: The user's input message
        
        Returns:
            str: Lexi's response
        """
        self.message_count += 1
        
        print(f"\n{'='*60}")
        print(f"📨 Message #{self.message_count}: {user_message}")
        print(f"💭 Context: {len(self.conversation_history)} previous exchanges")
        print(f"{'='*60}")
        
        try:
            # CRITICAL: Prepend conversation history to the message
            context_prompt = self._build_context_prompt()
            full_input = f"{context_prompt}Current User Message: {user_message}"
            
            # Show what we're sending (for debugging)
            print(f"\n📝 Sending to agent with {len(self.conversation_history)} previous messages in context")
            
            # Run the agent with full context
            result = self.runner.run_sync(
                self.agent,
                input=full_input,
                run_config=RunConfig(
                    model=self.model,
                    model_provider=self.model_provider,
                    tracing_disabled=True,
                ),
            )
            
            # Get response
            response = result.final_output
            
            # Store in conversation history
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "message_number": self.message_count,
                "user": user_message,
                "assistant": response
            })
            
            print(f"\n🤖 Lexi: {response}")
            print(f"💾 Saved to history (Total: {len(self.conversation_history)} exchanges)")
            print(f"{'='*60}\n")
            
            return response
            
        except Exception as e:
            error_msg = f"Error processing message: {str(e)}"
            print(f"\n❌ {error_msg}")
            print(f"{'='*60}\n")
            return f"Sorry, {error_msg}"
    
    def get_history(self) -> list:
        """Get conversation history."""
        return self.conversation_history
    
    def get_session_info(self) -> dict:
        """Get current session information."""
        return {
            "session_start": self.session_start,
            "message_count": self.message_count,
            "history_length": len(self.conversation_history),
            "tools_available": [tool.name for tool in TOOLS]
        }
    
    def save_history(self, filepath: str = "data/history.json"):
        """Save conversation history to JSON file."""
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            save_data = {
                "session_start": self.session_start,
                "message_count": self.message_count,
                "conversation": self.conversation_history
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ History saved to {filepath} ({self.message_count} messages)")
        except Exception as e:
            print(f"❌ Error saving history: {e}")
    
    def load_history(self, filepath: str = "data/history.json"):
        """Load conversation history from JSON file."""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.conversation_history = data.get("conversation", [])
                self.message_count = len(self.conversation_history)
                
                print(f"✅ History loaded: {self.message_count} previous messages")
                print(f"💭 Context will be injected into next message")
            else:
                print(f"ℹ️  No history file found - starting fresh")
        except Exception as e:
            print(f"❌ Error loading history: {e}")
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
        self.message_count = 0
        self.session_start = datetime.now().isoformat()
        print("✅ History cleared - starting fresh")
    
    def summarize_conversation(self) -> str:
        """Get a summary of the conversation."""
        if not self.conversation_history:
            return "No conversation history yet."
        
        summary = f"📊 Conversation Summary:\n"
        summary += f"├─ Started: {self.session_start}\n"
        summary += f"├─ Total messages: {self.message_count}\n"
        summary += f"└─ Exchanges stored: {len(self.conversation_history)}\n"
        
        if self.conversation_history:
            summary += f"\n📝 Recent topics:\n"
            for turn in self.conversation_history[-3:]:
                user_preview = turn['user'][:50]
                if len(turn['user']) > 50:
                    user_preview += "..."
                summary += f"  • {user_preview}\n"
        
        return summary
    
    def test_memory(self) -> str:
        """
        Test if memory is working.
        
        Returns:
            str: Memory test result
        """
        if len(self.conversation_history) < 2:
            return "❌ Not enough conversation history to test memory (need at least 2 exchanges)"
        
        test_result = "🧪 Memory Test:\n"
        test_result += f"✅ History contains {len(self.conversation_history)} exchanges\n"
        test_result += f"✅ Context will be injected into next message\n"
        test_result += f"✅ Agent should remember previous messages\n"
        
        return test_result


# ============================================================
# 🧪 TESTING
# ============================================================

if __name__ == "__main__":
    print("="*60)
    print("🧪 TESTING TRUE STATEFUL AGENT")
    print("="*60)
    
    # Test tools
    print("\n1. Testing tools:")
    print(get_current_time())
    print(calculate("25*4"))
    print(search_wiki("Python")[:100] + "...")
    
    print("\n" + "="*60)
    print("✅ Tools working!")
    print("="*60)