# API Endpoints

## Authentication Endpoints
- `POST /api/auth/token/` - Obtain JWT token pair
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/register/` - User registration

## User Endpoints
- `GET /api/users/` - List all users
- `POST /api/users/` - Create a new user
- `GET /api/users/{id}/` - Retrieve a specific user
- `PUT /api/users/{id}/` - Update a specific user
- `DELETE /api/users/{id}/` - Delete a specific user
- `POST /api/users/login/` - Custom token obtain view
- `POST /api/users/token/refresh/` - Refresh token
- `POST /api/users/register/` - Register a new user
- `GET /api/users/me/` - Get current user information
- `PUT /api/users/me/` - Update current user information
- `POST /api/users/upload-profile-photo/` - Upload profile photo

### User Role-Specific Endpoints
- `GET /api/users/adaylar/` - List all candidates
- `POST /api/users/adaylar/` - Create a new candidate
- `GET /api/users/adaylar/{id}/` - Retrieve a specific candidate
- `PUT /api/users/adaylar/{id}/` - Update a specific candidate
- `DELETE /api/users/adaylar/{id}/` - Delete a specific candidate

- `GET /api/users/adminler/` - List all admins
- `POST /api/users/adminler/` - Create a new admin
- `GET /api/users/adminler/{id}/` - Retrieve a specific admin
- `PUT /api/users/adminler/{id}/` - Update a specific admin
- `DELETE /api/users/adminler/{id}/` - Delete a specific admin

- `GET /api/users/yoneticiler/` - List all managers
- `POST /api/users/yoneticiler/` - Create a new manager
- `GET /api/users/yoneticiler/{id}/` - Retrieve a specific manager
- `PUT /api/users/yoneticiler/{id}/` - Update a specific manager
- `DELETE /api/users/yoneticiler/{id}/` - Delete a specific manager

- `GET /api/users/juri-uyeleri/` - List all jury members
- `POST /api/users/juri-uyeleri/` - Create a new jury member
- `GET /api/users/juri-uyeleri/{id}/` - Retrieve a specific jury member
- `PUT /api/users/juri-uyeleri/{id}/` - Update a specific jury member
- `DELETE /api/users/juri-uyeleri/{id}/` - Delete a specific jury member

## Announcement Endpoints
- `GET /api/announcements/` - List all announcements
- `POST /api/announcements/` - Create a new announcement
- `GET /api/announcements/{id}/` - Retrieve a specific announcement
- `PUT /api/announcements/{id}/` - Update a specific announcement
- `DELETE /api/announcements/{id}/` - Delete a specific announcement

### Faculty Endpoints
- `GET /api/announcements/faculties/` - List all faculties
- `POST /api/announcements/faculties/` - Create a new faculty
- `GET /api/announcements/faculties/{id}/` - Retrieve a specific faculty
- `PUT /api/announcements/faculties/{id}/` - Update a specific faculty
- `DELETE /api/announcements/faculties/{id}/` - Delete a specific faculty

### Department Endpoints
- `GET /api/announcements/departments/` - List all departments
- `POST /api/announcements/departments/` - Create a new department
- `GET /api/announcements/departments/{id}/` - Retrieve a specific department
- `PUT /api/announcements/departments/{id}/` - Update a specific department
- `DELETE /api/announcements/departments/{id}/` - Delete a specific department

### Criteria Endpoints
- `GET /api/announcements/criteria/` - List all criteria
- `POST /api/announcements/criteria/` - Create a new criterion
- `GET /api/announcements/criteria/{id}/` - Retrieve a specific criterion
- `PUT /api/announcements/criteria/{id}/` - Update a specific criterion
- `DELETE /api/announcements/criteria/{id}/` - Delete a specific criterion

## Application Endpoints
- `GET /api/applications/applications/` - List all applications
- `POST /api/applications/applications/` - Create a new application
- `GET /api/applications/applications/{id}/` - Retrieve a specific application
- `PUT /api/applications/applications/{id}/` - Update a specific application
- `DELETE /api/applications/applications/{id}/` - Delete a specific application
- `GET /api/applications/my/` - Get current user's applications
- `GET /api/applications/basvurular/` - List all applications (alternative endpoint)
- `GET /api/applications/basvurular/{id}/` - Retrieve a specific application (alternative endpoint)
- `GET /api/applications/basvurular/aday/{id}/` - Get applications for a specific candidate
- `GET /api/applications/basvurular/my/` - Get current user's applications (alternative endpoint)

## Document Endpoints
- `GET /api/documents/documents/` - List all documents
- `POST /api/documents/documents/` - Create a new document
- `GET /api/documents/documents/{id}/` - Retrieve a specific document
- `PUT /api/documents/documents/{id}/` - Update a specific document
- `DELETE /api/documents/documents/{id}/` - Delete a specific document
- `GET /api/documents/documents/my/` - Get current user's documents
- `POST /api/documents/documents/upload/` - Upload a document
- `GET /api/documents/belgeler/` - List all documents (alternative endpoint)
- `POST /api/documents/belgeler/` - Create a new document (alternative endpoint)
- `GET /api/documents/belgeler/{id}/` - Retrieve a specific document (alternative endpoint)
- `PUT /api/documents/belgeler/{id}/` - Update a specific document (alternative endpoint)
- `DELETE /api/documents/belgeler/{id}/` - Delete a specific document (alternative endpoint)
- `GET /api/documents/belgeler/my/` - Get current user's documents (alternative endpoint)
- `POST /api/documents/belgeler/upload/` - Upload a document (alternative endpoint)
- `GET /api/documents/my/` - Get current user's documents (alternative endpoint)

## Table 5 Endpoints
- `GET /api/applications/table5/` - List all Table 5 entries
- `POST /api/applications/table5/` - Create a new Table 5 entry
- `GET /api/applications/table5/{id}/` - Retrieve a specific Table 5 entry
- `PUT /api/applications/table5/{id}/` - Update a specific Table 5 entry
- `DELETE /api/applications/table5/{id}/` - Delete a specific Table 5 entry

## Score Endpoints
- `GET /api/applications/scores/` - List all scores
- `POST /api/applications/scores/` - Create a new score
- `GET /api/applications/scores/{id}/` - Retrieve a specific score
- `PUT /api/applications/scores/{id}/` - Update a specific score
- `DELETE /api/applications/scores/{id}/` - Delete a specific score

## API Documentation
- `GET /swagger/` - Swagger UI documentation
- `GET /swagger.json/` - Swagger JSON schema
- `GET /redoc/` - ReDoc documentation

## Django Admin
- `GET /admin/` - Django admin interface