# PyAlley
PyAlley - a framework for the *py Alley board game simulator and computer agent test bed with opportunities  for intelligent agent development and competition between agents. Spy Alley game rules are available at https://officialgamerules.org/game-rules/spy-alley/ as well as a PDF file in this repo.

*** Note *** On Windows I was able to successfully run the following tests inside the VsCode's Terminal for a Python enabled project.

<b>Interactive Test (number of human players can be zero for just observing the behaviors):</b>

cd Test_Interactive  
python SpyAlley.py

<b>Batch Test:</b>

cd Test_Batch  
python SpyAlley.py

<b>Leaderboard:</b>

|     Rank      |    Bot Name   |   Version    |   Author     |
| ------------- | ------------- |------------- |------------- |
|      #1       |     Z-bot     |      00      | Zbigniew W.  |
|      #2       |     J-bot     |      00      |  Joshua C.   |

<b>Latest batch run:</b>

...  
998  
999  
Z-bot #2 : 273 wins  
Z-bot #1 : 295 wins  
Z-bot #3 : 280 wins  
J-bot #1 : 55 wins  
J-bot #3 : 47 wins  
J-bot #2 : 50 wins  

<b>Spy Alley Board:</b>

![Spy Alley](SpyAlleyBoard.png?raw=true "Spy Alley Board")

<b>Custom methods to override:</b>

The J00_Bot is basically the ComputerPlayer class under a different name. The Z00_Bot only overrides one method - handleChallengePhase(), so sky is the limit as to what can be improved:

![Custom Methods](CustomMethodsToOverride.png?raw=true "Custom Methods")
