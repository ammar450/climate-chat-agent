@echo off
REM Climate Chat Agent - Quick Evaluation Script
REM 
REM This script runs the evaluation framework to test agent performance.
REM Make sure the agent server is running before executing.

echo ================================================================================
echo Climate Chat Agent - Evaluation Framework
echo ================================================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9 or higher
    pause
    exit /b 1
)

echo Select evaluation mode:
echo.
echo [1] Run all tests (recommended)
echo [2] Run specific test by ID
echo [3] Run tests by category
echo [4] Generate detailed report
echo [5] Quick test (run first 5 questions)
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo.
    echo Running all 30 evaluation tests...
    echo.
    python evaluation/evaluate_agent.py --report
    goto :end
)

if "%choice%"=="2" (
    set /p testid="Enter test ID (1-30): "
    echo.
    echo Running test %testid%...
    echo.
    python evaluation/evaluate_agent.py --question-id %testid%
    goto :end
)

if "%choice%"=="3" (
    echo.
    echo Available categories:
    echo - discovery
    echo - statistics  
    echo - aggregation
    echo - filtering
    echo - spatial
    echo - location
    echo - trends
    echo - comparison
    echo - extremes
    echo - long-term
    echo - exploration
    echo.
    set /p category="Enter category: "
    echo.
    echo Running %category% tests...
    echo.
    python evaluation/evaluate_agent.py --category %category% --report
    goto :end
)

if "%choice%"=="4" (
    set /p outfile="Enter output filename (default: evaluation_report.json): "
    if "%outfile%"=="" set outfile=evaluation_report.json
    echo.
    echo Running all tests and generating detailed report...
    echo.
    python evaluation/evaluate_agent.py --output %outfile%
    echo.
    echo Report saved to: %outfile%
    goto :end
)

if "%choice%"=="5" (
    echo.
    echo Running quick test (first 5 questions)...
    echo.
    for /l %%i in (1,1,5) do (
        python evaluation/evaluate_agent.py --question-id %%i
    )
    goto :end
)

echo Invalid choice. Please run the script again.

:end
echo.
echo ================================================================================
echo Evaluation complete!
echo ================================================================================
pause
