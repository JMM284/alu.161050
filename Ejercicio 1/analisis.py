import pandas as pd
import matplotlib.pyplot as plt
import os


processed_dir = "processed"
file_path = os.path.join(processed_dir, "mean_tripulation.csv")

df = pd.read_csv(file_path)

print(df)

plt.figure()
plt.bar(df["archivo"], df["duracion_media_segundos"])
plt.xticks(rotation=45)
plt.xlabel("CSV file (quarter)")
plt.ylabel("Mean trip duration (seconds)")
plt.title("Mean trip duration per quarter")

plt.tight_layout()
plt.savefig(os.path.join(processed_dir, "mean_trip_duration.png"))
plt.show()
