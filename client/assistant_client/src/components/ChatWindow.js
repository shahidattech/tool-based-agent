import React, { useEffect, useState } from 'react';
import { Paper, Button, IconButton, CircularProgress, TextField, Box, Typography } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import UserSelection from './UserSelection';
import { sendMessageToBot, deleteConversationHistory } from '../services/botService';
import PDFViewer from './PDFViewer';
import RoleToggle from './RoleToggle';
import sampleLogo from './sample_logo.jpeg'; // Adjust the path as necessary
import './ChatWindow.css';

const ChatWindow = () => {
  const [messages, setMessages] = useState([]);
  const [selectedRole, setSelectedRole] = useState(null);
  const [pdfUrl, setPdfUrl] = useState(null);
  const [botResponse, setBotResponse] = useState(null);
  const [loading, setLoading] = useState(false); // Loading state
  const [signature, setSignature] = useState(''); // Signature state

  useEffect(() => {
    console.log("PDF File URL in Chat Window: ", pdfUrl);
    setPdfUrl(pdfUrl);
  }, [pdfUrl]);

  const handleClose = () => {
    window.location.href = '/';
    handleDeleteConversationHistory(true);
  };

  const handleNewChat = () => {
    handleDeleteConversationHistory(false);
  };

  const handleDeleteConversationHistory = async (shouldNavigate = true) => {
    try {
      await deleteConversationHistory();
      setMessages([]);
      setPdfUrl(null);
      setBotResponse(null);
      setLoading(false);
      setSignature('');
      if (shouldNavigate) {
        window.location.href = '/';
      }
    } catch (error) {
      console.error('Failed to delete conversation history:', error);
    }
  };

  const extractPdfFileName = (botResponse) => {
    const pdfPattern = /(\w+\.pdf)/i; // Regular expression to match the PDF file name
    const match = botResponse.match(pdfPattern);
    return match ? match[0] : null; // Return the file name if found, otherwise return null
  };


  const handleSend = async (message) => {
    setMessages([...messages, { text: message, sender: selectedRole, id: messages.length }]);
    setLoading(true); // Set loading to true

    try {
      console.log("Selected Role: ", selectedRole);
      const prefixedMessage = `I am ${selectedRole}: ${message}`;
      const botResponse = await sendMessageToBot(prefixedMessage, selectedRole);

      if (botResponse.includes('.pdf')) {
        const pdfFileName = extractPdfFileName(botResponse);
        if (pdfFileName) {
          console.log(`Displaying PDF file: ${pdfFileName}`);
          setPdfUrl(pdfFileName); // Update this path as needed
          console.log("PDF URL: ", pdfUrl);
        }
      }

      const keyMappings = {
        full_name: 'Full Name',
        phone_primary: 'Primary Phone',
        phone_secondary: 'Secondary Phone',
        address: 'Address',
        policy: 'Policy',
        policy_no: 'Policy Number',
        effective_date: 'Effective Date',
        expiry_date: 'Expiry Date',
        provider: 'Provider',
        vehicle: 'Vehicle',
        vin: 'VIN',
        trim: 'Trim',
        miles: 'Miles',
        color: 'Color',
        trade_vehicle: 'Trade Vehicle',
        sale_price: 'Sale Price',
        rebate: 'Rebate',
        dealer_fees: 'Dealer Fees',
        trade_value: 'Trade Value',
        trade_payoff: 'Trade Payoff',
        tax_rate: 'Tax Rate',
        ssn: 'SSN',
        cibil_score: 'CIBIL Score',
        customer_resdiential_info: 'Customer Residential Info',
        duration_of_living: 'Duration of Living',
        residence_type: 'Residence Type',
        rent: 'Rent',
        employee_info: 'Employee Info',
        employment_type: 'Employment Type',
        duration_of_employment: 'Duration of Employment',
        organization: 'Organization',
        monthly_income: 'Monthly Income',
        agreement: 'Agreement',
        deal_number: 'Deal Number',
        option: 'Option',
        details: 'Details',
        loan_package_name: 'Loan Package Name',
        provider_name: 'Provider Name',
        provider_phone: 'Provider Phone',
        package_includes: 'Package Includes',
        loan_terms_in_months: 'Loan Terms (Months)',
        interest_rate: 'Interest Rate',
        min_cibil_score: 'Minimum CIBIL Score',
        monthly_payment: 'Monthly Payment'
      };
      
      const formatBotResponse = (botResponse) => {
        const formatDict = (dict, indent = 0) => {
          let result = '';
          const indentation = ' '.repeat(indent);
          for (const [key, value] of Object.entries(dict)) {
            if (key === '_id') continue; // Skip _id key
            const displayKey = keyMappings[key] || key; // Use meaningful name if available
            const boldKey = `**${displayKey}**`; // Make key bold
            if (Array.isArray(value)) {
              result += `${indentation}${boldKey}:\n`;
              value.forEach((item, index) => {
                if (typeof item === 'object' && item !== null) {
                  result += `${indentation}  Option ${index + 1}:`;
                  result += formatDict(item, indent + 4);
                } else {
                  result += `${indentation}  - ${item}\n`;
                }
              });
            } else if (typeof value === 'object' && value !== null) {
              result += `${indentation}${boldKey}:\n${formatDict(value, indent + 2)}`;
            } else {
              result += `${indentation}${boldKey}: ${value}\n`;
            }
          }
          return result;
        };
      
        const formatArray = (array, indent = 0) => {
          let result = '';
          array.forEach((item, index) => {
            result += `Option ${index + 1}:\n${formatDict(item, indent + 2)}`;
          });
          return result;
        };
      
        const extractAndFormatJson = (text) => {
          const jsonMatch = text.match(/{.*}|\[.*\]/);
          if (jsonMatch) {
            const jsonString = jsonMatch[0];
            try {
              const parsedJson = JSON.parse(jsonString.replace(/'/g, '"'));
              let formattedJson;
              if (Array.isArray(parsedJson)) {
                formattedJson = formatArray(parsedJson);
              } else {
                formattedJson = formatDict(parsedJson);
              }
              return text.replace(jsonString, `\n${formattedJson}`);
            } catch (e) {
              // JSON parsing failed, return original text
              return text;
            }
          }
          return text;
        };
      
        return extractAndFormatJson(botResponse);
      };
      const isDictOrListOfDicts = (response) => {
        console.log("isDictOrListOfDicts:: Response: ", response);
        try {
          // Extract JSON part from the response
          const jsonMatch = response.match(/{.*}|\[.*\]/);
          if (jsonMatch) {
            const jsonString = jsonMatch[0];
            const parsedResponse = JSON.parse(jsonString.replace(/'/g, '"'));
            if (Array.isArray(parsedResponse)) {
              return parsedResponse.every(item => typeof item === 'object' && item !== null);
            }
            return typeof parsedResponse === 'object' && parsedResponse !== null;
          }
          return false;
        } catch (e) {
          return false;
        }
      };
      
      const formattedBotResponse = isDictOrListOfDicts(botResponse) ? formatBotResponse(botResponse) : botResponse;


      setMessages((prevMessages) => [
        ...prevMessages,
        { text: formattedBotResponse, sender: 'AI FI', id: prevMessages.length },
      ]);

    } catch (error) {
      console.error('Failed to send message to bot:', error);
    } finally {
      setLoading(false); // Set loading to false
    }
  };

  // const handleRoleSelection = async (role) => {
  //   setSelectedRole(role);
  // };

  const handleSignatureSend = () => {
    handleSend(`Signature: ${signature}`);
    setSignature(''); // Clear the signature input after sending
  };

  return (
    <div className={`container ${pdfUrl ? 'with-pdf' : ''}`}>
      <div className='chat-window'>
        <Box sx={{ display: 'flex', alignItems: 'center', width: '100%', padding: 1 }}>
          <img src={sampleLogo} alt="Logo" style={{ height: '50px', marginRight: '10px' }} />
          <Typography variant="h6" component="div">
          Welcome to Your AI Finance Manager!
          </Typography>
        </Box>
        {selectedRole && (
          <Box sx={{ position: 'absolute', top: '10px', right: '10px', display: 'flex', gap: 1 }}>
            <IconButton 
              onClick={handleClose} 
              className='close-button'
              sx={{
                backgroundColor: '#f44336', // Red background
                color: '#fff', // White color
                '&:hover': {
                  backgroundColor: '#d32f2f', // Darker red on hover
                },
              }}
            >
              <CloseIcon />
            </IconButton>
            {messages.length > 0 && (
              <Button
                variant="contained"
                color="primary"
                onClick={handleNewChat}
                sx={{
                  backgroundColor: '#1976d2', // Blue background
                  color: '#fff', // White color
                  '&:hover': {
                    backgroundColor: '#1565c0', // Darker blue on hover
                  },
                }}
              >
                New Chat
              </Button>
            )}
          </Box>
        )}
        <Paper elevation={3} sx={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column' }}>
          {selectedRole && <RoleToggle selectedRole={selectedRole} onRoleChange={setSelectedRole} />}
          {!selectedRole ? (
            <UserSelection onSelect={setSelectedRole} />
          ) : (
            <>
              {loading && (
                  <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', marginTop: 2 }}>
                    <CircularProgress />
                  </Box>
                )}
              <MessageList messages={messages} />
              <MessageInput addMessage={handleSend} />
            </>
          )}
        </Paper>
      </div>
      {pdfUrl && (
        <div className='pdf-viewer-container'>
          <Paper elevation={3} sx={{ width: '100%', height: '95%', display: 'flex', flexDirection: 'column' }}> 
            <PDFViewer pdfUrl={pdfUrl} />
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', padding: 2 }}>
              <TextField
                label="Signature"
                variant="outlined"
                value={signature}
                onChange={(e) => setSignature(e.target.value)}
                sx={{ marginRight: 2 }}
              />
              <Button
                variant="contained"
                color="primary"
                onClick={handleSignatureSend}
              >
                Send Signature
              </Button>
            </Box>
          </Paper>
        </div>
      )}
    </div>
  );
};

export default ChatWindow;