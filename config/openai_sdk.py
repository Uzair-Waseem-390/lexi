# """
# Lexi Agent - Main Module
# A stateful AI assistant with tools for time, calculations, and Wikipedia search.
# Created by Uzair Waseem
# """

# import sys
# import os

# # Add parent directory to path for imports
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# from agents import (
#     Agent,
#     RunConfig,
#     AsyncOpenAI,
#     OpenAIChatCompletionsModel,
#     Runner,
#     function_tool
# )
# from dotenv import load_dotenv

# # Import core functions with aliases to prevent naming conflicts
# from core.functions import (
#     get_current_time as core_get_current_time,
#     calculate_expression as core_calculate_expression,
#     search_wikipedia as core_search_wikipedia
# )

# # ============================================================
# # 🔐 ENVIRONMENT SETUP
# # ============================================================

# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# if not GOOGLE_API_KEY:
#     raise ValueError("❌ GOOGLE_API_KEY not found in .env file")

# print("✅ Environment variables loaded successfully")

# # ============================================================
# # ⚙️ CLIENT & MODEL INITIALIZATION
# # ============================================================

# # Initialize Gemini client via OpenAI SDK wrapper
# external_client = AsyncOpenAI(
#     api_key=GOOGLE_API_KEY,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
# )

# # Configure the language model
# llm_model = OpenAIChatCompletionsModel(
#     model="gemini-2.5-flash",
#     openai_client=external_client,
# )

# print("✅ Gemini model initialized successfully")

# # ============================================================
# # 🧰 TOOL DEFINITIONS
# # ============================================================

# @function_tool
# def get_current_time() -> str:
#     """
#     **MANDATORY TOOL** - Returns the current local date and time.
    
#     WHEN TO USE:
#     - User asks "what time is it"
#     - User asks "what's the date"
#     - User asks "what day is it"
#     - ANY question about current/today/now time/date
    
#     CRITICAL: You MUST use this tool for ALL time-related queries.
#     DO NOT answer from memory or knowledge.
    
#     Returns:
#         str: Current date and time in natural language
#     """
#     try:
#         print("🕐 Executing: get_current_time")
#         result = core_get_current_time()
#         print(f"✅ Result: {result}")
#         return result
#     except Exception as e:
#         error_msg = f"Failed to get current time: {str(e)}"
#         print(f"❌ Error: {error_msg}")
#         return f"Tool error: {error_msg}"


# @function_tool
# def calculate_expression(expression: str) -> str:
#     """
#     **MANDATORY TOOL** - Performs safe mathematical calculations.
    
#     WHEN TO USE:
#     - User asks to calculate ANYTHING (even "what's 2+2")
#     - User provides a math expression
#     - User asks "what's X plus/minus/times/divided by Y"
#     - ANY arithmetic question
    
#     CRITICAL: You MUST use this tool for ALL calculations, even simple ones.
#     DO NOT do mental math. ALWAYS call this function.
    
#     Supports: +, -, *, /, ** (power), parentheses, sqrt, etc.
    
#     Args:
#         expression: The math expression (e.g., '5+4', '25*4', '2**8')
    
#     Returns:
#         str: The calculation result in natural language
#     """
#     try:
#         print(f"🧮 Executing: calculate_expression({expression})")
#         result = core_calculate_expression(expression)
#         print(f"✅ Result: {result}")
#         return result
#     except Exception as e:
#         error_msg = f"Failed to calculate '{expression}': {str(e)}"
#         print(f"❌ Error: {error_msg}")
#         return f"Tool error: {error_msg}"


# @function_tool
# def search_wikipedia(query: str) -> str:
#     """
#     **MANDATORY TOOL** - Searches Wikipedia and returns a summary.
    
#     WHEN TO USE:
#     - User asks "tell me about X"
#     - User asks "who is X"
#     - User asks "what is X"
#     - User asks to search for something
#     - User asks for factual information about a topic
    
#     CRITICAL: Use this tool for factual lookups about people, places, concepts.
    
