# DRF-task-Online-Book-Shop-
# EpicBooks API

This is a Django Rest Framework project that provides an API for `EpicBooks`.

## API Endpoints

The `EpicBooks` API provides the following endpoints:

- `GET /epicbooks/`: List all books.
- `GET /epicbooks/{id}/`: Retrieve a specific book by its ID.
- `POST /epicbooks/`: Create a new book.
- `PUT /epicbooks/{id}/`: Update a specific book by its ID.
- `PATCH /epicbooks/{id}/`: Partially update a specific book by its ID.
- `POST /epicbooks/{id}/add_to_favourite/`: Add a specific book to favourites.

## Usage

To use the `EpicBooks` API, send a HTTP request to one of the above endpoints. For `POST`, `PUT`, and `PATCH` requests, include the book data in the request body.

Please note that some endpoints may require authentication. Check the API documentation for more details.

## Testing

To run the tests for the `EpicBooks` API, use the following command:

```bash
python manage.py test
