# Sheets Trivia Bot
Autograding backend to run trivia games using Google Forms and Sheets

All code is in ``quickstart.py``

TL;DR: 
* set up Google Form and Sheet, make modifications in code
* run ``quickstart.py``
* Press enter for question 0 for initial setup
* Press enter once time is up for each question
* Code will look for last answers from each team *only* for current question number

## Detailed instructions
* Create Google Form with "Team Name", "Question Number", and "Answer" questions
* Link form with Google Sheet
* Get ``SPREADSHEET_ID`` from URL of sheet
* Add "Answer Key" and "Scores" tabs to sheet
* "Answer Key" sheet should have
  * Question Number,	Answers (case insensitive),	Points,	Range columns
  * Question numbers should be in order (out of order may cause a bug)
  * Answers are ';' separated values (B; Subra Suresh; Suresh; Subra)
  * Points have to be defined in the ``point_emojis`` dictionary
  * Range column must have 0's filled in if answer doesn't have a numerical range. This can be easily fixed in the future...
  * Do not leave any empty cells in these columns
* "Scores" will be filled by this code
  * Columns will be "Team",	"Score",	"Q1",	"Q2",	"Q3", ...
  * Set the Score column to something like ``=1*COUNTIF(C2:2, "✅") + 5*COUNTIF(C2:2, "🟢") + 0.5*COUNTIF(C2:2, "💚") ``
  * Emoji = correct answer
  * Incorrect answers are presented as text
  * You can manually grade these answers by replacing them with an emoji
  * Code should really make sure the answer isn't an emoji itself, but that probably won't be an issue...
* If code crashes, fill in ``teams`` list and last question ``number`` before restarting 
* Code will automatically fill in any new teams as they join
* Enter 'q' to quit
* Enter 'r' to go back a question and Enter again to rescore the current question