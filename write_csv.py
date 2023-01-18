import csv


class WriterCsv():

    def create_csv(name):
        with open(name, 'w', newline='') as file:
            csv.writer(file)

    def write_filename(name, filename):
        with open(name, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([filename])

    def write_headers(name, adding_time_values):
        with open(name, 'a', newline='') as file:
            writer = csv.writer(file)
            if adding_time_values:
                headers = ['Name', 'Number of occurences',
                           'Percentage of occurences', 'Total time', 'Time percentage', "Start and end times"]
            else:
                headers = ['Name', 'Number of occurences',
                           'Percentage of occurences']
            writer.writerow(headers)

    def write_row(name, adding_time_values, key, value, percentage, time_value_date, percentage_length, start_end_values):
        with open(name, 'a', newline='') as file:
            writer = csv.writer(file)
            if adding_time_values: 
                writer.writerow(
                    [key, value, percentage, time_value_date, percentage_length, start_end_values])            
            else:
                writer.writerow([key, value, percentage])

    def write_spacing(name):
        with open(name, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow('')

    def write_headers_total(name):
        with open(name, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['TOTAL'])
            # Writing names of columns
            writer.writerow(['Name', 'Number of occurences',
                            'Percentage of occurences'])

    def write_total(name, key, value, stat):
        with open(name, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([key, value, stat])