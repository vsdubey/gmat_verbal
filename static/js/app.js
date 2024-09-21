document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const getQuestionBtn = document.getElementById('getQuestionBtn');
    const generateQuestionBtn = document.getElementById('generateQuestionBtn');
    const showAnswerBtn = document.getElementById('showAnswerBtn');
    const questionDisplay = document.getElementById('questionDisplay');
    const answerDisplay = document.getElementById('answerDisplay');
    const messageDisplay = document.getElementById('messageDisplay');

    function showMessage(message, isError = false) {
        messageDisplay.textContent = message;
        messageDisplay.className = isError ? 'error' : 'success';
        messageDisplay.style.display = 'block';
        setTimeout(() => {
            messageDisplay.style.display = 'none';
        }, 5000);
    }

    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showMessage(data.error, true);
            } else {
                showMessage(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage('An error occurred while uploading the file.', true);
        });
    });

    getQuestionBtn.addEventListener('click', function() {
        fetch('/get_question')
            .then(response => {
                if (!response.ok) {
                    throw new Error('No questions available');
                }
                return response.json();
            })
            .then(data => {
                questionDisplay.textContent = data.question;
                answerDisplay.textContent = data.answer;
                answerDisplay.style.display = 'none';
                showAnswerBtn.style.display = 'block';
                showMessage('Question retrieved successfully');
            })
            .catch(error => {
                console.error('Error:', error);
                showMessage(error.message, true);
            });
    });

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
            answerDisplay.style.display = 'none';
            showAnswerBtn.style.display = 'block';
            showMessage('Question generated successfully');
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage(error.message, true);
        });
    });

    showAnswerBtn.addEventListener('click', function() {
        answerDisplay.style.display = 'block';
        this.style.display = 'none';
    });
});
