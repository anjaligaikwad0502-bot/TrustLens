# __pycache__/  
Contains auto-generated Python cache files.  
Improves execution speed during development.

# model/  
Stores all trained machine learning assets.  
Keeps model files separate from application logic.

# model/scam_model.pkl  
Pre-trained ML model for scam message detection.  
Loaded by Flask to generate predictions.

# static/  
Holds static frontend resources.  
Includes CSS and JavaScript files.

# static/js/script.js  
Manages client-side interactions and logic.  
Handles form submission and UI behavior.

# static/css/style.css  
Defines layout, colors, and UI styling.  
Improves readability and user experience.

# templates/  
Contains HTML templates rendered by Flask.  
Enables dynamic content rendering.

# templates/index.html  
Main interface for user input.  
Allows users to submit text for analysis.

# templates/result.html  
Displays scam detection results.  
Shows prediction outcome clearly to users.

# app.py  
Main backend application using Flask.  
Processes input and returns ML predictions.

# train_model.py  
Used to train the scam detection model.  
Saves the trained model for later use.

# dataset.csv  
Contains labeled training data.  
Used for building and evaluating the ML model.

# requirement.txt  
Lists all Python dependencies.  
Ensures smooth project setup and execution.
