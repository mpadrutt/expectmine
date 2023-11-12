# Sirius Export
{bdg-info}`STANDALONE` {bdg-primary}`POSTPROCESSING`

## Functionality
Write Summary files from a given project-space into the given project-space or
a custom location.

## Options

| Option                               | Description                                                                                                                                       |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| `-c, --zip, --compress`              | Summaries will be written into a compressed zip archive. This parameter will be ignored if the summary is written into the project-space.         |
| `--[no-]full-summary`                | Write project-wide summary files with ALL Hits. (Use with care! Might create large files and consume large amounts of memory for large projects.) |
| `-h, --help`                         | Show this help message and exit.                                                                                                                  |
| `--[no-]top-hit-summary`             | Write project-wide summary files with all Top Hits.                                                                                               |
| `-o, --output=<location>`            | Specify location (outside the project) for writing summary files. Per default summaries are written to the project-space.                         |
| `--[no-]top-hit-adduct-summary`      | Write project-wide summary files with all Top Hits and their adducts.                                                                             |
| `-V, --version`                      | Print version information and exit.                                                                                                               |
| `--all`                              | Output all predicted CSI:FingerID and CANOPUS probabilities (sets --fingerprints, --classyfire, --npc).                                           |
| `--classyfire`                       | Output predicted classyfire probabilities by CANOPUS.                                                                                             |
| `--fingerprint, --fingerprints`      | Output predicted fingerprint probabilities by CSI: FingerID.                                                                                      |
| `--maccs`                            | Output predicted MACCS fingerprint probabilities by CSI:FingerID (subset of --fingerprint).                                                       |
| `--npc`                              | Output predicted NPC (natural product classifier) probabilities by CANOPUS.                                                                       |
| `-p, --digits, --precision=<digits>` | Specify the number of digits used for printing floating-point values. -1 -> full-length Double value. Default: -1.                                |
| `--pubchem`                          | Output predicted PubChem fingerprint probabilities by CSI:FingerID (subset of --fingerprint).                                                     |
