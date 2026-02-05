import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest, { params }: { params: { userId: string } }) {
  const { userId } = params;

  try {
    let message, conversationId;

    // Check if request is JSON or form data
    const contentType = request.headers.get('content-type');

    if (contentType && contentType.includes('application/json')) {
      // Handle JSON request
      const jsonData = await request.json();
      message = jsonData.message;
      conversationId = jsonData.conversation_id;
    } else {
      // Handle form data request
      const formData = await request.formData();
      message = formData.get('message') as string;
      conversationId = formData.get('conversation_id') as string | null;
    }

    // Get authorization header from the original request to pass to backend
    const authHeader = request.headers.get('authorization');

    // Backend URL - use environment variable or default to local backend
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || process.env.BACKEND_API_URL || 'http://127.0.0.1:8003';

    // Construct the backend API URL
    const backendApiUrl = `${backendUrl}/users/${userId}/chat`;

    // Create JSON data to send to the backend
    const requestData = {
      message: message,
      conversation_id: conversationId || undefined
    };

    // Create the request to the backend
    const backendResponse = await fetch(backendApiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(authHeader && { 'Authorization': authHeader }) // Pass authorization header if present
      },
      body: JSON.stringify(requestData)
    });

    // Handle the case where the backend returns an error
    if (!backendResponse.ok) {
      const errorText = await backendResponse.text();
      console.error(`Backend API error: ${backendResponse.status} - ${errorText}`);

      // Return a proper response instead of throwing an error
      return NextResponse.json({
        conversation_id: conversationId || null,
        response: "Sorry, I encountered an error processing your request. Please make sure you're logged in.",
        timestamp: new Date().toISOString()
      }, {
        status: 200 // Return 200 to prevent frontend errors, but with error message
      });
    }

    const responseData = await backendResponse.json();

    return NextResponse.json(responseData);
  } catch (error) {
    console.error('Error in chat API route:', error);

    return NextResponse.json({
      conversation_id: null,
      response: "Sorry, I encountered an error processing your request. Please try again.",
      timestamp: new Date().toISOString()
    }, {
      status: 200 // Return 200 to prevent frontend errors, but with error message
    });
  }
}