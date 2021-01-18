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


## To Add new flows 

add it to the flow.json file at /static/data/flow.json 

How to add New command in flow.json:

example:"1": {
            "command": "FLOW START",
            "Position": {
                "top": 0.25,
                "left": 0,
                "scale": 1,
                "zoom": "300%"
            },
            "help": "https://www.nlpbots.com/"
        }

Note: 1 refers to the position the user wants to move to.

There are three major constraints for a command:
1. command Name (identified by command)

2. command Position(position attribute)

      Image is moved to a particular position by :
      a. scaling the image.
      b. zooming (if necessary).
      c. Moving the viewport of the user with the help of javascript function:

      Example:

      window.scrollTo({
            top: styles['top'] * document.body.scrollHeight,
            left: styles['left'] * document.body.scrollWidth,
          })

      Here styles['top] refers to the how much percentage of the scrollHeight of overall body is viewport moved.

      Similarly styles['left'] refers to how much percentage of the scrollWidth of overall body is viewport moved.

      If we would want to add a new position in future user can vary the values of top and left positions and then use the above.

      Command and could see the changes in the viewport as he would change the values in the percentages of height and width.

3. command help (help attribute);
    This is the url where the user wants to navigate for help functionality.

4. Every node should have back and home commands. 
      Back : will navigate user to just before point in work flow
      Home :will navigate user to home or start screen 
      In home entry there is a key isHome which is to identify as home so user when adding home can take any other home entry of any other node.

## To Add new FAQ to bot

add it to the faq.json file at /static/data/faq.json

## For front-end bot static messages use bot_text.json at /static/data/bot_text.json

## Use convert_language.py file to add multiple languages to FAQ and bot static message  

`python convert_language.py`

## Languages used in bot

 are configured in language.json at /static/data/language.json 

# To run the application 
from the root directory of the project
`python app.py`

The app starts running at your localhost and port 8000

To access the bot navigate to /bot in the url 

** this accepts GET request only with parameters 'user_message', 'current_position' 
current_position is the position at which user is and if the current_position is empty then by default it will take as home i.e 0
** for more faq add faq in faq.json file

API and there arrguments

* api: /bot_text  arrguments:user_message,current_position,language(id)

  * Eg. `Example http://127.0.0.1:8000/bot_text?user_message="select face entry"&current_position=1&language=1`

  * 'language' should be the id you get in the get request of 'getlanguage'

* api: /bot_voice  arrguments:user_message,current_position,language

  * 'user_message' in this api will be the voice data
  * It will be POST request and requires form data

* api: /suggestion  arrguments:user_message

* api: /get_faq  arrguments:language(id)

* api: /upload  arrguments:form data "document"

Whenever a file has been uploaded the file gets saved in '/static/database/filename'

* api: /getlanguage  arrguments:None

* api: /get_change_text  arrguments:language(id)


'app.py' and 'website_assistence.py' both are same but 'app.py' is used as API's and 'website_assistence.py' is used as normal python file which can be run in a terminal to see the output.