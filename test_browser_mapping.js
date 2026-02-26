// Test script to verify the mapping fix
// This would be run in the browser console

// Simulate the options to choices mapping
const testQuestion = {
  id: 'q1',
  question: 'Test question?',
  options: {
    'A': 'Choice A',
    'B': 'Choice B', 
    'C': 'Choice C',
    'D': 'Choice D'
  },
  correct: 0
};

// Test the mapping as done in startQuiz()
const mapped = {
  ...testQuestion,
  choices: testQuestion.choices || (testQuestion.options ? Object.values(testQuestion.options) : [])
};

console.log('Original options:', testQuestion.options);
console.log('Mapped choices:', mapped.choices);
console.log('Is array:', Array.isArray(mapped.choices));
console.log('Can map:', mapped.choices.map((c, i) => `${String.fromCharCode(65 + i)}. ${c}`).join('\n'));
