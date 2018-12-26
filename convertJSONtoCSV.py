import re
import json
import argparse
import pandas as pd

def convert_csv(filename):
    with open(filename) as f:
        data = json.load(f)
    for key in data:
        key['products'] = key['products'][0]
        if key.get('locations', {}):
            key['locations-name'] = key['locations'][0]['name']
            key['locations-url']  = key['locations'][0]['url']
            key.pop('locations')
    df = pd.DataFrame.from_records(data)
    df['listened'] = df['title'].apply(lambda x: True if re.match('^Listened to ', x) is not None else False)
    df['skipped'] = df['title'].apply(lambda x: True if re.match('^Skipped ', x) is not None else False)
    df['searched'] = df['title'].apply(lambda x: True if re.match('^Searched for ', x) is not None else False)
    df['title'] = df['title'].apply(lambda x: re.sub('^Listened to |^Skipped |^Searched for ', '', x))
    temp = df.rename(columns={'description': 'artist', 'titleUrl':'searchresultURL'})
    temp.to_csv('My Activity.csv', index=None)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add filename')
    parser.add_argument('filename')
    args = parser.parse_args()
    convert_csv(args.filename)