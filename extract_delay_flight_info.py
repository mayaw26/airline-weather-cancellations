import pandas as pd


# # read file
# merged_data = pd.read_csv("merged_flight_weather.csv")

# # check columns first
# print(merged_data.columns)

# # remove destination-related columns
# merged_data = merged_data.drop(columns=[
#     "destination",
#     "destination_tavg",
#     "destination_tmin",
#     "destination_tmax",
#     "destination_prcp",
#     "destination_snow",``
#     "destination_wspd",
#     "destination_pres"
# ])

# # check result
# print(merged_data.columns)
# print(merged_data.head())

# # save cleaned file
# merged_data.to_csv("merged_flight_weather_no_destination.csv", index=False)



# delay data
flights = pd.read_csv("flight_data_2024.csv")
print(flights["cancelled"].value_counts())


flights_no_cancelled = flights[flights["cancelled"] == 0]

flights_no_cancelled.to_csv("flight_data_2024_no_cancelled.csv", index=False)

flights = pd.read_csv("flight_data_2024_no_cancelled.csv")
flights = flights[["op_unique_carrier", "fl_date", "origin"]]

print(flights.head())
print(flights.columns)

#rename 
flights = flights.rename(columns={
    "op_unique_carrier": "airline",
    "fl_date": "date"
})

# to datetime
flights["date"] = pd.to_datetime(flights["date"])

#check result
print(flights.head())
print(flights.shape)

# keep only wanted airlines and origins
wanted_airlines = ["AA", "AS", "NK", "F9"]
wanted_origins = ["BOS", "DFW", "EWR", "LGA", "ORD", "SFO"]

flights = flights[
    (flights["airline"].isin(wanted_airlines)) &
    (flights["origin"].isin(wanted_origins))
]

# # convert date to datetime
# flights["date"] = pd.to_datetime(flights["date"])

weather = pd.read_csv("merged_flight_weather_no_destination.csv")

# make sure weather date is datetime too
weather["date"] = pd.to_datetime(weather["date"])

# check keys before merging
print(weather[["date", "airline", "origin"]].head())
print(flights[["date", "airline", "origin"]].head())

# merge cleaned flights to weather file
final_data = pd.merge(
    flights,
    weather,
    on=["date", "origin", "airline"],
    how="left"
)

# check result
print(final_data.head())
print(final_data.shape)
print(final_data.isna().sum())

# save final merged file
final_data.to_csv("final_flight_weather_dataset.csv", index=False)