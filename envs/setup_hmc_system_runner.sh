#!/bin/bash -e

# ----------------------------------------------------------------------------------------
# Script Name and Version
script_name='HMC ENVIRONMENT - PYTHON LIBRARIES FOR PACKAGE - RUNNER DATA - CONDA'
script_version="1.7.0"
script_date='2025/08/04'

# info message start
echo " ============================================================================="
echo " ==> "$script_name" (Version: "$script_version" Release_Date: "$script_date")"
echo " ==> START ..."


# Help Message
show_help() {
  echo ""
  echo "Usage: $0 [OPTIONS]"
  echo ""
  echo "This script sets up a Conda environment for the HMC runner system."
  echo ""
  echo "Options:"
  echo "  --env-tag <tag>               : Tag for environment (default: hmc_runner)"
  echo "  --env-root <path>             : Root folder for Miniconda install (default: ./conda)"
  echo "  --settings-file <filename>    : Settings file name (default: <env-tag>_settings)"
  echo "  --libraries-folder <name>     : Conda environment name (default: <env-tag>_libraries)"
  echo "  --requirements-file <file>    : Conda environment file (default: requirements_<env-tag>.yaml)"
  echo "  --miniconda-url <url>         : URL for Miniconda installer"
  echo "  --help                        : Show this help message"
  echo ""
  echo "Example:"
  echo "  ./setup_hmc_system_runner.sh --env-tag myenv --env-root ./env_root"
  echo ""
  exit 0
}
# ----------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------
# Default Parameters
ENV_TAG="hmc_runner"
ENV_ROOT="../conda"
SETTINGS_FILE=""
LIBRARIES_FOLDER=""
REQUIREMENTS_FILE=""
MINICONDA_URL="https://repo.continuum.io/miniconda/Miniconda3-py311_25.1.1-2-Linux-x86_64.sh"

# Parse Options
while [[ $# -gt 0 ]]; do
  case "$1" in
    --env-tag) ENV_TAG="$2"; shift 2 ;;
    --env-root) ENV_ROOT="$2"; shift 2 ;;
    --settings-file) SETTINGS_FILE="$2"; shift 2 ;;
    --libraries-folder) LIBRARIES_FOLDER="$2"; shift 2 ;;
    --requirements-file) REQUIREMENTS_FILE="$2"; shift 2 ;;
    --miniconda-url) MINICONDA_URL="$2"; shift 2 ;;
    --help) show_help ;;
    -*)
      echo "ERROR: Unknown option: $1"
      show_help
      ;;
    *)
      echo "ERROR: Invalid argument: $1"
      show_help
      ;;
  esac
done

# Resolve Derived Values
SETTINGS_FILE="${SETTINGS_FILE:-${ENV_TAG}_settings}"
LIBRARIES_FOLDER="${LIBRARIES_FOLDER:-${ENV_TAG}_libraries}"
REQUIREMENTS_FILE="${REQUIREMENTS_FILE:-requirements_${ENV_TAG}.yaml}"
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Functions
download_miniconda() {
  echo "[1/4] Downloading Miniconda..."
  curl -L "$MINICONDA_URL" -o miniconda.sh
  chmod +x miniconda.sh
}

install_miniconda() {
  echo "[2/4] Installing Miniconda to: $ENV_ROOT"
  bash miniconda.sh -b -p "$ENV_ROOT"
  export PATH="$ENV_ROOT/bin:$PATH"
}

create_conda_env() {
  echo "[3/4] Creating Conda environment: $LIBRARIES_FOLDER"
  conda env create -f "$REQUIREMENTS_FILE" -n "$LIBRARIES_FOLDER"
}

activate_conda_env() {
  echo "[4/4] Activating environment: $LIBRARIES_FOLDER"
  source "$ENV_ROOT/bin/activate"
  conda activate "$LIBRARIES_FOLDER"
}
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Execution Flow
main() {
  echo ""
  echo " ----------------------------------------------------------------------------- "
  echo " :: SETUP CONFIGURATION"
  echo "    ENV_TAG          = $ENV_TAG"
  echo "    ENV_ROOT         = $ENV_ROOT"
  echo "    SETTINGS_FILE    = $SETTINGS_FILE"
  echo "    LIBRARIES_FOLDER = $LIBRARIES_FOLDER"
  echo "    REQUIREMENTS_FILE= $REQUIREMENTS_FILE"
  echo "    MINICONDA_URL    = $MINICONDA_URL"
  echo " ----------------------------------------------------------------------------- "
  echo ""

  download_miniconda
  install_miniconda
  create_conda_env
  activate_conda_env

  echo ""
  echo " ----------------------------------------------------------------------------- "
  echo " :: SETUP COMPLETE"
  echo "    ENVIRONMENT '$LIBRARIES_FOLDER' IS READY"
  echo "    PYTHON PACKAGE(S) INSTALLED FROM: $REQUIREMENTS_FILE"
  echo "    CONDA BASE LOCATED AT: $ENV_ROOT"
  echo " ----------------------------------------------------------------------------- "
  echo ""

}

# call main 
main

# Info message end
echo " ==> "$script_name" (Version: "$script_version" Release_Date: "$script_date")"
echo " ==> ... END"
echo " ==> Bye, Bye"
echo " ============================================================================== "
# ----------------------------------------------------------------------------------------




