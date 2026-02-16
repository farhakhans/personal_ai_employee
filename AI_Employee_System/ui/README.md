Simple UI for Facebook/Instagram posters

Run locally:

1. Install dependencies (use venv):

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r AI_Employee_System/ui/requirements.txt
```

2. Run the test script (runs UI endpoints without starting server):

```powershell
python AI_Employee_System/ui/test_ui.py
```

3. Or start server and open browser:

```powershell
python -m AI_Employee_System.ui.app
# open http://localhost:5001
```
