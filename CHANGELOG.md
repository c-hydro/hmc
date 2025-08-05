
# Changelog

All notable changes to this project are documented here.

```{contents}
:local:
:depth: 2
```

## Version 4.x

### [4.0.0] – 2024-07-30

- Refactored the entire codebase and packages based on the new HMC code generation.

## Version 3.x

### [3.1.6] – 2024-03-26

- Support for HMC Fortran version 3.1.6.
- Added configuration parameters: `dset_datetime_run` and `dset_sub_path_run`.
- Set up Conda environment integration.
- Extended time-series tools for:
  - Gridded datasets.
  - Regional meteorological service formats.

### [3.1.5] – 2022-11-30

**Additions**:

- HMC Fortran v3.1.5 integration.
- Writers for discharges, dam volumes/levels in JSON.
- Time-series input for socket/release systems.
- Constant baseflow support per section via shapefile.
- Section filtering via `hmc_file_filter`.
- Temporary analysis directory handling.
- Dataset presence validation pre-run.
- Tools for:
  - Merging datasets across domains and deterministic runs.
  - Gridded dataset conversion and preprocessing.
  - Dam volume time-series handling.

**Fixes**:

- Numerous bug fixes in:
  - Static dataset handling.
  - JSON/summary time-series updates.
  - Gridded data compatibility.
  - Section format compatibility and warnings.

### [3.1.4] – 2021-03-08

- Added support for:
  - GeoTIFF and ASCII lake readers.
  - Automatic generation of lat/lon/cell area grids.
  - Catchment masks and catchment-based time-series.
  - Dataset dimension and undefined value validation.
- Introduced:
  - NetCDF conversion tools.
  - Bash launcher for model runs.
- Bug fixes in:
  - Interpolation and static file reading.
  - Dataset frequency/time slice handling.

### [3.1.3] – 2020-10-28

- Shapefile-based section extraction (`.info_sections.txt`).
- Tools for:
  - Binary to NetCDF conversion.
  - Probabilistic discharge merging.
  - JSON-to-ASCII (Dewetra) output conversion.
- Fixed netCDF time handling and orientation issues.

### [3.1.2] – 2020-08-19

- Support for HMC Fortran version 3.1.2.

## Version 1.x

### [1.8.5] – 2020-02-07

- Fixed time-series management and writing bugs.

### [1.8.4] – 2020-01-20

- Documentation added for model and packages.
- Probabilistic mode bugs fixed.
- JSON configuration supported.

### [1.8.0] – 2018-05-21

- Code refactoring for HMC Fortran v2.0.7.
- Migrated to Python 3.

### [1.7.0] – 2016-11-14

- Refactored based on HMC Fortran v2.0.6.

### [1.6.0] – 2015-09-28

- Updated code style and naming conventions.
- Enhanced algorithm/data structures.

### [1.5.0] – 2015-07-07

- Based on Regione Marche hydrologic chain.
- Updated Continuum Codes (modern Fortran).

### [1.0.0] – 2014-04-01

- Initial release from DRIHM/DRIHM2US research projects.
- Legacy DRiFt and Continuum Codes migration.
