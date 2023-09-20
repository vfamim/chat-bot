# Data Engineer Path

Minha trajetória para começar a ser um profissional de dados fullstack

## Project Organization

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io

---

| Field Name            | Description                                                                                                                                                                                                                                          |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| VendorId              | A code indicating the TPEP provider that provided the record. 1= Creative Mobile Technologies, LLC; 2= VeriFone Inc.                                                                                                                                 |
| tpep_pickup_datetime  | The date and time when the meter was engaged.                                                                                                                                                                                                        |
| tpep_dropoff_datetime | The date and time when the meter was disengaged.                                                                                                                                                                                                     |
| Passenger_count       | The number of passengers in the vehicle. This is a driver-entered value.                                                                                                                                                                             |
| Trip_distance         | The elapsed trip distance in miles reported by the taximeter.                                                                                                                                                                                        |
| PULocationID          | TLC Taxi Zone in which the taximeter was engaged                                                                                                                                                                                                     |
| DOLocationID          | TLC Taxi Zone in which the taximeter was disengaged                                                                                                                                                                                                  |
| RateCodeID            | The final rate code in effect at the end of the trip. 1= Standard rate 2=JFK 3=Newark 4=Nassau or Westchester 5=Negotiated fare 6=Group ride                                                                                                         |
| Store_and_fwd_flag    | This flag indicates whether the trip record was held in vehicle memory before sending to the vendor, aka “store and forward,” because the vehicle did not have a connection to the server. Y= store and forward trip N= not a store and forward trip |
| Payment_type          | A numeric code signifying how the passenger paid for the trip. 1= Credit card 2= Cash 3= No charge 4= Dispute 5= Unknown 6= Voided trip                                                                                                              |
| Fare_amount           | The time-and-distance fare calculated by the meter.                                                                                                                                                                                                  |
| Extra                 | Miscellaneous extras and surcharges. Currently, this only includes the $0.50 and $1 rush hour and overnight charges.                                                                                                                                 |
| MTA_tax               | $0.50 MTA tax that is automatically triggered based on the metered rate in use.                                                                                                                                                                      |
| Improvement_surchage  | $0.30 improvement surcharge assessed trips at the flag drop. The improvement surcharge began being levied in 2015.                                                                                                                                   |
| Tip_amount            | Tip amount – This field is automatically populated for credit card tips. Cash tips are not included.                                                                                                                                                 |
| Tolls_amount          | Total amount of all tolls paid in trip.                                                                                                                                                                                                              |
| Total_amount          | The total amount charged to passengers. Does not include cash tips.                                                                                                                                                                                  |
| Congestion_Surcharge  | Total amount collected in trip for NYS congestion surcharge.                                                                                                                                                                                         |
| Airport_fee           | $1.25 for pick up only at LaGuardia and John F. Kennedy Airports                                                                                                                                                                                     |

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
