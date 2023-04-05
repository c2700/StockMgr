1) Install Python
2) open PowerShell in admin mode
3) Drag the "db_setup.ps1" script to the powershell window & run it
4) run "python3 main.py"

if App does not run with provided root password, re-run the "db_setup.ps1" but without providing the root password

To test DB using test values exexcute
mysql -u 'root' StockDB < "test_vals\sql_db_init_vals.txt"


