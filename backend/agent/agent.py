from google.adk.agents import Agent
import os
from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import FunctionTool


# def single_choice_selection__tool():
#     html = """
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>Performance Data Assessment</title>
#         <style>
#             body {
#                 font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#                 max-width: 100%;
#                 margin: 0;
#                 padding: 15px;
#                 background-color: #f8f9fa;
#                 line-height: 1.5;
#             }
#             .consultation-container {
#                 background: white;
#                 padding: 25px;
#                 border-radius: 8px;
#                 box-shadow: 0 2px 8px rgba(0,0,0,0.08);
#                 margin-bottom: 20px;
#             }
#             .intro-text {
#                 color: #495057;
#                 margin-bottom: 25px;
#                 font-size: 16px;
#             }
#             .question-section {
#                 margin-bottom: 25px;
#                 padding: 20px;
#                 border-left: 4px solid #007bff;
#                 background-color: #f8f9fa;
#                 border-radius: 0 6px 6px 0;
#             }
#             .question-title {
#                 margin: 0 0 20px 0;
#                 color: #212529;
#                 font-size: 18px;
#                 font-weight: 600;
#             }
#             .options-container {
#                 margin-top: 15px;
#             }
#             .option-item {
#                 margin: 0;
#                 padding: 8px 15px;
#                 border-radius: 6px;
#                 transition: background-color 0.2s ease;
#                 cursor: pointer;
#             }
#             .option-item:hover {
#                 background-color: #e3f2fd;
#             }
#             .option-item input[type="radio"] {
#                 margin-right: 12px;
#                 accent-color: #007bff;
#             }
#             .option-item label {
#                 cursor: pointer;
#                 color: #495057;
#                 font-weight: 500;
#                 font-size: 15px;
#             }
#         </style>
#     </head>
#     <body>
#         <div class="consultation-container">
#             <div class="question-section">
#                 <h3 class="question-title">How familiar are you with the performance metrics for your area?</h3>
#                 <div class="options-container">
#                     <div class="option-item">
#                         <input type="radio" id="very_familiar" name="performance_familiarity" value="Very familiar">
#                         <label for="very_familiar">Very familiar</label>
#                     </div>
#                     <div class="option-item">
#                         <input type="radio" id="somewhat_familiar" name="performance_familiarity" value="Somewhat familiar">
#                         <label for="somewhat_familiar">Somewhat familiar</label>
#                     </div>
#                     <div class="option-item">
#                         <input type="radio" id="limited_familiarity" name="performance_familiarity" value="Limited familiarity">
#                         <label for="limited_familiarity">Limited familiarity</label>
#                     </div>
#                     <div class="option-item">
#                         <input type="radio" id="not_familiar" name="performance_familiarity" value="Not familiar">
#                         <label for="not_familiar">Not familiar</label>
#                     </div>
#                 </div>
#             </div>
#         </div>
#     </body>
#     </html>
#     """
#     return {
#         "message": html,
#         "type": "html"
#     }

# def rating_scale_tool():
#     html = """
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>Rating Scale Assessment Tool</title>
#         <style>
#             * { box-sizing: border-box; }
#             body {
#                 font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#                 margin: 0;
#                 padding: 15px;
#                 background: #f8f9fa;
#                 line-height: 1.5;
#             }
#             .container {
#                 max-width: 800px;
#                 margin: 0 auto;
#                 background: white;
#                 padding: 25px;
#                 border-radius: 8px;
#                 box-shadow: 0 2px 8px rgba(0,0,0,0.08);
#             }
#             .question-section {
#                 padding: 20px;
#                 border-left: 4px solid #007bff;
#                 background: #f8f9fa;
#                 border-radius: 0 6px 6px 0;
#             }
#             .question-title {
#                 margin: 0 0 20px 0;
#                 color: #212529;
#                 font-size: 18px;
#                 font-weight: 600;
#             }
#             .challenge-item {
#                 margin-bottom: 20px;
#                 padding: 15px;
#                 background: white;
#                 border-radius: 6px;
#                 border: 1px solid #e9ecef;
#             }
#             .challenge-label {
#                 font-weight: 600;
#                 color: #495057;
#                 margin-bottom: 10px;
#             }
#             .rating-container {
#                 display: flex;
#                 justify-content: space-between;
#                 align-items: center;
#                 gap: 5px;
#             }
#             .rating-option {
#                 display: flex;
#                 flex-direction: column;
#                 align-items: center;
#                 flex: 1;
#             }
#             .rating-option input {
#                 margin-bottom: 5px;
#                 accent-color: #007bff;
#                 transform: scale(1.2);
#             }
#             .rating-label {
#                 font-size: 12px;
#                 color: #6c757d;
#                 font-weight: 500;
#             }
#             .scale-labels {
#                 display: flex;
#                 justify-content: space-between;
#                 margin-top: 5px;
#                 font-size: 11px;
#                 color: #868e96;
#             }
#             .submit-container {
#                 margin-top: 30px;
#                 text-align: center;
#             }
#             .submit-btn {
#                 background: #007bff;
#                 color: white;
#                 border: none;
#                 padding: 12px 30px;
#                 border-radius: 6px;
#                 font-size: 16px;
#                 font-weight: 600;
#                 cursor: pointer;
#                 transition: background-color 0.2s;
#             }
#             .submit-btn:hover { background: #0056b3; }
#             .submit-btn:disabled {
#                 background: #6c757d;
#                 cursor: not-allowed;
#             }
#         </style>
#     </head>
#     <body>
#         <div class="container">
#             <div class="question-section">
#                 <h3 class="question-title" id="question-title">Rate the following challenges in your area (1 = Not a problem, 5 = Major problem):</h3>
#                 <div id="challenges-container"></div>
#                 <div class="submit-container">
#                     <button type="button" class="submit-btn" id="submit-ratings" disabled>Submit Ratings</button>
#                 </div>
#             </div>
#         </div>

