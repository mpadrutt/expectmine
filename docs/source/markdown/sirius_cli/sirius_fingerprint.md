# CSI: FingerID fingerprint (`fingerprint`)

<COMPOUND_TOOL> Predict molecular fingerprint from MS/MS and fragmentation trees for each compound individually using CSI:FingerID fingerprint prediction.

| Option           | Description                                                                                                              |
|------------------|--------------------------------------------------------------------------------------------------------------------------|
| `-h, --help`     | Show this help message and exit.                                                                                         |
| `--no-threshold` | Disable score threshold for formula candidates. CSI: FingerID fingerprints will be predicted for all formula candidates. |
| `-V, --version`  | Print version information and exit.                                                                                      |

## Commands

- `structure, search-structure-db` - <COMPOUND_TOOL> Search in molecular structure db for each compound individually using CSI: FingerID structure database search.
- `canopus, compound-classes` - <COMPOUND_TOOL> Predict compound categories for each compound individually based on its predicted molecular fingerprint (CSI: FingerID) using CANOPUS.
- `write-summaries, W` - <STANDALONE, POSTPROCESSING> Write Summary files from a given project-space into the given project-space or a custom location.
