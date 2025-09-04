from google.adk.agents import Agent
import os
from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm
import json

def load_questions():
    # Get the directory where this file is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    questions_file = os.path.join(current_dir, 'questions', 'delivery_staff.json')
    with open(questions_file, 'r') as f:
        return json.load(f)

def get_question_by_id(question_id):
    questions_data = load_questions()
    for question in questions_data['questions']:
        if question['id'] == str(question_id):
            return question
    return None

def format_question_for_agent(question):
    """Format a question object for presentation by the agent"""
    if not question:
        return None
        
    # Handle matrix-style questions
    if question.get('type') == 'matrix':
        formatted = f"Question: {question['question']}\n\n"
        
        for sub_q in question.get('subQuestions', []):
            formatted += f"For {sub_q['title']}:\n"
            formatted += "Options:\n"
            for option in sub_q['options']:
                formatted += f"- {option}\n"
            formatted += "\n"
        
        return formatted.strip()
    
    # Handle regular questions
    formatted = f"Question: {question['question']}\n"
    
    if question.get('options') and len(question['options']) > 0:
        formatted += "Options:\n"
        for option in question['options']:
            if option.strip():  # Skip empty options
                formatted += f"- {option}\n"
    
    return formatted.strip()

def get_next_question_id(current_response):
    """Extract current question ID from response and return next question ID"""
    import re
    # Look for ID[number] pattern in the response
    match = re.search(r'ID\[(\d+)\]', current_response)
    if match:
        current_id = int(match.group(1))
        return current_id + 1
    return 1  # Start with question 1 if no ID found

delivery_staff_agent = Agent(
   name="delivery_staff_agent",
   description="Agent for managing delivery staff engagement - presents one question at a time",
    instruction=f"""
    You are Riva, a virtual assistant for TAFE NSW delivery staff.

    IMPORTANT RULES:
    1. Present ONLY ONE question at a time from the delivery staff questions when conducting the consultation.
    2. If the user just started or you see no ID in the conversation, start with question ID 1.
    3. If you see ID[X] in the previous conversation, present the question with ID X+1.
    4. Always end your response with "ID[current_question_number]" when presenting a question.
    5. If the user asks any other query (not related to the consultation questions), answer helpfully and informatively as Riva, using your general knowledge and context.
    6. For matrix-type questions, present all sub-questions together with their respective options, formatting as shown.
    7. When presenting the last question (ID[74]), summarize the entire conversation and send it to the LLM to generate insights. These insights should capture key points about education delivery, workforce trends, challenges, skills gaps, students, training needs, opportunities, future needs, and infrastructure across HWHS disciplines.

    Question format:
    Question: [question text]
    Options:
    - option 1
    - option 2
    - option 3

    Matrix question format:
    Question: [main question]
    
    For [sub-question 1]:
    Options:
    - option 1
    - option 2
    
    For [sub-question 2]:
    Options:
    - option 1
    - option 2

    ID[current_question_number]

    Available questions: {load_questions()}

    Start with question ID 1 unless you detect a previous question ID in the conversation.
    """,
   model="gemini-2.5-flash"
)

# Helper function to run the agent with a specific question
def get_agent_response_for_question(question_id, context=None):
    question = get_question_by_id(question_id)
    if not question:
        return f"Question with ID {question_id} not found."
    
    formatted_question = format_question_for_agent(question)
    # Here you would actually call the agent with the formatted question
    return formatted_question