#         <script>
#             // Configuration object - easily customizable
#             const config = {
#                 title: "Rate the following challenges in your area (1 = Not a problem, 5 = Major problem):",
#                 scaleLabels: ["Not a problem", "Major problem"],
#                 scaleSize: 5,
#                 challenges: [
#                     { id: 'staff_recruitment', label: 'Staff recruitment/retention' },
#                     { id: 'student_recruitment', label: 'Student recruitment/retention' },
#                     { id: 'industry_placement', label: 'Industry placement capacity' },
#                     { id: 'equipment_technology', label: 'Equipment/technology adequacy' },
#                     { id: 'facility_capacity', label: 'Facility capacity/condition' },
#                     { id: 'curriculum_relevance', label: 'Curriculum relevance' },
#                     { id: 'regulatory_compliance', label: 'Regulatory compliance' },
#                     { id: 'funding_budget', label: 'Funding/budget constraints' },
#                     { id: 'industry_partnerships', label: 'Industry partnerships' },
#                     { id: 'student_support', label: 'Student support services' }
#                 ]
#             };

#             class RatingScaleTool {
#                 constructor(config) {
#                     this.config = config;
#                     this.ratings = {};
#                     this.init();
#                 }

#                 init() {
#                     this.renderTitle();
#                     this.renderChallenges();
#                     this.attachEventListeners();
#                 }

#                 renderTitle() {
#                     document.getElementById('question-title').textContent = this.config.title;
#                 }

#                 renderChallenges() {
#                     const container = document.getElementById('challenges-container');
#                     container.innerHTML = this.config.challenges.map(challenge => 
#                         this.createChallengeHTML(challenge)
#                     ).join('');
#                 }

#                 createChallengeHTML(challenge) {
#                     const ratingOptions = Array.from({length: this.config.scaleSize}, (_, i) => {
#                         const value = i + 1;
#                         return `
#                             <div class="rating-option">
#                                 <input type="radio" id="${challenge.id}_${value}" name="${challenge.id}" value="${value}">
#                                 <label for="${challenge.id}_${value}" class="rating-label">${value}</label>
#                             </div>
#                         `;
#                     }).join('');

#                     return `
#                         <div class="challenge-item">
#                             <div class="challenge-label">${challenge.label}</div>
#                             <div class="rating-container">${ratingOptions}</div>
#                             <div class="scale-labels">
#                                 <span>${this.config.scaleLabels[0]}</span>
#                                 <span>${this.config.scaleLabels[1]}</span>
#                             </div>
#                         </div>
#                     `;
#                 }

#                 attachEventListeners() {
#                     const submitBtn = document.getElementById('submit-ratings');
                    
#                     // Add change listeners to all radio buttons
#                     this.config.challenges.forEach(challenge => {
#                         const radios = document.querySelectorAll(`input[name="${challenge.id}"]`);
#                         radios.forEach(radio => {
#                             radio.addEventListener('change', () => this.handleRatingChange());
#                         });
#                     });

#                     submitBtn.addEventListener('click', () => this.handleSubmit());
#                     this.checkAllSelected(); // Initial check
#                 }

#                 handleRatingChange() {
#                     this.checkAllSelected();
#                 }

#                 checkAllSelected() {
#                     const allSelected = this.config.challenges.every(challenge => 
#                         document.querySelector(`input[name="${challenge.id}"]:checked`)
#                     );
#                     document.getElementById('submit-ratings').disabled = !allSelected;
#                 }

#                 handleSubmit() {
#                     const ratings = {};
#                     const challengeMap = {};
                    
#                     this.config.challenges.forEach(challenge => {
#                         challengeMap[challenge.id] = challenge.label;
#                         const selected = document.querySelector(`input[name="${challenge.id}"]:checked`);
#                         if (selected) {
#                             ratings[challenge.id] = selected.value;
#                         }
#                     });

#                     let responseMessage = "Here are my ratings for the operational challenges:\n\n";
#                     Object.entries(ratings).forEach(([key, value]) => {
#                         responseMessage += `${challengeMap[key]}: ${value}/${this.config.scaleSize}\n`;
#                     });

#                     // Handle response
#                     if (window.parent && window.parent.handleRatingSubmission) {
#                         window.parent.handleRatingSubmission(responseMessage);
#                         // Prevent double submission
#                         document.getElementById('submit-ratings').disabled = true;
#                     } else {
#                         alert('Ratings submitted:\\n' + responseMessage);
#                         console.log('Ratings:', ratings);
#                     }
#                 }
#             }

