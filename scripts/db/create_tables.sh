#!/bin/bash

# Configuration
DB_SERVER="192.168.4.3"
DB_USER="SA"
DB_PASSWORD="FFy2kGJzm2JO9Pb"
DB_NAME="MDEndpoints"

# SQL script file location
SQL_SCRIPT_PATH="create_tables.sql"
CONTAINER_NAME="mssql-server-persistence"

echo "Creating database 'AdvanceHuntingQuery' if it doesn't exist..."
# Use Docker exec to run SQL commands inside the container
docker exec -it $CONTAINER_NAME /opt/mssql-tools18/bin/sqlcmd -S localhost -U $DB_USER -P $DB_PASSWORD -C -Q "IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = '$DB_NAME') CREATE DATABASE $DB_NAME"

echo "Waiting for database creation to complete"
sleep 2

echo "Copying SQL script to container..."
# Copy the SQL script to the container
docker cp $SQL_SCRIPT_PATH $CONTAINER_NAME:/tmp/create_tables.sql


echo "Executing SQL script to create tables..."
# Execute the SQL script inside the container
docker exec -it $CONTAINER_NAME /opt/mssql-tools18/bin/sqlcmd -S localhost -U $DB_USER -P $DB_PASSWORD -C -d $DB_NAME -i /tmp/create_tables.sql

echo "Database setup complete!"
