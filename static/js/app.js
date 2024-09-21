document.addEventListener('DOMContentLoaded', function() {
    const generateQuestionBtn = document.getElementById('generateQuestionBtn');
    const questionDisplay = document.getElementById('questionDisplay');
    const answerDisplay = document.getElementById('answerDisplay');
    const showAnswerBtn = document.getElementById('showAnswerBtn');
    const messageDisplay = document.getElementById('messageDisplay');

    function showMessage(message, isError = false) {
        messageDisplay.textContent = message;
        messageDisplay.className = isError ? 'error' : 'success';
        messageDisplay.style.display = 'block';
        setTimeout(() => {
            messageDisplay.style.display = 'none';
        }, 5000);
    }

    generateQuestionBtn.addEventListener('click', function() {
        const difficulty = document.getElementById('difficultySelect').value;
        const type = document.getElementById('typeSelect').value;
        fetch('/generate_question', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ difficulty, type }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to generate question');
            }
            return response.json();
        })
        .then(data => {
            questionDisplay.textContent = data.question;
            answerDisplay.textContent = data.answer;
            answerDisplay.style.display = 'none'; // Hide answer initially
            showAnswerBtn.style.display = 'block'; // Show the "Show Answer" button
            showMessage('Question generated successfully');
        })
        .catch(error => {
            console.error('Generate question error:', error);
            showMessage(error.message, true);
        });
    });

    showAnswerBtn.addEventListener('click', function() {
        answerDisplay.style.display = 'block'; // Show the answer
    });
});