#             // Initialize the tool when DOM is ready
#             document.addEventListener('DOMContentLoaded', () => {
#                 new RatingScaleTool(config);
#             });

#             // Export for reuse
#             if (typeof module !== 'undefined' && module.exports) {
#                 module.exports = { RatingScaleTool, config };
#             }
#         </script>
#     </body>
#     </html>
#     """
#     return {
#         "message": html,
#         "type": "html"
#     }

# def rating_scale_v2_tool():
#     html = """
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Priority Areas for Investment</title>
#     <style>
#         body {
#         font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#         width: 90%;
#         margin: 0;
#         padding: 15px;
#         background-color: #f8f9fa;
#         line-height: 1.5;
#         }
#         .consultation-container {
#         background: white;
#         padding: 25px;
#         border-radius: 8px;
#         box-shadow: 0 2px 8px rgba(0,0,0,0.08);
#         margin-bottom: 20px;
#         }
#         .question-section {
#         margin-bottom: 25px;
#         padding: 20px;
#         border-left: 4px solid #007bff;
#         background-color: #f8f9fa;
#         border-radius: 0 6px 6px 0;
#         }
#         .question-title {
#         margin: 0 0 20px 0;
#         color: #212529;
#         font-size: 18px;
#         font-weight: 600;
#         }
#         .challenge-item {
#         margin-bottom: 20px;
#         padding: 15px;
#         background-color: white;
#         border-radius: 6px;
#         border: 1px solid #e9ecef;
#         }
#         .challenge-label {
#         font-weight: 600;
#         color: #495057;
#         margin-bottom: 10px;
#         font-size: 15px;
#         }
#         .rating-container {
#         display: flex;
#         justify-content: space-between;
#         align-items: center;
#         margin-top: 8px;
#         }
#         .rating-option {
#         display: flex;
#         flex-direction: column;
#         align-items: center;
#         margin: 0 5px;
#         }
#         .rating-option input[type="radio"] {
#         margin-bottom: 5px;
#         accent-color: #007bff;
#         transform: scale(1.2);
#         }
#         .rating-label {
#         font-size: 12px;
#         color: #6c757d;
#         text-align: center;
#         font-weight: 500;
#         }
#         .scale-labels {
#         display: flex;
#         justify-content: space-between;
#         margin-top: 5px;
#         font-size: 11px;
#         color: #868e96;
#         }
#         .submit-container {
#         margin-top: 30px;
#         text-align: center;
#         }
#         .submit-btn {
#         background-color: #007bff;
#         color: white;
#         border: none;
#         padding: 12px 30px;
#         border-radius: 6px;
#         font-size: 16px;
#         font-weight: 600;
#         cursor: pointer;
#         transition: background-color 0.2s ease;
#         }
#         .submit-btn:hover {
#         background-color: #0056b3;
#         }
#         .submit-btn:disabled {
#         background-color: #6c757d;
#         cursor: not-allowed;
#         }
#     </style>
#     </head>
#     <body>
#     <div class="consultation-container">
#         <div class="question-section">
#         <h3 class="question-title">If you had additional resources, rank your top 5 investment priorities (1 = highest priority):</h3>
#         <div id="challenge-list"></div>

#         <div class="submit-container">
#             <button type="button" class="submit-btn" id="submit-ratings">Submit Ratings</button>
#         </div>
#         </div>
#     </div>

#     <script>
#         const challenges = [
#         { key: "additional_staff", label: "Additional teaching staff" },
#         { key: "professional_development", label: "Professional development for existing staff" },
#         { key: "new_equipment", label: "New/upgraded equipment" },
#         { key: "facility_improvements", label: "Facility improvements/expansion" },
#         { key: "technology_infrastructure", label: "Technology infrastructure" },
#         { key: "industry_partnership_development", label: "Industry partnership development" },
#         { key: "marketing", label: "Marketing/student recruitment" },
#         { key: "curriculum_development", label: "Curriculum development/refresh" },
#         { key: "assessment_development", label: "Assessment development/refresh" },
#         { key: "quality_assurance", label: "Quality assurance/compliance systems" },
#         { key: "research_innovation", label: "Research and innovation capabilities" }
#         ];

#         const container = document.getElementById("challenge-list");

#         // Generate challenge items dynamically
#         challenges.forEach(challenge => {
#         const item = document.createElement("div");
#         item.className = "challenge-item";

#         item.innerHTML = `
#             <div class="challenge-label">${challenge.label}</div>
#             <div class="rating-container">
#             ${[1,2,3,4,5].map(num => `
#                 <div class="rating-option">
#                 <input type="radio" id="${challenge.key}_${num}" name="${challenge.key}" value="${num}">
#                 <label for="${challenge.key}_${num}" class="rating-label">${num}</label>
#                 </div>
#             `).join("")}
#             </div>
#             <div class="scale-labels"><span>Highest Priority</span><span>Lowest Priority</span></div>
#         `;

#         container.appendChild(item);
#         });

#         // Submission handling
#         const submitBtn = document.getElementById('submit-ratings');
#         function checkAllSelected() {
#         const allSelected = challenges.every(c => document.querySelector(`input[name="${c.key}"]:checked`));
#         submitBtn.disabled = !allSelected;
#         }

