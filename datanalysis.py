from fastapi import FastAPI, HTTPException, File, UploadFile
import pandas as pd
import io
import seaborn as sns
import matplotlib.pyplot as plt
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Configure the static directory for saving plots
os.makedirs("static", exist_ok=True)

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    """
    Upload and analyze CSV for Hostel Management data.
    """
    try:
        # Read CSV content into a DataFrame
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content))

        # Basic Data Overview
        data_overview = {
            "Shape": df.shape,
            "Columns": df.columns.tolist(),
            "Null Values": df.isnull().sum().to_dict(),
            "Data Types": df.dtypes.to_dict()
        }

        # Save CSV for further analysis
        file_path = f"static/{file.filename}"
        df.to_csv(file_path, index=False)

        return {"message": "File uploaded successfully", "overview": data_overview}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@app.get("/eda-summary/")
def eda_summary():
    """
    Perform EDA and generate visualizations for the uploaded data.
    """
    try:
        # Load the previously uploaded file
        file_path = "static/ml.csv"
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="No data file found for analysis")

        df = pd.read_csv(file_path)

        # Example Visualizations
        plots = []

        # Visualization 1: Room Booking Trends
        plt.figure(figsize=(10, 5))
        sns.countplot(data=df, x='room_type', palette='Set2')
        plt.title("Room Booking Distribution")
        plot_path = "static/room_booking_distribution.png"
        plt.savefig(plot_path)
        plt.close()
        plots.append(plot_path)

        # Visualization 2: Booking Revenue
        if 'revenue' in df.columns:
            plt.figure(figsize=(10, 5))
            sns.histplot(df['revenue'], kde=True, bins=20, color='green')
            plt.title("Revenue Distribution")
            plot_path = "static/revenue_distribution.png"
            plt.savefig(plot_path)
            plt.close()
            plots.append(plot_path)

        return {"message": "EDA performed successfully", "plots": plots}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during EDA: {str(e)}")


@app.get("/download-plot/{plot_name}")
def download_plot(plot_name: str):
    """
    Download generated plots by name.
    """
    plot_path = f"static/{plot_name}"
    if os.path.exists(plot_path):
        return FileResponse(plot_path)
    else:
        raise HTTPException(status_code=404, detail="Plot not found")
