from pathlib import Path
from xml.etree import ElementTree as ElementTree


def batchfile_has_spectral_library_files(batchfile: Path) -> bool:
    tree = ElementTree.parse(batchfile)
    root = tree.getroot()

    for child in root.findall(
        ".//batchstep[@method='io.github.mzmine.modules.io.import_rawdata_all.AllSpectralDataImportModule']"
    ):
        for parameter in child.findall(".//parameter[@name='Spectral library files']"):
            for files in parameter.findall(".//file"):
                return True
    return False


IMPORT_STEPS = [
    "io.github.mzmine.modules.io.import_rawdata_all.AllSpectralDataImportModule",
    "io.github.mzmine.modules.io.import_rawdata_mzml.MSDKmzMLImportModule",
    "io.github.mzmine.modules.io.deprecated_jmzml.MzMLImportModule",
]
EXPORT_STEPS = [
    "io.github.mzmine.modules.io.export_features_sirius.SiriusExportModule",
    "io.github.mzmine.modules.io.export_features_csv.CSVExportModularModule",
    "io.github.mzmine.modules.io.export_features_mgf.AdapMgfExportModule",
    "io.github.mzmine.modules.io.export_features_featureML.FeatureMLExportModularModule",
    "io.github.mzmine.modules.io.export_features_all_speclib_matches.ExportAllIdsGraphicalModule",
]