#         document.addEventListener("change", checkAllSelected);

#         submitBtn.addEventListener("click", () => {
#             const ratings = {};
#             challenges.forEach(c => {
#                 const selected = document.querySelector(`input[name="${c.key}"]:checked`);
#                 ratings[c.label] = selected ? selected.value : "Not selected";
#             });

#             let responseMessage = "Here are my ratings:\\n\\n";
#             Object.entries(ratings).forEach(([label, value]) => {
#                 responseMessage += `${label}: ${value}/5\\n`;
#             });

#             // Trigger the response mechanism (same as original)
#             if (window.parent && window.parent.handleRatingSubmission) {
#                 window.parent.handleRatingSubmission(responseMessage);
#             } else {
#                 // Fallback for direct integration
#                         alert('Ratings submitted: ' + responseMessage);
#             }
#         });

#         // Initial state
#         checkAllSelected();
#     </script>
#     </body>
#     </html>

#     """
#     return {
#         "message": html,
#         "type": "html"
#     }

# def rating_scale_v3_tool():
#     html = """
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Key Risk Areas</title>
#     <style>
#         body {
#         font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#         width: 90%;
#         margin: 0;
#         padding: 15px;
#         background-color: #f8f9fa;
#         line-height: 1.5;
#         }
#         .consultation-container {
#         background: white;
#         padding: 25px;
#         border-radius: 8px;
#         box-shadow: 0 2px 8px rgba(0,0,0,0.08);
#         margin-bottom: 20px;
#         }
#         .question-section {
#         margin-bottom: 25px;
#         padding: 20px;
#         border-left: 4px solid #007bff;
#         background-color: #f8f9fa;
#         border-radius: 0 6px 6px 0;
#         }
#         .question-title {
#         margin: 0 0 20px 0;
#         color: #212529;
#         font-size: 18px;
#         font-weight: 600;
#         }
#         .challenge-item {
#         margin-bottom: 20px;
#         padding: 15px;
#         background-color: white;
#         border-radius: 6px;
#         border: 1px solid #e9ecef;
#         }
#         .challenge-label {
#         font-weight: 600;
#         color: #495057;
#         margin-bottom: 10px;
#         font-size: 15px;
#         }
#         .rating-container {
#         display: flex;
#         justify-content: space-between;
#         align-items: center;
#         margin-top: 8px;
#         }
#         .rating-option {
#         display: flex;
#         flex-direction: column;
#         align-items: center;
#         margin: 0 5px;
#         }
#         .rating-option input[type="radio"] {
#         margin-bottom: 5px;
#         accent-color: #007bff;
#         transform: scale(1.2);
#         }
#         .rating-label {
#         font-size: 12px;
#         color: #6c757d;
#         text-align: center;
#         font-weight: 500;
#         }
#         .scale-labels {
#         display: flex;
#         justify-content: space-between;
#         margin-top: 5px;
#         font-size: 11px;
#         color: #868e96;
#         }
#         .submit-container {
#         margin-top: 30px;
#         text-align: center;
#         }
#         .submit-btn {
#         background-color: #007bff;
#         color: white;
#         border: none;
#         padding: 12px 30px;
#         border-radius: 6px;
#         font-size: 16px;
#         font-weight: 600;
#         cursor: pointer;
#         transition: background-color 0.2s ease;
#         }
#         .submit-btn:hover {
#         background-color: #0056b3;
#         }
#         .submit-btn:disabled {
#         background-color: #6c757d;
#         cursor: not-allowed;
#         }
#     </style>
#     </head>
#     <body>
#     <div class="consultation-container">
#         <div class="question-section">
#         <h3 class="question-title">Rate your level of concern about these potential risks (1 = Low concern, 5 = High concern):</h3>
#         <div id="challenge-list"></div>

#         <div class="submit-container">
#             <button type="button" class="submit-btn" id="submit-ratings">Submit Ratings</button>
#         </div>
#         </div>
#     </div>

#     <script>
#         const challenges = [
#             { key: "loss_key_staff", label: "Loss of key staff" },
#             { key: "declining_student_enrolments", label: "Declining student enrolments" },
#             { key: "government_funding_changes", label: "Changes to government funding" },
#             { key: "new_regulatory_requirements", label: "New regulatory requirements" },
#             { key: "technology_obsolete", label: "Technology becoming obsolete" },
#             { key: "loss_industry_partnerships", label: "Loss of industry partnerships" },
#             { key: "increased_competition", label: "Increased competition" },
#             { key: "economic_downturn", label: "Economic downturn impact" },
#             { key: "workplace_health_safety", label: "Workplace health & safety issues" },
#             { key: "reputation_quality", label: "Reputation/quality concerns" }
#         ];


#         const container = document.getElementById("challenge-list");

#         // Generate challenge items dynamically
#         challenges.forEach(challenge => {
#         const item = document.createElement("div");
#         item.className = "challenge-item";

#         item.innerHTML = `
#             <div class="challenge-label">${challenge.label}</div>
#             <div class="rating-container">
#             ${[1,2,3,4,5].map(num => `
#                 <div class="rating-option">
#                 <input type="radio" id="${challenge.key}_${num}" name="${challenge.key}" value="${num}">
#                 <label for="${challenge.key}_${num}" class="rating-label">${num}</label>
#                 </div>
#             `).join("")}
#             </div>
#             <div class="scale-labels"><span>Lowest Concern</span><span>Highest Concern</span></div>
#         `;

