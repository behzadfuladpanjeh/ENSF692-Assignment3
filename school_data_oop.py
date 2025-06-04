# school_data.py
# AUTHOR: Behzad Fuladpanjeh Hojaghan
#
# A terminal-based application for computing and printing statistics based on given input.

import numpy as np
import csv
from given_data import year_2013, year_2014, year_2015, year_2016, year_2017, year_2018, year_2019, year_2020, year_2021, year_2022


class SchoolData:
    """Handles the enrollment data and statistics operations."""

    def __init__(self):
        self.data = np.array([year_2013, year_2014, year_2015, year_2016, year_2017,
            year_2018, year_2019, year_2020, year_2021, year_2022]).reshape(10, 20, 3)

    def get_school_subarray(self, index):
        """Returns the subarray for a school by index."""
        return self.data[:, index, :]

    def print_general_stats(self):
        """
        Prints statistics for all schools and years.

        Parameters:
        data (np.ndarray): 3D enrollment array with shape (10, 20, 3).
        """
        print(f"Mean enrollment in 2013: {int(np.nanmean(self.data[0]))}")
        print(f"Mean enrollment in 2022: {int(np.nanmean(self.data[9]))}")
        print(f"Total graduating class of 2022: {int(np.nansum(self.data[9, :, 2]))}")
        print(f"Highest enrollment for a single grade: {int(np.nanmax(self.data))}")
        print(f"Lowest enrollment for a grade: {int(np.nanmin(self.data))}")

class SchoolMapper:
    def __init__(self, csv_path):
        self.schools = self._load_school_mapping(csv_path)

    def _load_school_mapping(self,csv_path):
        """
        Reads the CSV file and returns a list of (code, name) sorted by school code.

        Returns:
            list of tuples: [(school_code, school_name), ...] sorted by code
        """
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

    def get_school_index(self, code):
        """
        Gets the index of a school using a list of school codes.

        Parameters:
            code (int): School code input by the user


        Returns:
            tuple: (index in school array, school name)

        Raises: ValueError if code is invalid
        """

        for index, (school_code, school_name) in enumerate(self.schools):
            if school_code == code:
                return index, school_name
        raise ValueError("School code not found in dataset.")

class SchoolStats:
    def __init__(self, school_data:SchoolData):
        self.data = school_data
    def print_school_stats(self, school_idx, school_name, school_code):
        """
        Prints detailed enrollment statistics for a single school over a ten-year period.

        Parameters:
            school_idx (int): Index of the school in the data array.
            school_name (str): Name of the school.
            school_code (int): Code of the school.
        """
        subarray = self.data.get_school_subarray(school_idx)  # subarray view to extract a (10, 3) view

        print(f"\nSchool Name: {school_name}, School Code: {school_code}")

        # Print average enrollment per grade
        for grade in range(3):
            mean_val = int(np.nanmean(subarray[:, grade]))
            print(f"Mean enrollment for Grade {10 + grade}: {mean_val}")
        # Print overall highest and lowest grade enrollments for this school
        print(f"\nHighest enrollment for a single grade: {int(np.nanmax(subarray))}")
        print(f"Lowest enrollment for a single grade: {int(np.nanmin(subarray))}")

        # Print total enrollment per year
        for i, year in enumerate(range(2013, 2023)):
            total = int(np.nansum(subarray[i]))
            print(f"Total enrollment for {year}: {total}")

        # Compute and print ten-year total and mean
        ten_year_total = int(np.nansum(subarray))
        mean_total = int(np.floor(ten_year_total / 10))
        print(f"Total ten year enrollment: {ten_year_total}")
        print(f"Mean total enrollment over 10 years: {mean_total}")

        over_500 = subarray[subarray > 500] # Masking operation to filter values > 500
        if over_500.size > 0:
            median = int(np.nanmedian(over_500))
            print(f"For all enrollments over 500, the median value was: {median}")
        else:
            print("No enrollments over 500.")



def main():
    """
    Main entry point for the program.
    Handles user input and coordinates the display of requested statistics.
    """
    print("ENSF 692 School Enrollment Statistics")

    # Print Stage 1 requirements here

    school_data = SchoolData()
    school_mapper = SchoolMapper("Assignment3Data.csv")
    printer = SchoolStats(school_data)

    print(f"\nShape of full data array: {school_data.data.shape}")
    print(f"Dimensions of full data array: {school_data.data.ndim}")
    # Prompt for user input

    # Print Stage 2 requirements here


    try:
        user_input = input("\nEnter a valid school code (e.g., 1224): ").strip()
        school_code = int(user_input)
        index, name = school_mapper.get_school_index(school_code)

        print("\n***Requested School Statistics***")
        printer.print_school_stats(index, name, school_code)

    except ValueError as e:
        print(f"Error: {e}")
        return


    # Print Stage 3 requirements here
    print("\n***General Statistics for All Schools***\n")
    school_data.print_general_stats()

if __name__ == '__main__':
    main()

