# """
# Core Functions Module for Lexi Agent
# Implements the actual logic for all agent tools.

# Functions:
# 1. get_current_time() - Returns current date and time
# 2. calculate_expression() - Safely evaluates math expressions
# 3. search_wikipedia() - Searches Wikipedia and returns summaries
# """

# import datetime
# from sympy import sympify, SympifyError
# import wikipedia

# # Configure Wikipedia API
# wikipedia.set_rate_limiting(True)  # Prevents rate limit issues
# wikipedia.set_lang("en")  # English Wikipedia

# # ============================================================
# # 🕐 TIME FUNCTION
# # ============================================================

# def get_current_time() -> str:
#     """
#     Returns the current local date and time as a formatted string.
    
#     Returns:
#         str: Formatted time string (e.g., "It's currently 3:42 PM on October 20, 2025.")
    
#     Raises:
#         Exception: If datetime operations fail
#     """
#     try:
#         now = datetime.datetime.now()
#         formatted_time = now.strftime("%I:%M %p on %B %d, %Y")
        
#         print(f"[TIME] Retrieved: {formatted_time}")
        
#         return f"It's currently {formatted_time}."
    
#     except Exception as e:
#         print(f"[TIME] Error: {str(e)}")
#         raise Exception(f"Could not retrieve current time: {str(e)}")


# # ============================================================
# # 🧮 CALCULATION FUNCTION
# # ============================================================

# def calculate_expression(expression: str) -> str:
#     """
#     Safely evaluates a mathematical expression using SymPy.
    
#     Supports:
#     - Basic arithmetic: +, -, *, /
#     - Exponentiation: ** or ^
#     - Parentheses for grouping
#     - Common math functions: sqrt, sin, cos, etc.
    
#     Args:
#         expression: The math expression as a string (e.g., '25 * 4' or '2**8')
    
#     Returns:
#         str: Result in natural language (e.g., "25 * 4 equals 100")
    
#     Raises:
#         ValueError: If expression is invalid or unsafe
    
#     Examples:
#         >>> calculate_expression("25 * 4")
#         '25 * 4 equals 100'
#         >>> calculate_expression("2**10")
#         '2**10 equals 1024'
#         >>> calculate_expression("sqrt(144)")
#         'sqrt(144) equals 12'
#     """
#     if not expression or not isinstance(expression, str):
#         raise ValueError("Expression must be a non-empty string")
    
#     try:
#         # Use SymPy to safely parse and evaluate the expression
#         result = sympify(expression, evaluate=True)
        
#         # Ensure result is numeric
#         if not isinstance(result, (int, float)) and not result.is_number:
#             print(f"[CALC] Invalid result type for '{expression}': {type(result)}")
#             raise ValueError("Expression must evaluate to a number")
        
#         # Convert to float for consistency
#         numeric_result = float(result)
        
#         # Format result (remove .0 for whole numbers)
#         if numeric_result.is_integer():
#             formatted_result = int(numeric_result)
#         else:
#             formatted_result = round(numeric_result, 6)  # Limit decimal places
        
#         print(f"[CALC] '{expression}' = {formatted_result}")
        
#         return f"{expression} equals {formatted_result}."
    
#     except (SympifyError, ValueError, TypeError) as e:
#         print(f"[CALC] Error for '{expression}': {str(e)}")
#         raise ValueError(f"Could not calculate '{expression}': Invalid expression")
    
#     except Exception as e:
#         print(f"[CALC] Unexpected error for '{expression}': {str(e)}")
#         raise Exception(f"Calculation error: {str(e)}")


# # ============================================================
# # 📚 WIKIPEDIA SEARCH FUNCTION
# # ============================================================

# def search_wikipedia(query: str) -> str:
#     """
#     Searches Wikipedia and returns a concise summary.
    
#     Args:
#         query: The search term or topic (e.g., 'Nikola Tesla', 'Quantum Computing')
    
#     Returns:
#         str: Summary from Wikipedia with attribution
    
#     Raises:
#         Exception: If Wikipedia search fails for reasons other than disambiguation/not found
    
#     Examples:
#         >>> search_wikipedia("Nikola Tesla")
#         'According to Wikipedia, Nikola Tesla was a Serbian-American inventor...'
#     """
#     if not query or not isinstance(query, str):
#         raise ValueError("Query must be a non-empty string")
    
#     query = query.strip()
    
#     try:
#         # Get a 2-sentence summary from Wikipedia
#         summary = wikipedia.summary(query, sentences=2, auto_suggest=True)
        
#         print(f"[WIKI] Found summary for '{query}': {summary[:80]}...")
        
#         return f"According to Wikipedia, {summary}"
    
#     except wikipedia.exceptions.DisambiguationError as e:
#         # Multiple pages match - provide options
#         options = e.options[:5]  # Show top 5 matches
#         options_str = ", ".join(options)
        
#         print(f"[WIKI] Disambiguation for '{query}': {options}")
        
#         return (
#             f"Your query '{query}' could refer to multiple topics. "
#             f"Please be more specific. Did you mean: {options_str}?"
#         )
    
#     except wikipedia.exceptions.PageError:
#         # No page found
#         print(f"[WIKI] Page not found for '{query}'")
        
#         return (
#             f"I couldn't find a Wikipedia page for '{query}'. "
#             f"Please check the spelling or try a different search term."
#         )
    
#     except Exception as e:
#         # Unexpected error
#         print(f"[WIKI] Error searching for '{query}': {str(e)}")
#         raise Exception(f"Wikipedia search failed: {str(e)}")


