## Setup Instructions
### Obtain an API Key
To use the YouTube Data API v3, you will need to obtain an API key from the Google Developers Console. To do so, follow these steps:

1. Go to the Google Developers Console.
2. Create a new project by clicking on the dropdown menu at the top of the page and selecting "New Project."
3. Enter a name for your project and click "Create."
4. Once your project is created, select it from the dropdown menu at the top of the page.
5. In the left-hand navigation menu, click on "APIs & Services" > "Library."
6. Search for "YouTube Data API v3" and select it.
7. Click "Enable" to enable the API for your project.
8. In the left-hand navigation menu, click on "APIs & Services" > "Credentials."
9. Click "Create Credentials" > "API Key."
10. Copy your API key to use in the sentiment_analysis_youtube_api.py script.

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
