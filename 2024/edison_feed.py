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
    if 'data' not in state_data or 'races' not in state_data['data'] or not state_data['data']['races']:
        continue

    race = state_data['data']['races'][0]
    for candidate in race['candidates']:
        if candidate['party_id'] == 'republican':
            candidate['party'] = 'rep'
        elif candidate['party_id'] == 'democrat':
            candidate['party'] = 'dem'
        else:
            candidate['party'] = 'trd'

    candidates = {candidate['candidate_key']: candidate for candidate in race['candidates']}

    for data_point in race['timeseries']:
        data_point['state'] = state
        data_point['expected_votes'] = race.get('tot_exp_vote', 0)

        percentage_votes = collapse_percent_per_party(data_point['vote_shares'], candidates)

        for party in ['rep', 'dem', 'trd']:
            data_point[f'vote_shares_{party}'] = percentage_votes.get(party, 0)

        data_point.pop('vote_shares', None)
        records.append(data_point)

# Creating a DataFrame and saving to CSV
time_series_df = pd.DataFrame.from_records(records)
# Create a timestamp for the filename
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
output_path = f'Edison_{timestamp}.csv'
time_series_df.to_csv(output_path, encoding='utf-8', index=False)

print(f"Data successfully saved to {output_path}")
