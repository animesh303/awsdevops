exports.handler = async (event) => {
    console.log('Event received:', JSON.stringify(event, null, 2));
    
    const response = {
        statusCode: 200,
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        body: JSON.stringify({
            message: 'Hello from AWS Lambda!',
            timestamp: new Date().toISOString(),
            requestId: event.requestContext?.requestId || 'N/A',
            event: event
        })
    };
    
    return response;
};