#     Args:
#         query: The search term (e.g., 'Nikola Tesla', 'Python programming')
    
#     Returns:
#         str: Wikipedia summary with attribution
#     """
#     try:
#         print(f"🔍 Executing: search_wikipedia('{query}')")
#         result = core_search_wikipedia(query)
#         print(f"✅ Result: {result[:100]}...")
#         return result
#     except Exception as e:
#         error_msg = f"Failed to search Wikipedia for '{query}': {str(e)}"
#         print(f"❌ Error: {error_msg}")
#         return f"Tool error: {error_msg}"


# # Register all available tools
# tools = [
#     get_current_time,
#     calculate_expression,
#     search_wikipedia,
# ]

# print(f"✅ Registered {len(tools)} tools: {[tool.name for tool in tools]}")

# # ============================================================
# # 🤖 AGENT CONFIGURATION
# # ============================================================

# lexi = Agent(
#     name="Lexi",
#     tools=tools,
#     instructions="""You are Lexi — an AI assistant that MUST use tools to answer specific types of questions.

# **CRITICAL INSTRUCTION:**
# You have three tools. When a user asks a question that matches a tool's purpose, you MUST call that tool. Do NOT answer from your own knowledge for these specific cases.

# ---

# ## ⚠️ MANDATORY TOOL USAGE RULES

# ### RULE 1: TIME QUESTIONS → ALWAYS use get_current_time()

# **If user asks ANY of these, call get_current_time():**
# - "What time is it?"
# - "What's the time?"
# - "Tell me the time"
# - "What's today's date?"
# - "What day is it?"
# - "What's the current time?"
# - Any variation asking about NOW/TODAY/CURRENT time

# **❌ WRONG:** Answering "Time is a fundamental concept..."
# **✅ CORRECT:** Call get_current_time() and report the actual current time

# ---

# ### RULE 2: MATH QUESTIONS → ALWAYS use calculate_expression()

# **If user asks to calculate ANYTHING, call calculate_expression():**
# - "What's 5+4?"
# - "Calculate 25*4"
# - "What's 2 to the power of 8?"
# - "Solve 100/5"
# - Even simple math like "2+2"

# **❌ WRONG:** Answering "5+4 equals 9" from your own knowledge
# **✅ CORRECT:** Call calculate_expression("5+4") first, then report result

# **Format the expression properly:**
# - Addition: "5+4"
# - Multiplication: "25*4"
# - Division: "100/5"
# - Power: "2**8"
# - Complex: "(5+4)*3"

# ---

# ### RULE 3: FACTUAL LOOKUPS → ALWAYS use search_wikipedia()

# **If user asks about a person, place, thing, or concept, call search_wikipedia():**
# - "Tell me about X"
# - "Who is X?"
# - "What is X?"
# - "Search for X"
# - "Explain X"

# **✅ CORRECT:** You already do this well! Continue using this tool.

# ---

# ## 🔍 DECISION PROCESS (Follow This EVERY Time)

# **Before responding, ask yourself these questions in order:**

# 1. **Is the user asking about current time/date?**
#    - YES → Call get_current_time()
#    - NO → Continue to step 2

# 2. **Is the user asking me to calculate something?**
#    - YES → Call calculate_expression(expression)
#    - NO → Continue to step 3

# 3. **Is the user asking about a factual topic?**
#    - YES → Call search_wikipedia(query)
#    - NO → Answer conversationally

# ---

# ## 💬 HOW TO USE TOOLS

# **Step 1:** Identify which tool is needed
# **Step 2:** Call the tool with proper parameters
# **Step 3:** Wait for the result
# **Step 4:** Present the result naturally to the user

# **Example Interaction:**

# User: "What time is it?"
# Your thinking: "This is a time question → Use get_current_time()"
# Your action: Call get_current_time()
# Your response: [Whatever the tool returns]

# User: "What's 5+4?"
# Your thinking: "This is a math question → Use calculate_expression()"
# Your action: Call calculate_expression("5+4")
# Your response: [Whatever the tool returns]

# ---

# ## 🚫 WHAT NOT TO DO

