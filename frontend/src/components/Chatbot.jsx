import { useState } from 'react';
import { useImmer } from 'use-immer';
import ChatMessages from '../components/ChatMessages';
import ChatInput from '../components/ChatInput';

function Chatbot() {
  const [messages, setMessages] = useImmer([]);
  const [newMessage, setNewMessage] = useState('');
  const isLoading = messages.length && messages[messages.length - 1].loading;

  // API query function integrated within the Chatbot component
  async function queryChat(message) {
    const apiUrl = "http://127.0.0.1:5000";
    //const apiUrl = process.env.API_URL;
    console.log(apiUrl);
    if (!apiUrl) {
      console.error('API_URL is not defined in the .env file');
      return Promise.reject('API URL not defined');
    }

    const res = await fetch(`${apiUrl}/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: message }),
    });

    if (!res.ok) {
      const errorData = await res.json();
      return Promise.reject({ status: res.status, data: errorData });
    }

    return res.json();
  }

  async function submitNewMessage() {
    const trimmedMessage = newMessage.trim();
    if (!trimmedMessage || isLoading) return;

    // Add the user's message to the chat
    setMessages(draft => [
      ...draft,
      { role: 'user', content: trimmedMessage },
      { role: 'assistant', content: '', sources: [], loading: true }
    ]);
    setNewMessage('');

    try {
      // Send the query to the backend and receive the response
      const { answer, sources } = await queryChat(trimmedMessage);

      // Update the assistant's message with the response
      setMessages(draft => {
        draft[draft.length - 1] = {
          role: 'assistant',
          content: answer,
          sources,
          loading: false
        };
      });
    } catch (err) {
      console.error('Error querying the chatbot:', err);

      // Update the assistant's message to show an error
      setMessages(draft => {
        draft[draft.length - 1] = {
          role: 'assistant',
          content: 'An error occurred while fetching the response. Please try again.',
          sources: [],
          loading: false,
          error: true
        };
      });
    }
  }

  return (
    <div className='relative grow flex flex-col gap-6 pt-6'>
      {messages.length === 0 && (
        <div className='mt-3 font-urbanist text-primary-blue text-xl font-light space-y-2'>
          <p>👋 Welcome!</p>
          <p>
            I am here to assist you with insights derived from the vast knowledge integrated into this system.
          </p>
          <p>
            Ask me anything about the information provided or the features of this application, and I’ll do my best to help you.
          </p>
        </div>
      )}
      <ChatMessages messages={messages} isLoading={isLoading} />
      <ChatInput
        newMessage={newMessage}
        isLoading={isLoading}
        setNewMessage={setNewMessage}
        submitNewMessage={submitNewMessage}
      />
    </div>
  );
}

export default Chatbot;
