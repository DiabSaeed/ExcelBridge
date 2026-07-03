import pandas as pd
from typing import Dict, List, Any
class DataController:
    
    def process_downloaded(self, df: pd.DataFrame):
        
        try:
            json_result = df.to_dict(orient="records")
            return json_result
        except Exception as e:
            raise ValueError(f"Error processing uploaded data: {str(e)}")
    def process_uploaded(self, response: List[Dict[str,Any]]):
        
        try:
            df = pd.DataFrame(response)
            return df
        except Exception as e:
            raise ValueError(f"Error processing uploaded data: {str(e)}")
    