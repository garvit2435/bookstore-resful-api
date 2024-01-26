# MyBookstoreAPI

## Description
MyBookstoreAPI is a RESTful API developed using FastAPI for managing a bookstore. It allows users to perform CRUD operations on book data, such as adding, retrieving, updating, and deleting book details.

## Database Schema Design

The database consists of a single table named `Books`, with the following schema:

### Books Table
- `id`: Integer, Primary Key
- `title`: String
- `author`: String
- `isbn`: String
- `price`: Float
- `quantity`: Integer

## Setup and Installation

To set up and run the API on your local machine, follow these steps:

1. **Clone the Repository**
```bash
git clone https://github.com/garvit2435/bookstore-resful-api.git
```
3. **Install Dependencies**
```bash
pip install -r requirements.txt
```
4. **Start the Application**
```bash
uvicorn main:app --reload
```

## API Endpoints

The API provides the following endpoints:

### Authentication
- **POST /token**
- **Description**: Authenticates users and returns a JWT token.
- **Payload**: `username`, `password`
- **Returns**: `access_token`, `token_type`

### Book Management
- **POST /books**
- **Description**: Adds a new book to the database.
- **Payload**: `title`, `author`, `isbn`, `price`, `quantity`
- **Returns**: Book data
- **GET /books**
- **Description**: Retrieves a list of all books.
- **Returns**: List of books
- **GET /books/{isbn}**
- **Description**: Retrieves a specific book by ISBN.
- **Returns**: Book data
- **PUT /books/{isbn}**
- **Description**: Updates the details of a specific book.
- **Payload**: `title`, `author`, `price`, `quantity`
- **Returns**: Updated book data
- **DELETE /books/{isbn}**
- **Description**: Deletes a specific book by ISBN.
- **Returns**: Success message

## Unit Testing

Unit tests are written to ensure the API's functionality. To run these tests:

1. **Navigate to the Project Directory**
```bash
cd MyBookstoreAPI
```

2. **Execute Tests**
```bash
pytest
```
