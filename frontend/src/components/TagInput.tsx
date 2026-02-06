import React, { useState, KeyboardEvent } from 'react';

interface TagInputProps {
  selectedTags: string[];
  onChange: (tags: string[]) => void;
  label?: string;
  placeholder?: string;
}

const TagInput: React.FC<TagInputProps> = ({ 
  selectedTags, 
  onChange, 
  label = "Tags", 
  placeholder = "Type a tag and press Enter"
}) => {
  const [inputValue, setInputValue] = useState('');

  const addTag = () => {
    if (inputValue.trim() && !selectedTags.includes(inputValue.trim())) {
      onChange([...selectedTags, inputValue.trim()]);
      setInputValue('');
    }
  };

  const removeTag = (tagToRemove: string) => {
    onChange(selectedTags.filter(tag => tag !== tagToRemove));
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      addTag();
    } else if (e.key === 'Backspace' && inputValue === '' && selectedTags.length > 0) {
      // Remove the last tag when backspace is pressed with empty input
      const newTags = [...selectedTags];
      newTags.pop();
      onChange(newTags);
    }
  };

  return (
    <div className="space-y-2">
      {label && <label className="block text-sm font-medium text-gray-700">{label}</label>}
      <div className="flex flex-wrap gap-2 mb-2">
        {selectedTags.map((tag) => (
          <span 
            key={tag} 
            className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800"
          >
            {tag}
            <button
              type="button"
              onClick={() => removeTag(tag)}
              className="ml-2 text-blue-600 hover:text-blue-800"
            >
              ×
            </button>
          </span>
        ))}
      </div>
      <input
        type="text"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
      />
      <p className="text-xs text-gray-500">Press Enter to add a tag. Max 10 tags.</p>
    </div>
  );
};

export default TagInput;