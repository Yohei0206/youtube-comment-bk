@echo off
SET SCRIPT_DIR=%~dp0
SET VENV_PYTHON="%SCRIPT_DIR%venv\Scripts\python.exe"

IF NOT EXIST %VENV_PYTHON% (
    echo Error: Python executable not found in virtual environment.
    echo Please ensure the virtual environment is set up correctly.
    goto :eof
)

%VENV_PYTHON% -m uvicorn app.main:app --reload
