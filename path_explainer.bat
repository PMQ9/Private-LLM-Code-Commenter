@echo off
setlocal
set "SCRIPT_DIR=%~dp0"

:: Call the Python script with all arguments
python "%SCRIPT_DIR%src\modules\source_code_explanation\source_code_explanation.py" %*

endlocal