import glob
import xml.etree.ElementTree as ET
from pathlib import Path
import time
from write_csv import WriterCsv as wcsv


class WriteStats:

    """
    A class for writing statistics to a CSV file.
    """
    def write_stats(tier_search_value, adding_time_values, chosen_filename, foldername, check_specific_value, specific_value, all_words, subfolders):
        
        """
        Write statistics to a CSV file.

        Parameters:
        - tier_search_value (str): The ID of the tier to search for.
        - adding_time_values (bool): Whether to include time values in the CSV file.
        - chosen_filename (str): The name of the output CSV file.
        - foldername (str): The name of the folder containing the input files.
        - check_specific_value (bool): Whether to search for a specific value in the tier.
        - specific_value (str): The value to search for in the tier.
        - all_words (bool): Whether to count each word separately.
        - subfolders (bool): Whether to search subfolders for input files.
        """
             
        # Base variables
        dict_result = {}
        dict_stats = {}
        number_items = 0
        if (subfolders):
            folder_path = f'{foldername}/**/*.eaf'
        else:
            folder_path = f'{foldername}/*.eaf'
        name = f'{foldername}/{chosen_filename}.csv'
        # Check if file is already open
        try:
            wcsv.create_csv(name)
        except:
            print("Error file is opened")
            return False

        # Looping through each file
        for filepath in glob.iglob(folder_path, recursive=True):
            # Getting specific name of the file
            filename = Path(filepath).stem
            wcsv.write_filename(name, filename)
            tree = ET.parse(filepath)
            root = tree.getroot()
            # Preparing a temp dictionary to write values for each individual file
            tmp_dic = {}
            tmp_number_item = 0
            slots_dic = {}
            # Temporary dictionary for time values
            timestamp_value = {}
            # Dictionaries for start and end values
            start_end_dic = {}
            for child in root.findall('TIME_ORDER'):
                for time_slot in child:
                    slots_dic[time_slot.attrib['TIME_SLOT_ID']
                            ] = time_slot.attrib['TIME_VALUE']

        # Looping through each child, looking for specific tier
            for child in root.findall('TIER'):
                type = child.get('TIER_ID')
                if type == tier_search_value:                  
                    for subchild in child:
                        #Looking for specific value in tier
                        if check_specific_value:
                            if specific_value.lower() not in subchild[0][0].text.lower():
                                continue
                        # Adding time values
                        if adding_time_values:
                            try:
                                # Getting the timestamp values
                                timestamp1 = subchild[0].attrib['TIME_SLOT_REF1']
                                timestamp2 = subchild[0].attrib['TIME_SLOT_REF2']
                                value1 = int(slots_dic.get(timestamp1))
                                value2 = int(slots_dic.get(timestamp2))
                                timevalue = value2 - value1
                                # Updating the dictionary for time values
                                timestamp_value[subchild[0][0].text] = timestamp_value.get(
                            subchild[0][0].text, 0) + timevalue
                                start_end_dic[subchild[0][0].text] = start_end_dic.get(
                            subchild[0][0].text, "") + (f"Start time: {WriteStats.convert_time(value1)} - End time: {WriteStats.convert_time(value2)}. ")

                            except:
                                print('Error')

                        if (all_words):
                            for word in subchild[0][0].text.split():
                                dict_result[word] = dict_result.get(
                                    subchild[0][0].text, 0) + 1
                                tmp_dic[word] = tmp_dic.get(
                                    word, 0) + 1
                                number_items += 1
                                tmp_number_item += 1
                        else:
                            dict_result[subchild[0][0].text] = dict_result.get(
                                subchild[0][0].text, 0) + 1
                            tmp_dic[subchild[0][0].text] = tmp_dic.get(
                                subchild[0][0].text, 0) + 1
                            number_items += 1
                            tmp_number_item += 1
            # Writing names of columns
            wcsv.write_headers(name, adding_time_values)

            # Counter for looping through the array of time values while looping through dictionary
            count = 0
            # Looping through the temp dictionary to write values in .csv
            for item in tmp_dic:
                key = item
                value = tmp_dic[item]
                percentage = f"{round((value / tmp_number_item) * 100, 2)}%"
                if adding_time_values:
                    # Get time value of item, can use the same logic 
                    # since the dictionaries use the same keys and structure
                    start_end_values = start_end_dic[item]
                    time_value = int(timestamp_value[item]) / 1000
                    time_value_date = time.strftime('%H:%M:%S', time.gmtime(time_value))
                    # Get length of the recording/video file
                    max_length = int(list(slots_dic.values())[-1]) / 1000
                    percentage_length = f"{round((time_value / max_length) * 100, 2)}%"
                    wcsv.write_row(name, adding_time_values, key, value, percentage, time_value_date, percentage_length, start_end_values)
                    count += 1
                else:
                    wcsv.write_row(name, adding_time_values, key, value, percentage, False, False)
            # Spacing each file values and results in the .csv
            wcsv.write_spacing(name)

        wcsv.write_headers_total(name)
        # Looping for the total of all files
        for item in dict_result:
            key = item
            value = dict_result[item]
            stat = f"{round((value / number_items) * 100, 2)}%"
            dict_stats[key] = stat
            wcsv.write_total(name, key, value, stat)

    def convert_time(time_to_convert):
        time_value = int(time_to_convert) / 1000
        return  time.strftime('%H:%M:%S', time.gmtime(time_value))

if __name__ == '__main__':
    WriteStats.write_stats()
