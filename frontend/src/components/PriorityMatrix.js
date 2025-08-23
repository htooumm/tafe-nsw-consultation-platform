// components/PriorityMatrix/PriorityMatrix.js
import React, { useState, useEffect, useRef } from 'react';
import { AIService } from '../services/aiService';
import { DataService } from '../services/supabase';
import StakeholderForm from './PriorityMatrix_subcomponents/StakeholderForm';
import ConversationPanel from './PriorityMatrix_subcomponents/ConversationPanel';
import PrioritiesPanel from './PriorityMatrix_subcomponents/PrioritiesPanel';
import ActionsPanel from './PriorityMatrix_subcomponents/ActionsPanel';
import { conversationStyles } from '../styles/conversationStyles';

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
  const [selectedRadioOption, setSelectedRadioOption] = useState(null);

  const aiService = new AIService();
  const dataService = new DataService();

  const parseHtmlResponse = (htmlContent) => {
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = htmlContent;
    
    const radioInputs = tempDiv.querySelectorAll('input[type="radio"]');
    if (radioInputs.length > 0) {
      let questionText = "";
      const questionTitle = tempDiv.querySelector('.question-title, h3, .question');
      if (questionTitle) {
        questionText = questionTitle.textContent.trim();
      } else {
        const allText = tempDiv.textContent || "";
        const lines = allText.split('\n').map(line => line.trim()).filter(line => line);
        questionText = lines.find(line => line.includes('?')) || lines[0] || "Please select an option:";
      }
      
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
    setUserResponse(option);
    
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
      setUserResponse('');
      setSelectedRadioOption(null);
    }, 500);
  };

  const startConversation = async () => {
    if (!stakeholderInfo.name || !stakeholderInfo.role || !stakeholderInfo.department) {
      alert('Please fill in all required fields');
      return;
    }

    setCurrentStep('conversation');
    setIsLoading(true);

    try {
      console.log('Starting conversation with agent...'); 
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

      setConversationHistory([{
        sender: 'ai',
        message: aiResult.response,
        timestamp: new Date(),
        insights: aiResult.insights,
        interactive: aiResult.interactive_question_data || null
      }]);
      
      setSessionId(aiResult.sessionId);
    } catch (e) {
      console.error('Error starting conversation:', e);
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

  const handleSaveData = async () => {
    try {
      const stakeholder = await dataService.saveStakeholder({
        ...stakeholderInfo,
        created_at: new Date()
      });

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

      for (const msg of conversationHistory) {
        await dataService.saveMessage({
          session_id: session.id,
          sender: msg.sender,
          message_text: msg.message,
          timestamp: msg.timestamp,
          ai_insights: msg.insights || null
        });
      }

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
      <StakeholderForm
        stakeholderInfo={stakeholderInfo}
        setStakeholderInfo={setStakeholderInfo}
        onStartConversation={startConversation}
      />
    );
  }

  return (
    <>
      <style>{conversationStyles}</style>
      <div className="max-w-6xl mx-auto p-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <ConversationPanel
            conversationHistory={conversationHistory}
            userResponse={userResponse}
            setUserResponse={setUserResponse}
            isLoading={isLoading}
            selectedRadioOption={selectedRadioOption}
            onUserResponse={handleUserResponse}
            onRadioSelection={handleRadioSelection}
          />
          
          <div className="space-y-6">
            <PrioritiesPanel discoveredPriorities={discoveredPriorities} />
            <ActionsPanel
              onSaveData={handleSaveData}
              onExportData={exportData}
              onBack={onBack}
            />
          </div>
        </div>
      </div>
    </>
  );
};

export default PriorityMatrix;