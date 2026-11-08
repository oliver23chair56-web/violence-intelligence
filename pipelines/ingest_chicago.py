"""Download a bounded sample of Chicago reported offenses. No API credentials required."""
import argparse
import json
import urllib.parse
import urllib.request

URL = 'https://data.cityofchicago.org/resource/ijzp-q8t2.json'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='chicago_sample.json')
    parser.add_argument('--limit', type=int, default=100, choices=range(1, 1001))
    args = parser.parse_args()
    params = urllib.parse.urlencode({
        '$select': 'id,date,primary_type,description,community_area,case_number',
        '$where': "primary_type in('HOMICIDE','BATTERY','ASSAULT','ROBBERY')",
        '$order': 'date DESC',
        '$limit': str(args.limit),
    })
    req = urllib.request.Request(URL + '?' + params, headers={'User-Agent': 'ViolenceIntelligenceResearch/0.1'})
    with urllib.request.urlopen(req, timeout=30) as response:
        data = json.load(response)
    assert isinstance(data, list)
    with open(args.output, 'w', encoding='utf-8') as output:
        json.dump({'source': URL, 'sample_capped': True, 'records': data}, output, indent=2)
    print(f'Wrote {len(data)} reported offense records to {args.output}')


if __name__ == '__main__':
    main()
