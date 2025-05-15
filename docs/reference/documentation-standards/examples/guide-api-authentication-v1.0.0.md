# API Authentication Guide

## Overview

This guide explains how to authenticate with the API using various authentication methods. It covers API keys, OAuth 2.0, and JWT authentication.

## Authentication Methods

### API Keys

API keys provide a simple way to authenticate API requests.

#### How to Obtain an API Key

1. Log in to the developer portal
2. Navigate to "API Keys" section
3. Click "Generate New Key"
4. Copy the generated key

#### How to Use an API Key

```http
GET /api/v1/resources HTTP/1.1
Host: api.example.com
X-API-Key: your_api_key_here
```

### OAuth 2.0

OAuth 2.0 is recommended for applications acting on behalf of users.

#### Authorization Flow

1. Redirect the user to the authorization endpoint
2. User grants permission
3. Authorization server redirects back with an authorization code
4. Exchange the code for an access token
5. Use the access token to make API requests

#### Example Request with OAuth Token

```http
GET /api/v1/resources HTTP/1.1
Host: api.example.com
Authorization: Bearer your_oauth_token_here
```

### JWT Authentication

JWT (JSON Web Tokens) provide a stateless authentication mechanism.

#### JWT Structure

A JWT consists of three parts:
- Header: Contains the token type and signing algorithm
- Payload: Contains the claims (user information and metadata)
- Signature: Verifies the token hasn't been tampered with

#### Example Request with JWT

```http
GET /api/v1/resources HTTP/1.1
Host: api.example.com
Authorization: Bearer your_jwt_token_here
```

## Best Practices

1. **Never expose authentication credentials** in client-side code
2. **Use HTTPS** for all API requests
3. **Implement token expiration** and refresh mechanisms
4. **Apply the principle of least privilege** when assigning permissions
5. **Rotate API keys** periodically

## Troubleshooting

### Common Error Codes

- `401 Unauthorized`: Invalid or missing credentials
- `403 Forbidden`: Valid credentials but insufficient permissions
- `429 Too Many Requests`: Rate limit exceeded

### Debugging Tips

1. Verify the token hasn't expired
2. Check that the API key or token is being sent in the correct header
3. Ensure the token has the necessary scopes or permissions
4. Check for any IP restrictions on your API key

## Additional Resources

- [OAuth 2.0 Specification](https://oauth.net/2/)
- [JWT Introduction](https://jwt.io/introduction)
- [API Security Best Practices](https://example.com/api-security)