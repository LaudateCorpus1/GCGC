# read_log_file.py

# defines functions to parse and extract information from a specified log file
# Ellis Brown, June 2021

import pandas as pd
import re


## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                               getParsedData
#
# Purpose:
#   Given a filepath to a log file, create a pandas dataframe holding all information
#   for that log file. Each row is a different event.
#
# Parameters:
#   logfile -> a string with the path to the log file to read.
#
# Return:
#   a pandas dataframe, where rows are each an individual event. Columns are labeled, and
#   collect information on each event, such as when it occured, how long it lasted, and the name
## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def getParsedData(logfile):
    assert isinstance(logfile, str)  # input must be a string
    if not logfile:
        print("No logfile provided")
        return
    table = __manyMatch_LineSearch(event_parsing_string(), logfile)
    if not any(table):
        print("Unable to parse file " + str(logfile))
        return None
    parsed_data_table = pd.DataFrame(table).transpose()  # transpose to orient correctly
    parsed_data_table.columns = __columnNames()  # add column titles, allow for clear references
    return parsed_data_table


## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                         __manyMatch_LineSearch
#   Purpose:
#       Search through a file and return a list of matches for a regex search term
#
#   Parameters:
#       search_term      : string-> Terms to search for within data set
#       filepath         : string-> file path to log file
#   Return:
#       2 dimensional list structure. List of group's matches
#       table[index] = list of all matches associated with group at index - 1
#
## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def __manyMatch_LineSearch(
    match_term=None,  # regex terms to search for
    filepath=None,
):  # TRUE if data in a file
    num_match_groups = re.compile(match_term).groups
    table = [[] for i in range(num_match_groups)]
    # If there has been listed groups of interest within the regex search
    file = open(filepath, "r")
    for line in file:
        match = re.search(match_term, line)
        if match:
            # Find all matches of interest
            for i in range(0, num_match_groups):
                table[i].append(match.group(i + 1))  # +1 because group(0) is the whole string
            # add the match group number hit, so able to tell what match
    file.close()
    return table


# Access the column names for a parsed file. Note that these are dependent
# on the groups defined in event_string_parsing
def __columnNames():
    return [
        "DateTime",
        "TimeFromStart_seconds",
        "EventType",
        "EventName",
        "AdditionalEventInfo",
        "MemoryChange_MB",
        "Duration_miliseconds",
    ]


## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                       event_parsing_string
#
# Returns a regex-searchable string to handle parsing log lines.
# Defined regex groups are each section of the code
#
# GROUP 1: "DateTime" -> information on time of recording
# GROUP 2: "TimeFromStart_seconds" -> time of beginning of event in seconds
# GROUP 3: "EventType" -> Either concurrent or stop the world pause
# GROUP 4: "EventName" -> Specific action from the event. Example : "(pause) Young"
# GROUP 5: "AdditionalEventInfo" -> Information about the event
# GROUP 6: "MemoryChange_MB" -> Memory changed, following this patten: before->after(max_heapsize)
# GROUP 7: "Duration_miliseconds" -> How long it took for the event to occur in miliseconds
#
#  Return: string
## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def event_parsing_string():
    # Implementation note: Be aware that spaces within the strings are intentional.
    datetime = "^(?:\[(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}\+\d{4})\])?"  # [2020-11-16T14:54:16.414+0000]
    timefromstart = "\[(\d+\.\d+)s\]"  #                                 [123.321s]
    outputlevel = "\[\w+ ?\]"  #                                         [info]
    phase = "\[gc\s*\]"  # NOTE: this does NOT accept anything but 'gc' level outputs
    log_number = " GC\(\d+\) "  #                                        GC(123)
    event_type = "((?:Pause)|(?:Concurrent)) "  #                        Pause
    event_name = "((?:\w+ ?){1,3}) "  #                                  Young
    additional_event_info = "(\((?:\w+ ?){1,3}\) ){0,3}"  #             (Evacuation Pause) (Normal)
    memory_change = "(\d+\w->\d+\w\(?\d+?\w?\)?){0,1} ?"  #              500M->212M(1200M)
    event_duration_ms = "(\d+\.\d+)ms"  #                                200.31ms
    return (
        datetime
        + timefromstart
        + outputlevel
        + phase
        + log_number
        + event_type
        + event_name
        + additional_event_info
        + memory_change
        + event_duration_ms
    )
