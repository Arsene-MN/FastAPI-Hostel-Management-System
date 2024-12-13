# FastAPI Hostel Management App

This is backend for a hostel management system built using FastAPI. Has features like CRUD as well as data manipulation capabilities for Machine Learning. Test with Postman at:<br>
*/hostels*  
*/rooms*  
*/bookings*

## Installation

Clone the repo using:
```bash
git clone https://github.com/Arsene-MN/FastAPI-Hostel-Management-System.git
```
Create a virtual environment.
```bash
python -m venv fastapi_env
```
Install Packages.
```bash
pip install -r requirements.txt
```

## Usage

Run the main fastapi application for development and test with Postman.
```bash
fastapi dev
```
Use this to perform various data manipulation operations like *dataframes*, *right joining*, *outer joining*, and others.
```bash
python dataops.py
```
Use this to generate around 500,000 records using [_faker_](https://fakerjs.dev) to get more data for efficient machine learning development.
```bash
python gendata.py
```
## Further data manipulation

To change data from one API into a csv file, split the csv file into two and rejoin them. Check in *splitdata.py* and uncomment based on which step you are on.
```bash
python splitdata.py
```
To take data from two APIs, change them into csv files, remove some columns from each csv file and then join the two csv files into one. Check in *splitwith2.py* and uncomment based on which step you are on.
```bash
python splitwith2.py
```
To read *ml.csv*
```bash
python readml.py
```
To analyse data from *ml.csv* and visualize it.
```bash
python datanalysis.py
```
Use Jupyter to open *ExploratoryDataAnalysis.ipynb* for even further data visualization and manipulation of ml.csv
