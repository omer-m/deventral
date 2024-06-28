from pydantic import BaseModel
from typing import Dict, List, Optional, Union, List


class CSVUploadResponse(BaseModel):
    filename: str
    data: Dict[str, List]

class NullCount(BaseModel):
    pass

class NullsHigherThan(BaseModel):
    pass

class HighMissingCorrelations(BaseModel):
    pass

class PredictMissings(BaseModel):
    pass

class NullCounts(BaseModel):
    pass

class NullsHigherThans(BaseModel):
    pass

class HighMissingCorrelation(BaseModel):
    pass

class PredictMissings(BaseModel):
    pass

class ExactDuplicates(BaseModel):
    pass

class EntityDuplicates(BaseModel):
    pass

class DuplicateColumns(BaseModel):
    pass

class AnalysisResponse(BaseModel):
    missing_values: Union[
        NullCount, NullsHigherThan, HighMissingCorrelations, PredictMissings
    ]
    duplicate_values: Union[
        ExactDuplicates, EntityDuplicates, DuplicateColumns
    ]

class AnalysisResult(BaseModel):
    missing_values: Optional[Dict[str, Union[NullCounts, NullsHigherThans, HighMissingCorrelation, PredictMissings]]]
    duplicate_values: Optional[Dict[str, Union[ExactDuplicates, EntityDuplicates, DuplicateColumns]]]
