# AI Financial Agent

This project is designed to provide support to customers and dealers through a Financial Agent that leverages OpenAI and Azure OpenAI. It consists of three main components:

- **Client**: A React.js application.
- **Web Services**: Services that simulate DMV processes, payments, OTP generation, and validation.
- **Assistant**: The AI agent, exposed through its API, can be integrated with any client.

## How to Start the Application

### Prerequisites

- **Node.js**: Required to run the Client.
- **Docker**: You may need Docker Desktop. If not already installed, get it from Docker Desktop.
  - Ensure Docker is running on your system.

### Setup Steps

#### Step 1: Start Web Services

1. Navigate to the `WebServices` folder.
2. Run the following command:
   ```bash
   docker-compose up --build

3. In a few seconds, the Web Services will be running. To verify, visit: http://localhost:8001/mocked/api/v1/webservices/docs

#### Step 2: Start Assistant Services
This project can run on either the OpenAI or Azure OpenAI platforms.
Configure the Assistant for OpenAI or Azure OpenAI


For OpenAI:

Get your API key from OpenAI API.

For OpenAI:

   1. Get your API key from OpenAI API.
   2. Update the following in Assistant/docker-compose.yml:

   - AI_SOURCE=openai # Set to 'azure_openai' or 'openai'
   - OPENAI_API_KEY='Your OpenAI API Key here'

    For Azure OpenAI:

    1. In your Azure portal, navigate to Resource Management → Keys & Endpoint to find your Azure OpenAI key. Ensure the GPT-4 model is enabled.

    2. Update the following environment variables in Assistant/docker-compose.yml:

    ```bash
        - AI_SOURCE=azure_openai
        - AZURE_OPENAI_ENDPOINT=https://xyzz.openai.azure.com/
        - AZURE_OPENAI_API_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXX
        - AZURE_OPENAI_API_VERSION='2024-05-01-preview'
        - AZURE_OPENAI_MODEL_NAME=gpt-4

    3. Start the Assistant
    1. Navigate to the Assistant folder.
    2. Run the following command:
        
    docker-compose up --build


    4. In a few seconds, the Assistant will be running. To verify, visit: http://localhost:8000/llm/api/v1/assistant/docs#/

#### Step 3: Start  start Assistant Client.

1. Navigate to the client/assistant_client folder.
2. Run the following commands:

npm install
npm start

The UI will be available at: http://localhost:3000/

Demo:

https://app.recorditor.com/recording/2466d969113205a3c5cbb6819f99caee417d54fbd8c0da06a5e8b72652ccc1829f9f9d24eecc179b100651275dc23eb7b2d9ee51049162a7bf114758e057b0b