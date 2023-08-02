from src.models.preprocessingConstants import *
from src.utils.manipulateData import *


# Messy architecture, shouldn't be importing from utils, but I'm working fast atm


# Formula for VSP from: https://doi.org/10.1016/j.trd.2017.05.016
# Formula for VSP mode pollutants: https://doi.org/10.1016/j.trd.2006.06.005


def addVspToDataFrame(df: pd.DataFrame):
    v = df[SPEED_COLUMN]
    a = df[ACCELERATION_COLUMN]
    grade = df[GRADE_COLUMN]
    df[VSP_COLUMN] = v * (1.1 * a + 9.81 * np.sin(np.arctan(grade)) + 0.132) + 0.000302 * v**3
    return df

def computeVspMode(vsp: float):
    vsp_ranges = [-2, 0, 1, 4, 7, 10, 13, 16, 19, 23, 28, 33, 39]
    for i, upper_limit in enumerate(vsp_ranges):
        if vsp < upper_limit:
            return i + 1
    return 14

def addVspModeToDataFrame(df: pd.DataFrame):
    df[MODE_COLUMN] = df[VSP_COLUMN].apply(computeVspMode)
    return df

def importModelFromCSV(model: str):
    '''

    :param model: name of the csv with model, eg "Coelho2006" for Coelho2006.csv
    :return:
    '''

    MODEL_PATH = os.path.join(PATH_TO_MODELS,f"{model}.csv")
    df = pd.read_csv(MODEL_PATH,
                     #NB : Path here could be refactored
                     usecols=[MODE_COLUMN,
                              NOx_COLUMN,
                              HC_COLUMN,
                              CO2_COLUMN,
                              CO_COLUMN]).dropna()
    return df

def addPollutantsToDataFrame(data_df: pd.DataFrame, model_df: pd.DataFrame):
    # Note: could be refactored with pollutant columns given in entry (projectVariables)
    data_df = data_df.merge(model_df[[MODE_COLUMN, CO2_COLUMN, NOx_COLUMN, HC_COLUMN, CO_COLUMN]], on=MODE_COLUMN, how='left')

    return data_df