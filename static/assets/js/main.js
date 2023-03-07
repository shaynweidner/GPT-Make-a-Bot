const firstMessageToShow = 1;
const messageForm = document.querySelector('.message-form');
const messageInput = document.querySelector('.message-input');
const clearBtn = document.querySelector('#clear-button');
const messagesContainer = document.querySelector('.messages-container');
const sendButton = document.querySelector(".send-button");

// Start button handling

messageForm.addEventListener('submit', async (event) => { // Event listener to submit the form when Enter key is pressed or when Send button is clicked
    event.preventDefault(); // Prevents the default behavior of the form after submitting
    const messageText = messageInput.value.trim(); // Get the value of the input field without whitespace
    messageInput.value = ''; // clear the input field after submitting
    const message2 = document.createElement('div'); // Create a new div element for sent messages
    message2.classList.add('message', 'sent'); // Add classes ('message' and 'sent') to the created div element
    const message2Text = document.createElement('div'); // Create a new div element to display the text content of the message
    message2Text.classList.add('message-text'); // Add class ('message-text') to the created div element 
    message2Text.textContent = messageText; // Set the text content of the new message element to the submitted text message
    message2.appendChild(message2Text); // Append the message text to the original created message2 container
    messagesContainer.appendChild(message2); // Append the whole message with time stamp to the global message board
    messagesContainer.scrollTop = messagesContainer.scrollHeight; // scroll to the bottom of the messages container
    if (messageText === '') {
        return;
    } else {
        // disable sendButton
        sendButton.disabled = true; // Disable the send button until the response arrives

        // put.dot-flashing into message bubble while waiting for chatbot response
        const pendingMessage = messagePending();
        messagesContainer.appendChild(pendingMessage);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        if (!pendingMessage) {
            console.error("Failed to create a messagePending element");
            return;
        }
    }

    try { // try block handles exceptions that may occur within

        const message = await createMessage(messageText); // Await to create an chatbot response message  

        const pendingMessage = document.querySelector('.messages-container .message.received .message-pending');
        if (pendingMessage) {
          pendingMessage.remove();
        }
        
        messagesContainer.appendChild(message); // Once the message response is returned from createMessage function, it will be appended to the message container
        messagesContainer.scrollTop = messagesContainer.scrollHeight; // then scroll to the bottom of the message container
        sendButton.disabled = false; // re-enable the send button;
    } catch (error) { // Catching any error that could occurs within try block
        sendButton.disabled = false; // re-enable the send button;
        console.error('There was a problem while creating the message:', error); // log an error message along with error causing details
    }
});

clearBtn.addEventListener('click', (event) => { // Add click event for clearing previous conversation histories
    const confirmed = window.confirm("Are you sure you want to clear the conversation history?");  // Prompt the user to confirm if they want to clear the chatbot history

    if (confirmed) { // If user confirms to clear the chatbot history then:
        messagesContainer.innerHTML = ''; // Empty out all the previously sent and received messages from the user
        fetch('/erase_chatbot', { // Call the URL route /erase_chatbot for "POST" request method using "fetch" api
            method: 'POST', // set the request method as POST to send json data
            headers: {
                'Content-Type': 'application/json' // declare the content type header as json
            },
            body: JSON.stringify({}) // Pass empty json object in the body of request message
        })
            .then(response => {
                if (!response.ok) { // Check if the response result does not contain any error
                    throw new Error('Network response was not ok'); // If response contain errors throw an error
                }
            })
            .then(() => { // when response is ok, set the following operations:
                location.reload(); // Reload the current page after some time interval
            })
            .catch(error => { // If there is an error in above try block the we can catch it here likewise
                console.error('There was a problem with the fetch operation:', error); // Log an error message along with error causing details
            });
    }
});

// End button handling



