# Python User Migration (Django)

## ⚙️ Setup

1. Add environment variables

```
DESCOPE_PROJECT_ID=<your descope project id>
DESCOPE_MANAGEMENT_KEY=<your descope management key>
```
The Project ID can be found [here](https://app.descope.com/settings/project).
The Descope Management Key can be found [here](https://app.descope.com/settings/company/managementkeys).


2. Run script

```
python -m venv venv


On MacOS and Linux:
source venv/bin/activate

On Windows:
.\venv\Scripts\activate

pip install -r requirements.txt

python -m src.main
```
