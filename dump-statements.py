import json

def main():
    with open('candidacies.json', 'r') as file:
        data = json.load(file)
    statements = [candidacy['statement_to_voters'] for candidacy in data if len(candidacy['statement_to_voters']) > 5]
    with open('statements.json', 'w', encoding='utf-8') as json_file:
        json.dump(statements, json_file, ensure_ascii=False, indent=4)
    
if __name__ == "__main__":
    main()
