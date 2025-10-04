# CORS Configuration Verification

## Configuration Summary

The FastAPI application has been configured with CORS middleware to allow requests from the frontend application.

### CORS Settings

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Requirements Coverage

✅ **Requirement 6.1**: Permitir solicitudes CORS desde http://localhost:3001
- Configured with `allow_origins=["http://localhost:3001"]`

✅ **Requirement 6.2**: Incluir headers CORS apropiados
- `allow_credentials=True` - Allows cookies and authentication headers
- `allow_methods=["*"]` - Allows all HTTP methods (GET, POST, PUT, DELETE, OPTIONS, etc.)
- `allow_headers=["*"]` - Allows all headers

✅ **Requirement 6.3**: Responder correctamente a solicitudes OPTIONS (preflight)
- FastAPI's CORSMiddleware automatically handles OPTIONS preflight requests

## Testing CORS

### Manual Testing with curl

1. **Test OPTIONS preflight request:**
```bash
curl -X OPTIONS http://localhost:8081/api/health \
  -H "Origin: http://localhost:3001" \
  -H "Access-Control-Request-Method: GET" \
  -H "Access-Control-Request-Headers: content-type" \
  -v
```

Expected response headers:
- `Access-Control-Allow-Origin: http://localhost:3001`
- `Access-Control-Allow-Methods: DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT`
- `Access-Control-Allow-Headers: content-type`
- `Access-Control-Allow-Credentials: true`

2. **Test GET request with Origin header:**
```bash
curl http://localhost:8081/api/health \
  -H "Origin: http://localhost:3001" \
  -v
```

Expected response headers:
- `Access-Control-Allow-Origin: http://localhost:3001`
- `Access-Control-Allow-Credentials: true`

3. **Test POST preflight:**
```bash
curl -X OPTIONS http://localhost:8081/api/participantes \
  -H "Origin: http://localhost:3001" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: content-type" \
  -v
```

### Automated Testing

Run the test script:
```bash
# Make sure the server is running first
uvicorn main:app --host 0.0.0.0 --port 8081

# In another terminal, run the test
python test_cors.py
```

### Browser Testing

1. Start the FastAPI server:
```bash
uvicorn main:app --host 0.0.0.0 --port 8081
```

2. Open browser console on http://localhost:3001 and run:
```javascript
fetch('http://localhost:8081/api/health', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json'
  },
  credentials: 'include'
})
.then(response => response.json())
.then(data => console.log('Success:', data))
.catch(error => console.error('Error:', error));
```

If CORS is configured correctly, you should see the response without any CORS errors.

## Common CORS Headers Explained

- **Access-Control-Allow-Origin**: Specifies which origins can access the resource
- **Access-Control-Allow-Methods**: Specifies which HTTP methods are allowed
- **Access-Control-Allow-Headers**: Specifies which headers can be used in requests
- **Access-Control-Allow-Credentials**: Indicates whether credentials (cookies, auth headers) can be included
- **Access-Control-Max-Age**: How long preflight results can be cached (set by FastAPI automatically)

## Troubleshooting

### CORS Error: "No 'Access-Control-Allow-Origin' header"
- Verify the server is running
- Check that the Origin header matches exactly: `http://localhost:3001`
- Ensure the middleware is added before route definitions

### CORS Error: "Preflight request failed"
- Check that OPTIONS method is not blocked
- Verify all required headers are allowed
- Check server logs for errors

### Credentials Not Working
- Ensure `allow_credentials=True` is set
- Frontend must use `credentials: 'include'` in fetch requests
- Origin must be explicitly listed (cannot use wildcard with credentials)
