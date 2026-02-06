import { NextApiRequest, NextApiResponse } from 'next';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/pages/api/auth/[...nextauth]'; // Adjust path as needed

// Define the handler for the POST request
export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  // Only allow POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({ error: { code: 'METHOD_NOT_ALLOWED', message: 'Only POST requests allowed' } });
  }

  try {
    // Extract user_id from the URL
    const { user_id } = req.query;

    // Get the session to verify the user is authenticated
    const session = await getServerSession(req, res, authOptions);

    if (!session) {
      return res.status(401).json({ 
        error: { 
          code: 'UNAUTHORIZED', 
          message: 'Invalid or missing authentication token' 
        } 
      });
    }

    // Verify that the user_id in the URL matches the authenticated user
    if (session.user?.id !== user_id) {
      return res.status(403).json({ 
        error: { 
          code: 'FORBIDDEN', 
          message: 'Access denied. User ID mismatch.' 
        } 
      });
    }

    // Parse the request body
    const { message, timestamp, metadata } = req.body;

    // Validate the message field
    if (!message || typeof message !== 'string') {
      return res.status(400).json({ 
        error: { 
          code: 'INVALID_REQUEST', 
          message: 'Message is required and must be a string' 
        } 
      });
    }

    // Process the chat message and return a response
    // This is where you'd integrate with OpenAI's API or your own AI service
    const response = `Echo: ${message}`;
    
    // Return the response
    return res.status(200).json({
      id: `resp_${Date.now()}`,
      response,
      timestamp: new Date().toISOString(),
      status: 'success',
      metadata: {
        processing_time_ms: 120 // Example processing time
      }
    });
  } catch (error) {
    console.error('Error handling chat request:', error);
    return res.status(500).json({ 
      error: { 
        code: 'INTERNAL_ERROR', 
        message: 'An unexpected error occurred' 
      } 
    });
  }
}