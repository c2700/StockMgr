cls
Write-Host "Please Install MariaDB before proceeding"
Pause

$db_data_dir = "${PSScriptRoot}\db\data";
$db_data_dir_cfg_file = "${db_data_dir}\my.ini";

Stop-Service StockMgrDB_Service -Verbose
cmd /c sc delete StockMgrDB_Service
Remove-Item -Verbose -Debug -Confirm -Force ${db_data_dir}
cls

$r_pass = Read-Host "enter root password to setup db (same password you gave when installing mariadb. Leave blank if not entered)";
Write-Host "Enter Credentials that will be "
$user = Read-Host "enter username ";
$pass = Read-Host "enter password";



Write-Host "Setting '${db_data_dir}' as the  data directory and installing 'StockMgrDB_Service' as DB service for the StockManager App"
mariadb-install-db.exe -o -W StockMgrDB_socket.sock -S "StockMgrDB_Service" -P 3306 -d "$db_data_dir"

Write-Host "Set a description to the installed StockMgrDB_Service service"
cmd /c sc description "StockMgrDB_Service" "DB service for the stock manager"

Start-Service "StockMgrDB_Service" -Verbose
Get-Service "StockMgrDB_Service"

$_root_user_args_array_obj = @("-u", "root")
if ("$r_pass" -ne "") {
    $_root_user_args_array_obj += ("-p", "$r_pass")
}

Write-Host "Creating StockDB in the set datadir ${db_data_dir}";
mysql -v -v -v @_root_user_args_array_obj -e "CREATE DATABASE StockDB"

Write-Host "Creating up necessary Tables in StockDB";
cat "${PSScriptRoot}\db_setup.sql" | mysql -u root StockDB;

Write-Host "Setting up Creds for StockDB Database";
mysql -v -v -v -u root -e "CREATE USER '${user}'@localhost IDENTIFIED BY '${pass}'" StockDB;

Write-Host "Granting all privileges for user ${user} over StockDB database";
$_query = "GRANT ALL PRIVILEGES ON *.* TO '${user}'@localhost IDENTIFIED BY '${pass}'"
mysql -v -v -v -u root -e "$_query" StockDB;

Write-Host "Commiting user permission changes";
mysql -v -v -v -u root -e "FLUSH PRIVILEGES" StockDB;

