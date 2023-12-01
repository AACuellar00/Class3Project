

def average_location_data(aq_data, obtained_value):
    if aq_data['idx'] == (obtained_value['idx']):
        if aq_data["last_time_collected"].__eq__(obtained_value["last_time_gen"]):
            return aq_data
        else:
            average = aq_data["aqa"] * aq_data["averaged_times"]
            average += obtained_value["aqi"]
            average = round(average/(aq_data["averaged_times"] + 1))
            aq_data["averaged_times"] += 1
            aq_data["aqc"] = obtained_value["aqi"]
            aq_data["aqa"] = average
            aq_data["last_time_collected"] = obtained_value["last_time_gen"]
    return aq_data


def threshold_less_than_aq_of_day(user_threshold, aq_of_day):
    if user_threshold < aq_of_day:
        return 1
    else:
        return 0
