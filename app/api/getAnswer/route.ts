import { NextResponse } from "next/server";

export async function POST(request: Request) {
  try {
    // Parse the request body
    const { question, sources } = await request.json();
    const payload = JSON.stringify({
      model: "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
      messages: [
        { role: "system", content: sources },
        { role: "user", content: question },
      ],
      stream: true, // Enable streaming
    })
    console.log("payload: " + payload);

    // Call your FastAPI endpoint
    const fastApiResponse = await fetch("http://localhost:8000/infer", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: payload,
    });

    if (!fastApiResponse.ok) {
      const errorMessage = await fastApiResponse.text();
      return NextResponse.json(
        { error: `FastAPI error: ${errorMessage}` },
        { status: fastApiResponse.status }
      );
    }

    if (!fastApiResponse.body) {
      throw new Error("FastAPI response body is null.");
    }

    // Create a streaming response by piping chunks
    const encoder = new TextEncoder();
    const readableStream = new ReadableStream({
      async start(controller) {
        const reader = fastApiResponse.body?.getReader();
        if (!reader) {
          controller.close();
          return;
        }

        // Read chunks from the FastAPI response
        while (true) {
          const { value, done } = await reader.read();
          if (done) break;

          // Send the chunk to the client
          controller.enqueue(value);
        }

        controller.close();
      },
    });

    return new Response(readableStream, {
      status: 202,  // Set the status code to 202
      headers: { "Content-Type": "text/plain; charset=utf-8" },
    });
  } catch (error) {
    console.error("Error in getAnswer route:", error);
    return NextResponse.json(
      { error: "Internal Server Error" },
      { status: 500 }
    );
  }
}
