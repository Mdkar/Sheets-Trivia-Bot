import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
# SPREADSHEET_ID = "16sepHYJtTzbqVpEM3fnvlB-rea59T1a-OmZXyoy1vUI"
SPREADSHEET_ID = "1G5JtJq0RNRR7QBRcbZ7fK1OD0L9CdaUspz_YJWGbgQ0"
RESPONSES_NAME = "Form Responses 1!B:D"
ANSWERS_NAME = "Answer Key!A:D"
SCORES_NAME = "Scores"

point_emojis = {1: "✅", 5: "🟢", 20: "💚"}
def get_emoji(points):
    return point_emojis.get(points, "❓")

def n2a(n):
    d, m = divmod(n,26) # 26 is the number of ASCII letters
    return '' if n < 0 else n2a(d-1)+chr(m+65) # chr(65) = 'A'

TEAM_IDX = 0
QUESTION_IDX = 1
ANSWER_IDX = 2


def main():

  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)
    question = 0 # replace with the question number if code crashes
    teams = [] # fill this in if code crashes
# "go to scs day", 
# "rag",
# "compilers",
# "5506",
# "afsoc we lose",
# "noodleheads",
# "sassyscripters",
# "thunderbuddies",
# "lisa yu li",
# "the jaybirds",
# "iron man",
# "bangalore boys",
# "quiz wizzes"]
    repeat = True
    
    while(repeat):
        i = input(f"Press enter to score question {question}:")
        if i == "q": # Quit the program
            repeat = False
            break
        if i == "r": # Rescore the prev question
            question -= 1
            continue
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SPREADSHEET_ID, range=ANSWERS_NAME)
            .execute()
        )
        answer_key = result.get("values", [])
        if question > len(answer_key):
            if input("No more questions, press r to rescore the last question, any key to quit") == "r":
                question -= 1
            else:
                return
        correct_sols = []
        points = 0
        if question > 0:
            validate_num = int(answer_key[question][0])
            if validate_num != question:
                print(f"Error: question {question} is not same as answer key question {validate_num}")
            correct_sols = answer_key[question][1].lower().split(";")
            correct_sols = [sol.strip() for sol in correct_sols]
            points = int(answer_key[question][2])
            answer_range = int(answer_key[question][3])
        print(f"{correct_sols}, {points}")

        if not answer_key:
            print("No answer key found.")
            return
        
        # print(answer_key)

        result = (
            sheet.values()
            .get(spreadsheetId=SPREADSHEET_ID, range=RESPONSES_NAME)
            .execute()
        )
        values = result.get("values", [])

        if not values:
            print("No responses found.")
            return
        # print(values)

        team_inputs = {}
        for row in values:
            if row[QUESTION_IDX] == str(question):
                team = row[TEAM_IDX].strip().lower()
                answer = row[ANSWER_IDX].strip().lower()
                if team not in teams:
                    teams.append(team)
                if answer_range == 0 and answer in correct_sols:
                    team_inputs[team] = get_emoji(points)
                elif answer_range > 0:
                    try:
                        answer = int(answer)
                        correct_sol = int(correct_sols[0])
                        if answer >= correct_sol - answer_range and answer <= correct_sol + answer_range:
                            team_inputs[team] = get_emoji(points)
                        else:
                            team_inputs[team] = answer
                    except ValueError:
                        team_inputs[team] = answer
                else:
                    team_inputs[team] = answer
                   
        print(team_inputs)
        for t in teams:
            if t not in team_inputs:
                team_inputs[t] = "❌"
        write_col = [team_inputs[t] for t in teams]
        if question > 0:
            # Write to the sheet
            # update team names
            values = [[t] for t in teams]
            body = {"values": values}
            result = (
                sheet.values()
                .update(
                    spreadsheetId=SPREADSHEET_ID,
                    range=f"{SCORES_NAME}!A2:A",
                    valueInputOption="RAW",
                    body=body,
                )
                .execute()
            )
            # update answers
            values = [[w] for w in write_col]
            body = {"values": values}
            c = n2a(question+1)

            result = (
                sheet.values()
                .update(
                    spreadsheetId=SPREADSHEET_ID,
                    range=f"{SCORES_NAME}!{c}2:{c}",
                    valueInputOption="RAW",
                    body=body,
                )
                .execute()
            )
        if question == 0:
            print("Game ready")
        question += 1

  except HttpError as err:
    print(err)


if __name__ == "__main__":
  main()