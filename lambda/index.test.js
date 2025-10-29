const { handler } = require('./index');

describe('Lambda Handler', () => {
  test('should return 200 status code', async () => {
    const event = {
      requestContext: {
        requestId: 'test-request-id'
      }
    };
    
    const result = await handler(event);
    
    expect(result.statusCode).toBe(200);
    expect(result.headers['Content-Type']).toBe('application/json');
    
    const body = JSON.parse(result.body);
    expect(body.message).toBe('Hello from AWS Lambda!');
    expect(body.requestId).toBe('test-request-id');
  });
  
  test('should handle missing requestContext', async () => {
    const event = {};
    
    const result = await handler(event);
    
    expect(result.statusCode).toBe(200);
    
    const body = JSON.parse(result.body);
    expect(body.requestId).toBe('N/A');
  });
});