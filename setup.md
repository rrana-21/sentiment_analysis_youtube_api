## Setup Instructions
### Obtain an API Key
To use the YouTube Data API v3, you will need to obtain an API key from the Google Developers Console. To do so, follow these steps:

Go to the Google Developers Console.
Create a new project by clicking on the dropdown menu at the top of the page and selecting "New Project."
Enter a name for your project and click "Create."
Once your project is created, select it from the dropdown menu at the top of the page.
In the left-hand navigation menu, click on "APIs & Services" > "Library."
Search for "YouTube Data API v3" and select it.
Click "Enable" to enable the API for your project.
In the left-hand navigation menu, click on "APIs & Services" > "Credentials."
Click "Create Credentials" > "API Key."
Copy your API key to use in the sentiment_analysis.py script.

### Dependencies
To run the sentiment_analysis.py script, you will need to install the following dependencies:

google-auth==1.35.0
google-auth-oauthlib==0.4.6
google-auth-httplib2==0.4.6
google-api-python-client==2.19.0
numpy==1.14.0
pandas==1.3.4
transformers==4.12.5

You can install these dependencies by running pip install -r requirements.txt in your command prompt or terminal.
