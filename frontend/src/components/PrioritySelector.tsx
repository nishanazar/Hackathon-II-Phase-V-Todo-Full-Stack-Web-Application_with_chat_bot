import React from 'react';

interface PrioritySelectorProps {
  selectedPriority: number;
  onChange: (priority: number) => void;
  label?: string;
}

const PrioritySelector: React.FC<PrioritySelectorProps> = ({ 
  selectedPriority, 
  onChange, 
  label = "Priority" 
}) => {
  const priorities = [
    { value: 1, label: 'Low', color: 'text-green-600' },
    { value: 2, label: 'Medium-Low', color: 'text-lime-600' },
    { value: 3, label: 'Medium', color: 'text-yellow-600' },
    { value: 4, label: 'Medium-High', color: 'text-orange-600' },
    { value: 5, label: 'High', color: 'text-red-600' },
  ];

  return (
    <div className="space-y-2">
      {label && <label className="block text-sm font-medium text-gray-700">{label}</label>}
      <div className="grid grid-cols-5 gap-2">
        {priorities.map((priority) => (
          <button
            key={priority.value}
            type="button"
            onClick={() => onChange(priority.value)}
            className={`py-2 px-3 rounded-md border text-center ${
              selectedPriority === priority.value
                ? `${priority.color} bg-opacity-20 border-opacity-50 border-current font-semibold`
                : 'border-gray-300 text-gray-700 hover:bg-gray-50'
            }`}
          >
            <span className="text-xs">{priority.label}</span>
          </button>
        ))}
      </div>
      <div className="flex justify-between text-xs text-gray-500 mt-1">
        <span>Less Important</span>
        <span>More Important</span>
      </div>
    </div>
  );
};

export default PrioritySelector;