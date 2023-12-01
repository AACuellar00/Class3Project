from . import db


def average_location_data(aq, aq_entry, last_time_collected):
    average = aq_entry.particulate_matter_level_average * aq_entry.times_averaged
    average += aq
    average /= (aq_entry.times_averaged + 1)
    aq_entry.particulate_matter_level_current = aq
    aq_entry.particulate_matter_level_average = average
    aq_entry.times_averaged += 1
    aq_entry.last_time_collected = last_time_collected
    db.session.commit()


def threshold_less_than_aq_of_day(user_threshold, aq_of_day):
    if user_threshold < aq_of_day:
        return 1
    else:
        return 0
