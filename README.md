# Whatsapp parser
This script takes in a .txt file exported via whatsapp and parses it, outputting a structured .csv file and a wordcloud as a png.  
The script leverages a custom class that handles most of the data manipulation, while the *generator* file addresses user input.  

A generic Whatsapp file template is the following, describing for fictional purposes a Ninja Turtles pizza night (also, crafted adhoc to display the wordcloud capabilities):
    
    02/07/2015, 14:20 - Leonardo: stasera pizza?
    02/07/2015, 14:24 - Raffaello: <Media omitted>
    02/07/2015, 14:26 - Michelangelo: siiii pizza pizza pizza pizza
    02/07/2015, 14:26 - Donatello: qualcuno gestisca michelangelo
    02/07/2015, 14:32 - Michelangelo: pizza pizza pizza
    02/07/2015, 14:35 - Leonardo: ok messaggio ricevuto - ordiniamo 4 margherite?
    02/07/2015, 14:36 - Raffaello: mamma mia Leo un po'di vita...
    02/07/2015, 14:38 - Raffaello: <Media omitted>
    02/07/2015, 14:39 - Donatello: allora una marinara, una margherita, una capricciosa e un calzone?
    02/07/2015, 14:39 - Michelangelo: ho mica detto pizza?

## How to use:
- Extract a conversation file from whatsapp and place it into the script folder. (Make sure **not** to extract media files)  

<img src="/imgs/ninjas.jpg" width="400">

The script will:
- Check for all .txts available in its folder. If multiple files are found, the user is asked to specify one.  
- Parse data into a dataframe structure, isolating Date, Time, User, Message components (plus an extra column for tokenized words).  
- Ask the user if they want a User-specific wordcloud.  
- Save both dataframe and wordcloud (in .csv and .png) format into an /output folder.  

A sample output:  
<img src="/output/wordcloud.jpg" width="432">


---

**Important Limitations**
- The script does not handle well multi-line messages. (A nice solution is shared in this [medium post](https://towardsdatascience.com/build-your-own-whatsapp-chat-analyzer-9590acca9014) )
- Stopwords included are for Italian and English languages. They can be easily extended by editing the class. 
- The script was tested from an android Whatsapp extract
- The wordcloud is not sophisticated in the way it cuts words shorter than 5 characters and does not merge together singulars/plurals.

### Needed Libraries
- os
- sys
- Pandas
- Matplotlib
- re
- nltk
- [Wordcloud](https://github.com/amueller/word_cloud) --> [Datacamp Tutorial](https://www.datacamp.com/community/tutorials/wordcloud-python)
