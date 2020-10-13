# Website assistance bot

## Requirements
- python
- nltk
- spellchecker
- flask

Install python and then install other requirements,

` pip install -r requirements.txt`

After sucessfully installing all the requirements then open the python command line and install the nltk models.

In python command line

> import nltk

> nltk.download('all')

> nltk.download('stopwords')


# To run the application 
from the root directory of the project
`python app.py`

The app starts running at your localhost and port 5000

To access the bot navigate to /bot in the url 

** this accepts GET request only with parameters 'user_message', 'current_position' 
current_position is the position at which user is and if the current_position is empty then by default it will take as home i.e 0

API and there arrguments
api: /bot  arrguments:user_message,current_position
api: /suggestion  arrguments:user_message
api: /get_faq  arrguments:None

