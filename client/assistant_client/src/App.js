import React from 'react';
import ChatWindow from './components/ChatWindow';
import { Container, Box } from '@mui/material';

function App() {
  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          height: '100vh',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
        <ChatWindow />
      </Box>
    </Container>
  );
}

export default App;
