# DigitalOcean Deployment Guide for SocialSphere AI

This guide provides step-by-step instructions for deploying your social media SaaS application on DigitalOcean's App Platform.

## Prerequisites
- DigitalOcean account (already created)
- Your application code in a Git repository (GitHub, GitLab) or ready to upload
- Database connection details (if using an external database)
- Domain name (if you plan to use a custom domain)

## Step 1: Prepare Your Application

Before deploying to DigitalOcean, ensure your application is properly configured:

1. Verify your `requirements.txt` file includes all necessary dependencies
2. Ensure your application uses environment variables for configuration
3. Make sure your application listens on `$PORT` (App Platform sets this automatically)
4. Add a `Procfile` to your project root with the following content:
   ```
   web: gunicorn --worker-tmp-dir /dev/shm src.main:app
   ```
5. Ensure your database connection uses environment variables

## Step 2: Create a New App on DigitalOcean App Platform

1. Log in to your DigitalOcean account
2. Navigate to the App Platform section from the left sidebar
3. Click "Create App" button
4. Choose your source:
   - Connect to GitHub/GitLab repository (recommended)
   - Upload source code directly

## Step 3: Configure Your App

1. Select the repository and branch to deploy (if using GitHub/GitLab)
2. Configure the app settings:
   - Select "Web Service" as the component type
   - Choose "Python" as the environment
   - Set the following:
     - Build Command: `pip install -r requirements.txt`
     - Run Command: `gunicorn --worker-tmp-dir /dev/shm src.main:app`
     - HTTP Port: `5000`
   - Select a plan (Basic: $12/mo or Professional: $24/mo recommended)
   - Enable auto-deploy (optional)

## Step 4: Configure Environment Variables

Add the following environment variables:
```
SECRET_KEY=<generate-a-secure-random-string>
FLASK_ENV=production
DATABASE_URL=<your-database-connection-string>
```

## Step 5: Set Up Database

1. In your DigitalOcean dashboard, go to "Databases"
2. Click "Create Database Cluster"
3. Select MySQL as the database engine
4. Choose a plan (Starter: $15/mo recommended for beginning)
5. Select the same region as your App Platform deployment
6. Name your cluster (e.g., "socialsphere-db")
7. Click "Create Database Cluster"
8. Once created, create a new database:
   - Click on your cluster
   - Go to "Users & Databases"
   - Create a database named "socialsphere"
   - Create a user with a strong password
9. Get your connection details:
   - Go to the "Connection Details" tab
   - Copy the connection string
10. Update your App Platform environment variables:
    - Go back to your App Platform app
    - Add/update the `DATABASE_URL` environment variable with the connection string
    - Format: `mysql+pymysql://username:password@host:port/socialsphere`

## Step 6: Configure Domain and SSL

1. In your App Platform app settings, go to the "Domains" tab
2. You have two options:
   - Use the default DigitalOcean subdomain (e.g., yourapp.ondigitalocean.app)
   - Add a custom domain:
     - Click "Add Domain"
     - Enter your domain name
     - Follow the DNS configuration instructions provided by DigitalOcean
3. SSL is automatically configured by DigitalOcean for both default and custom domains

## Step 7: Deploy Your Application

1. Review all settings
2. Click "Create Resources" or "Deploy to Production"
3. Wait for the build and deployment process to complete (5-10 minutes)

## Step 8: Initialize Your Database

After deployment, you'll need to initialize your database:

1. Go to your App Platform app console
2. Click on the "Console" tab
3. Run your database initialization script:
   ```
   python -m src.migrations.initialize_production_db
   ```

## Step 9: Verify Deployment

1. Once deployment is complete, click the app URL to open your application
2. Test the following:
   - User registration and login
   - Admin functionality
   - Core features of your application

## Step 10: Post-Deployment Tasks

1. Set up monitoring (optional):
   - Enable App Platform metrics
   - Configure alerts for important events
2. Set up regular database backups:
   - Enable automated backups for your database in DigitalOcean
3. Configure logging:
   - Check application logs in the "Logs" tab of your App Platform app

## Troubleshooting Common Issues

1. **Build Failures**:
   - Check build logs for specific errors
   - Verify all dependencies are in requirements.txt
   - Ensure your code is compatible with the Python version on App Platform

2. **Runtime Errors**:
   - Check application logs
   - Verify environment variables are correctly set
   - Test database connection

3. **Database Connection Issues**:
   - Verify connection string format
   - Check database firewall settings
   - Ensure database service is running

4. **Domain/SSL Issues**:
   - Verify DNS configuration
   - Allow time for DNS propagation (up to 48 hours)
   - Check SSL certificate status in app settings