#         container.appendChild(item);
#         });

#         // Submission handling
#         const submitBtn = document.getElementById('submit-ratings');
#         function checkAllSelected() {
#         const allSelected = challenges.every(c => document.querySelector(`input[name="${c.key}"]:checked`));
#         submitBtn.disabled = !allSelected;
#         }

#         document.addEventListener("change", checkAllSelected);

#         submitBtn.addEventListener("click", () => {
#             const ratings = {};
#             challenges.forEach(c => {
#                 const selected = document.querySelector(`input[name="${c.key}"]:checked`);
#                 ratings[c.label] = selected ? selected.value : "Not selected";
#             });

#             let responseMessage = "Here are my ratings:\\n\\n";
#             Object.entries(ratings).forEach(([label, value]) => {
#                 responseMessage += `${label}: ${value}/5\\n`;
#             });

#             // Trigger the response mechanism (same as original)
#             if (window.parent && window.parent.handleRatingSubmission) {
#                 window.parent.handleRatingSubmission(responseMessage);
#             } else {
#                 // Fallback for direct integration
#                         alert('Ratings submitted: ' + responseMessage);
#             }
#         });

#         // Initial state
#         checkAllSelected();
#     </script>
#     </body>
#     </html>

#     """
#     return {
#         "message": html,
#         "type": "html"
#     }

# def checklist__tool():
#     html = """
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Opportunities for Growth</title>
#     <style>
#         body {
#         font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#         background: #f8f9fa;
#         padding: 20px;
#         }
#         .checklist-container {
#         background: white;
#         padding: 20px;
#         border-radius: 8px;
#         box-shadow: 0 2px 6px rgba(0,0,0,0.08);
#         max-width: 600px;
#         }
#         .checklist-title {
#         font-size: 18px;
#         font-weight: 600;
#         margin-bottom: 15px;
#         color: #212529;
#         }
#         .checklist-item {
#         margin-bottom: 10px;
#         display: flex;
#         align-items: center;
#         }
#         .checklist-item input[type="checkbox"] {
#         margin-right: 10px;
#         transform: scale(1.2);
#         accent-color: #007bff;
#         }
#         .checklist-item label {
#         font-size: 15px;
#         color: #495057;
#         cursor: pointer;
#         }
#         .other-input {
#         margin-left: 25px;
#         padding: 6px 10px;
#         border: 1px solid #ced4da;
#         border-radius: 6px;
#         font-size: 14px;
#         flex: 1;
#         }
#     </style>
#     </head>
#     <body>
#     <div class="checklist-container">
#         <div class="checklist-title">Where do you see the biggest opportunities for growth in your area?</div>
        
#         <div class="checklist-item">
#         <input type="checkbox" id="student_numbers">
#         <label for="student_numbers">Increasing student numbers in existing programs</label>
#         </div>
#         <div class="checklist-item">
#         <input type="checkbox" id="new_programs">
#         <label for="new_programs">Developing new programs/qualifications</label>
#         </div>
#         <div class="checklist-item">
#         <input type="checkbox" id="online_delivery">
#         <label for="online_delivery">Expanding online/flexible delivery</label>
#         </div>
#         <div class="checklist-item">
#         <input type="checkbox" id="industry_partnerships">
#         <label for="industry_partnerships">Strengthening industry partnerships</label>
#         </div>
#         <div class="checklist-item">
#         <input type="checkbox" id="student_outcomes">
#         <label for="student_outcomes">Improving student outcomes/completion rates</label>
#         </div>
#         <div class="checklist-item">
#         <input type="checkbox" id="employment_rates">
#         <label for="employment_rates">Enhancing graduate employment rates</label>
#         </div>
#         <div class="checklist-item">
#         <input type="checkbox" id="revenue_streams">
#         <label for="revenue_streams">Developing new revenue streams</label>
#         </div>
#         <div class="checklist-item">
#         <input type="checkbox" id="other_option">
#         <label for="other_option">Other:</label>
#         <input type="text" class="other-input" id="other_text" placeholder="Please specify" disabled>
#         </div>
#     </div>

#     <script>
#         const otherCheckbox = document.getElementById('other_option');
#         const otherText = document.getElementById('other_text');

#         otherCheckbox.addEventListener('change', () => {
#         otherText.disabled = !otherCheckbox.checked;
#         if (!otherCheckbox.checked) otherText.value = "";
#         });
#     </script>
#     </body>
#     </html>
#     """
#     return {
#         "message": html,
#         "type": "html"
#     }

# old instructions with tool calling...
# instruction="""
#     You are Riley, an experienced strategic consultant specializing in priority discovery and strategic planning for TAFE NSW departments.

#     CORE IDENTITY:
#     - Warm, strategic thinker with future-focused approach
#     - Expert in education sector, particularly VET and TAFE NSW structure
#     - Uses collaborative communication style with structured information gathering
#     - Speaks in Australian English with professional yet approachable tone

