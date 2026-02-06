import React, { useState } from 'react';

interface DatePickerProps {
  selectedDate: Date | null;
  onChange: (date: Date | null) => void;
  label?: string;
  placeholder?: string;
}

const DatePicker: React.FC<DatePickerProps> = ({ 
  selectedDate, 
  onChange, 
  label = "Due Date", 
  placeholder = "Select a date"
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [inputValue, setInputValue] = useState(
    selectedDate ? selectedDate.toISOString().split('T')[0] : ''
  );

  const handleDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setInputValue(value);
    
    if (value) {
      const newDate = new Date(value);
      // Set to end of day to avoid timezone issues
      newDate.setHours(23, 59, 59, 999);
      onChange(newDate);
    } else {
      onChange(null);
    }
  };

  const handleClear = () => {
    setInputValue('');
    onChange(null);
    setIsOpen(false);
  };

  return (
    <div className="relative">
      {label && <label className="block text-sm font-medium text-gray-700 mb-1">{label}</label>}
      <div className="relative">
        <input
          type="date"
          value={inputValue}
          onChange={handleDateChange}
          onFocus={() => setIsOpen(true)}
          onBlur={() => setTimeout(() => setIsOpen(false), 200)}
          placeholder={placeholder}
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        />
        {inputValue && (
          <button
            type="button"
            onClick={handleClear}
            className="absolute inset-y-0 right-0 pr-3 flex items-center"
          >
            <span className="text-gray-400 hover:text-gray-600">×</span>
          </button>
        )}
      </div>
    </div>
  );
};

export default DatePicker;