# # ============================================================
# # 🧪 TESTING
# # ============================================================

# if __name__ == "__main__":
#     print("="*60)
#     print("🧪 TESTING CORE FUNCTIONS")
#     print("="*60 + "\n")
    
#     # Test 1: Time
#     print("Test 1: get_current_time()")
#     try:
#         time_result = get_current_time()
#         print(f"✅ {time_result}\n")
#     except Exception as e:
#         print(f"❌ Error: {e}\n")
    
#     # Test 2: Calculations
#     print("Test 2: calculate_expression()")
#     test_expressions = [
#         "25 * 4",
#         "2**10",
#         "sqrt(144)",
#         "(8 + 2) * 5",
#     ]
    
#     for expr in test_expressions:
#         try:
#             calc_result = calculate_expression(expr)
#             print(f"✅ {calc_result}")
#         except Exception as e:
#             print(f"❌ {expr}: {e}")
    
#     print()
    
#     # Test 3: Wikipedia
#     print("Test 3: search_wikipedia()")
#     test_queries = [
#         "Nikola Tesla",
#         "Python programming language",
#     ]
    
#     for query in test_queries:
#         try:
#             wiki_result = search_wikipedia(query)
#             print(f"✅ {wiki_result[:100]}...\n")
#         except Exception as e:
#             print(f"❌ {query}: {e}\n")
    
#     print("="*60)
#     print("✅ TESTING COMPLETED")
#     print("="*60)

"""
Core Functions Module for Lexi Agent
Implements the actual logic for all agent tools.
"""

import datetime
from sympy import sympify, SympifyError
import wikipedia

# Configure Wikipedia API
wikipedia.set_rate_limiting(True)
wikipedia.set_lang("en")

# ============================================================
# 🕐 TIME FUNCTION
# ============================================================

def get_current_time() -> str:
    """Returns the current local date and time as a formatted string."""
    try:
        now = datetime.datetime.now()
        formatted_time = now.strftime("%I:%M %p on %B %d, %Y")
        print(f"[TIME] Retrieved: {formatted_time}")
        return f"It's currently {formatted_time}."
    except Exception as e:
        print(f"[TIME] Error: {str(e)}")
        raise Exception(f"Could not retrieve current time: {str(e)}")


# ============================================================
# 🧮 CALCULATION FUNCTION
# ============================================================

def calculate_expression(expression: str) -> str:
    """Safely evaluates a mathematical expression using SymPy."""
    if not expression or not isinstance(expression, str):
        raise ValueError("Expression must be a non-empty string")
    
    try:
        result = sympify(expression, evaluate=True)
        
        if not isinstance(result, (int, float)) and not result.is_number:
            print(f"[CALC] Invalid result type for '{expression}': {type(result)}")
            raise ValueError("Expression must evaluate to a number")
        
        numeric_result = float(result)
        
        if numeric_result.is_integer():
            formatted_result = int(numeric_result)
        else:
            formatted_result = round(numeric_result, 6)
        
        print(f"[CALC] '{expression}' = {formatted_result}")
        return f"{expression} equals {formatted_result}."
    
    except (SympifyError, ValueError, TypeError) as e:
        print(f"[CALC] Error for '{expression}': {str(e)}")
        raise ValueError(f"Could not calculate '{expression}': Invalid expression")
    except Exception as e:
        print(f"[CALC] Unexpected error for '{expression}': {str(e)}")
        raise Exception(f"Calculation error: {str(e)}")


# ============================================================
# 📚 WIKIPEDIA SEARCH FUNCTION
# ============================================================

def search_wikipedia(query: str) -> str:
    """Searches Wikipedia and returns a concise summary."""
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string")
    
    query = query.strip()
    
    try:
        summary = wikipedia.summary(query, sentences=2, auto_suggest=True)
        print(f"[WIKI] Found summary for '{query}': {summary[:80]}...")
        return f"According to Wikipedia, {summary}"
    
    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options[:5]
        options_str = ", ".join(options)
        print(f"[WIKI] Disambiguation for '{query}': {options}")
        return (
            f"Your query '{query}' could refer to multiple topics. "
            f"Please be more specific. Did you mean: {options_str}?"
        )
    
    except wikipedia.exceptions.PageError:
        print(f"[WIKI] Page not found for '{query}'")
        return (
            f"I couldn't find a Wikipedia page for '{query}'. "
            f"Please check the spelling or try a different search term."
        )
    
    except Exception as e:
        print(f"[WIKI] Error searching for '{query}': {str(e)}")
        raise Exception(f"Wikipedia search failed: {str(e)}")


# ============================================================
# 🧪 TESTING
# ============================================================

if __name__ == "__main__":
    print("="*60)
    print("🧪 TESTING CORE FUNCTIONS")
    print("="*60 + "\n")
    
    # Test Time
    print("Test 1: get_current_time()")
    try:
        print(f"✅ {get_current_time()}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
    
    # Test Calculations
    print("Test 2: calculate_expression()")
    for expr in ["25*4", "2**10", "sqrt(144)", "(8+2)*5"]:
        try:
            print(f"✅ {calculate_expression(expr)}")
        except Exception as e:
            print(f"❌ {expr}: {e}")
    
    print()
    
    # Test Wikipedia
    print("Test 3: search_wikipedia()")
    for query in ["Nikola Tesla", "Python programming"]:
        try:
            result = search_wikipedia(query)
            print(f"✅ {result[:100]}...\n")
        except Exception as e:
            print(f"❌ {query}: {e}\n")
    
    print("="*60)
    print("✅ TESTING COMPLETED")
    print("="*60)