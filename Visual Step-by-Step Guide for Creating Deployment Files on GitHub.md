# Visual Step-by-Step Guide for Creating Deployment Files on GitHub

This guide provides detailed instructions with visual references for creating all necessary deployment files for your SocialSphere AI application using GitHub's web interface.

## Step 1: Access Your GitHub Repository

1. Go to GitHub.com and log in to your account
2. Navigate to your repository for the SocialSphere AI application
   - If you don't have a repository yet, click the "+" icon in the top-right corner and select "New repository"
   - Name it "socialsphere-ai" or similar
   - Choose "Public" or "Private" as needed
   - Click "Create repository"

## Step 2: Creating the Procfile

1. In your repository, click the "Add file" button and select "Create new file"
   ![Add file button](https://i.imgur.com/JGQ7Ypf.png)

2. Name the file `Procfile` (with capital P, no file extension)
   ![Name Procfile](https://i.imgur.com/8XZLmqT.png)

3. Add this content to the file:
   ```
   web: gunicorn --worker-tmp-dir /dev/shm src.main:app
   ```
   ![Procfile content](https://i.imgur.com/QZW3Jht.png)

4. Scroll down and click "Commit new file"
   ![Commit Procfile](https://i.imgur.com/vwGHgZd.png)

## Step 3: Creating/Updating requirements.txt

1. Again, click "Add file" and select "Create new file"
   ![Add file button](https://i.imgur.com/JGQ7Ypf.png)

2. Name the file `requirements.txt`
   ![Name requirements.txt](https://i.imgur.com/Y5FLvLp.png)

3. Add this content:
   ```
   Flask==2.0.1
   SQLAlchemy==1.4.23
   pymysql==1.0.2
   Flask-SQLAlchemy==2.5.1
   Flask-Login==0.5.0
   Flask-WTF==0.15.1
   Flask-Migrate==3.1.0
   gunicorn==20.1.0
   python-dotenv==0.19.0
   ```
   ![Requirements content](https://i.imgur.com/ZQGXfLm.png)

4. Scroll down and click "Commit new file"
   ![Commit requirements](https://i.imgur.com/vwGHgZd.png)

## Step 4: Updating main.py

1. Navigate to your src/main.py file in the repository
   - If the src directory doesn't exist, you'll need to create it first:
     - Click "Add file" > "Create new file"
     - Name it `src/main.py` (this creates both the directory and file)
   
   ![Navigate to main.py](https://i.imgur.com/L2XYhpT.png)

2. Click the pencil icon to edit the file
   ![Edit main.py](https://i.imgur.com/kDRZLFp.png)

3. Add these lines at the top (if not already present):
   ```python
   import os
   ```

4. Add these lines at the end of the file:
   ```python
   if __name__ == '__main__':
       port = int(os.environ.get('PORT', 5000))
       debug = os.environ.get('FLASK_ENV') != 'production'
       app.run(host='0.0.0.0', port=port, debug=debug)
   ```
   ![Main.py content](https://i.imgur.com/9XZmqht.png)

5. Scroll down and click "Commit changes"
   ![Commit main.py](https://i.imgur.com/vwGHgZd.png)

## Step 5: Creating a Basic Flask Application (if needed)

If you don't have the application code yet, here's how to create a basic structure:

1. Create `src/__init__.py`:
   - Click "Add file" > "Create new file"
   - Name it `src/__init__.py`
   - Leave it empty
   - Commit the file

2. Create or update `src/main.py` with a basic Flask application:
   ```python
   import os
   from flask import Flask, render_template, jsonify

   app = Flask(__name__)
   app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-testing')

   @app.route('/')
   def index():
       return jsonify({"status": "success", "message": "SocialSphere AI API is running"})

   if __name__ == '__main__':
       port = int(os.environ.get('PORT', 5000))
       debug = os.environ.get('FLASK_ENV') != 'production'
       app.run(host='0.0.0.0', port=port, debug=debug)
   ```

## Next Steps

Once you've created these files in your GitHub repository, your code will be ready for deployment on DigitalOcean. The next steps will be:

1. Setting up a DigitalOcean App Platform project
2. Connecting your GitHub repository
3. Configuring environment variables
4. Deploying your application

Would you like detailed instructions for these next steps as well?
