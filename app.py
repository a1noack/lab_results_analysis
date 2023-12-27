import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st



# ========== Load the data ==========
filename = "lab_results/Lab results master sheet.xlsx"
dfs = pd.read_excel(filename, sheet_name=None)
df_orig = dfs['Sheet1']  # get "Sheet1" (there's only one sheet for now)


# ========== Get data into correct format ==========
columns = df_orig.columns
test_datetimes = columns[5:]
test_dates = [d.split(':')[0] for d in test_datetimes]

data = {"Date": test_dates}
for i, row in df_orig.iterrows():
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
ref_range_lower = df_orig.loc[df_orig['Test Name'] == option, 'Ref. Range Lower'].values[0]
ref_range_upper = df_orig.loc[df_orig['Test Name'] == option, 'Ref. Range Upper'].values[0]

# Plotly plot
fig = px.line(df, x='Date', y=option, markers=True, title=f"{option} over Time")
fig.update_traces(mode='markers+lines', hoverinfo='text+name', text=df[option])
fig.update_layout(hovermode='x unified')

# make sure max and min values are covered in range
readings = [r for r in list(df[option]) if not np.isnan(r)]
min_y = min(min(readings), ref_range_lower)
max_y = max(max(readings), ref_range_upper)

# Adding horizontal lines for reference values
if not np.isnan(ref_range_lower):
    fig.add_hline(y=ref_range_lower, line_dash="dash", line_color="red")
if not np.isnan(ref_range_upper):
    fig.add_hrect(y0=ref_range_lower, y1=ref_range_upper, line_width=0, fillcolor="green", opacity=0.2)
    fig.add_hline(y=ref_range_upper, line_dash="dash", line_color="red")

# Adjusting y-axis limits
buffer = 0.4 * (max_y - min_y)  # 10% buffer above and below the reference range
fig.update_yaxes(range=[min_y - buffer, max_y + buffer])

# Calculate differences between consecutive values
percent_diffs = [(readings[i+1] - readings[i]) / readings[i] for i in range(len(readings) - 1)]
percent_diffs = [p*100 for p in percent_diffs]

for i in range(len(percent_diffs)):
    st.text(f"Percent difference between readings {i} and {i+1}: {percent_diffs[i]:.2f}%")

st.plotly_chart(fig)