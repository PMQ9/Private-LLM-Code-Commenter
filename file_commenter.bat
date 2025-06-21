@echo off
setlocal
set "SCRIPT_DIR=%~dp0"

:: Call the Python script with all arguments
python "%SCRIPT_DIR%src\modules\ollama_commenter\ollama_commenter.py" %*

endlocal