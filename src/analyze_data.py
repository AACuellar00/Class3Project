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
