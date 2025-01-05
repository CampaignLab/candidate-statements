# candidate-statements
Understanding candidate messaging and public statements helps identify patterns and develop effective counter-messaging strategies. 

The goal is to build a system to collect and analyze public statements made by Reform UK candidates across various platforms, identifying common themes, rhetoric patterns, and potential misinformation.

## Statements from Democracy Club

First source will be candidate statements from the 2024 GE collected by Democracy Club and available via their API.

You will need to create an account at [Democracy Club](https://candidates.democracyclub.org.uk/). Once you have done so, place it in your `.env` file as follows:

```
TOKEN=<your token>
```

Run the tool to download the statements.

```
pip install load-dotenv
pip install requests
python get_statements.py
```

Currently takes about 30 minutes to download as Democracy Club has rate limits we have to follow.
