import pandas as pd
import requests
from requests.exceptions import RequestException
from datetime import datetime

def collapse_percent_per_party(results_by_candidate, candidates):
    percent_per_party = {}
    for candidate, count in results_by_candidate.items():
        party = candidates[candidate]['party']
        percent_per_party[party] = percent_per_party.get(party, 0) + count
    return percent_per_party

# List of state names to fetch results for
states = [
    'Alaska', 'Alabama', 'Arkansas', 'Arizona', 'California', 'Colorado', 'Connecticut', 
    'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Iowa', 'Idaho', 'Illinois', 'Indiana', 
    'Kansas', 'Kentucky', 'Louisiana', 'Massachusetts', 'Maryland', 'Maine', 'Michigan', 
    'Minnesota', 'Missouri', 'Mississippi', 'Montana', 'North Carolina', 'North Dakota', 
    'Nebraska', 'New Hampshire', 'New Jersey', 'New Mexico', 'Nevada', 'New York', 'Ohio', 
    'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 
    'Tennessee', 'Texas', 'Utah', 'Virginia', 'Vermont', 'Washington', 'Wisconsin', 
    'West Virginia', 'Wyoming'
]

all_results = {}
for state in states:
    formatted_state = state.lower().replace(' ', '-')
    state_url = f'https://static01.nyt.com/elections-assets/pages/data/2024-11-05/results-{formatted_state}-president.json'
    try:
        print(f'Fetching Results from {state}')
        response = requests.get(state_url)
        response.raise_for_status()  # Raise an error for bad status codes
        state_data = response.json()
        all_results[formatted_state] = state_data
    except RequestException as e:
        print(f"Error fetching results for {state}: {e}")
        continue

records = []
for state, state_data in all_results.items():
    if 'races' not in state_data or not state_data['races']:
        continue

    race = state_data['races'][0]
    reporting_units = race.get('reporting_units', [])

    for unit in reporting_units:
        for candidate in unit['candidates']:
            if 'nyt_id' not in candidate:
                continue
            candidate_key = candidate['nyt_id']
            if candidate_key.startswith('trump'):
                candidate['party'] = 'rep'
            elif candidate_key.startswith('harris'):
                candidate['party'] = 'dem'
            else:
                candidate['party'] = 'trd'

        candidates = {candidate['nyt_id']: candidate for candidate in unit['candidates']}

        record = {
            'state': state,
            'county': unit.get('name', 'statewide'),
            'level': unit.get('level', 'state'),
            'total_votes': unit.get('total_votes', 0),
            'expected_votes': unit.get('total_expected_vote', 0)
        }

        for candidate in unit['candidates']:
            party = candidate.get('party', 'trd')
            record[f'vote_shares_{party}'] = candidate['votes']['total']

        records.append(record)

# Creating a DataFrame and saving to CSV
time_series_df = pd.DataFrame.from_records(records)
# Create a timestamp for the filename
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
output_path = f'/users/saraheaglesfield/Election Data Feed/Edison_{timestamp}.csv'
time_series_df.to_csv(output_path, encoding='utf-8', index=False)

print(f"Data successfully saved to {output_path}")
