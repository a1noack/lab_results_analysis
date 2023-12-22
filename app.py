import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


# ========== Load the data ==========
filename = "lab_results/Lab results master sheet.xlsx"
dfs = pd.read_excel(filename, sheet_name=None)
df = dfs['Sheet1']  # get "Sheet1" (there's only one sheet for now)
df.head()


# ========== Get data into correct format ==========
columns = df.columns
test_datetimes = columns[5:]
test_dates = [d.split(':')[0] for d in test_datetimes]

data = {"Date": test_dates}
for i, row in df.iterrows():
    test_name = row['Test Name']
    values = []
    for test_datetime in test_datetimes:
        values.append(row[test_datetime])
    data[test_name] = values

df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])


# ========== Build Streamlit app ==========
st.title("Blood Marker Analysis")

# Dropdown menu for selecting a blood marker
option = st.selectbox("Select a Blood Marker", df.columns[1:])

# Plotting
fig, ax = plt.subplots()
ax.plot(df['Date'], df[option], marker='o', linestyle='-')
ax.set_title(f"{option} over Time")
ax.set_xlabel("Date")
ax.set_ylabel(option)
ax.grid(True)

st.pyplot(fig)