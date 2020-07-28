import datetime
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
from paras import *
#look==> https://opendata.cwb.gov.tw/dist/opendata-swagger.html

root_url = 'http://opendata.cwb.gov.tw/api/v1/rest/datastore/'
dataid_list = ['O-A0001-001', 'O-A0002-001', 'O-A0003-001']

def get_data(data_id, limit):
	api_url = '{}{}?Authorization={}'.format(root_url, data_id, api_key)  #&limit={}  , limit
	r = requests.get(api_url)
	data = r.json()
	return data

def parse_json(data):
	columns = ['stationId', 'locationName', 'lat', 'lon', 'obstime', 'ELEV', 'RAIN', 'MIN_10', 'HOUR_3', 'HOUR_6', 'HOUR_12', 'HOUR_24', 'NOW']
	df = pd.DataFrame(columns=columns)
	data_dict = {}
	locations = data['records']['location']
	row = -1
	for location in locations:
		row = row + 1
		data_dict['stationId'] = location['stationId']
		data_dict['locationName'] = location['locationName']
		data_dict['obstime'] = location['time']['obsTime']
		data_dict['lat'] = location['lat']
		data_dict['lon'] = location['lon']

		factors = location['weatherElement']
		for factor in factors:
			factor_name = factor['elementName']
			data_dict[factor_name] = factor['elementValue']

		parameters = location['parameter']
		for parameter in parameters:
			factor_name = parameter['parameterName']
			data_dict[factor_name] = parameter['parameterValue']

		for key in data_dict.keys():
			df.loc[row,key] = data_dict[key]
	return df

if __name__ == "__main__":
	for dataid in dataid_list:
		json_data = get_data(dataid, 100)
		df = parse_json(json_data)

		current_datetime = datetime.datetime.now()
		df['reportTime'] = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

		save_file_name = './{}{}data.csv'.format(current_datetime.strftime('%Y-%m-%d_%H-%M-%S'), dataid)
		df.to_csv(save_file_name, encoding='utf-8', index=False)
		print('save ok:)')
