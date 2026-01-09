# Divvy Trips Analysis

## 1. CSV Download
One of the provided URLs (`Divvy_Trips_2220_Q1.zip`) does not work because the URL is invalid. This issue is already mentioned in the exercise statement, so I skipped this file. The rest of the ZIP files were successfully downloaded, extracted into CSV format, and the original ZIP files were deleted to save disk space.

## 3. Data Exploration
### a. Type of data
The dataset contains information about trips from the Divvy bike-sharing system. Each row represents a single trip and includes data such as start and end times, station names, trip duration, and user type.

### b. Possible analyses
Looking at the available columns, I can perform several analyses:
- Calculate the average trip duration per quarter.
- Find the most used stations for starting and ending trips.
- Compare usage patterns between subscribers and casual users.

### c. Normalization
The data is denormalized, as all the information related to a trip is stored in a single table instead of being split into multiple related tables.

### d. Required preprocessing
Before analyzing the data, I performed the following steps:
- Converting date columns to `datetime` format.
- Calculating `tripduration` for the files where the column was missing only one.

### e. Null values
While exploring the datasets, I identified that there are quite a few null values, but they are very specific to certain columns depending on the file:

* **Demographic data (gender, birthyear):** I detected a huge amount of nulls, especially in the 2018 and 2019 files. I believe this happens because these are optional fields; "Subscriber" users usually provide them, but "Casual" users likely don't fill this out.
* **Station Data (end_station_name, end_station_id):** In the 2020 Q1 dataset, some isolated nulls appear. I believe this is a technical synchronization error, possibly due to GPS issues or "ghost trips" that didn't close properly in the system.

The critical time columns have no nulls, so the mean calculations in my `processor.py` script are reliable.

## 4. Mean Trip Duration
The mean trip duration was calculated for each CSV file following this priority:
1. Use the `tripduration` column if it exists.
2. If not, use the `01 - Rental Details Duration In Seconds Uncapped` column.
3. If neither exists, calculate it using the `started_at` and `ended_at` timestamps.

## 5. Extra Analysis
- A simple visualization was created to compare the mean trip duration across quarters.
- The results are saved as a summary CSV in the `processed` folder.

## 7. Data Delivery
If I had to deliver this project in a professional environment, I would follow these steps:
- Store original CSVs in a cloud storage system like AWS S3 for immutable backups.
- Load the processed data into a SQL database (PostgreSQL or Snowflake) for efficient querying by other departments.
- Expose the results through an API or a Dashboard (Tableau/PowerBI) so business analysts can see trends without accessing raw data.