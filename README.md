#### Order



* **Experiment setup**



* **set subject ID**



* **Tobii - Calibration**



* **Exp 1 Gaze Angle**
* **5 blocks of varying angles**



* **Tobii - Calibration**



* **Exp 2 Movies**
* **"calibration" for 3D-4p**
* **5 Movies**







* **Tobii Blink removal**







PupilResponseModel/

│

├── README.md

├── .gitignore

├── setup.py

│

├── experiments/

│   ├── exp1\_gaze\_angle.py

│   └── exp2\_movies.py

│

├── analysis/

│   ├── exp1\_gaze\_angle/

│   │   ├── 01\_pupil\_detection.ipynb

│   │   ├── 02\_gaze\_angle\_model.ipynb

│   │   └── 03\_validation.ipynb

│   │

│   └── exp2\_dynamic\_pupil/

│       ├── 01\_preprocessing.ipynb

│       ├── 02\_open\_dpsm.ipynb

│       └── 03\_model\_validation.ipynb

│

├── src/

│   ├── \_\_init\_\_.py

│   ├── gaze\_angle/

│   │   ├── \_\_init\_\_.py

│   │   ├── pupil\_detection.py

│   │   └── gaze\_angle\_model.py

│   │

│   └── dpsm/

│       ├── \_\_init\_\_.py

│       ├── preprocessing.py

│       ├── event\_extraction.py

│       ├── video\_handler.py

│       └── pupil\_prediction.py

│

└── data/

&#x20;   ├── stimuli/

&#x20;   │   └── movies/

&#x20;   │       ├── movie\_01.mp4

&#x20;   │       ├── movie\_02.mp4

&#x20;   │       └── ...

&#x20;   │

&#x20;   ├── raw/

&#x20;   │   ├── exp1\_gaze\_angle/

&#x20;   │   │   └── subject\_001/

&#x20;   │   │       ├── fixation\_positions.csv

&#x20;   │   │       ├── camera\_properties.json

&#x20;   │   │       └── trials/

&#x20;   │   │           ├── trial\_001/

&#x20;   │   │           │   ├── eye\_video.mp4

&#x20;   │   │           │   └── eye\_timestamps.csv

&#x20;   │   │           ├── trial\_002/

&#x20;   │   │           │   ├── eye\_video.mp4

&#x20;   │   │           │   └── eye\_timestamps.csv

&#x20;   │   │           └── ...

&#x20;   │   │

&#x20;   │   └── exp2\_dynamic\_pupil/

&#x20;   │       └── subject\_001/

&#x20;   │           ├── movie\_order.csv

&#x20;   │           ├── calibration/

&#x20;   │           │   ├── fixation\_positions.csv

&#x20;   │           │   ├── eye\_video.mp4

&#x20;   │           │   └── eye\_timestamps.csv

&#x20;   │           │

&#x20;   │           ├── camera\_properties.json

&#x20;   │           │

&#x20;   │           └── trials/

&#x20;   │               ├── trial\_001/

&#x20;   │               │   ├── movie\_name.txt

&#x20;   │               │   ├── eye\_video.mp4

&#x20;   │               │   └── eye\_timestamps.csv

&#x20;   │               ├── trial\_002/

&#x20;   │               │   ├── movie\_name.txt

&#x20;   │               │   ├── eye\_video.mp4

&#x20;   │               │   └── eye\_timestamps.csv

&#x20;   │               └── ...

&#x20;   │

&#x20;   ├── intermediate/

&#x20;   │   ├── exp1\_gaze\_angle/

&#x20;   │   │   └── subject\_001/

&#x20;   │   │       ├── pupil\_detections.csv

&#x20;   │   │       └── gaze\_corrected\_pupil.csv

&#x20;   │   │

&#x20;   │   └── exp2\_dynamic\_pupil/

&#x20;   │       └── subject\_001/

&#x20;   │           ├── visual\_events/

&#x20;   │           ├── gaze\_coordinates.csv

&#x20;   │           └── measured\_pupil\_corrected.csv

&#x20;   │

&#x20;   └── processed/

&#x20;       ├── exp1\_gaze\_angle/

&#x20;       │   ├── gaze\_angle\_model.pkl

&#x20;       │   ├── model\_parameters.csv

&#x20;       │   └── validation\_results.csv

&#x20;       │

&#x20;       └── exp2\_dynamic\_pupil/

&#x20;           └── subject\_001/

&#x20;               ├── dpsm\_parameters.csv

&#x20;               ├── predicted\_pupil\_size.csv

&#x20;               ├── residuals.csv

&#x20;               └── plots/

