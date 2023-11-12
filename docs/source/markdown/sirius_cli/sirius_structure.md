# Sirius structure search 
{bdg-success}`COMPOUND TOOL`

## Functionality
Search in molecular structure db for each compound individually using
CSI:FingerID structure database search.

## Options

| Option                                                            | Description                                                                                                                                                                                                                                                                                                                                                                                                                        |
|-------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `-d, --db, --database=<dbName>[,<dbName>...]`                     | Search structure in the union of the given databases. If no database is given, the default database(s) are used. Example: possible DBs: 'ALL,ALL_BUT_INSILICO,BIO,PUBCHEM,MESH,HMDB,KNAPSACK,CHEBI,PUBMED,KEGG,HSDB,MACONDA,METACYC,GNPS,ZINCBIO,UNDP,YMDB,PLANTCYC,NORMAN,ADDITIONAL,PUBCHEMANNOTATIONBIO,PUBCHEMANNOTATIONDRUG,PUBCHEMANNOTATIONSAFETYANDTOXIC,PUBCHEMANNOTATIONFOOD,KEGGMINE,ECOCYCMINE,YMDBMINE'. Default: BIO |
| `-h, --help`                                                      | Show this help message and exit.                                                                                                                                                                                                                                                                                                                                                                                                   |
| `-l, --elgordo, tag-lipids, flag-lipids=<injectElGordoCompounds>` | Tag candidates that are matching lipid class determined by El Gordo in CSI:FingerID candidate list. Default: True                                                                                                                                                                                                                                                                                                                  |
| `-V, --version`                                                   | Print version information and exit.                                                                                                                                                                                                                                                                                                                                                                                                |

## Follow-up commands

- `canopus, compound-classes` - Predict compound categories for each compound individually based on its predicted molecular fingerprint (CSI:FingerID) using CANOPUS.
- [`write-summaries, W`](sirius_export) - Write Summary files from a given project-space into the given project-space or a custom location.
