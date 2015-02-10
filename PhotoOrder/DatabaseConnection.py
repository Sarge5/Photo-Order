__author__ = 'Sarge'

import pymysql
import sys
import datetime
import urllib.parse
import traceback
from PySide.QtCore import *
from PySide.QtGui import *


class DatabaseConnection(QObject):

    connectionChange = Signal()

    def __init__(self, config):
        super().__init__()
        self.config = config
        try:
            self.connection = pymysql.connect(
                host=self.config.getDBServer(),
                database=self.config.getDBName(),
                user=self.config.getDBUser(),
                password=self.config.getDBPass())
        except:
            self.connection = False
            message = QMessageBox()
            message.setText('Error connecting to database')
            text = traceback.format_exc().splitlines()
            text = text[0] + text[-1]
            message.setDetailedText(text)
            message.setIcon(QMessageBox.Warning)
            message.exec_()

    def reconnect(self):
        if self.connection == False:
            try:
                self.connection = pymysql.connect(
                    host=self.config.getDBServer(),
                    database=self.config.getDBName(),
                    user=self.config.getDBUser(),
                    password=self.config.getDBPass())
            except:
                self.connection = False
        else:
            try:
                self.connection.close()
                self.connection = pymysql.connect(
                    host=self.config.getDBServer(),
                    database=self.config.getDBName(),
                    user=self.config.getDBUser(),
                    password=self.config.getDBPass())
            except:
                self.connection = False
                message = QMessageBox()
                message.setText('Error connecting to database')
                text = traceback.format_exc().splitlines()
                text = text[0] + text[-1]
                message.setDetailedText(text)
                message.setIcon(QMessageBox.Warning)
                message.exec_()
        self.connectionChange.emit()

    def checkTableExists(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """SELECT count(*)
                FROM information_schema.TABLES
                WHERE (TABLE_SCHEMA = %s) AND (TABLE_NAME = %s)""",
                (self.config.getDBName(), 'folder'))
            result = cursor.fetchone()[0]
            cursor.close()
            return result
        except:
            message = QMessageBox()
            message.setText('Error checking database')
            text = traceback.format_exc().splitlines()
            text = text[0] + text[-1]
            message.setDetailedText(text)
            message.setIcon(QMessageBox.Critical)
            message.exec_()
            pass

    def createTables(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """
                SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
                SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
                SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS `folder` (
                  `idfolder` INT NOT NULL AUTO_INCREMENT,
                  `url` VARCHAR(60) NOT NULL,
                  `name` VARCHAR(60) NOT NULL,
                  `active` INT NOT NULL DEFAULT 1,
                  PRIMARY KEY (`idfolder`),
                  UNIQUE INDEX `url_UNIQUE` (`url` ASC),
                  UNIQUE INDEX `name_UNIQUE` (`name` ASC))
                ENGINE = InnoDB;
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS `picture` (
                  `idpicture` INT NOT NULL AUTO_INCREMENT,
                  `idfolder` INT NOT NULL,
                  `name` VARCHAR(140) NULL,
                  `link` VARCHAR(100) NOT NULL,
                  `ordered` INT NOT NULL DEFAULT 0,
                  PRIMARY KEY (`idpicture`),
                  INDEX `fk_folder_idfolder_idx` (`idfolder` ASC),
                  CONSTRAINT `fk_folder_idfolder`
                    FOREIGN KEY (`idfolder`)
                    REFERENCES `folder` (`idfolder`)
                    ON DELETE CASCADE
                    ON UPDATE NO ACTION)
                ENGINE = InnoDB;
                """
            )
            cursor.execute(
                """
                SET SQL_MODE=@OLD_SQL_MODE;
                SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
                SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
                """
            )
            cursor.close()
        except:
            message = QMessageBox()
            message.setText('Error creating database')
            text = traceback.format_exc().splitlines()
            text = text[0] + text[-1]
            message.setDetailedText(text)
            message.setIcon(QMessageBox.Critical)
            message.exec_()
            pass

    def getFolders(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """
                SELECT *
                FROM folder
                ORDER BY active DESC;
                """
            )
            result = cursor.fetchall()
            cursor.close()
            return result
        except:
            message = QMessageBox()
            message.setText('Error retrieving folder')
            text = traceback.format_exc().splitlines()
            text = text[0] + text[-1]
            message.setDetailedText(text)
            message.setIcon(QMessageBox.Critical)
            message.exec_()
            pass

    def addFolder(self, folder, folderphotos):
        try:
            cursor = self.connection.cursor()
            time = datetime.datetime.now()
            folderUrl = urllib.parse.quote(folder.text(0)) + time.strftime("%Y-%m-%d")
            folderName = folder.text(0) + " - " + time.strftime("%Y-%m-%d")
            cursor.execute(
                """
                INSERT INTO folder(url, name, active)
                VALUES (%s, %s, 1);
                """,
                [folderUrl, folderName]
            )
            folderid = cursor.lastrowid
            self.connection.commit()
            cursor.close()
            self.addFolderPictures(folderid, folderphotos)
        except:
            message = QMessageBox()
            message.setText('Error adding folder')
            text = traceback.format_exc().splitlines()
            text = text[0] + text[-1]
            message.setDetailedText(text)
            message.setIcon(QMessageBox.Critical)
            message.exec_()
            pass

    def getFolderPictures(self, foldername):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """
                SELECT *
                FROM picture
                LEFT JOIN folder
                USING (idfolder)
                WHERE (folder.name = %s);
                """,
                [foldername]
            )
            result = cursor.fetchall()
            cursor.close()
            return result
        except:
            message = QMessageBox()
            message.setText('Error retrieving folder pictures')
            text = traceback.format_exc().splitlines()
            text = text[0] + text[-1]
            message.setDetailedText(text)
            message.setIcon(QMessageBox.Critical)
            message.exec_()
            pass

    def addFolderPictures(self, folderid, folderphotos):
        try:
            cursor = self.connection.cursor()
            for photo in folderphotos:
                url = photo[1]['url'] + '&raw=1'
                name = photo[0]
                cursor.execute(
                    """
                    INSERT INTO picture(idfolder, name, link, ordered)
                    VALUES (%s, %s, %s, 0)
                    """,
                    [folderid, name, url]
                )
            self.connection.commit()
            cursor.close()
        except:
            message = QMessageBox()
            message.setText('Error adding folder pictures')
            text = traceback.format_exc().splitlines()
            text = text[0] + text[-1]
            message.setDetailedText(text)
            message.setIcon(QMessageBox.Critical)
            message.exec_()
            pass

    def saveFolder(self, folderid, folderurl, foldername, active):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """
                UPDATE folder
                SET url = %s, name = %s, active = %s
                WHERE idfolder = %s
                """,
                (folderurl, foldername, active, folderid)
            )
            self.connection.commit()
            cursor.close()
        except:
            message = QMessageBox()
            message.setText('Error saving share properties')
            text = traceback.format_exc().splitlines()
            text = text[0] + text[-1]
            message.setDetailedText(text)
            message.setIcon(QMessageBox.Critical)
            message.exec_()
            pass