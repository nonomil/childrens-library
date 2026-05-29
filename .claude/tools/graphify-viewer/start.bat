@echo off
chcp 65001 >nul 2>&1
title Code Map Viewer

:: .claude/tools/graphify-viewer/ → project root is 3 levels up
set "ROOT=%~dp0..\..\.."

:: Determine graph.json path: arg > auto-detect in docs/代码库-知识图谱/
if "%~1"=="" (
    :: Try to find *-LLM图谱/graph.json
    for /d %%d in ("%ROOT%\docs\代码库-知识图谱\*-LLM图谱") do (
        if exist "%%d\graph.json" set "GRAPH_JSON=%%d\graph.json"
    )
    if not defined GRAPH_JSON (
        if exist "%ROOT%\graphify-out\graph.json" (
            set "GRAPH_JSON=%ROOT%\graphify-out\graph.json"
        ) else (
            echo ERROR: No graph.json found. Run graphify scan first.
            pause
            exit /b 1
        )
    )
) else (
    set "GRAPH_JSON=%~1"
)

:: Regenerate viewer_data.js from graph.json
echo [1/3] Generating viewer data from %GRAPH_JSON%...
python "%~dp0generate_viewer.py" "%GRAPH_JSON%"
if errorlevel 1 (
    echo ERROR: Failed to generate viewer data.
    pause
    exit /b 1
)

:: Start viewer server in background (serve from graphify-viewer dir)
echo [2/3] Starting viewer server on port 3335...
cd /d "%~dp0"
start /b python "%~dp0viewer_server.py" --host 127.0.0.1 --port 3335

:: Wait for server to be ready
timeout /t 1 /nobreak >nul

:: Open browser
echo [3/3] Opening browser...
start http://localhost:3335/viewer_template.html

echo.
echo Code Map Viewer is running at http://localhost:3335
echo Press Ctrl+C or close this window to stop.
echo.
:loop
timeout /t 60 /nobreak >nul
goto loop
