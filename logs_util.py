import datetime
from pathlib import Path

# function that calls all the information and the utilization gathered and save it into the logs folder
def save_log(log_type, log_data):
    # Create a 'logs' directory if it doesn't already exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Generate a timestamp in the format 'YYYYMMDD-HHMMSS'
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    # Create a log file name with the format 'log_type_timestamp.log'
    log_filename = f"{log_type}_{timestamp}.log"
    # Construct the full path to the log file
    log_filepath = logs_dir / log_filename

    # Open the log file for writing
    with open(log_filepath, 'w') as log_file:
        # Check the type of log_data
        if isinstance(log_data, str):
            # If log_data is a string, write it to the file as is
            log_file.write(log_data)
        elif isinstance(log_data, tuple):
            # If log_data is a tuple, write each element on a new line
            for line in log_data:
                log_file.write(str(line) + "\n")
        else:
            # For any other type, write the string representation of log_data to the file
            log_file.write(str(log_data))

    # Print a message indicating the log file path
    print(f"{log_type.capitalize()} log saved to {log_filepath}")