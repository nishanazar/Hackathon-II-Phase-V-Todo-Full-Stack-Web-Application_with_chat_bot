// Test script to debug API calls
// This script can help verify if the backend API is accessible and working correctly

async function testBackendAPI() {
  console.log('Testing backend API connectivity...');

  // Use the same API base URL as in api.ts
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

  try {
    // Test the health endpoint first
    const healthResponse = await fetch(`${API_BASE_URL}/health`);
    console.log('Health check response:', await healthResponse.text());

    // Test the root endpoint
    const rootResponse = await fetch(`${API_BASE_URL}`);
    console.log('Root endpoint response:', await rootResponse.text());
  } catch (error) {
    console.error('Error testing backend API:', error);
  }
}

// Run the test
testBackendAPI();