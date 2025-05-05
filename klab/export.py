from enum import Enum
from exceptions import *

class Export(Enum):
    '''
    Data that can be exported
    '''
    STRUCTURE = "structure"
    DATA = "data"
    VIEW = "view"
    LEGEND = "legend"
    REPORT = "report"
    DATAFLOW = "dataflow"
    PROVENANCE_FULL = "provenance_full"
    PROVENANCE_SIMPLIFIED = "provenance_simplified"


class ExportFormat(Enum):
    '''
    Formats to export results from k.LAB to disk.
    '''
    PNG_IMAGE = ("image/png", [Export.DATA, Export.LEGEND, Export.VIEW])
    GEOTIFF_RASTER = ("image/tiff", [Export.DATA])
    GEOJSON_FEATURES = ("application/json", [Export.DATA])
    JSON_CODE = ("application/json", [Export.LEGEND, Export.STRUCTURE])
    KDL_CODE = ("text/plain", [Export.DATAFLOW])
    KIM_CODE = ("text/plain", [Export.PROVENANCE_FULL, Export.PROVENANCE_SIMPLIFIED])
    ELK_GRAPH_JSON = ("application/json", [Export.DATAFLOW, Export.PROVENANCE_FULL, Export.PROVENANCE_SIMPLIFIED])
    CSV_TABLE = ("text/csv", [Export.VIEW])
    PDF_DOCUMENT = ("application/pdf", [Export.REPORT])
    EXCEL_TABLE = ("application/vnd.ms-excel", [Export.VIEW])
    WORD_DOCUMENT = ("application/vnd.openxmlformats-officedocument.wordprocessingml.document", [Export.REPORT])
    BYTESTREAM = ("application/octet-stream", [Export.DATA])

    def getMediaType(self) -> str:
        return self.value[0]
    
    def isText(self) -> bool:
        mt = self.value[0]
        return "text/plain" == mt or "application/json" == mt or "text/csv" == mt
    
    def isExportAllowed(self, export: Export) -> bool:
        allowedList = self.value[1]
        return export in allowedList
    
    def __str__(self) -> str:
        return f"{self.value[0]}"

    @staticmethod
    def fromMediaType(value: str):
        if not value:
            return None
        for ef in ExportFormat:
            if ef.value.lower() == value.lower():
                return ef
        raise KlabIllegalArgumentException(f"No ExportFormat available by the value: {value}")

    @staticmethod
    def fromMediaTypeList(value: list):
        efl = []
        for v in value:
            ef = ExportFormat.fromValue(v)
            if ef:
                efl.append(ef)
            
        return efl