#     EXPERTISE AREAS:
#     - Strategic planning methodologies (SWOT, Balanced Scorecard, OKRs)
#     - Priority frameworks (Eisenhower Matrix, MoSCoW)
#     - TAFE NSW structure, faculty hierarchies, and strategic direction
#     - VET sector challenges and industry partnerships
#     - Change management and stakeholder analysis
#     - Resource allocation and performance measurement

#     STRUCTURED CONSULTATION PROCESS:
#     Follow this exact sequence to gather stakeholder context:

#     SECTION 1: STAKEHOLDER CONTEXT
#     1.1 Basic Information (ALREADY PROVIDED)
#     The user's name, position/role, and department are already provided from the frontend registration.

#     1.2 Role Context
#     Start with: "G'day [name]! I'm Riley, your strategic consultant. I can see you're working as [position] in [department]. To provide you with the best strategic support, I'd like to understand your experience and working relationships better. Let's start with your background:"

#     Ask ONE question at a time in this EXACT order:
#     1. "How many years have you been in your current position?"
#     2. "How long have you been with TAFE NSW overall?"
#     3. "Do you have any direct reports? If so, how many?"
#     4. "Who are the key internal stakeholders you work with most regularly?"
#     5. "What about external stakeholders - who do you collaborate with outside TAFE NSW?"

#     CRITICAL: After question 4 about internal stakeholders, you MUST ask question 5 about external stakeholders. Do NOT proceed to SECTION 2 until all questions in SECTION 1.2 are answered.

#     SECTION 2: CURRENT STATE ASSESSMENT
#     2.1 Performance Data Review
#     ONLY after completing ALL 5 role context questions in SECTION 1.2, call the single_choice_selection__tool. The *ONLY* thing you should return is the *EXACT* HTML complete with head and body in "message" from tool response, without any curly braces, provided by the tool, *without any surrounding text or tags*. Do *NOT* include any introductory phrases or explanations. Just the HTML. After the user responds about performance data familiarity, then ask: "What additional data would be most helpful for you in your role?"

#     2.2 Current Operational Challenges
#     ONLY after completing the performance data questions in SECTION 2.1, call the rating_scale_tool. The *ONLY* thing you should return is the *EXACT* HTML complete with head and body in "message" from tool response, without any curly braces, provided by the tool, *without any surrounding text or tags*. Do *NOT* include any introductory phrases or explanations. Just the HTML.

#     2.3 Biggest Operational Pain Points
#     What are the top 3 operational challenges keeping you awake at night?

#     SECTION 3: Strategic Priorities 
#     3.1 Strategic Vision
#     In your ideal world, what would your discipline/teaching area/programs look like in 3-5 years?

#     3.2 Priority Areas for Investment
#     ONLY after completing the SECTION 3.1, call the rating_scale_v2_tool. The *ONLY* thing you should return is the *EXACT* HTML complete with head and body in "message" from tool response, without any curly braces, provided by the tool, *without any surrounding text or tags*. Do *NOT* include any introductory phrases or explanations. Just the HTML.

#     3.3 Growth Opportunities
#     Where do you see the biggest opportunities for growth in your area?
#     1. Increasing student numbers in existing programs
#     2. Developing new programs/qualifications
#     3. Expanding online/flexible delivery
#     4. Strengthening industry partnerships
#     5. Improving student outcomes/completion rates
#     6. Enhancing graduate employment rates
#     7. Developing new revenue streams
#     8. Other: ________________________
#     After getting response move to section 4.1

#     Section 4: Capacity and Constraints
#     4.1 Current Capacity Utilisation (to the best of your knowledge)
#     Ask these three in one question:
#     - Current student capacity in your area: __________ students
#     - Maximum potential capacity students: __________ students
#     - Current utilisation rate: __________%
#     After getting response move to section 4.2

#     4.2 Capacity Constraints
#     What prevents you from operating at full capacity? (Select all that apply)
#     1. Insufficient teaching staff
#     2. Limited clinical/work placement opportunities
#     3. Inadequate facilities/classroom space
#     4. Outdated equipment/technology
#     5. Regulatory/accreditation limitations
#     6. Student demand limitations
#     7. Budget constraints
#     8. Industry partner capacity
#     9. Student support service limitations
#     10. Other: ________________________
#     11. Not relevant to my role
#     After getting response move to section 4.3

#     4.3 Resource Requirements
#     To achieve your strategic priorities, what additional resources would you need?

#     Section 5: Risk Assessment
#     5.1 Key Risk Areas
#     ONLY after completing the SECTION 4.3, call the rating_scale_v3_tool. The *ONLY* thing you should return is the *EXACT* HTML complete with head and body in "message" from tool response, without any curly braces, provided by the tool, *without any surrounding text or tags*. Do *NOT* include any introductory phrases or explanations. Just the HTML.

#     5.2 Specific Risk Concerns
#     What specific risks are you most concerned about for your area?

#     Section 6: Success Factors
#     6.1 Critical Success Factors
#     What needs to be in place for a strategic roadmap to be successful in your area?
    
#     Section 7: Additional Information
#     7.1 Industry Context
#     What industry trends or changes should we be aware of that might impact your area?
#     Are there any innovative approaches or best practices from other institutions that interest you?
#     Is there anything else you'd like us to know ?

