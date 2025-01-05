import requests
from dotenv import load_dotenv
import os
import json
from datetime import datetime  
import time 
import logging  

load_dotenv()
token = os.getenv("TOKEN")
headers = {
    'Authorization': f"Token {token}"
}
BASE_URL = "https://candidates.democracyclub.org.uk/api/next"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S')

def make_request(url):
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response
        elif response.status_code == 429:  # Throttled response
            wait_time = int(response.headers.get('Retry-After', 30))  # Default to 30 seconds if not specified
            time.sleep(wait_time)
        else:
            print(f"Failed to retrieve data: {response.status_code}")
            return None

def main():
    logging.info("Starting")
    response = make_request(f"{BASE_URL}/elections/parl.2024-07-04")

    if response is None:
        return

    data = response.json()

    ballot_urls = [ballot['url'] for ballot in data['ballots']]

    output_data = []
    ballots = 0
    for ballot_url in ballot_urls:
        ballot_response = make_request(ballot_url)
        if ballot_response is None:
            continue

        ballot_data = ballot_response.json()
        candidacies = ballot_data.get("candidacies", [])
        for candidacy in candidacies:
        
            if candidacy["party_name"] == "Reform UK":
                person_url = candidacy["person"]["url"]
                person_response = make_request(person_url)
                if person_response is None:
                    continue

                person_data = person_response.json()

                if "statement_to_voters" in person_data:
                    # Find the candidacy with the most recent created date
                    most_recent_candidacy = None
                    most_recent_time = None

                    for candidacy in person_data.get("candidacies", []):
                        created_time = datetime.fromisoformat(candidacy["created"])

                        if most_recent_time is None or created_time > most_recent_time:
                            most_recent_time = created_time
                            most_recent_candidacy = candidacy

                    if most_recent_candidacy:
                        output_data.append({
                            "name": person_data["name"],
                            "statement_to_voters": person_data["statement_to_voters"],
                            "statement_to_voters_last_updated": person_data.get("statement_to_voters_last_updated"),
                            "ballot_url": most_recent_candidacy["ballot"]["url"]  # Assuming the ballot URL is in the candidacy
                        })

        ballots += 1
        if (ballots % 10) == 0:
            logging.info(f"{ballots} constituencies completed.")  # Use logging instead of print
    # Write the output data to a JSON file
    with open('candidacies.json', 'w', encoding='utf-8') as json_file:
        json.dump(output_data, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
