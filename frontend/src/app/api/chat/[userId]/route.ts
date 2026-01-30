import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest, { params }: { params: { userId: string } }) {
  const { userId } = params;

  try {
    // Get the form data from the request
    const formData = await request.formData();
    const message = formData.get('message') as string;
    const conversationId = formData.get('conversation_id') as string | null;

    // Backend URL - use environment variable or default to local backend
    const backendUrl = process.env.BACKEND_API_URL || 'http://127.0.0.1:8001';

    // Construct the backend API URL
    const backendApiUrl = `${backendUrl}/chat/${userId}`;

    // Create form data to send to the backend
    const backendFormData = new FormData();
    backendFormData.append('message', message);
    if (conversationId) {
      backendFormData.append('conversation_id', conversationId);
    }

    // Create the request to the backend
    const backendResponse = await fetch(backendApiUrl, {
      method: 'POST',
      body: backendFormData
    });

    if (!backendResponse.ok) {
      const errorText = await backendResponse.text();
      console.error(`Backend API error: ${backendResponse.status} - ${errorText}`);
      throw new Error(`Backend API error: ${backendResponse.status}`);
    }

    const responseData = await backendResponse.json();

    return NextResponse.json(responseData);
  } catch (error) {
    console.error('Error in chat API route:', error);

    return NextResponse.json({
      conversation_id: null,
      response: "Sorry, I encountered an error processing your request. Please try again.",
      tool_calls: [],
      timestamp: new Date().toISOString()
    }, {
      status: 500
    });
  }
}