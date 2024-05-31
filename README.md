# Social Network API

This is a Django Rest Framework based API for a social networking application. It includes functionalities for user authentication, searching users, and managing friend requests.

## Features

- User Signup and Login
- Search Users by Email and Name
- Send, Accept, and Reject Friend Requests
- List Friends
- List Pending Friend Requests
- Rate Limiting: Users can send a maximum of 3 friend requests within a minute

## Prerequisites

- Docker
- Docker Compose

## Installation Steps

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/ramesh89852/assignment.git
    cd social_network
    ```

2. **Setup Docker**:
    ```bash
    docker-compose up --build
    ```

3. **Run Migrations**:
    ```bash
    docker-compose run web python manage.py migrate
    ```

4. **Create Superuser**:
    ```bash
    docker-compose run web python manage.py createsuperuser
    ```

5. **Access the Application**:
    Open your browser and navigate to `http://localhost:8000`



### Additional Notes

- Ensure that the `postman_collection.json` and `postman_environment.json` files are included in your GitHub repository at the specified paths.
- Update the links in the "Postman Collection and Environment Variables" section to point to the actual files in your repository.
