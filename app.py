<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JPMC Q&A Bot</title>
    <!-- Tailwind CSS for styling -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Google Fonts: Inter -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        /* Custom styles for the app */
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f0f4f8; /* Light blue-gray background */
        }
        /* JPMC-inspired color scheme */
        .jpmc-blue {
            background-color: #005ea6;
        }
        .jpmc-blue-text {
            color: #005ea6;
        }
        .jpmc-gray {
            background-color: #5a5a5a;
        }
        /* Custom styles for the response box */
        #response-box {
            white-space: pre-wrap; /* Preserves formatting and line breaks */
            word-wrap: break-word; /* Breaks long words to prevent overflow */
        }
        /* Simple loading spinner animation */
        .spinner {
            border: 4px solid rgba(0, 0, 0, 0.1);
            width: 36px;
            height: 36px;
            border-radius: 50%;
            border-left-color: #005ea6;
            animation: spin 1s ease infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body class="flex items-center justify-center min-h-screen">
    <!-- Main container for the application -->
    <div class="w-full max-w-2xl mx-auto p-6 md:p-8 bg-white rounded-2xl shadow-2xl">
        <!-- Header Section -->
        <div class="text-center mb-6">
            <h1 class="text-3xl md:text-4xl font-bold jpmc-blue-text">JPMC Q&A Bot</h1>
            <p class="text-gray-500 mt-2">Your specialized assistant for all things JPMorgan Chase</p>
        </div>

        <!-- Input Section -->
        <div class="flex flex-col sm:flex-row gap-3 mb-4">
            <input type="text" id="question-input" placeholder="e.g., When was JPMorgan Chase founded?" class="flex-grow p-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 transition">
            <button id="submit-btn" class="jpmc-blue hover:bg-blue-800 text-white font-bold py-3 px-6 rounded-lg transition duration-300 shadow-md">
                Ask Question
            </button>
        </div>

        <!-- Response Section -->
        <div class="mt-6 p-5 bg-gray-50 rounded-lg border border-gray-200 min-h-[150px]">
            <h2 class="text-lg font-semibold text-gray-700 mb-2">Answer:</h2>
            <!-- Loading spinner, hidden by default -->
            <div id="loader" class="hidden flex justify-center items-center h-24">
                <div class="spinner"></div>
            </div>
            <!-- Response content will be displayed here -->
            <div id="response-box" class="text-gray-800">
                <p class="text-gray-400">Your answer will appear here...</p>
            </div>
        </div>
    </div>

    <script>
        // DOM element references
        const submitButton = document.getElementById('submit-btn');
        const questionInput = document.getElementById('question-input');
        const responseBox = document.getElementById('response-box');
        const loader = document.getElementById('loader');

        // Event listener for the submit button
        submitButton.addEventListener('click', getAnswer);
        
        // Event listener for pressing "Enter" in the input field
        questionInput.addEventListener('keyup', (event) => {
            if (event.key === 'Enter') {
                getAnswer();
            }
        });

        /**
         * Fetches an answer from the Gemini API based on the user's question.
         */
        async function getAnswer() {
            const userQuestion = questionInput.value.trim();
            if (!userQuestion) {
                responseBox.innerHTML = '<p class="text-red-500">Please enter a question.</p>';
                return;
            }

            // Show loader and disable input/button
            loader.classList.remove('hidden');
            responseBox.innerHTML = '';
            submitButton.disabled = true;
            submitButton.classList.add('opacity-50', 'cursor-not-allowed');
            questionInput.disabled = true;

            // System prompt to constrain the LLM to only answer JPMC-related questions
            const systemPrompt = `You are a specialized Q&A assistant for JPMorgan Chase (JPMC). Your sole purpose is to answer questions related to JPMC's business, history, financials, and operations. If a user asks a question that is NOT about JPMC, you MUST respond with: 'I am a JPMC specialist and can only answer questions about JPMorgan Chase. Please ask me something related to the company.' Do not answer any questions about other topics, people, or companies.`;
            
            const fullPrompt = `${systemPrompt}\n\nUser's question: "${userQuestion}"`;

            // Function to make the API call with exponential backoff
            const fetchWithBackoff = async (retries = 3, delay = 1000) => {
                try {
                    const apiKey = ""; // API key is handled by the environment
                    const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key=${apiKey}`;
                    
                    const payload = {
                        contents: [{
                            parts: [{ text: fullPrompt }]
                        }]
                    };

                    const response = await fetch(apiUrl, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(payload)
                    });

                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }

                    const result = await response.json();
                    
                    if (result.candidates && result.candidates.length > 0 && result.candidates[0].content.parts.length > 0) {
                        return result.candidates[0].content.parts[0].text;
                    } else {
                        throw new Error("Invalid response structure from API.");
                    }

                } catch (error) {
                    if (retries > 0) {
                        await new Promise(res => setTimeout(res, delay));
                        return fetchWithBackoff(retries - 1, delay * 2);
                    } else {
                        throw error;
                    }
                }
            };

            try {
                const answer = await fetchWithBackoff();
                responseBox.textContent = answer;
            } catch (error) {
                console.error('Error fetching answer:', error);
                responseBox.innerHTML = '<p class="text-red-500">Sorry, something went wrong while fetching the answer. Please try again.</p>';
            } finally {
                // Hide loader and re-enable input/button
                loader.classList.add('hidden');
                submitButton.disabled = false;
                submitButton.classList.remove('opacity-50', 'cursor-not-allowed');
                questionInput.disabled = false;
            }
        }
    </script>
</body>
</html>
