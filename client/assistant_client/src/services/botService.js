import axios from 'axios';

const ASSISTANT_API_URL = 'http://localhost:8000/nova/ai-fi/api/v1/assistant/ai_assistant/ai-assistant/';
const WEBSERVICE_BASE_URL = 'http://localhost:8001/nova/ai-fi/api/v1/webservices/document-management/download/';
const DELETE_CONVERSATION_HISTORY_URL = 'http://localhost:8000/nova/ai-fi/api/v1/assistant/ai_assistant/delete_conversation_history';

export const sendMessageToBot = async (message, customer_type) => {
  try {
    // Get session_id from local storage if it exists
    const session_id = localStorage.getItem('session_id');
    
    const payload = {
      "query": message,
      "session_id": session_id,
      "customer_type": customer_type,
    };
    console.log('Sending message to bot:', message);
    const response = await axios.post(ASSISTANT_API_URL, payload, {
      headers: {
        'accept': 'application/json',
        'Content-Type': 'application/json'
      }
    });
    console.log('Bot response:', response.data["message"]);
    // If response data contains session_id, store it in local storage session_id key, Below is the response format
    if (response.data["data"] && response.data["data"]["session_id"]) {
      localStorage.setItem('session_id', response.data["data"]["session_id"]);
    }
    return response.data["message"];
  } catch (error) {
    console.error('Error sending message to bot:', error);
    throw error;
  }
};

// Make call to this GET method http://localhost:8001/nova/ai-fi/api/v1/webservices/document-management/download/johndoe_contract.pdf
// to download the PDF file

export const downloadPdf = async (pdfUrl) => {
  try {
    console.log('Downloading PDF:', pdfUrl);
    const full_url = WEBSERVICE_BASE_URL + pdfUrl;
    const response = await axios.get(full_url, {
      responseType: 'blob'
    });
    console.log('PDF downloaded:', response);
    return response.data;
  } catch (error) {
    console.error('Error downloading PDF:', error);
    throw error;
  }
};

// Write function to make call curl -X 'DELETE' \
  // 'http://localhost:8000/nova/ai-fi/api/v1/assistant/ai_assistant/delete_conversation_history' \
  // -H 'accept: */*'
export const deleteConversationHistory = async () => {
  try {
    console.log('Deleting conversation history');
    const response = await axios.delete(DELETE_CONVERSATION_HISTORY_URL, {
      headers: {
        'accept': '*/*'
      }
    });
    console.log('Conversation history deleted:', response);
    return response.data;
  } catch (error) {
    console.error('Error deleting conversation history:', error);
    throw error;
  }
}