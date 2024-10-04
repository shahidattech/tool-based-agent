import React from 'react';
import { ToggleButton, ToggleButtonGroup, Box } from '@mui/material';

const RoleToggle = ({ selectedRole, onRoleChange }) => {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginBottom: 2 }}>
      <ToggleButtonGroup
        value={selectedRole}
        exclusive
        onChange={(e, newRole) => {
          if (newRole !== null) {
            onRoleChange(newRole);
          }
        }}
        aria-label="role selection"
      >
        <ToggleButton
          value="customer"
          aria-label="customer"
          sx={{
            backgroundColor: 'lightgrey',
            color: 'black',
            '&.Mui-selected': {
              backgroundColor: 'darkgreen',
              color: 'white',
            },
            '&:hover': {
              backgroundColor: selectedRole === 'customer' ? 'darkgreen' : 'lightgrey',
              color: 'black',
            }
          }}
        >
          Customer
        </ToggleButton>
        <ToggleButton
          value="dealer"
          aria-label="dealer"
          sx={{
            backgroundColor: 'lightgrey',
            color: 'black',
            '&.Mui-selected': {
              backgroundColor: 'darkgreen',
              color: 'white',
            },
            '&:hover': {
              backgroundColor: selectedRole === 'dealer' ? 'darkgreen' : 'lightgrey',
              color: 'black',
            }
          }}
        >
          Dealer
        </ToggleButton>
      </ToggleButtonGroup>
    </Box>
  );
};

export default RoleToggle;