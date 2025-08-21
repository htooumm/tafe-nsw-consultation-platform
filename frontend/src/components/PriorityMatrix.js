import React, { useState, useEffect, useRef } from 'react'; // Import useRef
import { AIService } from '../services/aiService';
import { DataService } from '../services/supabase';
import { Send, Download, Save, MessageCircle } from 'lucide-react';

// Add CSS styles for better HTML formatting
const conversationStyles = `
  .conversation-message {
    line-height: 1.3;
  }
  .conversation-message p {
    margin-bottom: 0.25rem;
    line-height: 1.3;
  }
  .conversation-message p:last-child {
    margin-bottom: 0;
  }
  .conversation-message .consultation-container {
    background: transparent;
    padding: 0;
    margin: 0;
    box-shadow: none;
  }
  .conversation-message .question-section {
    margin: 0;
    padding: 15px;
    border-left: 3px solid #007bff;
    background-color: #f8f9fa;
    border-radius: 0 6px 6px 0;
  }
  .conversation-message .intro-text {
    margin-bottom: 15px;
    font-size: 14px;
    color: #495057;
  }
  .conversation-message .question-title {
    margin: 0 0 15px 0;
    font-size: 16px;
    font-weight: 600;
    color: #212529;
  }
  .conversation-message .options-container {
    margin-top: 10px;
  }
  .conversation-message .option-item {
    margin: 0;
    padding: 6px 10px;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }
  .conversation-message .option-item:hover {
    background-color: #e3f2fd;
  }
  .conversation-message .option-item input[type="radio"] {
    margin-right: 8px;
    accent-color: #007bff;
  }
  .conversation-message .option-item label {
    cursor: pointer;
    color: #495057;
    font-weight: 500;
    font-size: 14px;
    margin: 0;
  }
  .conversation-message * {
    margin-top: 0;
  }
  .conversation-message h1, .conversation-message h2, .conversation-message h3 {
    margin-bottom: 0.5rem;
    font-weight: 600;
  }
`;

