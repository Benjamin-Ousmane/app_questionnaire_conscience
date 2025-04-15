# Streamlit Desktop App for Consciousness Evaluation

## Overview
This is a **Streamlit** web application for evaluating the subjective consciousness of patients. 
The application allows users to enter details such as date, time, evaluator information, and consciousness-related assessments. 
The output data is stored in an **Excel file**.

The web app can be converted to a Desktop app with Stilte and Electron
(for more informations : https://github.com/whitphx/stlite/blob/main/packages/desktop/README.md)


## Installation to run the Python WEB application locally
1. **Prerequisites**
- Python 3.8+
- pip

2. **Install Python Dependencies**
(streamlit MUST NOT be commented in the requirements.txt)
```sh
pip install -r requirements.txt
```

3. **Running the Python Application**
Verify that the `file_path` in `app.py` is just the excel file (you can change the name of the file):
```python
file_path = "evaluation_data.xlsx" # to run in streamlit app 
```

```sh
streamlit run app.py
```

## Installation to run the DESKTOP application 
1. **Prerequisites**
- Node.js 
- Python 3.8+
- pip

2. **Install Dependencies**
(streamlit MUST be commented in the requirements.txt)
```sh
npm install
```
This command will create `node_modules` folder

3. **Building the JavaScript Application**
Verify that the `file_path` in `app.py` is in the `mnt/` folder (you can change the name of the file):
```python
file_path = "/mnt/evaluation_data.xlsx" # to run with .exe app
```

```sh
npm run dump
```
This command will convert the Python App in a Javascript app in the `build` folder

You can run de Javascript App locally with this command : 
```sh
npm run serve
```

4. **Create the .exe from the JavaScript Application**
```sh
npm run app:dist
```
The executable file (`.exe`) will be available in the `dist/` folder.

5. **Excel output file**
By default, the output excel file will be saved in this path `C:\Users\{User}\conscience_data`
If you want to change the path, update `{{home}}/conscience_data` in the `package.json` file :
```json
{
  "stlite": {
    "desktop": {
      "nodeJsWorker": true,
      "nodefsMountpoints": {
        "/mnt": "{{home}}/conscience_data" 
        // "/mnt": "D:" example for an USB 
      }
    }
  }
}
```
Then, you need to redo steps 3. and 4.

## Contributors
- **Benjamin-Ousmane M'Bengue**
- **Bruno Michelot**

## License
...
