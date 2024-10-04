import React, { useState } from 'react';
import { Box, TextField, IconButton } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import { useMyContext } from '../MyContext'; // Import the context

const MessageInput = ({ addMessage }) => {
  const [input, setInput] = useState('');
  const { state, setState } = useMyContext();

  const handleSend = () => {
    if (input.trim()) {
      addMessage(input);
      setInput('');
    }
  };

  return (
    <Box sx={{ display: 'flex', padding: 1 }}>
      <TextField
        fullWidth
        variant="outlined"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={(e) => {
          if (e.key === 'Enter') handleSend();
        }}
      />
      <IconButton color="primary" onClick={handleSend}>
        <SendIcon />
      </IconButton>
    </Box>
  );
};

export default MessageInput;
