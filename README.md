
---

### Snap Logistics Project Documentation

### Overview

The Logistics Application is a Django-based web platform designed to efficiently manage and streamline the delivery process for logistics operations. This application is inspired by services like Snap Food and is tailored to handle all aspects of delivery management, from creation to tracking, using real-time data for optimal route and pricing calculations.

#### Core Functionality

1. **Delivery Management**:
   - **Create Deliveries**: Users can initiate new delivery requests by specifying origin and destination locations. Each delivery is assigned a unique code, facilitating easy tracking and management.
   - **Update Deliveries**: The application allows for updating delivery statuses, including marking deliveries as completed or canceled. This feature ensures that users can manage and monitor their delivery tasks effectively.
   - **View Deliveries**: Users can view a comprehensive list of all deliveries, including detailed information such as delivery code, status, and pricing. This helps in overseeing ongoing and historical deliveries.

2. **Integration with Neshan API**:
   - **Route Calculation**: The application integrates with the Neshan API to calculate the distance and estimated time of arrival (ETA) for each delivery. This integration provides users with accurate and up-to-date information on expected delivery times.
   - **Dynamic Pricing**: Delivery pricing is calculated dynamically based on the distance and ETA. This model ensures that pricing is fair and transparent, adjusting in real-time according to the delivery parameters.

3. **User Authentication and Authorization**:
   - **Authentication**: Access to the application is controlled through user authentication, utilizing Django’s authentication framework. Users must log in to access the platform's features.
   - **Permissions**: Custom permissions are implemented to control access to various functionalities based on user roles. This includes permissions for superusers and couriers, ensuring that users only have access to the features relevant to their role.

4. **API Endpoints**:
   - **Create Delivery**: An API endpoint for creating new deliveries by providing details such as origin and destination coordinates.
   - **Retrieve Delivery Status**: Allows users to check the status of a specific delivery using its unique code.
   - **List Deliveries**: Provides a list of all deliveries with options to filter by status and pricing.
   - **Cancel Delivery**: Enables users to cancel a delivery by its code, updating its status accordingly.

#### Technical Details

- **Framework**: Developed using Django, a robust web framework for building scalable web applications.
- **API Integration**: Leverages the Neshan API for accurate route and ETA calculations.
- **Database**: Uses PostgreSQL for reliable and scalable data storage.
- **Authentication**: Implements Django’s authentication system with JWT-based token management for secure user access.
- **Permissions**: Incorporates custom permissions to manage user access based on roles.

The Logistics Application aims to enhance the efficiency and effectiveness of logistics operations by providing a comprehensive platform for managing deliveries, optimizing routes, and tracking delivery statuses in real-time. It combines modern web technologies with real-time data to ensure a seamless and accurate logistics management experience.



### Introduction

The Logistics Module is a Django-based component designed to manage and optimize delivery processes within a larger system. It handles creating, updating, and tracking deliveries, and integrates with the Neshan API to provide accurate route calculations and estimated delivery times. This module is part of a broader application, offering essential backend functionalities for efficient delivery management.


#### Prerequisites
- Python 3.x
- Django 5.x
- PostgreSQL
- psycopg2

#### Installation and Setup

**Manual Installation**
1. Clone the repository:
    ```
    git clone https://github.com/username/project-name.git
    ```
2. Navigate to the project directory:
    ```
    cd project-name
    ```
3. Create a virtual environment and install dependencies:
    ```
    python -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    ```
4. Configure the database and run migrations:
    ```
    python manage.py migrate
    ```
5. Start the development server:
    ```
    python manage.py runserver
    ```

---

### Usage

1. **Access the Admin Panel**:
   - Navigate to `http://localhost:8000/admin` to manage deliveries, users, and other data.

2. **Create a Superuser**:
   ```
   python manage.py createsuperuser
   ```

