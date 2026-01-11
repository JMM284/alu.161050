# Divvy Trips Analysis

## 1. CSV Download
One of the provided URLs (`Divvy_Trips_2220_Q1.zip`) does not work because the URL is invalid. This issue is in the exercise statement, so I skipped this file. The rest of the ZIP files were successfully downloaded, extracted into CSV format, and the original ZIP files were deleted to save disk space.

## 3. Data Exploration
### a. Type of data
The dataset contains information about trips from the Divvy bike-sharing system. Each row represents a single trip and includes data such as start and end times, station names, trip duration, and user type.

### b. Possible analyses
Looking at the available columns, I can perform some analyses:
- Calculate the average trip duration per quarter.
- Find the most used stations for starting and ending trips.
- Compare usage patterns between subscribers and casual users.

### c. Normalization
The data is denormalized, as all the information related to a trip is stored in a single table instead of being split into multiple related tables.

### d. Required preprocessing
Before analyzing the data, I performed the following steps:
- Converting date columns to `datetime` format
- Removing commas from numeric strings to allow mathematical calculations.
- Calculating `tripduration` for the file where this column was missing.


### e. Null values
While exploring the datasets, I identified that there are quite a few null values, but they are very specific to certain columns depending on the file:

* **Demographic data (gender, birthyear):** I detected a lot of nulls, especially in the 2018 and 2019 files. I think that this happens because these are optional fields; "Subscriber" users usually provide them, but "Casual" users likely don't fill this out.
* **Station Data (end_station_name, end_station_id):** In the 2020 Q1 dataset, some isolated nulls appear. I think that this maybe could be an error, possibly due to GPS issues or trips that didn't close properly in the system.


## 4. Mean Trip Duration
The mean trip duration was calculated for each CSV file following this priority:
1. Use the `tripduration` column if it exists.
2. If not, use the `01 - Rental Details Duration In Seconds Uncapped` column.

I used the "01 - Rental Details Duration In Seconds Uncapped" column because it contains equivalent information and the trip duration column was missing in that CSV.


## 5. Extra Analysis
Some analysis was performed:
- A simple visualization was created to compare the mean trip duration across quarters.
- The mean trip duration for each quarter is displayed from the `mean_tripulation.csv` file.

![Mean Trip Duration Chart](processed/mean_trip_duration.png)

## 7. Data Delivery
In a real professional scenario, I would organize the delivery of this project as follows:

- First, I would store the original CSV files in a cloud storage service such as AWS S3 to keep immutable backups of the raw data.

- Then, I would load the processed data into a relational database like PostgreSQL, which would allow faster queries and easier analysis.

- Finally, I would make the results available through a dashboard or an API, so business analysts could explore trends without needing direct access to the raw files.