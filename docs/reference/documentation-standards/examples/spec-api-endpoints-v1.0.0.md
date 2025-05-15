# API Endpoints Specification

## Overview

This specification defines the API endpoints for the system, including their request/response formats, authentication requirements, and error handling.

## Base URL

```
https://api.example.com/v1
```

## Authentication

All API endpoints require authentication using one of the following methods:

- API Key (via `X-API-Key` header)
- OAuth 2.0 Bearer Token (via `Authorization` header)
- JWT (via `Authorization` header)

See the [API Authentication Guide](./guide-api-authentication-v1.0.0.md) for details.

## Endpoints

### Users

#### GET /users

Retrieve a list of users.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| page | integer | No | Page number (default: 1) |
| limit | integer | No | Results per page (default: 20, max: 100) |
| sort | string | No | Field to sort by (default: "created_at") |
| order | string | No | Sort order ("asc" or "desc", default: "desc") |
| status | string | No | Filter by status ("active", "inactive", "pending") |

**Response:**

```json
{
  "data": [
    {
      "id": "user_123",
      "name": "John Doe",
      "email": "john@example.com",
      "status": "active",
      "created_at": "2025-01-15T08:30:00Z",
      "updated_at": "2025-01-15T08:30:00Z"
    },
    {
      "id": "user_456",
      "name": "Jane Smith",
      "email": "jane@example.com",
      "status": "active",
      "created_at": "2025-01-16T10:15:00Z",
      "updated_at": "2025-01-16T10:15:00Z"
    }
  ],
  "meta": {
    "total": 42,
    "page": 1,
    "limit": 20,
    "pages": 3
  }
}
```

#### GET /users/{id}

Retrieve a specific user by ID.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | User ID |

**Response:**

```json
{
  "data": {
    "id": "user_123",
    "name": "John Doe",
    "email": "john@example.com",
    "status": "active",
    "created_at": "2025-01-15T08:30:00Z",
    "updated_at": "2025-01-15T08:30:00Z"
  }
}
```

#### POST /users

Create a new user.

**Request Body:**

```json
{
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "password": "securePassword123",
  "role": "user"
}
```

**Response:**

```json
{
  "data": {
    "id": "user_789",
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "status": "active",
    "created_at": "2025-05-15T01:15:00Z",
    "updated_at": "2025-05-15T01:15:00Z"
  }
}
```

## Error Handling

All endpoints follow a consistent error response format:

```json
{
  "error": {
    "code": "invalid_request",
    "message": "The request was invalid",
    "details": [
      {
        "field": "email",
        "message": "Email is already in use"
      }
    ]
  }
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|------------|-------------|
| invalid_request | 400 | The request was malformed or contained invalid parameters |
| unauthorized | 401 | Authentication is required or failed |
| forbidden | 403 | The authenticated user lacks permission |
| not_found | 404 | The requested resource was not found |
| rate_limited | 429 | Too many requests in a given amount of time |
| server_error | 500 | An unexpected server error occurred |

## Rate Limiting

API requests are limited to 100 requests per minute per API key or user. Rate limit information is included in the response headers:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1714955760
```

## Versioning

The API uses URL versioning (e.g., `/v1/users`). When breaking changes are introduced, a new version will be released (e.g., `/v2/users`).

## Data Types

| Type | Format | Example |
|------|--------|--------|
| date | ISO 8601 date | "2025-05-15" |
| datetime | ISO 8601 datetime | "2025-05-15T01:15:00Z" |
| uuid | UUID v4 | "123e4567-e89b-12d3-a456-426614174000" |
| email | Valid email address | "user@example.com" |

## Implementation Notes

- All endpoints must validate input parameters
- Responses should be cached where appropriate
- Sensitive operations should be logged for audit purposes
- All endpoints must handle partial failures gracefully