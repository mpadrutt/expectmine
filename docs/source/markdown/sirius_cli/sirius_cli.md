# Sirius CLI Help

## Why this page?
During my development I found it easier to use a markdown based documentation
instead of always using the `--help` command. I thought it might be useful for
someone else.

## General command structure.
```bash
sirius [-hV] [--noCite] [--recompute] [--cores=<numOfCores>]
              [--instance-buffer=<initialInstanceBuffer>] [--log=<logLevel>]
              [--maxmz=<maxMz>] [--workspace=<workspace>]
              [[-o=<outputProjectLocation>] [--no-compression]
              [--update-fingerprint-version]
              [--naming-convention=<projectSpaceFilenameFormatter>]]
              [[-i=<inputPath>[,<inputPath>...] [-i=<inputPath>[,
              <inputPath>...]]... [--ignore-formula] [--allow-ms1-only]]
              [-z=<parentMz> [--adduct=<ionType>] [-f=<formula>] -2=<ms2File>[,
              <ms2File>...] [-1=<ms1File>[,<ms1File>...]]]...] [COMMAND]
```
### Options


| Command                                                                                 | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|-----------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| -h, --help                                                                              | Show this help message and exit.                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| -V, --version                                                                           | Print version information and exit.                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| --log, --loglevel=<logLevel>                                                            | Set logging level of the Jobs SIRIUS will execute. Valid values: SEVERE, WARNING, INFO, FINER, ALL. Default: WARNING.                                                                                                                                                                                                                                                                                                                                               |
| --cores, --processors=<numOfCores>                                                      | Number of CPU cores to use. If not specified, Sirius uses all available cores.                                                                                                                                                                                                                                                                                                                                                                                      |
| --instance-buffer, --compound-buffer, --initial-compound-buffer=<initialInstanceBuffer> | Number of compounds that will be loaded into the Memory. A larger buffer ensures that there are enough compounds available to use all cores efficiently during computation. A smaller buffer saves Memory. To load all compounds immediately, set it to -1. Default (numeric value 0): 3 x --cores. Note that for <DATASET_TOOLS> the compound buffer may have no effect because these tools may have to load compounds simultaneously into the memory. Default: 0. |
| --workspace=<workspace>                                                                 | Specify Sirius workspace location. This is the directory for storing property files, logs, databases, and caches. This is NOT for the project-space that stores the results! Default is $USER_HOME/.sirius-<MINOR_VERSION>.                                                                                                                                                                                                                                         |
| --recompute                                                                             | Recompute results of ALL tools where results are already present. Per default, already present results will be preserved, and the instance will be skipped for the corresponding Task/Tool.                                                                                                                                                                                                                                                                         |
| --maxmz=<maxMz>                                                                         | Only consider compounds with a precursor m/z lower or equal [--maxmz]. All other compounds in the input will be skipped. Default: Infinity.                                                                                                                                                                                                                                                                                                                         |
| --noCite, --noCitations, --no-citations                                                 | Do not write summary files to the project-space.                                                                                                                                                                                                                                                                                                                                                                                                                    |

### Specify OUTPUT Project-Space

| Command                                             | Description                                                                                                                                                               |
|-----------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| -o, --output, --project=<outputProjectLocation>     | Specify the project-space to write into. If no [--input] is specified, it is also used as input. For compression use the File ending .zip or .sirius.                     |
| --naming-convention=<projectSpaceFilenameFormatter> | Specify a naming scheme for the compound directories in the project-space. Default % index_%filename_%compoundname.                                                       |
| --no-compression                                    | Does not use compressed project-space format (not recommended) when creating the project-space. If an existing project-space is opened, this parameter has no effect.     |
| --update-fingerprint-version                        | Updates Fingerprint versions of the input project to the one used by this SIRIUS version. WARNING: All Fingerprint related results (CSI: FingerID, CANOPUS) will be lost! |

### Specify multi-compound inputs (.ms, .mgf, .mzML/.mzXml, .sirius)

| Command                                  | Description                                                                                                                                                                                                                                                                             |
|------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| -i, --input=<inputPath>[,<inputPath>...] | Specify the input in multi-compound input formats: Preprocessed mass spectra in .ms or .mgf file format, LC/MS runs in .mzML/.mzXml format or already existing SIRIUS project-spaces (uncompressed/compressed) but also any other file type e.g. to provide input for STANDALONE tools. |
| --ignore-formula                         | Ignore given molecular formula if present in .ms or .mgf input files.                                                                                                                                                                                                                   |
| --allow-ms1-only                         | Allow MS1 only data to be imported.                                                                                                                                                                                                                                                     |

