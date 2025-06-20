# SocialSphere AI - Deployment Guide

This guide provides step-by-step instructions for deploying SocialSphere AI to a production environment. We'll use the "Small Business Package" configuration, which offers a good balance of cost, performance, and ease of setup.

## Deployment Overview

1. Register a domain name
2. Set up hosting environment
3. Configure database service
4. Set up SSL and CDN
5. Deploy the application
6. Configure email service
7. Set up monitoring
8. Perform post-deployment verification

## Detailed Steps

### 1. Domain Registration (Google Domains)

1. Go to [Google Domains](https://domains.google.com)
2. Search for your desired domain name (e.g., socialsphereai.com)
3. Select and purchase the domain (typically $12-20/year)
4. Enable privacy protection (included free with Google Domains)
5. Keep the confirmation email and login details secure

### 2. Hosting Setup (DigitalOcean App Platform)

1. Create a [DigitalOcean account](https://www.digitalocean.com)
2. Set up billing information
3. Navigate to the App Platform section
4. Click "Create App"
5. Connect to your GitHub/GitLab repository containing the SocialSphere AI code
   - If your code isn't in a repository yet, create one and push your code
6. Select the repository and branch to deploy
7. Configure the app:
   - Select "Web Service" as the component type
   - Choose "Python" as the environment
   - Set the following:
     - Build Command: `pip install -r requirements.txt`
     - Run Command: `gunicorn --worker-tmp-dir /dev/shm src.main:app`
     - HTTP Port: `5000`
   - Select a plan (Basic: $12/mo or Professional: $24/mo recommended)
   - Enable auto-deploy (optional)
8. Add environment variables:
   ```
   SECRET_KEY=<generate-a-secure-random-string>
   FLASK_ENV=production
   DATABASE_URL=<your-database-connection-string>
   ```
9. Click "Next" and review your settings
10. Click "Create Resources"

### 3. Database Setup (DigitalOcean Managed MySQL)

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

### 4. SSL and CDN Setup (Cloudflare)

1. Create a [Cloudflare account](https://www.cloudflare.com)
2. Add your domain:
   - Click "Add a Site"
   - Enter your domain name
   - Select the Free plan to start
3. Update nameservers:
   - Cloudflare will provide you with nameservers
   - Go to Google Domains
   - Navigate to DNS settings
   - Replace Google nameservers with Cloudflare nameservers
   - Wait for DNS propagation (can take up to 24 hours)
4. Configure Cloudflare settings:
   - SSL/TLS: Set to "Full" mode
   - Enable "Always Use HTTPS"
   - Enable Auto Minify for HTML, CSS, and JavaScript
5. Add DNS records:
   - Type: CNAME
   - Name: @ (or www)
   - Target: Your DigitalOcean App URL
   - Proxy status: Proxied

### 5. Application Deployment

1. Prepare your application for production:
   - Update your `main.py` to use the production database:
     ```python
     app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
     ```
   - Ensure debug mode is disabled in production:
     ```python
     if __name__ == '__main__':
         debug = os.environ.get('FLASK_ENV') != 'production'
         app.run(host='0.0.0.0', port=5000, debug=debug)
     ```
   - Add a `Procfile` to your repository:
     ```
     web: gunicorn --worker-tmp-dir /dev/shm src.main:app
     ```
   - Add `gunicorn` to your `requirements.txt`

2. Update database configuration:
   - Create a migration script to initialize the production database
   - Ensure your models are properly defined

3. Push changes to your repository:
   ```bash
   git add .
   git commit -m "Prepare for production deployment"
   git push
   ```

4. Deploy your application:
   - If auto-deploy is enabled, the app will deploy automatically
   - Otherwise, manually deploy from the DigitalOcean App Platform dashboard

5. Run database migrations:
   - Use the DigitalOcean Console feature to access your app's console
   - Run your database initialization script

### 6. Email Service Setup (Mailgun)

1. Create a [Mailgun account](https://www.mailgun.com)
2. Verify your domain:
   - Add the domain you registered
   - Follow Mailgun's instructions to add DNS records to Cloudflare
3. Get your API key from the Mailgun dashboard
4. Add to your App Platform environment variables:
   ```
   MAILGUN_API_KEY=<your-api-key>
   MAILGUN_DOMAIN=<your-domain>
   ```
5. Update your application code to use Mailgun for sending emails

### 7. Monitoring Setup (Sentry)

1. Create a [Sentry account](https://sentry.io)
2. Create a new project for Python
3. Get your DSN (Data Source Name)
4. Add to your App Platform environment variables:
   ```
   SENTRY_DSN=<your-sentry-dsn>
   ```
5. Update your application code to initialize Sentry:
   ```python
   import sentry_sdk
   from sentry_sdk.integrations.flask import FlaskIntegration

   sentry_sdk.init(
       dsn=os.environ.get('SENTRY_DSN'),
       integrations=[FlaskIntegration()],
       traces_sample_rate=1.0
   )
   ```
6. Add `sentry-sdk[flask]` to your `requirements.txt`

### 8. Post-Deployment Verification

1. Test your application:
   - Visit your domain (https://yourdomain.com)
   - Test user registration and login
   - Test admin functionality
   - Test all critical features

2. Check monitoring:
   - Verify Sentry is receiving data
   - Check application logs in DigitalOcean

3. Set up regular backups:
   - Enable automated backups for your database in DigitalOcean

4. Security checks:
   - Verify SSL is working correctly
   - Test that sensitive routes require authentication
   - Ensure admin routes are properly protected

## Maintenance and Operations

### Regular Maintenance Tasks

1. **Database Backups**: Verify automated backups are running weekly
2. **Security Updates**: Update dependencies monthly
3. **Performance Monitoring**: Review Sentry metrics bi-weekly
4. **SSL Certificate**: Ensure auto-renewal is working (check 30 days before expiration)

### Scaling Considerations

As your user base grows, consider:

1. Upgrading your DigitalOcean App Platform plan
2. Scaling up your database resources
3. Implementing a caching layer (Redis)
4. Moving static assets to a dedicated object storage

### Troubleshooting Common Issues

1. **Application Errors**:
   - Check Sentry for detailed error reports
   - Review application logs in DigitalOcean

2. **Database Connection Issues**:
   - Verify connection string is correct
   - Check database firewall settings
   - Ensure database service is running

3. **Slow Performance**:
   - Check database query performance
   - Review application resource usage
   - Consider adding caching

4. **Email Delivery Problems**:
   - Verify Mailgun API key and domain
   - Check Mailgun logs for delivery issues

## Cost Management

Monitor your monthly costs:

1. DigitalOcean App Platform: $12-24/month
2. DigitalOcean Managed MySQL: $15-30/month
3. Google Domains: ~$12-20/year
4. Cloudflare: Free tier to start
5. Mailgun: ~$35/month for 50,000 emails
6. Sentry: Free tier to start

Total estimated monthly cost: $60-100/month

## Next Steps and Optimizations

After successful deployment, consider:

1. Setting up a staging environment for testing
2. Implementing CI/CD pipelines for automated testing
3. Creating a disaster recovery plan
4. Optimizing database queries and adding indexes
5. Implementing a content delivery strategy for media files
