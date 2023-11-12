# Sirius CSI:FingerID
{bdg-success}`COMPOUND TOOL`

## Functionality
Predict molecular fingerprint from MS/MS and fragmentation trees for each
compound individually using CSI:FingerID fingerprint prediction.

## Options

| Option           | Description                                                                                                              |
|------------------|--------------------------------------------------------------------------------------------------------------------------|
| `-h, --help`     | Show this help message and exit.                                                                                         |
| `--no-threshold` | Disable score threshold for formula candidates. CSI: FingerID fingerprints will be predicted for all formula candidates. |
| `-V, --version`  | Print version information and exit.                                                                                      |

## Follow-up commands

- [`structure, search-structure-db`](sirius_structure) Search in molecular structure db for each compound individually using CSI: FingerID structure database search.
- `canopus, compound-classes` - Predict compound categories for each compound individually based on its predicted molecular fingerprint (CSI: FingerID) using CANOPUS.
- [`write-summaries, W`](sirius_export)   - Write Summary files from a given project-space into the given project-space or a custom location.
