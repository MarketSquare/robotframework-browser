import json

""" Sorts and prints in descending order by duration function call
    execution times in execution-times.log.

    BrowserLibrary debug option needs to be True to record times to the logfile.
"""

with open("Browser/wrapper/execution-times.log") as log_file:
    data = [json.loads(row) for row in log_file]
    result = sorted(data, key=lambda i: i["executionTime"], reverse=True)
    for item in result:
        print(item)
    # print(result)
