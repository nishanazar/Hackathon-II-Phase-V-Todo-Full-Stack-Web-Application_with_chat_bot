# Quickstart Guide: Floating AI Chat Widget

## Prerequisites

Before implementing the floating AI chat widget, ensure your development environment has:

- Node.js 18+ installed
- Next.js 16+ project set up
- Better Auth configured for authentication
- OpenAI account with ChatKit access

## Environment Variables

Add the following environment variable to your `.env.local` file:

```bash
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=pk_your_openai_domain_key_here
```

Make sure to add your production domain to the OpenAI domain allowlist.

## Installation

1. Install the OpenAI ChatKit JS Agent:

```bash
npm install @openai/chatkit-jsagent
```

2. Verify installation by checking your `package.json`:

```json
{
  "dependencies": {
    "@openai/chatkit-jsagent": "^latest"
  }
}
```

## Basic Implementation

### 1. Create the Floating Chat Component

Create a new file at `frontend/src/components/FloatingChat/FloatingChatWidget.tsx`:

```tsx
'use client';

import { useState, useEffect } from 'react';
import { Chat } from '@openai/chatkit-jsagent';
import { useAuth } from 'better-auth/react';

const FloatingChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const { isAuth, user } = useAuth();

  // Only show widget for authenticated users
  if (!isAuth) return null;

  return (
    <div className={`fixed bottom-4 right-4 z-50 transition-all duration-300 ${isOpen ? 'w-80 h-[500px]' : 'w-auto h-auto'}`}>
      {isOpen ? (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl overflow-hidden w-full h-full">
          <div className="flex justify-between items-center p-3 bg-blue-500 text-white">
            <span>AI Assistant</span>
            <button onClick={() => setIsOpen(false)} className="text-white">
              ×
            </button>
          </div>
          <div className="h-[calc(100%-40px)]">
            <Chat
              apiEndpoint={`/api/${user.id}/chat`}
              theme="auto"
              // Additional props as needed
            />
          </div>
        </div>
      ) : (
        <button
          onClick={() => setIsOpen(true)}
          className="bg-blue-500 text-white rounded-full p-3 shadow-lg hover:bg-blue-600 transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
        </button>
      )}
    </div>
  );
};

export default FloatingChatWidget;
```

### 2. Create the Global Provider

Create a provider component at `frontend/src/components/FloatingChat/FloatingChatProvider.tsx`:

```tsx
'use client';

import { ReactNode } from 'react';
import FloatingChatWidget from './FloatingChatWidget';

type Props = {
  children: ReactNode;
};

const FloatingChatProvider = ({ children }: Props) => {
  return (
    <>
      {children}
      <FloatingChatWidget />
    </>
  );
};

export default FloatingChatProvider;
```

### 3. Integrate into Layout

Wrap your application with the provider in `frontend/src/app/layout.tsx`:

```tsx
import FloatingChatProvider from '../components/FloatingChat/FloatingChatProvider';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <FloatingChatProvider>
          {children}
        </FloatingChatProvider>
      </body>
    </html>
  );
}
```

## API Endpoint

Create the API endpoint at `backend/src/api/{user_id}/chat/route.py`:

```python
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from backend.auth import get_current_user
from backend.models.user import User

router = APIRouter()

class ChatMessage(BaseModel):
    message: str
    userId: str

@router.post("/api/{user_id}/chat")
async def handle_chat(user_id: str, message_data: ChatMessage, current_user: User = Depends(get_current_user)):
    # Verify that the user_id in the URL matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Process the chat message and return a response
    # This is where you'd integrate with OpenAI's API or your own AI service
    response = f"Echo: {message_data.message}"
    
    return {"response": response}
```

## Testing

1. Start your development server:

```bash
npm run dev
```

2. Navigate to any page in your application
3. Verify that the floating chat icon appears in the bottom-right corner for authenticated users
4. Click the icon to open the chat panel
5. Send a test message and verify it reaches your backend endpoint
6. Close the chat panel and verify it collapses properly

## Troubleshooting

### Chat widget not appearing
- Verify that you're logged in (the widget only shows for authenticated users)
- Check that the provider is properly wrapped around your layout

### API communication failing
- Ensure the NEXT_PUBLIC_OPENAI_DOMAIN_KEY is correctly set
- Verify that your domain is allowed in OpenAI's domain allowlist
- Check that the API endpoint follows the correct pattern

### Styling issues
- Ensure Tailwind CSS is properly configured in your project
- Check that the theme="auto" setting works with your existing dark mode implementation