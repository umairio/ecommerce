
---

# Django E-commerce Platform

This project features a Django-based e-commerce platform with essential buyer-side functionalities, including product browsing, adding items to a cart, placing orders, and managing user profiles. It uses Docker Compose for a simplified setup and PostgreSQL for the database.

## Project Structure
- **User Authentication**: Includes user registration, login, and profile management.
- **Product Catalog**: Browse through a list of products with detailed information.
- **Profile Management**: Create, edit, and delete user profiles.
- **Order History**: View previous orders and track current ones.
- **Reviews**: Add and view product reviews.
- **Docker Compose**: Manages the Django application and database.
- **Testing**: Contains unit tests for core functionalities.

## Prerequisites
Ensure you have the following installed:
- Git
- Docker
- Docker Compose

## Setup and Installation
### Clone the Repository
```bash
git clone https://github.com/UmaiRIO/ecommerce.git
cd ecommerce
```

### Start the Application with Docker Compose
```bash
docker-compose up
```

This command will build the Django application, start the PostgreSQL database, and run the Django server.

### Migrate the Database

```bash
docker-compose run web python manage.py migrate
```

### Create a Superuser
To create a Django superuser for accessing the admin interface, run the following command after starting the application:

```bash
docker-compose run web python manage.py createsuperuser
```

This will prompt you to enter a username, email address, and password for the superuser. Once completed, you can log into the Django admin interface to manage users and other admin-related tasks.

### Stop the Application
```bash
docker-compose down
```

This command stops all containers and removes them.

## Troubleshooting
If you encounter issues, try the following:
- Ensure Docker and Docker Compose are installed and running.
- Check that you've provided the correct environment variables in `.env`.
- Use `docker-compose logs` to review logs from the running containers.

## Contributing
Contributions are welcome. Here's how you can contribute:
- Fork the repository and create a new branch for your feature or bug fix.
- Commit and push your changes.
- Open a pull request for review.

## Acknowledgements
Thank you to the Django and Docker communities for providing the tools and resources to create this project.

---
