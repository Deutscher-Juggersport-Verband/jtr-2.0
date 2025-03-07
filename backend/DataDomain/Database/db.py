import logging
import os

from flask import Flask
from flask_migrate import current, upgrade
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def executeSqlFile(filename: str) -> None:

    with open(filename, 'r') as sql_file:
        sqlCommands = sql_file.read()

    connection = db.engine.raw_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(sqlCommands)
        connection.commit()

    except Exception as e:
        connection.rollback()
        logging.error(
            f'Database | db | Fehler beim Ausführen der SQL-Datei: {e}')

    finally:
        cursor.close()
        connection.close()


def executeSqlCommandsToInitDatabase(app: Flask) -> None:

    folderPath = os.path.join(
        app.config['DATABASE_PATH'],
        'data/init-database')

    for filename in os.listdir(folderPath):
        if filename.endswith('.sql'):
            fullPath = os.path.join(folderPath, filename)

            executeSqlFile(fullPath)


def initDatabase(app: Flask) -> None:

    with app.app_context():
        if current() != 'head':
            upgrade()

        if os.getenv('GENERATE_TEST_DATA'):
            executeSqlCommandsToInitDatabase(app)
