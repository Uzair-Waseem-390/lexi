"""
Chainlit Application Handler
Manages STATEFUL chat interface and user interactions
"""

import chainlit as cl
from core.agent_state import LexiAgent
from config.openai_sdk import llm_model, external_client

# Global agent instance (maintains state per session)
lexi_agent = None


# ============================================================
# 🎬 CHAT START
# ============================================================

@cl.on_chat_start
async def start():
    """Initialize Lexi when chat starts"""
    global lexi_agent
    
    print("\n" + "="*60)
    print("🎬 NEW STATEFUL CHAT SESSION STARTED")
    print("="*60)
    
    # Create STATEFUL agent instance
    lexi_agent = LexiAgent(
        model=llm_model,
        model_provider=external_client
    )
    
    # Load previous history if exists
    lexi_agent.load_history()
    
    # Build welcome message
    welcome_msg = """👋 **Hi! I'm Lexi, your STATEFUL AI assistant.**

🧠 **I have memory!** I remember our entire conversation, so:
- You can refer back to previous topics
- I won't repeat myself unnecessarily
- We can build on our discussion naturally

---

**What I can do:**

🕐 **Get current time and date**  
Try: "What time is it?"

🧮 **Calculate math expressions**  
Try: "Calculate 25 * 4" or "What's 2 to the power of 8?"

📚 **Search Wikipedia**  
Try: "Tell me about Nikola Tesla"

💬 **Remember context**  
Try: Ask me something, then refer back to it later!

---

What would you like to know?"""
    
    await cl.Message(content=welcome_msg).send()
    
    # If history was loaded, show context
    if lexi_agent.message_count > 0:
        context_msg = f"""ℹ️ **Previous conversation loaded**
        
I remember our last {lexi_agent.message_count} messages. Feel free to continue where we left off!"""
        await cl.Message(content=context_msg).send()
    
    print("✅ Welcome message sent")


# ============================================================
# 💬 MESSAGE HANDLING (WITH STATE)
# ============================================================

@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages with full conversation context"""
    global lexi_agent
    
    if lexi_agent is None:
        await cl.Message(
            content="❌ Agent not initialized. Please refresh the page."
        ).send()
        return
    
    user_input = message.content
    
    # Special debug commands
    if user_input.lower() == "/memory":
        summary = lexi_agent.summarize_conversation()
        test = lexi_agent.test_memory()
        await cl.Message(content=f"{summary}\n\n{test}").send()
        return
    
    if user_input.lower() == "/clear":
        lexi_agent.clear_history()
        await cl.Message(content="✅ Memory cleared! Starting fresh.").send()
        return
    
    # Show thinking indicator with context info
    history_length = len(lexi_agent.get_history())
    
    msg = cl.Message(content="")
    await msg.send()
    
    # Process message through STATEFUL agent
    # The agent receives full conversation history injected into the prompt
    response = lexi_agent.process_message(user_input)
    
    # Update message with response
    msg.content = response
    await msg.update()
    
    # Save history after each message
    lexi_agent.save_history()
    
    # Show session info in console
    session_info = lexi_agent.get_session_info()
    print(f"📊 Session: {session_info['message_count']} messages, "
          f"{session_info['history_length']} in history")


# ============================================================
# 🎮 SPECIAL COMMANDS
# ============================================================

@cl.action_callback("show_context")
async def show_context():
    """Show current conversation context"""
    global lexi_agent
    
    if lexi_agent:
        summary = lexi_agent.summarize_conversation()
        await cl.Message(content=f"**Conversation Context:**\n\n{summary}").send()


@cl.action_callback("clear_history")
async def clear_history():
    """Clear conversation history"""
    global lexi_agent
    
    if lexi_agent:
        lexi_agent.clear_history()
        await cl.Message(
            content="✅ Conversation history cleared. Starting fresh!"
        ).send()


# ============================================================
# 👋 CHAT END
# ============================================================

@cl.on_chat_end
async def end():
    """Save history when chat ends"""
    global lexi_agent
    
    if lexi_agent:
        lexi_agent.save_history()
        
        # Print final summary
        print("\n" + "="*60)
        print("💾 CONVERSATION SAVED")
        print(lexi_agent.summarize_conversation())
        print("👋 CHAT SESSION ENDED")
        print("="*60 + "\n")


# ============================================================
# 🧪 TESTING
# ============================================================

if __name__ == "__main__":
    print("="*60)
    print("ℹ️  This module should be run via main.py")
    print("   Run: chainlit run main.py")
    print("="*60)