const PriorityMatrix = ({ onBack }) => {
  const [currentStep, setCurrentStep] = useState('intro');
  const [stakeholderInfo, setStakeholderInfo] = useState({
    name: '',
    role: '',
    department: '',
    email: ''
  });
  const [conversationHistory, setConversationHistory] = useState([]);
  const [userResponse, setUserResponse] = useState('');
  const [discoveredPriorities, setDiscoveredPriorities] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null); // Create a ref for the messages container
  const messagesContainerRef = useRef(null); // Add a ref for the messages container
  const [selectedRadioOption, setSelectedRadioOption] = useState(null); // New state for radio buttons

  const aiService = new AIService();
  const dataService = new DataService();

  // Format message to handle basic markdown-style formatting
  // Update the formatMessage function to handle HTML with better styling
  const formatMessage = (message) => {
    if (!message) return '';
    
    // Check if the message contains HTML tags
    if (message.includes('<') && message.includes('>')) {
      // Add CSS classes to the container for better styling and remove submit buttons
      let cleanedHtml = message;
      
      // Remove submit buttons from forms
      cleanedHtml = cleanedHtml.replace(/<input[^>]*type=["']submit["'][^>]*>/gi, '');
      
      // If it's a complete HTML document, extract only the body content
      if (cleanedHtml.includes('<!DOCTYPE') || cleanedHtml.includes('<html')) {
        const bodyMatch = cleanedHtml.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
        if (bodyMatch) {
          cleanedHtml = bodyMatch[1];
        }
      }
      
      return (
        <div 
          className="conversation-message"
          dangerouslySetInnerHTML={{ __html: cleanedHtml }} 
          style={{
            lineHeight: '1.3',
          }}
          onClick={(e) => {
            // Handle radio button clicks in HTML content
            if (e.target.type === 'radio') {
              const value = e.target.value;
              if (value) {
                handleRadioSelection(value);
              }
            }
          }}
        />
      );
    }
    
    // Original formatting logic for non-HTML messages (markdown-style)
    const lines = message.split('\n');
    const formattedLines = lines.map((line, index) => {
      let formattedLine = line;
      
      // Handle numbered lists (1. 2. 3. etc.)
      if (/^\d+\.\s\*\*/.test(line)) {
        const parts = line.match(/^(\d+\.\s)\*\*(.*?)\*\*:?\s*(.*)/);
        if (parts) {
          return (
            <div key={index} className="mb-1">
              <span className="font-semibold text-blue-700">{parts[1]}</span>
              <span className="font-bold text-gray-900">{parts[2]}</span>
              {parts[3] && <span className="text-gray-800">: {parts[3]}</span>}
            </div>
          );
        }
      }
      
      // Handle bold text **text**
      if (formattedLine.includes('**')) {
        const parts = formattedLine.split(/(\*\*.*?\*\*)/);
        return (
          <div key={index} className="mb-0.5">
            {parts.map((part, partIndex) => {
              if (part.startsWith('**') && part.endsWith('**')) {
                return <span key={partIndex} className="font-bold text-gray-900">{part.slice(2, -2)}</span>;
              }
              return <span key={partIndex}>{part}</span>;
            })}
          </div>
        );
      }
      
      // Handle regular lines with minimal spacing
      if (line.trim() === '') {
        return null; // Skip empty lines completely
      }
      
      return <div key={index} className="mb-0.5">{line}</div>;
    });
    
    // Filter out null values (empty lines)
    const filteredLines = formattedLines.filter(line => line !== null);
    
    return <div className="leading-snug space-y-0.5">{filteredLines}</div>;
  };

  // Add this function to parse HTML and extract interactive elements
  // Update the parseHtmlResponse function to automatically select radio options
  const parseHtmlResponse = (htmlContent) => {
    // Create a temporary div to parse the HTML
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = htmlContent;
    
    // Check if there are radio buttons (in any form or structure)
    const radioInputs = tempDiv.querySelectorAll('input[type="radio"]');
    if (radioInputs.length > 0) {
      // Extract question text - look for the question title or main text
      let questionText = "";
      const questionTitle = tempDiv.querySelector('.question-title, h3, .question');
      if (questionTitle) {
        questionText = questionTitle.textContent.trim();
      } else {
        // Fallback: extract text content before radio buttons
        const allText = tempDiv.textContent || "";
        const lines = allText.split('\n').map(line => line.trim()).filter(line => line);
        questionText = lines.find(line => line.includes('?')) || lines[0] || "Please select an option:";
      }
      
      // Extract options from radio buttons
      const options = Array.from(radioInputs).map(input => {
        const label = tempDiv.querySelector(`label[for="${input.id}"]`);
        if (label) {
          return label.textContent.trim();
        }
        return input.value || input.getAttribute('value') || 'Option';
      });
      
      if (options.length > 0) {
        return {
          hasInteractive: true,
          cleanMessage: questionText,
          interactive: {
            type: "choice",
            question: questionText,
            options: options
          }
        };
      }
    }
    
    return {
      hasInteractive: false,
      cleanMessage: htmlContent,
      interactive: null
    };
  };

  const handleRadioSelection = async (option) => {
    setSelectedRadioOption(option);
    setUserResponse(option); // Automatically fill the text box
    
    // Automatically send the response after a brief delay
    setTimeout(async () => {
      setIsLoading(true);
      const newConversation = [
        ...conversationHistory,
        { sender: 'user', message: option, timestamp: new Date(), isInteractiveResponse: true },
      ];
      setConversationHistory(newConversation);

      try {
        const aiResult = await aiService.generateResponse(
          option,
          { 
            ...stakeholderInfo, 
            conversationHistory: newConversation,
            user_id: stakeholderInfo.email || 'anonymous',
            session_id: sessionId
          },
          'riley'
        );

        // Parse HTML response if it contains interactive elements
        let interactive = aiResult.interactive_question_data;
        let cleanMessage = aiResult.response;
        
        if (aiResult.response.includes('<form>') || aiResult.response.includes('<input type="radio"')) {
          const parsed = parseHtmlResponse(aiResult.response);
          if (parsed.hasInteractive) {
            interactive = parsed.interactive;
            cleanMessage = parsed.cleanMessage;
          }
        }

        setConversationHistory(prev => [
          ...prev,
          { 
            sender: 'ai', 
            message: cleanMessage,
            htmlMessage: aiResult.response,
            timestamp: new Date(),
            insights: aiResult.insights,
            interactive: interactive
          }
        ]);
        setSessionId(aiResult.sessionId);
      } catch (e) {
        console.error('Interactive response error:', e);
        setConversationHistory(prev => [
          ...prev,
          { 
            sender: 'ai', 
            message: "Sorry, there was an error processing your selection.", 
            timestamp: new Date()
          }
        ]);
      }
      setIsLoading(false);
      setUserResponse(''); // Clear the text box
      setSelectedRadioOption(null); // Reset selection
    }, 500); // Small delay to show the selection
  };

  // Improved scroll to bottom function
  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  };

  // Scroll to bottom whenever conversationHistory changes
  useEffect(() => {
    scrollToBottom();
  }, [conversationHistory]);

  const startConversation = async () => {
    if (!stakeholderInfo.name || !stakeholderInfo.role || !stakeholderInfo.department) {
      alert('Please fill in all required fields');
      return;
    }

    setCurrentStep('conversation');
    setIsLoading(true);

    try {
      console.log('Starting conversation with agent...'); 
      // Send initial message to get onboarding response from agent
      const aiResult = await aiService.generateResponse(
        "Hello, I'd like to start a strategic priority consultation.",
        { 
          ...stakeholderInfo, 
          conversationHistory: [],
          user_id: stakeholderInfo.email || 'anonymous'
        },
        'riley'
      );

      console.log('Agent onboarding response:', aiResult);

      // Start conversation with agent's onboarding message
      setConversationHistory([{
        sender: 'ai',
        message: aiResult.response,
        timestamp: new Date(),
        insights: aiResult.insights,
        interactive: aiResult.interactive_question_data || null // Store interactive data if present
      }]);
      
      setSessionId(aiResult.sessionId);
    } catch (e) {
      console.error('Error starting conversation:', e);
      // Fallback message if agent fails
      setConversationHistory([{
        sender: 'ai',
        message: "G'day! I'm Riley, your strategic consultant. I'm having a bit of trouble getting started, but I'm here to help you identify strategic priorities. What brings you here today?",
        timestamp: new Date()
      }]);
    }
    setIsLoading(false);
  };

  const handleUserResponse = async () => {
    if (!userResponse.trim() || isLoading) return;
    const outgoing = userResponse;
    setUserResponse('');
    setIsLoading(true);

    const newConversation = [
      ...conversationHistory,
      { sender: 'user', message: outgoing, timestamp: new Date() },
    ];
    setConversationHistory(newConversation);

    try {
      console.log('Starting request...'); 
      const aiResult = await aiService.generateResponse(
        outgoing,
        { 
          ...stakeholderInfo, 
          conversationHistory: newConversation,
          user_id: stakeholderInfo.email || 'anonymous',
          session_id: sessionId
        },
        'riley'
      );

      console.log('Request completed, result:', aiResult); 

      // Parse HTML response if it contains interactive elements
      let interactive = aiResult.interactive_question_data;
      let cleanMessage = aiResult.response;
      
      if (aiResult.response.includes('<form>') || aiResult.response.includes('<input type="radio"')) {
        const parsed = parseHtmlResponse(aiResult.response);
        if (parsed.hasInteractive) {
          interactive = parsed.interactive;
          cleanMessage = parsed.cleanMessage;
        }
      }

      // Add AI response to conversation
      setConversationHistory(prev => [
        ...prev,
        { 
          sender: 'ai', 
          message: cleanMessage, // Use clean message without HTML form
          htmlMessage: aiResult.response, // Store original HTML
          timestamp: new Date(),
          insights: aiResult.insights,
          interactive: interactive
        }
      ]);
      setSessionId(aiResult.sessionId);
    } catch (e) {
      console.error('Request error:', e);
      setConversationHistory(prev => [
        ...prev,
        { 
          sender: 'ai', 
          message: "Sorry, there was an error generating a response.", 
          timestamp: new Date()
        }
      ]);
    }
    setIsLoading(false);
  };

  const handleInteractiveResponse = async () => { // No argument needed now
    if (!selectedRadioOption || isLoading) return; // Check selectedRadioOption
    setIsLoading(true);

    const outgoing = selectedRadioOption; // Use the state
    setSelectedRadioOption(null); // Reset selected option after sending

    const newConversation = [
      ...conversationHistory,
      { sender: 'user', message: outgoing, timestamp: new Date(), isInteractiveResponse: true },
    ];
    setConversationHistory(newConversation);

    try {
      console.log('Sending interactive response to agent...');
      const aiResult = await aiService.generateResponse(
        outgoing, // Send the selected option as the message
        { 
          ...stakeholderInfo, 
          conversationHistory: newConversation,
          user_id: stakeholderInfo.email || 'anonymous',
          session_id: sessionId
        },
        'riley'
      );

      console.log('Interactive response completed, result:', aiResult);

      setConversationHistory(prev => [
        ...prev,
        { 
          sender: 'ai', 
          message: aiResult.response, 
          timestamp: new Date(),
          insights: aiResult.insights,
          interactive: aiResult.interactive_question_data || null
        }
      ]);
      setSessionId(aiResult.sessionId);
    } catch (e) {
      console.error('Interactive response error:', e);
      setConversationHistory(prev => [
        ...prev,
        { 
          sender: 'ai', 
          message: "Sorry, there was an error processing your selection.", 
          timestamp: new Date()
        }
      ]);
    }
    setIsLoading(false);
  };

  const handleSaveData = async () => {
    try {
      // Save stakeholder if not exists
      const stakeholder = await dataService.saveStakeholder({
        ...stakeholderInfo,
        created_at: new Date()
      });

      // Save consultation session
      const session = await dataService.saveConsultationSession({
        stakeholder_id: stakeholder.id,
        consultation_type: 'priority_discovery',
        session_data: { 
          priorities: discoveredPriorities,
          conversation: conversationHistory
        },
        completion_percentage: discoveredPriorities.length > 0 ? 75 : 25
      });

      setSessionId(session.id);

      // Save conversation messages
      for (const msg of conversationHistory) {
        await dataService.saveMessage({
          session_id: session.id,
          sender: msg.sender,
          message_text: msg.message,
          timestamp: msg.timestamp,
          ai_insights: msg.insights || null
        });
      }

      // Save individual priorities
      if (discoveredPriorities.length > 0) {
        const priorityData = discoveredPriorities.map(p => ({
          session_id: session.id,
          title: p.title,
          description: p.description,
          importance_score: p.importance,
          urgency_score: p.urgency,
          theme: p.themes.join(', ')
        }));

        await dataService.savePriorities(priorityData);
      }

      alert('Data saved successfully!');
    } catch (error) {
      console.error('Error saving data:', error);
      alert('Error saving data. Please try again.');
    }
  };

  const exportData = () => {
    const exportData = {
      stakeholder: stakeholderInfo,
      consultation_type: 'priority_discovery',
      conversation: conversationHistory,
      discovered_priorities: discoveredPriorities,
      export_date: new Date().toISOString()
    };

    const dataStr = JSON.stringify(exportData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `priority-consultation-${stakeholderInfo.name.replace(/\s+/g, '-')}-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
  };

  if (currentStep === 'intro') {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="bg-white rounded-lg shadow-sm border p-8">
          <h1 className="text-2xl font-bold text-gray-900 mb-6">
            Priority Discovery Consultation
          </h1>
          
          <div className="mb-8">
            <p className="text-gray-600 mb-4">
              This AI-guided consultation will help identify and prioritize strategic initiatives for your department. 
              The process takes about 15-20 minutes and involves a conversation with Riley, our AI consultant.
            </p>
            
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h3 className="font-medium text-blue-900 mb-2">What to Expect:</h3>
              <ul className="text-blue-800 text-sm space-y-1">
                <li>• Strategic discussion about your department's priorities</li>
                <li>• AI-powered analysis of challenges and opportunities</li>
                <li>• Automatic categorization and scoring of priorities</li>
                <li>• Downloadable summary and action plan</li>
              </ul>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8 text-black">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Full Name *
              </label>
              <input
                type="text"
                value={stakeholderInfo.name}
                onChange={(e) => setStakeholderInfo({...stakeholderInfo, name: e.target.value})}
                className="w-full p-3 text-black border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Enter your full name"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Role/Position *
              </label>
              <input
                type="text"
                value={stakeholderInfo.role}
                onChange={(e) => setStakeholderInfo({...stakeholderInfo, role: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="e.g., Department Manager, Team Leader"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Department *
              </label>
              <select
                value={stakeholderInfo.department}
                onChange={(e) => setStakeholderInfo({...stakeholderInfo, department: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Select Department</option>
                <option value="Health & Community Services">Health & Community Services</option>
                <option value="Human Services">Human Services</option>
                <option value="Nursing & Midwifery">Nursing & Midwifery</option>
                <option value="Allied Health">Allied Health</option>
                <option value="Mental Health">Mental Health</option>
                <option value="Aged Care">Aged Care</option>
                <option value="Disability Services">Disability Services</option>
                <option value="Administration">Administration</option>
                <option value="Other">Other</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Email Address
              </label>
              <input
                type="email"
                value={stakeholderInfo.email}
                onChange={(e) => setStakeholderInfo({...stakeholderInfo, email: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="your.email@tafe.nsw.edu.au"
              />
            </div>
          </div>

          <button
            onClick={startConversation}
            className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 font-medium"
          >
            Start Priority Consultation
          </button>
        </div>
      </div>
    );
  }

  return (
    <>
      <style>{conversationStyles}</style>
      <div className="max-w-6xl mx-auto p-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Conversation Panel */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-sm border">
            <div className="p-4 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
                <MessageCircle className="w-5 h-5" />
                Conversation with Riley
              </h2>
            </div>
            
            <div 
              className="h-96 overflow-y-auto p-4 space-y-4" 
              ref={messagesContainerRef} // Add ref to the container
            > 
              {conversationHistory.map((msg, index) => (
                <div key={index} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-xs lg:max-w-md px-4 py-3 rounded-lg ${
                    msg.sender === 'user' 
                      ? 'bg-blue-600 text-white' 
                      : 'bg-gray-100 text-gray-900'
                  }`}>
                    {msg.sender === 'ai' && (
                      <div className="text-xs text-gray-600 mb-1">Riley</div>
                    )}
                    <div className="text-sm whitespace-pre-wrap break-words">
                      {msg.isInteractiveResponse ? (
                        <span className="font-medium">{msg.message}</span>
                      ) : msg.interactive ? (
                        // Show clean message without HTML form for interactive responses
                        formatMessage(msg.message)
                      ) : (
                        formatMessage(msg.htmlMessage || msg.message)
                      )}
                    </div>
                    {msg.insights && msg.insights.length > 0 && (
                      <div className="mt-2 pt-2 border-t border-gray-200">
                        <div className="text-xs text-gray-500">Insights:</div>
                        {msg.insights.map((insight, i) => (
                          <div key={i} className="text-xs text-blue-600 mt-1">
                            • {insight.message}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))}
              
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-gray-100 rounded-lg px-4 py-3">
                    <div className="flex items-center gap-2">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                      <span className="text-sm text-gray-600">Riley is thinking...</span>
                    </div>
                  </div>
                </div>
              )}
              
              {/* Add this div at the end of the messages container */}
              <div ref={messagesEndRef} />
            </div>
            
            <div className="p-4 text-black border-t border-gray-200">
              {conversationHistory.length > 0 && conversationHistory[conversationHistory.length - 1].interactive && 
               (conversationHistory[conversationHistory.length - 1].interactive.type === "choice" || 
                conversationHistory[conversationHistory.length - 1].interactive.type === "radio") ? (
                <div className="flex flex-col gap-3">
                  <p className="text-sm text-gray-700 font-medium">
                    {conversationHistory[conversationHistory.length - 1].interactive.question}
                  </p>
                  <div className="bg-gray-50 rounded-lg p-3 space-y-2">
                    {conversationHistory[conversationHistory.length - 1].interactive.options.map((option, index) => (
                      <label 
                        key={index} 
                        className="flex items-center p-2 rounded hover:bg-gray-100 cursor-pointer transition-colors"
                      >
                        <input
                          type="radio"
                          name="performanceFamiliarity"
                          value={option}
                          checked={selectedRadioOption === option}
                          onChange={(e) => handleRadioSelection(e.target.value)}
                          className="form-radio h-4 w-4 text-blue-600 focus:ring-blue-500"
                        />
                        <span className="ml-3 text-gray-700">{option}</span>
                      </label>
                    ))}
                  </div>
                  <div className="text-xs text-gray-500 italic">
                    Selecting an option will fill the text box below. You can then send it or modify it.
                  </div>
                </div>
              ) : null}
              
              <div className="flex gap-2 mt-3">
                <input
                  type="text"
                  value={userResponse}
                  onChange={(e) => setUserResponse(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleUserResponse()}
                  placeholder="Type your response..."
                  className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  disabled={isLoading}
                />
                <button
                  onClick={handleUserResponse}
                  disabled={isLoading || !userResponse.trim()}
                  className="px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Send className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Priorities Panel */}
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow-sm border">
            <div className="p-4 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900">Identified Priorities</h3>
            </div>
            <div className="p-4">
              {discoveredPriorities.length === 0 ? (
                <p className="text-gray-500 text-sm text-center py-4">
                  Priorities will appear here as we discuss your challenges and opportunities.
                </p>
              ) : (
                <div className="space-y-4">
                  {discoveredPriorities.map((priority, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-4">
                      <h4 className="font-medium text-gray-900 mb-2">{priority.title}</h4>
                      <p className="text-sm text-gray-600 mb-3">{priority.description}</p>
                      
                      <div className="grid grid-cols-2 gap-2 text-xs">
                        <div>
                          <span className="text-gray-500">Importance:</span>
                          <div className="bg-gray-200 rounded-full h-2 mt-1">
                            <div 
                              className="bg-blue-600 h-2 rounded-full" 
                              style={{width: `${priority.importance * 10}%`}}
                            ></div>
                          </div>
                        </div>
                        <div>
                          <span className="text-gray-500">Urgency:</span>
                          <div className="bg-gray-200 rounded-full h-2 mt-1">
                            <div 
                              className="bg-red-600 h-2 rounded-full" 
                              style={{width: `${priority.urgency * 10}%`}}
                            ></div>
                          </div>
                        </div>
                      </div>
                      
                      <div className="mt-2">
                        <div className="flex flex-wrap gap-1">
                          {priority.themes.map((theme, i) => (
                            <span key={i} className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded">
                              {theme}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Actions Panel */}
          <div className="bg-white rounded-lg shadow-sm border">
            <div className="p-4 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900">Actions</h3>
            </div>
            <div className="p-4 space-y-3">
              <button
                onClick={handleSaveData}
                className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
              >
                <Save className="w-4 h-4" />
                Save Data
              </button>
              
              <button
                onClick={exportData}
                className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                <Download className="w-4 h-4" />
                Export Report
              </button>
              
              <button
                onClick={onBack}
                className="w-full px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
              >
                Back to Dashboard
              </button>
            </div>
          </div>
        </div>
        </div>
      </div>
    </>
  );
};

export default PriorityMatrix;
