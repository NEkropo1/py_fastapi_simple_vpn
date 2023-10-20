Simple VPN(algorithm is via proxies)

# Installation  
### Docker

To run the application in a Docker container, follow these steps:

Install Docker by following the instructions for your operating system:  
        [Docker for Windows](https://docs.docker.com/desktop/install/windows-install/)  
        [Docker for Mac](https://docs.docker.com/desktop/install/mac-install/)  
        [Docker for Linux](https://docs.docker.com/desktop/install/linux-install/)  

After installing and initializing docker,  
### Clone the repository:

```bash
git clone https://github.com/NEkropo1/py_fastapi_simple_vpn
```
### Service
Copy `.env_sample` file to `.env` and refactor values to your needs.  
Pass your proxies to proxies/proxies.py instead of fillers.  

### Build and run the Docker images:

```bash
docker-compose up --build
```
Reminder: After the first build, you can run it with command:
`
docker-compose up
` without flag '--build'

# Usage  
### Running the Application

Once the Docker container is running, you can access the FastAPI application  
at http://0.0.0.0:8000.


### Endpoints

Here are the available endpoints:
Also available via swagger at http://localhost:8000/docs#

    /register/ (POST) - Register a new user.
    /login/ (POST) - Log in as a user.
    /edit_data/ (PUT) - Edit user data.
    /statistics/ (GET) - Get user statistics.
    /create_site (POST) - Create a new site.
    /site_content/ (GET) - Get site content.

# Mirrored Linking and Link Refactoring

The VPN application utilizes a mirrored linking approach that enables the dynamic  
creation of routes for new sites, subdomains, etc. When a user accesses a mirrored link,  
the application internally maps it to the corresponding remote site.

For instance, when a user accesses `google.com` through the VPN, the application  
automatically converts the URL to `localhost/google.com`, enabling seamless access to the  
remote content through the VPN.

Link refactoring is a critical part of the application's functionality. When the application  
fetches content from a site, it dynamically modifies the HTML content to ensure that all the  
links within the site are properly refactored to mirror the correct routes within the VPN. This  
refactoring process ensures that the site's functionality remains intact within the VPN environment.

By implementing mirrored linking and link refactoring, the VPN application provides a seamless and secure  
browsing experience for users, enabling access to a wide range of online content  
with enhanced privacy and security features.


To run the tests, follow these steps:

- Open a terminal or command prompt.

- Execute the following command to find the container name:

```bash
docker ps
```
- Access the Docker container shell:

```bash

docker exec -it <container_name> bash
```
- Run the tests using pytest:

```bash
pytest
```
