import React, { useEffect, useRef } from 'react';
import { List, ListItem, ListItemText, Box } from '@mui/material';
import {marked} from 'marked';

const MessageList = ({ messages }) => {
  const listRef = useRef(null);

  useEffect(() => {
    if (listRef.current) {
      listRef.current.scrollTop = listRef.current.scrollHeight;
    }
  }, [messages]);

  const getColorBySender = (sender) => {
    switch (sender) {
      case 'customer':
        return '#dde2e8';
      case 'dealer':
        return '#dde2e8';
      case 'AI-FI':
        return '#ffeaae';
      default:
        return '#ffeaae';
    }
  };

  const getIconColorBySender = (sender) => {
    switch (sender) {
      case 'customer':
        return 'blue';
      case 'dealer':
        return 'green';
      case 'AI-FI':
        return 'yellow';
      default:
        return 'skyblue';
    }
  };

  const getTextColorBySender = (sender) => {
    switch (sender) {
      case 'customer':
        return 'white';
      case 'dealer':
        return 'white';
      case 'AI-FI':
        return 'yellow';
      default:
        return 'white';
    }
  };

  return (
    <List ref={listRef} sx={{ overflow: 'auto', flex: 1 }}>
      {console.log(messages)}
      {messages.map((message) => (
        <ListItem
          key={message.id}
          sx={{
            display: 'flex',
            justifyContent: message.sender === 'customer' || message.sender === 'dealer' ? 'flex-end' : 'flex-start',
          }}
        >
          <span
              style={{
                display: 'inline-block',
                width: '40px',
                height: '40px',
                borderRadius: '50%',
                // border: '1px solid #ccc',
                backgroundColor: getIconColorBySender(message.sender),
                color: getTextColorBySender(message.sender),
                fontFamily: 'Arial, sans-serif',
                fontWeight: 'bold',
                fontSmooth: 'auto',
                textAlign: 'center',
                lineHeight: '40px',
                // marginLeft: message.sender === 'customer' || message.sender === 'dealer' ? '0' : '10px',
                textTransform: 'uppercase',
              }}
              >{message.sender === "customer" ? "C" : message.sender === "dealer" ? "D" : "AI"}</span>
         <Box
            sx={{
              maxWidth: '50%',
              backgroundColor: getColorBySender(message.sender),
              color: 'text.secondary',
              borderRadius: 2,
              borderTopLeftRadius: 0,
              borderBottomLeftRadius: 10,
              border: `1px solid ${getIconColorBySender(message.sender)}`,
              padding: 1,
              margin: 1,
              fontFamily: 'Cursive, sans-serif',
              wordWrap: 'break-word',
              overflowWrap: 'break-word',
              whiteSpace: 'pre-wrap', // Ensure newlines are respected
            }}
          >
            <ListItemText
              primary={
                <span
                  dangerouslySetInnerHTML={{
                    __html: marked(message.text),
                  }}
                />
              }
            />
          </Box>
        </ListItem>
      ))}
    </List>
  );
};

export default MessageList;