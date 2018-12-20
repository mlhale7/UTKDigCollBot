# UTKDigCollBot
Code for a Twitterbot [@UTKDigCollBot](https://twitter.com/UTKDigCollBot) for UTK's digital collections

This repository shares code that supports two methods of implementing a Twitter Bot for the University of Tennessee's digital collections. One takes a static JSON file of links pulled using an OAI harvester and randomized to create Twitter content (Bot_usingJSON). The second pulls a random record from UTK's OAI endpoint, excluding any sets that share thumbnails for their Open Graph image tags (og:image) since these images appear grainy on Twitter.

A number of individuals have written helpful instructions on different methods for creating Twitter Bots. I particularly benefitted from reading Scott Carlson's "You Should Make a Twitter Bot for Your G/L/A/M's Digital Collection(s)"[http://www.scottcarlson.info/you-should-make-a-twitter-bot/]. I initially had the idea to create a Bot thanks to Jeanette Sewell's presentation "The Wonderful World of Bots." Other informational resources on Bots include:
1. http://cheapbotsdonequick.com  
2. http://www.zachwhalen.net/posts/how-to-make-a-twitter-bot-with-google-spreadsheets-version-04/ 
3. http://programminghistorian.github.io/ph-submissions/lessons/intro-to-twitterbots
4. https://botwiki.org/resources/twitterbots/

For hosting, Amazon Web Services (AWS) Lambda and Heroku are options. Cheap Bots Done Quick provides hosting.

Last, but not least, thanks to @markpbaggett for his help in implementing this.
