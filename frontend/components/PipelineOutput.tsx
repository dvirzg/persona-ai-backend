import React, { useState } from 'react';
import { ChevronDown, ChevronRight } from 'lucide-react';

interface StepData {
  phase: string;
  status: string;
  thinking: string;
  details?: Record<string, any>;
  response?: Record<string, any>;
}

interface CollapsibleSectionProps {
  title: string;
  children: React.ReactNode;
}

const CollapsibleSection: React.FC<CollapsibleSectionProps> = ({ title, children }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="border rounded-lg mb-4">
      <button
        className="w-full px-4 py-2 flex items-center justify-between bg-gray-50 hover:bg-gray-100 rounded-t-lg"
        onClick={() => setIsOpen(!isOpen)}
      >
        <span className="font-medium">{title}</span>
        {isOpen ? <ChevronDown size={20} /> : <ChevronRight size={20} />}
      </button>
      {isOpen && (
        <div className="p-4 border-t">
          {children}
        </div>
      )}
    </div>
  );
};

const PipelineOutput: React.FC<{ steps: StepData[] }> = ({ steps }) => {
  return (
    <div className="max-w-3xl mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">🚀 Pipeline Processing</h2>
      
      {steps.map((step, index) => (
        <div key={index} className="mb-6">
          <div className="flex items-center gap-2 mb-2">
            <div className={`w-3 h-3 rounded-full ${
              step.status === 'complete' ? 'bg-green-500' : 
              step.status === 'in_progress' ? 'bg-blue-500' : 'bg-gray-500'
            }`} />
            <h3 className="text-lg font-semibold">
              {step.phase.charAt(0).toUpperCase() + step.phase.slice(1)}
            </h3>
            <span className="text-sm text-gray-500">
              {step.status}
            </span>
          </div>

          <CollapsibleSection title="📝 Thinking Process">
            <div className="space-y-4">
              <div className="bg-gray-50 p-3 rounded">
                <p className="font-medium">Main Thought:</p>
                <p>{step.thinking}</p>
              </div>
              
              {step.details && Object.keys(step.details).length > 0 && (
                <div className="bg-gray-50 p-3 rounded">
                  <p className="font-medium mb-2">Details:</p>
                  <pre className="whitespace-pre-wrap text-sm">
                    {JSON.stringify(step.details, null, 2)}
                  </pre>
                </div>
              )}
            </div>
          </CollapsibleSection>

          {step.response && (
            <CollapsibleSection title="🎯 Final Results">
              <pre className="whitespace-pre-wrap text-sm bg-gray-50 p-3 rounded">
                {JSON.stringify(step.response, null, 2)}
              </pre>
            </CollapsibleSection>
          )}
        </div>
      ))}
    </div>
  );
};

export default PipelineOutput; 