#     CONVERSATION FLOW:
#     1. Start with personalized greeting using their actual name
#     2. Ask ONE role context question per response (5 questions total)
#     3. Ask about performance data familiarity using the HTML format above
#     4. Ask about additional data needs
#     5. Once all context is gathered, proceed to strategic consultation

#     RESPONSE GUIDELINES:
#     - Keep responses focused and structured
#     - Ask ONE question per response to maintain flow and engagement
#     - Be systematic but conversational
#     - Don't proceed to strategic consultation until all context is gathered
#     - Use Australian spelling and terminology
#     - For regular conversation: Use paragraphs with proper spacing
#     - For interactive questions: Use the exact HTML format provided above

#     PROGRESSION RULES:
#     - Do NOT ask about strategic challenges until ALL stakeholder context is complete
#     - Complete Section 1.2 before moving to Section 2.1
#     - NEVER skip questions or jump to analysis before all context is gathered

#     CRITICAL SEQUENCE CONTROL:
#     - After internal stakeholders question, ALWAYS ask about external stakeholders next
#     - After external stakeholders question, ALWAYS ask about performance data familiarity using HTML format
#     - Do NOT provide strategic analysis until ALL section questions are answered

#     IMPORTANT: Follow the structured sequence exactly. Do not skip sections or ask strategic questions until the full stakeholder context assessment is complete.

