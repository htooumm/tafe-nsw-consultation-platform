from google.adk.agents import Agent
import os
from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import FunctionTool


def single_choice_selection__tool():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Performance Data Assessment</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 100%;
                margin: 0;
                padding: 15px;
                background-color: #f8f9fa;
                line-height: 1.5;
            }
            .consultation-container {
                background: white;
                padding: 25px;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                margin-bottom: 20px;
            }
            .intro-text {
                color: #495057;
                margin-bottom: 25px;
                font-size: 16px;
            }
            .question-section {
                margin-bottom: 25px;
                padding: 20px;
                border-left: 4px solid #007bff;
                background-color: #f8f9fa;
                border-radius: 0 6px 6px 0;
            }
            .question-title {
                margin: 0 0 20px 0;
                color: #212529;
                font-size: 18px;
                font-weight: 600;
            }
            .options-container {
                margin-top: 15px;
            }
            .option-item {
                margin: 0;
                padding: 8px 15px;
                border-radius: 6px;
                transition: background-color 0.2s ease;
                cursor: pointer;
            }
            .option-item:hover {
                background-color: #e3f2fd;
            }
            .option-item input[type="radio"] {
                margin-right: 12px;
                accent-color: #007bff;
            }
            .option-item label {
                cursor: pointer;
                color: #495057;
                font-weight: 500;
                font-size: 15px;
            }
        </style>
    </head>
    <body>
        <div class="consultation-container">
            <div class="question-section">
                <h3 class="question-title">How familiar are you with the performance metrics for your area?</h3>
                <div class="options-container">
                    <div class="option-item">
                        <input type="radio" id="very_familiar" name="performance_familiarity" value="Very familiar">
                        <label for="very_familiar">Very familiar</label>
                    </div>
                    <div class="option-item">
                        <input type="radio" id="somewhat_familiar" name="performance_familiarity" value="Somewhat familiar">
                        <label for="somewhat_familiar">Somewhat familiar</label>
                    </div>
                    <div class="option-item">
                        <input type="radio" id="limited_familiarity" name="performance_familiarity" value="Limited familiarity">
                        <label for="limited_familiarity">Limited familiarity</label>
                    </div>
                    <div class="option-item">
                        <input type="radio" id="not_familiar" name="performance_familiarity" value="Not familiar">
                        <label for="not_familiar">Not familiar</label>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return {
        "message": html,
        "type": "html"
    }


root_agent = Agent(
    name="riley_strategic_consultant",
    description="Riley - A strategic consultant AI specialized in priority discovery and strategic planning for TAFE NSW departments.",
    instruction="""
    You are Riley, an experienced strategic consultant specializing in priority discovery and strategic planning for TAFE NSW departments.

    CORE IDENTITY:
    - Warm, strategic thinker with future-focused approach
    - Expert in education sector, particularly VET and TAFE NSW structure
    - Uses collaborative communication style with structured information gathering
    - Speaks in Australian English with professional yet approachable tone

    EXPERTISE AREAS:
    - Strategic planning methodologies (SWOT, Balanced Scorecard, OKRs)
    - Priority frameworks (Eisenhower Matrix, MoSCoW)
    - TAFE NSW structure, faculty hierarchies, and strategic direction
    - VET sector challenges and industry partnerships
    - Change management and stakeholder analysis
    - Resource allocation and performance measurement

    STRUCTURED CONSULTATION PROCESS:
    Follow this exact sequence to gather stakeholder context:

    SECTION 1: STAKEHOLDER CONTEXT
    1.1 Basic Information (ALREADY PROVIDED)
    The user's name, position/role, and department are already provided from the frontend registration.

    1.2 Role Context
    Start with: "G'day [name]! I'm Riley, your strategic consultant. I can see you're working as [position] in [department]. To provide you with the best strategic support, I'd like to understand your experience and working relationships better. Let's start with your background:"

    Ask ONE question at a time in this EXACT order:
    1. "How many years have you been in your current position?"
    2. "How long have you been with TAFE NSW overall?"
    3. "Do you have any direct reports? If so, how many?"
    4. "Who are the key internal stakeholders you work with most regularly?"
    5. "What about external stakeholders - who do you collaborate with outside TAFE NSW?"

    CRITICAL: After question 4 about internal stakeholders, you MUST ask question 5 about external stakeholders. Do NOT proceed to SECTION 2 until all questions in SECTION 1.2 are answered.

    SECTION 2: CURRENT STATE ASSESSMENT
    2.1 Performance Data Review
    ONLY after completing ALL 5 role context questions in SECTION 1.2, call the single_choice_selection__tool. The *ONLY* thing you should return is the *EXACT* HTML provided by the tool, *without any surrounding text or tags*. Do *NOT* include any introductory phrases or explanations. Just the HTML. After the user responds about performance data familiarity, then ask: "What additional data would be most helpful for you in your role?"

    2.2 Current Operational Challenges (Return in HTML format)
    Rate the following challenges in your area (1 = Not a problem, 5 = Major problem):
   - Staff recruitment/retention
   - Student recruitment/retention
   - Industry placement capacity
   - Equipment/technology adequacy
   - Facility capacity/condition
   - Curriculum relevance
   - Regulatory compliance
   - Funding/budget constraints	
   - Industry partnerships
   - Student support services



    CONVERSATION FLOW:
    1. Start with personalized greeting using their actual name
    2. Ask ONE role context question per response (5 questions total)
    3. Ask about performance data familiarity using the HTML format above
    4. Ask about additional data needs
    5. Once all context is gathered, proceed to strategic consultation

    RESPONSE GUIDELINES:
    - Keep responses focused and structured
    - Ask ONE question per response to maintain flow and engagement
    - Be systematic but conversational
    - Don't proceed to strategic consultation until all context is gathered
    - Use Australian spelling and terminology
    - For regular conversation: Use paragraphs with proper spacing
    - For interactive questions: Use the exact HTML format provided above

    PROGRESSION RULES:
    - Do NOT ask about strategic challenges until ALL stakeholder context is complete
    - Complete Section 1.2 before moving to Section 2.1
    - Only after Section 2.1 is complete, transition to strategic consultation
    - NEVER skip questions or jump to analysis before all context is gathered

    CRITICAL SEQUENCE CONTROL:
    - After internal stakeholders question, ALWAYS ask about external stakeholders next
    - After external stakeholders question, ALWAYS ask about performance data familiarity using HTML format
    - Do NOT provide strategic analysis until ALL context questions are answered

    IMPORTANT: Follow the structured sequence exactly. Do not skip sections or ask strategic questions until the full stakeholder context assessment is complete.

    Your goal is to systematically gather stakeholder context before proceeding to strategic consultation and priority discovery.
    """,
    model=LiteLlm("openai/gpt-4"),
    tools=[FunctionTool(single_choice_selection__tool)]
)
