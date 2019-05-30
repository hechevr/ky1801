# Music Reduction -- Chord Identification
# Group: ky1801

### Structure

    .
    ├── data                    # Available data
    ├── system                     # Chord Identification system code
    ├── test                    # HMM and LSTM model testing code
    ├── report                    # Report and presentation ppt
    └── README.md

### Built With

* python3.5
* tensorflow1.13.1
* keras2.1.2
* sklearn
* music21
* numpy

### Testing Command

To generate pretrain dataset (the definition can be found in report)

```
python generate_pretrain_dataset.py
```

To run system on xxx.mxl file

```
python main.py xxx.mxl
```

### Future Work

* Machine learning approach for parameters in system
* Machine learning approach for time unit splitting
* Collecting more data
* Improved HMM model