// This function takes a message as input and returns a promise that will resolve to the response from the chatbot server
function createMessage(question) {

    // Return a new promise with resolver and rejector functions as arguments
    return new Promise((resolve, reject) => {
        const data = { question } // Create an object with the message text as a property
        fetch('/chatbot', { // Send a POST request to the /chatbot endpoint of the server
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data) // Set the body of the request as the JSON representation of the message object
        })
            .then(response => { // Handle the response from the server
                if (!response.ok) { // Check if the response returned an error status code
                    throw new Error('Network response was not ok'); // If so, throw an error with a custom message
                }
                return response.json(); // Otherwise, parse the response body as JSON and return it
            })
            .then(json => { // Handle the JSON data received from the server
                // Create a new div element to hold the received message
                const response = document.createElement('div');
                response.classList.add('message', 'received'); // Add CSS classes to the new div element
                const responseText = document.createElement('div');
                responseText.classList.add('message-text'); // Add a CSS class to the inner div element holding the message text
                responseText.textContent = json.response; // Set the text content of the inner div element to the response received from the chatbot server
                response.append(responseText); // Add the inner div element to the new div element
                resolve(response); // Resolve the promise with the new div element as its value
            })
            .catch(error => { // Handle errors that may occur during the fetch operation
                console.error('There was a problem with the fetch operation:', error); // If there's an error, log it to the console
                reject(error); // Reject the promise with the error as its value
            });
    });
}





// Function to initialize chat history with past messages
function initialize() {
    // Fetch conversation history JSON file from the server 
    fetch('static/_conversation_history.json')
        .then(response => response.json())  // When data is received, parse it as JSON
        .then(data => {                     // After parsing JSON data
            parsePastMessages(data);         // Call a function to loop through each past message and add to chatbox
        })
        .catch(error => {                   // If there's any error fetching or parsing the JSON file:
            console.error('There was an error parsing the conversation history:', error);
        });
}

// Function to loop through past chat messages and display them in the appropriate message container
function parsePastMessages(arr) {
    for (let i = firstMessageToShow; i < arr.length; i++) {     // Loops through each past message one by one
        if (arr[i].role === 'user') {                           // Checks if the message is sent by 'user'
            const message = document.createElement('div');      // Create a new message element div
            message.classList.add('message', 'sent');           // Add CSS class names to the div element
            const messageText = document.createElement('div');  // Create another element for the message text
            messageText.classList.add('message-text');          // Add CSS class names to the message text element
            messageText.textContent = arr[i].content;           // Set the text content of the message text element to the message content
            message.appendChild(messageText);                    // Append the message text element to the message element div
            messagesContainer.appendChild(message);              // Append the message element div to the messages container
            messagesContainer.scrollTop = messagesContainer.scrollHeight;   // Scrolls down to the latest message in the container
        } else if (arr[i].role === 'assistant') {                // Checks if the message is sent by 'assistant'
            const message = document.createElement('div');       // Create a new message element div
            message.classList.add('message', 'received');         // Add CSS class names to the div element
            const messageText = document.createElement('div');   // Create another element for the message text
            messageText.classList.add('message-text');           // Add CSS class names to the message text element
            messageText.textContent = arr[i].content;            // Set the text content of the message text element to the message content
            message.appendChild(messageText);                      // Append the message text element to the message element div
            messagesContainer.appendChild(message);               // Append the message element div to the messages container
            messagesContainer.scrollTop = messagesContainer.scrollHeight;    // Scrolls down to the latest message in the container
        }
    }
}

function messagePending() {
    const response = document.createElement('div');
    response.classList.add('message', 'received'); // Add CSS classes to the new div element

    const PendingMessage = document.createElement('div');
    PendingMessage.classList.add('message', 'received'); // Add CSS classes to the new div element
    const responseText = document.createElement('div');
    responseText.classList.add('message-pending'); // Add a CSS class to the inner div element holding the message text
    const dotFlashingDiv = document.createElement('div');
    dotFlashingDiv.classList.add('dot-flashing'); // Add a CSS class to the inner div element holding the message text    
    responseText.appendChild(dotFlashingDiv);
    PendingMessage.append(responseText); // Add the inner div element to the new div element
    return PendingMessage;
}



window.onload = initialize();