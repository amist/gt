set FILENAME=%DATE:/=-%-%TIME::=-%
set FILENAME=%FILENAME: =%
set FILENAME=%FILENAME:,=.%.log

type tsp.config >> %FILENAME%

for /l %%x in (1, 1, 150) do (
    echo run number %%x
    echo new run >> %FILENAME%
    python -m gt.tests.test_tsp >> %FILENAME% 2>&1
)
echo new run >> %FILENAME%