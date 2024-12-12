import React, { useState } from 'react';
import './styles.css';

function App() {
  const [question, setQuestion] = useState(''); // unified state for scenario and follow-up
  const [candidateAnswer, setCandidateAnswer] = useState('');
  const [responseData, setResponseData] = useState(null);
  const [loading, setLoading] = useState(false);

  // fetch the initial scenario when the app loads
  React.useEffect(() => {
    fetch('http://localhost:5000/get_scenario')
      .then((res) => res.json())
      .then((data) => setQuestion(data.scenario));
  }, []);

  const submitAnswer = () => {
    setLoading(true);
    fetch('http://localhost:5000/submit_answer', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ answer: candidateAnswer }),
    })
      .then((res) => {
        if (!res.ok) throw new Error('Failed to submit answer');
        return res.json();
      })
      .then((data) => {
        setResponseData(data);
        setQuestion(data.followup_question); // replace the question with the follow-up
        setCandidateAnswer(''); // clear the input field
        setLoading(false);
      })
      .catch((error) => {
        alert('Error: ' + error.message);
        setLoading(false);
      });
  };

  return (
    <div className="container">
      <div className="title">Credentialing Interview</div>
      <div className="scenario">
        <strong>Question:</strong> {question || 'Loading...'}
      </div>
      <textarea
        value={candidateAnswer}
        onChange={(e) => setCandidateAnswer(e.target.value)}
        placeholder="Type your response here..."
      />
      <button className="button" onClick={submitAnswer} disabled={loading}>
        {loading ? 'Submitting...' : 'Submit Answer'}
      </button>
      {responseData && (
        <div className="response">
          <div>
            <strong>Scores:</strong> {JSON.stringify(responseData.scores)}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
