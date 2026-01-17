<p align="center"><b>2026-01-16</b></p>

<h1 align="center">📊 Dataset:
  global_freelancers_raw.csv
</h1>
<h2 align="center2>📌 Project Summary: Global Freelancers Data Cleaning</h2>

The Problem: The raw dataset contained over hundreds of thousands of freelancer records with inconsistent formats, missing values, mixed numeric/categorical data, and text irregularities. Columns like Gender, is_active, Age, Hourly Rate, Client Satisfaction, and Rating were messy and unreliable for analysis.

The Fix: I cleaned and standardized the data by:

Harmonizing categorical columns (Gender, is_active)

Converting numeric columns (Age, Hourly Rate, Client Satisfaction, Rating) and handling missing or invalid values safely

Preserving missing data as NaN instead of guessing

Removing symbols, extra characters, and formatting inconsistencies in text and numeric columns

The Result: A fully cleaned, analysis-ready dataset that allows accurate reporting and analysis of freelancer demographics, activity, rates, and client satisfaction. All changes were verified to ensure data integrity.

📁 Repository contains:

raw_data/ → Original messy dataset

cleaned_data/ → Cleaned and standardized CSV

scripts/ → Python cleaning scripts

Before/After examples for quick reference
<hr>

<h3>🧹 Data Cleaning Process:</h3>

First thing first, I loaded the raw data into a CSV reader using <code>pd.read_csv()</code>.  
This allowed me to view the structure of the dataset, understand what values each column contains,
and check the data type of every column in order to identify missing or wrong values.

This step is important because it allows me to visualize the data before applying any cleaning.  
Data cleaning decisions should always be based on what the data actually looks like, not on assumptions.

<hr>

<h3>Cleaning the <code>gender</code> column:</h3>

The <code>gender</code> column contained inconsistent values such as:

<code>F</code>, <code>f</code>, <code>female</code>, <code>FEMALE</code>  
<code>M</code>, <code>m</code>, <code>male</code>, <code>MALE</code>

These values all represent the same two categories, but they were stored in different formats.

What I did:

- All female-related values were changed to <code>Female</code> using <code>.replace()</code>
- All male-related values were changed to <code>Male</code> using <code>.replace()</code>

This ensures consistency and prevents the same gender from being treated as different categories.

<hr>

<h3>Cleaning the <code>is_active</code> column:</h3>

Before changing anything, I inspected the column using <code>.unique()</code> and <code>.value_counts()</code>.  
This was necessary to understand which values exist and how many of each value are present.

Similar to the <code>gender</code> column, this column contained different values representing the same meaning, such as:

- <code>1</code>, <code>Y</code>, <code>yes</code> → active  
- <code>0</code>, <code>N</code>, <code>no</code> → not active  

Using <code>.unique()</code>, I identified all the different values and then standardized them:

- <code>N</code>, <code>0</code>, <code>no</code> → <code>False</code>  
- <code>Y</code>, <code>1</code>, <code>yes</code> → <code>True</code>  

At the end, there were some empty cells.  
These were filled with the value <code>Unknown</code>, since assuming <code>True</code> or <code>False</code>
would not be accurate.

<hr>

<h3>Cleaning the <code>age</code> column:</h3>

The column was forced to be numeric using <code>pd.to_numeric()</code>.  
Any empty values, text, or wrong formats were converted to <code>NaN</code>.

This was done because age should be a number, and it cannot be analyzed or used
for modeling if it is stored as text.  
Using <code>errors='coerce'</code> avoids crashes and safely marks invalid data as missing.

After that, the column was converted to <code>Int64</code>.  
<code>Int64</code> (capital I) was used instead of normal <code>int</code> because regular integers
cannot store missing values, while <code>Int64</code> can represent missing ages as <code>&lt;NA&gt;</code>.

A missing age most likely means the platform did not collect the information
or there was a data collection issue.  
Inventing values would change the truth of the dataset.

<hr>

<h3>Cleaning the <code>hourly_rate (USD)</code> column:</h3>

The <code>hourly_rate (USD)</code> column contained mixed formats.
Some values included currency symbols, text, or other non-numeric characters.

To fix this, I first converted the column to string and removed everything
except numbers and decimal points using:

<code>.astype(str)</code> and <code>.str.replace(r'[^\d.]', '', regex=True)</code>

This step ensures that values like <code>$100</code>, <code>USD 50</code>, or <code>75$</code>
are cleaned and kept only as numeric values.

After cleaning the characters, the column was converted to numeric using
<code>pd.to_numeric()</code> with <code>errors='coerce'</code>.
Any invalid or empty values were safely converted to <code>NaN</code> instead of
causing errors.

The column now has a data type of <code>float64</code>, which is expected since
hourly rates can include decimal values.

Leaving missing values as <code>NaN</code> is intentional.
A missing hourly rate most likely means the freelancer did not provide it
or the platform failed to collect it.
Filling or guessing these values would introduce false information.

After cleaning, I verified the results using:
<code>.dtype</code>, <code>.unique()</code>, <code>.dropna()</code>, and general dataset inspection.

Some freelancers have missing or zero hourly rates.  
If the freelancer is active but the <code>hourly_rate</code> is <code>0</code> or <code>NaN</code>, it likely means they did not earn anything during the period or the platform failed to collect their information.  
Missing values are left as <code>NaN</code> instead of being guessed, to maintain truth in the data.

This principle applies to ratings and other columns as well: **never invent data**, only clean what exists.
<hr>
<h3>Cleaning the <code>client_satisfaction</code> column:</h3>

The <code>client_satisfaction</code> column contained percentages stored as strings,
sometimes with the <code>%</code> symbol, and occasionally missing values.

To clean it:

Removed the <code>%</code> sign from the strings using <code>.str.rstrip('%')</code>.  
   This converts values like <code>'84%'</code> into <code>'84'</code>.

Converted the column to numeric using <code>pd.to_numeric()</code> with <code>errors='coerce'</code>.  
   Any invalid or empty values were converted to <code>NaN</code>.

After this, <code>client_satisfaction</code> is a <code>float64</code> column.  
Missing values were left as <code>NaN</code> because we cannot assume or invent a satisfaction score —  
it reflects that the platform likely did not collect the information.

Finally, I inspected the column using <code>.unique()</code> and <code>.isnull().sum()</code>
to verify the cleaning worked as expected.
<hr>

<h3>Cleaning the <code>rating</code> column:</h3>

The <code>rating</code> column contains freelancer ratings, which are numeric values like 1.0 to 5.0.  

I converted the column to numeric using <code>pd.to_numeric()</code> with <code>errors='coerce'</code>.  
This ensures that any text, empty values, or invalid entries are converted to <code>NaN</code> safely.  

I intentionally did **not fill missing ratings**.  
A missing rating usually means the freelancer has not been rated yet, or was not active.  
Filling it with a default value would introduce false information and distort the dataset.
<br>
<hr>
<br>
<h2 align="center">DIRTY DATA</h2>
<p align="center">
  <img src="https://github.com/Kanco0/pydc2/blob/main/ds10/beforecleaning.png" width="60%">
</p>

<h2 align="center">CLEANED DATA</h2>
<p align="center">
  <img src="https://github.com/Kanco0/pydc2/blob/main/ds10/aftercleaning.png" width="60%">
</p>

