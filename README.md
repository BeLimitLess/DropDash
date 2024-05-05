# DropDash: Secure File Sharing Application

DropDash is a secure, user-friendly, and scalable file-sharing web application that allows users to upload, share, and manage files of any size with ease. Built with Flask, DropDash leverages Azure Blob Storage, Azure Table Storage, and Azure Content Delivery Network (CDN) to provide a robust and efficient file-sharing experience.

## Features

- **Secure File Sharing**: Implement robust security measures, including optional password protection and time-limited access, ensuring the confidentiality and integrity of shared files.
- **User-Friendly Interface**: Intuitive and responsive web interface that simplifies the file-sharing process, making it accessible to users of all technical backgrounds.
- **Scalability and Performance**: Leverage Azure Blob Storage for scalable and high-performance file storage, Azure Table Storage for efficient metadata management, and Azure CDN for enhanced content delivery and availability.
- **Expiration Logic**: Time-based expiration for shared links, enhancing data privacy and security by restricting access after a set duration.
- **Automated Cleanup**: Employ Azure Functions for automated cleanup of expired files, optimizing system efficiency.
- **Universal File Compatibility**: Support for sharing any file type, accommodating diverse user needs.

## Getting Started

These instructions will help you set up the project locally for development and testing purposes.

### Prerequisites

- Python (version 3.6 or later)
- Azure Subscription (for deploying and utilizing Azure services)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/belimitless/DropDash.git
```
2. Navigate to the project directory:
```bash

cd DropDash
```
3. Install dependencies:
```bash

pip install -r requirements.txt
```
4. Rename the `.env-sample` file to `.env` and add your Azure service settings:


5. Run the Flask application:
```bash

flask run
```
The application should now be running locally, and you can access it at `http://localhost:5000`.

## Deployment

To deploy the DropDash application to Azure, follow these steps:

1. Create an Azure App Service instance.
2. Configure deployment settings to connect to your Git repository.
3. Set up necessary environment variables for Azure services (Blob Storage, Table Storage, CDN).
4. Deploy the application code to the App Service instance.

### Vercel Deployment

You can also deploy the DropDash application to Vercel using the following command:
```bash

vercel --prod
```

## Contributing

Contributions to DropDash are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
