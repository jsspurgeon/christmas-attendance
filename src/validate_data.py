import pandas as pd
import logging
import yaml
from pydantic import BaseModel, ValidationError, validator, constr
from typing import Optional
import math

# configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# Load the attendance data source from the config.yml file
with open("./src/config.yml", "r") as file:
    config = yaml.safe_load(file)

class AttendanceModel(BaseModel):
    Activity_Type_Description: Optional[constr(strip_whitespace=True)] = None
    Activity_Type_ID: int
    Create_Date_Time: Optional[constr(strip_whitespace=True)] = None
    Data_Entry_Method: Optional[constr(strip_whitespace=True)] = None
    Data_Entry_Method_ID: Optional[float] = None
    Data_Entry_Person: Optional[constr(strip_whitespace=True)] = None
    Entry_Note: Optional[constr(strip_whitespace=True)] = None
    Entry_Type_Description: Optional[constr(strip_whitespace=True)] = None
    Entry_Value: int
    EntryType_ID: int
    Metric_Name: Optional[constr(strip_whitespace=True)] = None
    Ministry_Description: Optional[constr(strip_whitespace=True)] = None
    Ministry_ID: int
    New_Attendance_Tracker_ID: int
    Service_Date: Optional[constr(strip_whitespace=True)] = None
    Service_Date_ID: int
    Service_Date_Time: Optional[constr(strip_whitespace=True)] = None
    Service_Description: Optional[constr(strip_whitespace=True)] = None
    Service_ID: int
    Service_Instance_ID: Optional[float] = None
    Service_Time: Optional[constr(strip_whitespace=True)] = None
    Site_Description: Optional[constr(strip_whitespace=True)] = None
    Site_Master_ID: Optional[float] = None

    @validator("*", pre=True, always=True)
    def allow_nan(cls, v):
        if isinstance(v, float) and math.isnan(v):
            return None
        return v


# Import the dataframe
df = pd.read_csv(f"./data/raw/{config['data_source']['attendance']['file_name']}")
df.columns = [col.replace(" ", "_") for col in df.columns]

# Validate the first n rows of the dataframe
df = df.sample(15)

n = 0
for row in df.iterrows():
    row_dict = row[1].to_dict()
    try:
        validated_data = AttendanceModel.validate(row_dict)
    except ValidationError as e:
        logging.info(f"Validation error: {e}")
        n += 1
logging.info("Validation complete:")
logging.info(f"Validation errors: {n}")
