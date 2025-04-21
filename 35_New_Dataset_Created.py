import pandas as pd
import numpy as np
import re
from datetime import datetime, timedelta
from Summarizing_Current_Dataset import summarize_dataset

# Step 1: Create new time_stamp values from "3/6/2019 00:00:00 AM" to "3/6/2019 11:59:59 PM"
start_time = datetime(2019, 3, 6, 0, 0, 0)  # "3/6/2019 00:00:00 AM"
end_time = datetime(2019, 3, 6, 23, 59, 59)  # "3/6/2019 11:59:59 PM"
time_stamps = pd.date_range(start=start_time, end=end_time, freq='S')

# Define the file path
file_path = r'continuous_factory_process.csv'

# Step 2: Generate new data based on min/max values
min_max_values = summarize_dataset(file_path)
new_data = {}

# Define raw material properties data based on time slots
def get_material_properties(timestamp):
    hour = timestamp.hour
    if 0 <= hour < 6:
        return {
            "Machine1": [11.54, 200, 1027.43, 247],
            "Machine2": [12.59, 236, 601.11, 257],
            "Machine3": [9.02, 186, 421.16, 204],
        }
    elif 6 <= hour < 12:
        return {
            "Machine1": [12.9, 215, 980.53, 251],
            "Machine2": [12.59, 236, 601.11, 257],
            "Machine3": [9.02, 186, 421.16, 204],
        }
    elif 12 <= hour < 18:
        return {
            "Machine1": [12.59, 236, 601.11, 257],
            "Machine2": [12.85, 241, 556.7, 256],
            "Machine3": [9.86, 192, 408.97, 202],
        }
    else:
        return {
            "Machine1": [12.22, 201, 1048.06, 252],
            "Machine2": [12.85, 241, 556.7, 256],
            "Machine3": [8.83, 221, 433.18, 205],
        }

def generate_custom_distribution(size, ranges, percentages):
    values = []
    for r, p in zip(ranges, percentages):
        count = int(size * p)
        values.extend(np.random.uniform(r[0], r[1], count))
    np.random.shuffle(values)
    return np.array(values[:size])

for i, (column, (min_val, max_val)) in enumerate(min_max_values.items()):
    if column == "Machine1.RawMaterialFeederParameter.U.Actual":
        new_data[column] = generate_custom_distribution(len(time_stamps), [(1200, 1250), (800, 1000), (1251, 1350), (200, 799)], [0.9, 0.1, 0.05, 0.05])
        
    elif column in ["Machine2.RawMaterialFeederParameter.U.Actual", "Machine3.RawMaterialFeederParameter.U.Actual"]:
        new_data[column] = generate_custom_distribution(len(time_stamps), [(200, 230), (231, 266), (0, 199)], [0.9, 0.05, 0.05])
        
    elif column == "FirstStage.CombinerOperation.Temperature1.U.Actual":
        new_data[column] = generate_custom_distribution(len(time_stamps), [(99, 110), (111, 118), (min_val, 99)], [0.6, 0.3, 0.1])
        
    elif column == "FirstStage.CombinerOperation.Temperature2.U.Actual":
        new_data[column] = generate_custom_distribution(len(time_stamps), [(99, 110), (111, 118), (min_val, 99)], [0.3, 0.6, 0.1])
        
    elif re.match(r"^Machine\d+\.RawMaterial\.Property\d+$", column):
        machine_number, property_number = re.findall(r"Machine(\d+)\.RawMaterial\.Property(\d+)", column)[0]
        machine_number = int(machine_number)
        property_number = int(property_number)
        
        values = [get_material_properties(ts)[f"Machine{machine_number}"][property_number - 1] for ts in time_stamps]
        new_data[column] = values
    
    elif re.match(r"^Stage1\.Output\.Measurement\d+\.U\.Actual$", column):
        if column == "Stage1.Output.Measurement0.U.Actual":
            new_data[column] = generate_custom_distribution(len(time_stamps), [(12, 12.5), (12.6, 13), (13.1, 20)], [0.8, 0.15, 0.05])
        else:
            total_values = len(time_stamps)
            num_majority = int(0.95 * total_values)
            num_zeros = int(0.01 * total_values)
            num_max_value = int(0.02 * total_values)
            num_negative = int(0.02 * total_values)

            majority_values = np.random.uniform(max_val - 0.5, max_val + 0.5, num_majority)
            zeros = np.zeros(num_zeros)
            max_value_approx = np.full(num_max_value, max_val)
            negative_values = np.random.uniform(min_val, 0, num_negative)

            combined_values = np.concatenate([majority_values, zeros, max_value_approx, negative_values])
            np.random.shuffle(combined_values)
            new_data[column] = combined_values
    
    elif re.match(r"^Stage2\.Output\.Measurement\d+\.U\.Actual$", column):
        total_values = len(time_stamps)
        values = np.random.uniform(0, max_val + 5, total_values)
        new_data[column] = values
    
    elif "Setpoint" in column:
        # Generate only max_val for all Setpoint values (no zeros)
        new_data[column] = np.full(len(time_stamps), max_val)
    
    elif min_val < 0:
        num_negative = int(0.0005 * len(time_stamps))
        num_positive = len(time_stamps) - num_negative
        negative_values = np.random.uniform(min_val, 0, num_negative)
        positive_values = np.random.uniform(0, max_val, num_positive)
        combined_values = np.concatenate([negative_values, positive_values])
        np.random.shuffle(combined_values)
        new_data[column] = combined_values
    
    else:
        new_data[column] = np.random.uniform(min_val, max_val, len(time_stamps))

new_data_df = pd.DataFrame(new_data)
new_data_df['time_stamp'] = time_stamps

# Add a "No." column at the beginning of the dataset
new_data_df.insert(0, 'No', range(1, len(new_data_df) + 1))

new_data_df.to_csv('data_generated.csv', index=False)
print("Data saved to 'data_generated.csv'.")