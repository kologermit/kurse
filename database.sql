-- --------------------------------------------------------
-- Хост:                         localhost
-- Версия сервера:               PostgreSQL 13.8 on x86_64-pc-linux-musl, compiled by gcc (Alpine 11.2.1_git20220219) 11.2.1 20220219, 64-bit
-- Операционная система:         
-- HeidiSQL Версия:              12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES  */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Дамп структуры для таблица public.booking
CREATE TABLE IF NOT EXISTS "booking" (
	"roomCode" INTEGER NOT NULL DEFAULT '0',
	"beginDate" DATE NOT NULL DEFAULT '2020-01-01',
	"bookingData" JSON NOT NULL DEFAULT '{}'
);

-- Экспортируемые данные не выделены.

-- Дамп структуры для таблица public.clients
CREATE TABLE IF NOT EXISTS "clients" (
	"cliendId" SERIAL,
	"beginDate" DATE NOT NULL DEFAULT '2020-01-01',
	"endDate" DATE NOT NULL DEFAULT '2020-01-02',
	"clientPrepayment" REAL NOT NULL DEFAULT '0',
	"clientData" JSON NOT NULL DEFAULT '{}'
);

-- Экспортируемые данные не выделены.

-- Дамп структуры для таблица public.hotels
CREATE TABLE IF NOT EXISTS "hotels" (
	"hotelCode" SERIAL,
	"hotelName" TEXT NOT NULL DEFAULT 'DefaultName',
	"directorTIN" BIGINT NOT NULL DEFAULT '0',
	"hotelDrector" TEXT NOT NULL DEFAULT 'DefaultDirector',
	"hotelOwner" TEXT NOT NULL DEFAULT 'DefaultOwner',
	"hotelAddress" TEXT NOT NULL DEFAULT 'DefaultAddress'
);

-- Экспортируемые данные не выделены.

-- Дамп структуры для таблица public.posts
CREATE TABLE IF NOT EXISTS "posts" (
	"postCode" SERIAL,
	"postName" TEXT NOT NULL DEFAULT 'DefaultName'
);

-- Экспортируемые данные не выделены.

-- Дамп структуры для таблица public.rooms
CREATE TABLE IF NOT EXISTS "rooms" (
	"roomCode" SERIAL,
	"roomDscription" TEXT NOT NULL DEFAULT 'DefaultDescription',
	"countBeds" SMALLINT NOT NULL DEFAULT '0',
	"costPerDay" REAL NOT NULL DEFAULT '0',
	"roomStatus" TEXT NOT NULL DEFAULT 'free',
	"hotelCode" INTEGER NULL DEFAULT NULL
);

-- Экспортируемые данные не выделены.

-- Дамп структуры для таблица public.staff
CREATE TABLE IF NOT EXISTS "staff" (
	"humanTIN" BIGINT NOT NULL DEFAULT '0',
	"fullName" TEXT NOT NULL DEFAULT 'DefaultFullName',
	"hotelCode" INTEGER NOT NULL DEFAULT '0',
	"postCode" INTEGER NOT NULL DEFAULT '0'
);

-- Экспортируемые данные не выделены.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
