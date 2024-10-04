import React from 'react';
import { Button, Box, Typography } from '@mui/material';

const UserSelection = ({ onSelect }) => {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
      <Typography variant="h5" sx={{ marginBottom: 2 }}>
        Continue as
      </Typography>
      <Box>
        <Button variant="contained" onClick={() => onSelect('customer')} sx={{ marginRight: 2 }}>
          Customer
        </Button>
        <Button variant="contained" onClick={() => onSelect('dealer')}>
          Dealer
        </Button>
      </Box>
    </Box>
  );
};

export default UserSelection;
