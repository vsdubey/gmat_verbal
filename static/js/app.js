document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const getQuestionBtn = document.getElementById('getQuestionBtn');
    const generateQuestionBtn = document.getElementById('generateQuestionBtn');
    const showAnswerBtn = document.getElementById('showAnswerBtn');
    const questionDisplay = document.getElementById('questionDisplay');
    const answerDisplay = document.getElementById('answerDisplay');

    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while uploading the file.');
        });
    });

    getQuestionBtn.addEventListener('click', function() {
        fetch('/get_question')
            .then(response => response.json())
            .then(data => {
                questionDisplay.textContent = data.question;
                answerDisplay.textContent = data.answer;
                answerDisplay.style.display = 'none';
                showAnswerBtn.style.display = 'block';
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while fetching the question.');
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
        .then(response => response.json())
        .then(data => {
            questionDisplay.textContent = data.question;
            answerDisplay.textContent = data.answer;
            answerDisplay.style.display = 'none';
            showAnswerBtn.style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while generating the question.');
        });
    });

    showAnswerBtn.addEventListener('click', function() {
        answerDisplay.style.display = 'block';
        this.style.display = 'none';
    });
});