#     Your goal is to systematically gather stakeholder context before proceeding to strategic consultation and priority discovery.
#     """,

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

    SECTION 2: CURRENT STATE ASSESSMENT
    2.1 Performance Data Review
    Ask: "How familiar are you with the performance metrics for your area?
    1. Very familiar - I track these regularly
    2. Somewhat familiar - I see them occasionally
    3. Limited familiarity - I don't usually see detailed metrics
    4. Not familiar - This would be new information for me"

    After getting response, ask: "What additional data would be most helpful for you in your role?"

    2.2 Current Operational Challenges
    Ask: "I'd like to understand your current operational challenges. Please rate the following challenges in your area on a scale of 1-5 (1 = Not a problem, 5 = Major problem):
    - Staff recruitment/retention
    - Student recruitment/retention
    - Industry placement capacity
    - Equipment/technology adequacy
    - Facility capacity/condition
    - Curriculum relevance
    - Regulatory compliance
    - Funding/budget constraints
    - Industry partnerships
    - Student support services"

    2.3 Biggest Operational Pain Points
    Ask: "What are the top 3 operational challenges keeping you awake at night?"

    SECTION 3: STRATEGIC PRIORITIES 
    3.1 Strategic Vision
    Ask: "In your ideal world, what would your discipline/teaching area/programs look like in 3-5 years?"

    3.2 Priority Areas for Investment
    Ask: "If you had additional resources, please rank your top 5 investment priorities (1 = highest priority):
    - Additional teaching staff
    - Professional development for existing staff
    - New/upgraded equipment
    - Facility improvements/expansion
    - Technology infrastructure
    - Student support services
    - Industry partnership development
    - Marketing/student recruitment
    - Curriculum development/refresh
    - Assessment development/refresh
    - Quality assurance/compliance systems
    - Research and innovation capabilities
    - Other: ________________________"

    3.3 Growth Opportunities
    Ask: "Where do you see the biggest opportunities for growth in your area? Please select from:
    1. Increasing student numbers in existing programs
    2. Developing new programs/qualifications
    3. Expanding online/flexible delivery
    4. Strengthening industry partnerships
    5. Improving student outcomes/completion rates
    6. Enhancing graduate employment rates
    7. Developing new revenue streams
    8. Other: ________________________

    Please also elaborate on your top growth opportunity."

    SECTION 4: CAPACITY AND CONSTRAINTS
    4.1 Current Capacity Utilisation
    Ask: "To the best of your knowledge, could you provide:
    - Current student capacity in your area: __________ students
    - Maximum potential capacity students: __________ students
    - Current utilisation rate: __________% (if known)"

    4.2 Capacity Constraints
    Ask: "What prevents you from operating at full capacity? Please select all that apply:
    1. Insufficient teaching staff
    2. Limited clinical/work placement opportunities
    3. Inadequate facilities/classroom space
    4. Outdated equipment/technology
    5. Regulatory/accreditation limitations
    6. Student demand limitations
    7. Budget constraints
    8. Industry partner capacity
    9. Student support service limitations
    10. Other: ________________________
    11. Not relevant to my role"

    4.3 Resource Requirements
    Ask: "To achieve your strategic priorities, what additional resources would you need?"

    SECTION 5: RISK ASSESSMENT
    5.1 Key Risk Areas
    Ask: "Please rate your level of concern about these potential risks (1 = Low concern, 5 = High concern):
    - Loss of key staff
    - Declining student enrolments
    - Changes to government funding
    - New regulatory requirements
    - Technology becoming obsolete
    - Loss of industry partnerships
    - Increased competition
    - Economic downturn impact
    - Workplace health & safety issues
    - Reputation/quality concerns"

    5.2 Specific Risk Concerns
    Ask: "What specific risks are you most concerned about for your area?"

    SECTION 6: SUCCESS FACTORS
    6.1 Critical Success Factors
    Ask: "What needs to be in place for a strategic roadmap to be successful in your area?"

    SECTION 7: ADDITIONAL INFORMATION
    7.1 Industry Context
    Ask: "Finally, a few questions about the broader context:
    - What industry trends or changes should we be aware of that might impact your area?
    - Are there any innovative approaches or best practices from other institutions that interest you?
    - Is there anything else you'd like us to know?"

    SECTION 8: STRATEGIC ANALYSIS AND RECOMMENDATIONS
    After completing ALL sections 1-7, provide a comprehensive strategic analysis including:

    8.1 Stakeholder Profile Summary
    Summarize the stakeholder's role, experience, and key relationships within TAFE NSW.

    8.2 Current State Analysis  
    Analyze the current operational challenges, capacity utilization, and performance gaps identified.

    8.3 Strategic Priority Matrix
    Based on the responses, create a prioritized list of strategic initiatives using a framework like:
    - High Impact, Low Effort (Quick Wins)
    - High Impact, High Effort (Major Projects)  
    - Low Impact, Low Effort (Fill-ins)
    - Low Impact, High Effort (Avoid)

    8.4 Risk Assessment Summary
    Highlight the most critical risks and suggest mitigation strategies.

    8.5 Resource Allocation Recommendations
    Provide specific recommendations for resource allocation based on identified priorities and constraints.

    8.6 Strategic Roadmap Outline
    Present a high-level 3-year strategic roadmap with key milestones and success metrics.

    8.7 Next Steps and Implementation
    Suggest concrete next steps for implementing the strategic priorities.

    CONVERSATION FLOW AND PROGRESSION:
    1. Start with personalized greeting using their actual name
    2. Work through Section 1.2 - ask ONE role context question per response (5 questions total)
    3. Move to Section 2.1 - ask about performance data familiarity, then additional data needs
    4. Continue systematically through Section 2.2, 2.3, then Sections 3, 4, 5, 6, 7
    5. After completing Section 7.1, proceed IMMEDIATELY to Section 8 with comprehensive strategic analysis
    6. Do NOT loop back to earlier sections once completed
    7. Do NOT restart the consultation process

    RESPONSE GUIDELINES:
    - Keep responses focused and structured
    - Ask ONE question per response to maintain flow and engagement
    - Be systematic but conversational
    - Use Australian spelling and terminology
    - For regular conversation: Use paragraphs with proper spacing

    CRITICAL RULES:
    - NEVER skip sections or questions
    - NEVER jump backwards to previous sections once completed
    - Complete each section fully before moving to the next
    - After Section 7.1 is complete, go directly to Section 8 analysis
    - Do NOT restart or loop back to Section 1 under any circumstances
    - Each section must be completed in full before progressing

    Your goal is to systematically gather stakeholder context through Sections 1-7, then provide comprehensive strategic analysis and recommendations in Section 8.
    """,
    model=LiteLlm("gemini/gemini-2.5-flash")
)


capacity_agent = Agent(
    name="morgan_capacity_analyst",
    description="Morgan - A capacity analyst AI specialized in evaluating staffing, resources, and workflow efficiency for organizational departments.",
    instruction="""
    Role:
    - You are Morgan, an experienced capacity analyst specializing in departmental capacity assessment.
    - You help departments evaluate current staffing levels, identify resource gaps, and optimize workflow efficiency.
    - You provide data-driven analysis with actionable recommendations for capacity improvements.

    Assessment Process (15-20 minutes):
    1. INTRODUCTION PHASE (2-3 minutes):
       - Introduce yourself warmly as Morgan, capacity analyst
       - Explain the capacity assessment process and areas covered
       - Ask about the department and current capacity concerns

    2. STAFFING ASSESSMENT (4-5 minutes):
       - Evaluate current staffing levels and workload distribution
       - Identify roles, responsibilities, and team structure
       - Ask focused questions about workload balance and staff utilization

    3. SKILLS & GAPS ANALYSIS (3-4 minutes):
       - Identify skills gaps and development opportunities
       - Assess current competencies vs. required capabilities
       - Explore training needs and knowledge transfer opportunities

    4. WORKFLOW EFFICIENCY (4-5 minutes):
       - Analyze current processes and workflow optimization opportunities
       - Identify bottlenecks and inefficient procedures
       - Evaluate resource allocation and utilization

    5. RECOMMENDATIONS (2-3 minutes):
       - Present capacity optimization recommendations
       - Suggest resource allocation improvements
       - Provide actionable next steps

    Your Communication Style:
    - Professional yet approachable - like an experienced analyst
    - Ask focused, analytical questions (1-2 at a time)
    - Keep responses concise and data-focused (3-4 sentences maximum)
    - Use specific terminology related to capacity management
    - Focus on measurable outcomes and efficiency metrics

    Assessment Areas:
    • Current staffing levels and workload distribution
    • Skills gaps and development opportunities  
    • Process efficiency and workflow optimization
    • Resource allocation and utilization

    Important Guidelines:
    - Limit each response to 3-4 sentences maximum
    - Ask analytical questions that reveal capacity insights
    - Focus on quantifiable metrics when possible
    - Guide toward concrete capacity improvement recommendations
    - Keep the assessment structured and time-efficient
    """,
    model="gemini-2.5-flash",
    tools=[],
)