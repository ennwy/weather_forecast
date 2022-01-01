

from time import mktime, strptime, timezone


def is_data_valid(parameter):
	parameters = {
		"date",
		"temp",
		"pcp",
		"clouds",
		"pressure",
		"humidity",
		"wind_speed"
		}
	result = False
	if parameter in parameters:
	    result = True
	return result


def parse_date_to_timestamp(dates):
    timestamp_dates = []
    for date in dates:
        timestamp = int(mktime(strptime(date, "%d.%m.%Y"))) - timezone
        timestamp_dates.append(timestamp)

    return timestamp_dates


def parse_data_from_list(data):
    all_data = []
    for day in data:

        parameters = {}

        parameters["city"] = day[0]
        parameters["date"] = day[1]
        parameters["temp"] = day[2]
        parameters["pcp"] = day[3]
        parameters["clouds"] = day[4]
        parameters["pressure"] = day[5]
        parameters["humidity"] = day[6]
        parameters["wind_speed"] = day[7]

        all_data.append(parameters)
    return all_data


def unpack_list_with_lists(data):
    data = [value for value_in_list in data for value in value_in_list]
    return data

    
