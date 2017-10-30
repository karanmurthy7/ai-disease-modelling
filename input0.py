population_count = 100
sick_people_count = 91


def goal_message(s):
    message = "\n********************************************************************\n"
    if HAS_VIRUS_WON:
        message += "END: Oh no! Common Cold has taken over (90% of) the world!"
    else:
        message = "END: With cold under control (<10%), the World is a better place to live."
    message += "\n********************************************************************\n"

    return message