### Specify generic inputs (CSV) on a per compound level

| Command                                        | Description                                                                                                                                  |
|------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| -1, --ms1=<ms1File>[,<ms1File>...]             | MS1 spectra files.                                                                                                                           |
| -2, --ms2=<ms2File>[,<ms2File>...]             | MS2 spectra files.                                                                                                                           |
| -z, --mz, --precursor, --parentmass=<parentMz> | The mass of the parent ion for the specified ms2 spectra.                                                                                    |
| --adduct, --ionization=<ionType>               | Specify the adduct for this compound. Default: [M+?]+.                                                                                       |
| -f, --formula=<formula>                        | Specify the neutralized formula of this compound. This will be used for tree computation. If given, no mass decomposition will be performed. |

## Commands

| Command                                                  | Description                                                                                                                                                                                                |
|----------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `config`                                                 | Override all possible default configurations of this toolbox from the command line.                                                                                                                        |
| `project-space, PS`                                      | Modify a given project space: Read project(s) with `--input`, apply modification and write the result via `--output`. If either `--input` or `--output` is given, the modifications will be made in-place. |
| `custom-db, DB`                                          | Generate a custom searchable structure database. Import multiple files with compounds as SMILES or InChi into this DB.                                                                                     |
| `similarity`                                             | Computes the similarity between all compounds in the dataset and outputs a matrix of similarities.                                                                                                         |
| `decomp`                                                 | Small tool to decompose masses with given deviation, ionization, chemical alphabet, and chemical filter.                                                                                                   |
| `mgf-export, MGF`                                        | Exports the spectra of a given input as MGF.                                                                                                                                                               |
| `ftree-export`                                           | Exports the fragmentation trees of a project into various formats.                                                                                                                                         |
| `prediction-export, EPR`                                 | Exports predictions from CSI: FingerID and CANOPUS.                                                                                                                                                        |
| `fingerprinter, FP`                                      | Compute SIRIUS compatible fingerprints from PubChem standardized SMILES in TSV format.                                                                                                                     |
| `gui, GUI`                                               | Starts the graphical user interface of SIRIUS.                                                                                                                                                             |
| `asService, rest, REST`                                  | Experimental/unstable: Starts SIRIUS as a background (REST) service that can be requested via a REST-API.                                                                                                  |
| [`login`](sirius_login)                                  | Allows a user to log in for SIRIUS Webservices (e.g., CSI: FingerID or CANOPUS) and securely store a personal access token.                                                                                |
| `settings`                                               | Configure persistent (technical) settings of SIRIUS (e.g., ProxySettings or ILP Solver).                                                                                                                   |
| `install-autocompletion`                                 | Generates and installs an Autocompletion-Script with all subcommands. Default installation is for the current user.                                                                                        |
| [`write-summaries, W`](sirius_export)                    | Write summary files from a given project space into the given project space or a custom location.                                                                                                          |
| `lcms-align, A`                                          | Preprocessing: Align and merge compounds of multiple LCMS Runs. Use this tool if you want to import from mzML/mzXml.                                                                                       |
| `canopus, compound-classes`                              | Compound Tool: Predict compound categories for each compound individually based on its predicted molecular fingerprint (CSI: FingerID) using CANOPUS.                                                      |
| [`formula, tree, sirius`](sirius_formula_identification) | Compound Tool: Identify molecular formulas for each compound individually using fragmentation trees and isotope patterns.                                                                                  |
| `passatutto`                                             | Compound Tool: Compute a decoy spectra based on the fragmentation trees of the given input spectra. If no molecular formula is provided in the input, the top-scoring computed formula is used.            |
| [`fingerprint`](sirius_fingerprint)                      | Compound Tool: Predict molecular fingerprints from MS/MS and fragmentation trees for each compound individually using CSI: FingerID fingerprint prediction.                                                |
| `zodiac, rerank-formulas`                                | Dataset Tool: Identify Molecular formulas of all compounds in a dataset together using ZODIAC.                                                                                                             |
| [`structure, search-structure-db`](sirius_structure)     | Compound Tool: Search in molecular structure db for each compound individually using CSI: FingerID structure database search.                                                                              |


```{toctree}
---
maxdepth: 1
hidden:
---
sirius_login
sirius_formula_identification
sirius_structure
sirius_fingerprint
sirius_export
```
