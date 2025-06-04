# school_data.py
# AUTHOR: Behzad Fuladpanjeh Hojaghan
#
# A terminal-based application for computing and printing statistics based on given input.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc. 
# You may import any modules from the standard Python library.
# Remember to include docstrings and comments.


import numpy as np
import csv
from given_data import year_2013, year_2014, year_2015, year_2016, year_2017, year_2018, year_2019, year_2020, year_2021, year_2022

# Declare any global variables needed to store the data here
data = np.array([
        year_2013, year_2014, year_2015, year_2016, year_2017,
        year_2018, year_2019, year_2020, year_2021, year_2022
    ]).reshape(10, 20, 3)

# You may add your own additional classes, functions, variables, etc.
def load_school_mapping(csv_path):

    schools = {}
    with open(csv_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            code = row.get("School Code")
            name = row.get("School Name")
            if code and name:
                code = int(code.strip())
                if code not in schools:
                    schools[code] = name.strip()
    # Sort by school code and return list of tuples
    sorted_schools = sorted(schools.items())
    return sorted_schools

def get_school_index(code, sorted_school_list):

    for index, (school_code, school_name) in enumerate(sorted_school_list):
        if school_code == code:
            return index, school_name
    raise ValueError("School code not found in dataset.")


def print_school_stats(school_idx, school_name, school_code):
    """Prints stats for a given school."""
    subarray = data[:, school_idx, :]  # subarray view to extract a (10, 3) view

    print(f"\nSchool Name: {school_name}, School Code: {school_code}")


    for grade in range(3):
        mean_val = int(np.nanmean(subarray[:, grade]))
        print(f"Mean enrollment for Grade {10 + grade}: {mean_val}")

    print(f"\nHighest enrollment for a single grade: {int(np.nanmax(subarray))}")
    print(f"Lowest enrollment for a single grade: {int(np.nanmin(subarray))}")

    for i, year in enumerate(range(2013, 2023)):
        total = int(np.nansum(subarray[i]))
        print(f"Total enrollment for {year}: {total}")

    ten_year_total = int(np.nansum(subarray))
    mean_total = int(np.floor(ten_year_total / 10))
    print(f"Total ten year enrollment: {ten_year_total}")
    print(f"Mean total enroll,emt over 10 years: {mean_total}")

    over_500 = subarray[subarray > 500] # Masking operation to filter values > 500
    if over_500.size > 0:
        median = int(np.nanmedian(over_500))
        print(f"For all enrollments over 500, the median value was: {median}")
    else:
        print("No enrollments over 500.")

def print_general_stats():
    """Prints statistics for all schools and years."""
    print(f"Mean enrollment in 2013: {int(np.nanmean(data[0]))}")
    print(f"Mean enrollment in 2022: {int(np.nanmean(data[9]))}")
    print(f"Total graduating class of 2022: {int(np.nansum(data[9, :, 2]))}")
    print(f"Highest enrollment for a single grade: {int(np.nanmax(data))}")
    print(f"Lowest enrollment for a grade: {int(np.nanmin(data))}")

def main():
    print("ENSF 692 School Enrollment Statistics")
    print(f"\nShape of full data array: {data.shape}")
    print(f"Dimensions of full data array: {data.ndim}")
    # Print Stage 1 requirements here
    # Create 3D array: (years, schools, grades)


    # Prompt for user input

    # Print Stage 2 requirements here
    school_list = load_school_mapping("Assignment3Data.csv")

    try:
        user_input = input("\nEnter a valid school code (e.g., 1224): ").strip()
        school_code = int(user_input)
        index, name = get_school_index(school_code, school_list)

        print("\n***Requested School Statistics***")
        print_school_stats( index, name, school_code)

    except ValueError as e:
        print(f"Error: {e}")
        return


    # Print Stage 3 requirements here
    print("\n***General Statistics for All Schools***\n")
    print_general_stats()

if __name__ == '__main__':
    main()

