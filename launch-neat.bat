@ECHO OFF

IF NOT EXIST "%~dp0python\.venv\" (
	ECHO Creating virtual environment
	python -m venv "%~dp0python\.venv"
	
	ECHO Installing python packages in virtual environment
	"%~dp0python\.venv\Scripts\pip.exe" install -r "%~dp0python\requirements.txt"
)

cd "%~dp0python\""
"%~dp0python\.venv\Scripts\python.exe" "r4_neat.py"