3. **Interact with the Application**:
   - **Create a Delivery**: Send a `POST` request to `/api/deliveries/` with the delivery details.
   - **View Deliveries**: Send a `GET` request to `/api/deliveries/` to list all deliveries.
   - **Retrieve Delivery Status**: Send a `GET` request to `/api/deliveries/{code}/` to get the status of a specific delivery by its unique code.

---

### Project Structure

**`delivery_app/`**: Main application directory containing core functionality.
  - **`models.py`**: Defines the core models:
    - **`Courier`**: Represents delivery personnel with details such as name, status, and wallet.
    - **`Location`**: Stores latitude and longitude for delivery points.
    - **`Delivery`**: Manages deliveries, including details such as origin, destination, status, price, and assigned courier.
    - **`Wallet`**: Manages financial information for couriers.
    - **`Transaction`**: Records financial transactions related to wallets.
  - **`views/`**: Handles all delivery-related requests and business logic.
  - **`serializers/`**: Serializers for the `Delivery` model and other related data.
  - **`permissions/`**: Custom permissions for handling user access.
  - **`urls.py`**: URL routing for the application.
  - **`static/`**: Static files (CSS, JS, images).
  - **`templates/`**: HTML templates for rendering.
  - **`migrations/`**: Database migration files.
  - **`requirements.txt`**: Python dependencies required for the project.

---


### Models

**`Courier`**  
Represents the delivery personnel with the following attributes:
- `user`: One-to-one link to the Django User model.
- `name`: Name of the courier (max length: 50 characters).
- `wallet`: One-to-one link to the Wallet model.
- `courier_status`: Status of the courier (integer).
- `plate`: Vehicle plate number (max length: 8 characters).
- `courier_phone_number`: Contact number of the courier (max length: 11 characters).

**`Location`**  
Stores the geographical coordinates of delivery points:
- `lat`: Latitude (float).
- `long`: Longitude (float).

**`Delivery`**  
Manages delivery details and assignments:
- `code`: Unique identifier for the delivery (max length: 16 characters).
- `origin`: Foreign key linking to the `Location` model (starting point).
- `destination`: Foreign key linking to the `Location` model (end point).
- `courier`: Foreign key linking to the `Courier` model (optional).
- `delivery_status`: Status of the delivery (integer).
- `max_delivery_time`: Maximum expected delivery time (string, max length: 120 characters).
- `delivery_price`: Price of the delivery (float).

**`Wallet`**  
Handles financial transactions:
- `current_money`: Amount of money in the wallet (integer, optional).

**`Transaction`**  
Records financial transactions related to wallets:
- `wallet`: Foreign key linking to the `Wallet` model.
- `amount`: Amount of the transaction (float, optional).

---

### Serializers

**`DeliverySerializer`**  
Serializes the `Delivery` model for creating and retrieving delivery data. Includes all fields of the `Delivery` model.

**`DeliveryStatusSerializer`**  
Serializes the delivery status information. Includes:
- `code`: Unique identifier of the delivery.
- `delivery_status`: Current status of the delivery.

**`CreateDeliverySerializer`**  
Validates and serializes data for creating a new delivery. Requires:
- `origin_lat`: Latitude of the origin (float).
- `origin_long`: Longitude of the origin (float).
- `destination_lat`: Latitude of the destination (float).
- `destination_long`: Longitude of the destination (float).

---
### Authentication and Permissions

The application uses Django's authentication framework to secure API endpoints, along with custom permissions to control access to specific functionalities.

- **Authentication**:
  - The application employs JSON Web Token (JWT) authentication for API access. Users, including couriers, must log in to receive a token.
  - Couriers can log in and refresh their tokens using the `CourierLoginView` and `CourierRefreshView`.

- **Permissions**:
  - **CourierPermission**: This custom permission ensures that only users who are associated with a `Courier` model instance can access specific views.
    - If a user has an associated `Courier` object, they are granted permission to interact with views that require courier-specific access.
  - **SuperUserPermission**: This permission restricts access to superusers for specific administrative actions.
    - Only authenticated users who are marked as superusers are allowed to access views protected by this permission.

