import pandas as pd
import json

data=open("sample_airbnb.listingsAndReviews.json","r",encoding='utf-8')
file=json.load(data)

property_table={'_id':[],'Name':[],'Property_type':[],'Room_type':[],'Date':[],'Accomodates':[],'Price':[],'Address':[],'Country':[],'Location':[],'Rating':[],'Amenities':[]}
for i in range(len(file)):
    property_table['_id'].append(file[i].get('_id'))
    property_table['Name'].append(file[i].get('name'))
    property_table['Property_type'].append(file[i].get('property_type'))
    property_table['Room_type'].append(file[i].get('room_type'))
    property_table['Date'].append(file[i].get('last_scraped'))
    property_table['Accomodates'].append(file[i].get('accommodates'))
    property_table['Price'].append(file[i].get('price'))
    property_table['Address'].append(file[i]['address'].get('street'))
    property_table['Country'].append(file[i]['address'].get('country'))
    property_table['Location'].append(file[i]['address']['location'].get('coordinates'))
    property_table['Rating'].append(file[i]['review_scores'].get('review_scores_rating'))
    property_table['Amenities'].append(file[i].get('amenities'))

df=pd.DataFrame(property_table)

with open('property_raw.json', 'w') as f:
    f.write(df.to_json(orient='records', lines=True))

review_table={'Property_id':[],'Review_id':[],'Reviewer_name':[],'Comment':[]}
for i in range(len(file)):
    if len(file[i].get('reviews'))>0:
        for j in range(len(file[i].get('reviews'))):
            review_table['Property_id'].append(file[i]['reviews'][j]['listing_id'])
            review_table['Review_id'].append(file[i]['reviews'][j]['_id'])
            review_table['Reviewer_name'].append(file[i]['reviews'][j].get('reviewer_name'))
            review_table['Comment'].append(file[i]['reviews'][j].get('comments'))
df=pd.DataFrame(review_table)

with open('review_raw.json', 'w') as f:
    f.write(df.to_json(orient='records', lines=True))

with open('property_table_raw.json', 'w') as f:
    json.dump(property_table, f)

review_raw=[]
for i in range(149792):
    review_raw.append(dict(Property_id=review_table['Property_id'][i],Review_id=review_table['Review_id'][i],Reviewer_name=review_table['Reviewer_name'][i],Comment=review_table['Comment'][i]))
with open('review_raw.json', 'w') as f:
    json.dump(review_table, f, indent=4)
