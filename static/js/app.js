document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const getQuestionBtn = document.getElementById('getQuestionBtn');
    const generateQuestionBtn = document.getElementById('generateQuestionBtn');
    const showAnswerBtn = document.getElementById('showAnswerBtn');
    const questionDisplay = document.getElementById('questionDisplay');
    const answerDisplay = document.getElementById('answerDisplay');
    const messageDisplay = document.getElementById('messageDisplay');
    const searchInput = document.getElementById('searchInput');
    const searchBtn = document.getElementById('searchBtn');
    const searchResults = document.getElementById('searchResults');

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
            console.log('Upload response:', data);
            if (data.error) {
                showMessage(data.error, true);
            } else {
                showMessage(data.message);
            }
        })
        .catch(error => {
            console.error('Upload error:', error);
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
                console.log('Get question response:', data);
                displayQuestion(data);
            })
            .catch(error => {
                console.error('Get question error:', error);
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
            console.log('Generate question response:', data);
            displayQuestion(data);
        })
        .catch(error => {
            console.error('Generate question error:', error);
            showMessage(error.message, true);
        });
    });

    searchBtn.addEventListener('click', function() {
        const query = searchInput.value.trim();
        if (!query) {
            showMessage('Please enter a search query', true);
            return;
        }
        fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Search response:', data);
            displaySearchResults(data);
        })
        .catch(error => {
            console.error('Search error:', error);
            showMessage('An error occurred while searching for questions.', true);
        });
    });

    showAnswerBtn.addEventListener('click', function() {
        answerDisplay.style.display = 'block';
        this.style.display = 'none';
    });

    function displayQuestion(data) {
        questionDisplay.textContent = data.question;
        answerDisplay.textContent = data.answer;
        answerDisplay.style.display = 'none';
        showAnswerBtn.style.display = 'block';
        showMessage('Question retrieved successfully');
    }

    function displaySearchResults(results) {
        searchResults.innerHTML = '';
        if (results.length === 0) {
            searchResults.textContent = 'No results found.';
            return;
        }
        const ul = document.createElement('ul');
        results.forEach(result => {
            const li = document.createElement('li');
            li.innerHTML = `
                <strong>Question:</strong> ${result.question}<br>
                <strong>Similarity:</strong> ${(result.similarity * 100).toFixed(2)}%<br>
                <strong>Difficulty:</strong> ${result.difficulty}<br>
                <strong>Source:</strong> ${result.source}
            `;
            li.addEventListener('click', () => displayQuestion(result));
            ul.appendChild(li);
        });
        searchResults.appendChild(ul);
    }
});
