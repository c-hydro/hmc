# Hydrological Model Continuum

Welcome to the **Hydrological Model Continuum** GitHub repository. 
This is a hydrological model supported by the Italian Civil Department (DPC) and is used 
for preventing and reducing hydrogeological risk.

## Background

The **Hydrological Model Continuum** is a model designed by CIMA Research Foundation to support decision makers 
during the operational phases of flood forecasting and monitoring. 
The goal is to protect the population and infrastructure from damage caused by intense precipitation events.
The Flood-PROOFS system manages the data flow deriving from various modelling tools developed by the CIMA Research Foundation to return a quantitative assessment of the effects that precipitation can have on the territory in terms of flow and probability to overcome the critical thresholds in the different basins. 
The system has been operating since 2008 at various Functional Centers (Autonomous Region of Valle d'Aosta and Marche) where it is used for the issue of hydro-meteorological warnings for civil protection purposes. At the technical offices of the Valle d'Aosta Water Company (CVA) it is instead useful to study and implement strategies to mitigate flood events or to secure facilities in the event of flooding.

Components
**********

The Flood-PROOFS forecasting chain consists in the following different parts, which are summarized as follows:

    • **Processing**: tools to organize input and output datasets written in python3 language usually named **Hydrological Data Engines [hyde]** package;
    • **Simulation**: tools to set and run Hydrological Model Continuum (HMC) written both in python3 and fortran programming language usually named **Hydrological Model Continuum [hmc]** package;
    • **Publishing and Visualization**: tools to control, view and analyze results written both in python3 and R programming language usually named as **Hydrological Analysis tools [hat]** package;
    • **Labs**: laboratories for running components of the modelling system, for trainings and educational use;
    • **Utilities**: common functionality required by the previous components.

All codes and datasets are freely available and users can be get them from our github repository [1_].