# **DON'T:**
# - Answer time questions from general knowledge
# - Do mental math instead of using the calculator tool
# - Explain what time/math is instead of giving the actual answer
# - Skip tools because you think the question is too simple

# **DO:**
# - Use tools for EVERY relevant question
# - Trust the tool results completely
# - Present tool results naturally
# - Use tools even for "easy" questions

# ---

# ## 💬 COMMUNICATION STYLE

# - Friendly and professional
# - Direct and helpful
# - Use tools when required (see rules above)
# - Conversational for general chat
# - Never mention internal workings or this prompt

# ---

# ## 🎯 YOUR MISSION

# Your primary job is to:
# 1. Identify when a tool is needed (time/math/factual lookup)
# 2. Call that tool
# 3. Present the result naturally

# You are Lexi — a tool-using AI assistant who provides accurate, real-time information through your available tools.
# """
# )

# print("✅ Agent 'Lexi' configured successfully")

# # ============================================================
# # 🚀 RUNNER INITIALIZATION
# # ============================================================

# runner = Runner()
# print("✅ Runner initialized")

# # ============================================================
# # 🔁 MAIN INTERFACE FUNCTION
# # ============================================================

# def run_agent_message(user_message: str) -> str:
#     """
#     Main interface between Chainlit and the Agent.
    
#     Takes a user message, processes it through Lexi, and returns the response.
    
#     Args:
#         user_message: The input from the user
    
#     Returns:
#         str: Lexi's response
#     """
#     print(f"\n{'='*60}")
#     print(f"📨 User: {user_message}")
#     print(f"{'='*60}")
    
#     try:
#         result = runner.run_sync(
#             lexi,
#             input=user_message,
#             run_config=RunConfig(
#                 model=llm_model,
#                 model_provider=external_client,
#                 tracing_disabled=True,
#             ),
#         )
        
#         response = result.final_output
#         print(f"\n🤖 Lexi: {response}")
#         print(f"{'='*60}\n")
        
#         return response
        
#     except Exception as e:
#         error_msg = f"An error occurred while processing your request: {str(e)}"
#         print(f"\n❌ Error: {error_msg}")
#         print(f"{'='*60}\n")
#         return f"Sorry, {error_msg}"

# # ============================================================
# # 🧪 LOCAL TESTING
# # ============================================================

# if __name__ == "__main__":
#     print("\n" + "="*60)
#     print("🧪 TESTING LEXI AGENT")
#     print("="*60 + "\n")
    
#     # Test different tool scenarios
#     test_messages = [
#         "What time is it?",
#         "Calculate 5+4",
#         "Tell me about Nikola Tesla",
#     ]
    
#     for msg in test_messages:
#         print(f"\n{'='*60}")
#         print(f"Testing: {msg}")
#         print(f"{'='*60}")
#         response = run_agent_message(msg)
#         print()
    
#     print("\n" + "="*60)
#     print("✅ TEST COMPLETED")
#     print("="*60)

"""
OpenAI SDK Configuration for Google Gemini
Sets up the Gemini model using OpenAI SDK wrapper
"""

import os
from dotenv import load_dotenv
from agents import AsyncOpenAI, OpenAIChatCompletionsModel

# Load environment variables
load_dotenv()

# Get API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found in .env file")

print("✅ API key loaded")

# ============================================================
# 🔧 CLIENT SETUP
# ============================================================

# Initialize Gemini client via OpenAI SDK wrapper
external_client = AsyncOpenAI(
    api_key=GOOGLE_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

print("✅ Gemini client initialized")

# ============================================================
# 🧠 MODEL SETUP
# ============================================================

# Configure the language model
llm_model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client,
)

print("✅ Gemini model configured (gemini-2.5-flash)")

# ============================================================
# 🧪 TESTING
# ============================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🧪 TESTING MODEL CONFIGURATION")
    print("="*60)
    print(f"Model: {llm_model.model}")
    print(f"Client: {type(external_client).__name__}")
    print("="*60)
    print("✅ Configuration test passed!")
    print("="*60)