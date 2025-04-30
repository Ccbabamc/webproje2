# API Endpoint Fixes

## Summary of Changes

Based on the API endpoints list, the following fixes were made to ensure frontend API calls match the correct backend endpoints:

### Authentication Endpoints
- Fixed login endpoint from `/auth/login` to `/api/auth/login/`
- Fixed logout endpoint from `/auth/logout` to `/api/auth/logout/`
- Fixed token refresh endpoint from `/auth/token/refresh` to `/api/auth/token/refresh/`
- Changed Authorization header from `Bearer` to `Token` format to match Django's token authentication

### User Endpoints
- Fixed user endpoints from `/users` to `/api/users/`
- Fixed current user endpoint from `/users/me` to `/api/users/me/`
- Fixed user by ID endpoint from `/users/{id}` to `/api/users/{id}/`
- Fixed profile photo upload endpoint from `/api/profile/photo/` to `/api/users/upload-profile-photo/`

### Application Endpoints
- Fixed application endpoints from `/api/applications/{id}/` to `/api/applications/applications/{id}/`
- Fixed application submission endpoint from `/api/applications/{id}/submit/` to `/api/applications/applications/{id}/submit/`
- Fixed application status update endpoint from `/api/applications/{id}/status/` to `/api/applications/applications/{id}/status/`
- Fixed application evaluation endpoint from `/api/applications/{id}/evaluate/` to `/api/applications/applications/{id}/evaluate/`

### Document Endpoints
- Fixed document upload endpoint from `/api/applications/{id}/documents/` to `/api/documents/documents/upload/`

### Profile Endpoints
- Fixed profile endpoints from `/api/profile/` to `/api/users/me/`

## General Fixes
- Ensured all API URLs end with a trailing slash (`/`) to match Django's URL pattern
- Ensured all API URLs start with `/api/` prefix
- Updated token format in Authorization header from `Bearer {token}` to `Token {token}` to match Django's token authentication

These changes ensure that frontend API calls correctly match the backend endpoints defined in the API documentation.