#### Example Usage:
- `CourierPermission`: Applied to API views that handle courier-specific tasks, such as assigning or viewing deliveries.
- `SuperUserPermission`: Applied to API views for administrative purposes, such as managing delivery listings or creating new deliveries.

These custom permissions help ensure that users only have access to the features they are authorized to use, providing a secure and controlled environment for managing deliveries and courier assignments.

---

### API Endpoints

This application provides several key API endpoints for managing deliveries:

1. **Create Delivery**  
   - **Endpoint**: `/api/deliveries/`  
   - **Method**: `POST`  
   - **Description**: Create a new delivery with origin and destination coordinates.  
   - **Request**:  

     ```json
     {
       "origin_lat": "float",
       "origin_long": "float",
       "destination_lat": "float",
       "destination_long": "float"
     }
     ```  

   - **Response**: `{"message": "Delivery created successfully"}`

2. **Retrieve Delivery Status**  
   - **Endpoint**: `/api/deliveries/{code}/`  
   - **Method**: `GET`  
   - **Description**: Get details and status of a delivery using its code.

3. **List Deliveries**  
   - **Endpoint**: `/api/deliveries/`  
   - **Method**: `GET`  
   - **Description**: Retrieve all deliveries with optional filtering.

4. **Cancel Delivery**  
   - **Endpoint**: `/api/deliveries/cancel/{code}/`  
   - **Method**: `POST`  
   - **Description**: Cancel a delivery by its unique code.



---
### Views and Logic

This section provides details on the views and the associated logic for handling various API requests:

1. **CourierLoginView** and **CourierRefreshView**
   - **Purpose**: Handle JWT authentication for couriers. `CourierLoginView` is for obtaining tokens, and `CourierRefreshView` is for refreshing them.

2. **DeliveryList**
   - **Purpose**: Lists all deliveries. Restricted to superusers.
   - **Details**: Uses Django's `ListAPIView` to fetch and serialize all delivery records.

3. **welcome_page**
   - **Purpose**: Renders a welcome page.
   - **Details**: Simple view to display a static HTML page.

4. **add_delivery**
   - **Purpose**: Handles the creation of a new delivery. 
   - **Details**: Uses POST requests to create a delivery, calculate the price and duration using the Neshan API, and save the delivery in the database.

5. **RetrieveDeliverystatus**
   - **Purpose**: Retrieves the status of a specific delivery by its code.
   - **Details**: Uses Django's `RetrieveAPIView` to get and serialize the delivery status.

6. **cancle_delivery**
   - **Purpose**: Cancels a delivery by its code.
   - **Details**: Uses POST requests to change the delivery status to canceled.

7. **ChooseDelivery** and **ShowAvailableDelivery**
   - **Purpose**: List deliveries based on specific criteria. `ChooseDelivery` lists all deliveries, while `ShowAvailableDelivery` lists only those that are available.
   - **Details**: Both use `ListAPIView` to filter and serialize delivery records based on permissions.

8. **api_to_neshan**
   - **Purpose**: Helper function to interact with the Neshan API for route details.
   - **Details**: Fetches and parses route data from the Neshan API.

9. **CreateDelivery**
   - **Purpose**: Creates a new delivery using validated input data.
   - **Details**: Uses Django REST Framework's `APIView` to handle POST requests, validate data, and create a delivery record with calculated price and duration.


---
#### Authors

- Parsa Mohebian - parsa1382mohebian@gmail.com
- Soroush Salamati - soroushsalamati94@gmail.com
- Fatemeh Khanmohammadi - fatemeh@------.com
- hamidreza sayadi - hamidreza.mugen@gmail.com

#### License
This project does not have a specific license. Feel free to use and modify the code as needed. If you choose to use or distribute it, consider adding an appropriate open-source license.

#### References
- Django Documentation: [Django Documentation](https://docs.djangoproject.com/)

---