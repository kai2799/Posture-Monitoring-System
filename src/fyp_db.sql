-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 29, 2024 at 08:24 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `fyp_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `log_db`
--

CREATE TABLE `log_db` (
  `Username` varchar(50) NOT NULL,
  `Password` varchar(30) NOT NULL,
  `Birthday` varchar(100) NOT NULL,
  `profile_pic` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `log_db`
--

INSERT INTO `log_db` (`Username`, `Password`, `Birthday`, `profile_pic`) VALUES
('Kai', '1111', '27021999', 'C:/Users/gawoo/F/UI/yes-cheers.gif'),
('User1', '2222', '01042010', 'C:/Users/gawoo/F/UI/Profile.png');

-- --------------------------------------------------------

--
-- Table structure for table `record_db`
--

CREATE TABLE `record_db` (
  `Record_ID` varchar(1000) NOT NULL,
  `Username` varchar(1000) NOT NULL,
  `Record_Date` varchar(1000) NOT NULL,
  `Record_Time` varchar(1000) NOT NULL,
  `Improper_Count` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `record_db`
--

INSERT INTO `record_db` (`Record_ID`, `Username`, `Record_Date`, `Record_Time`, `Improper_Count`) VALUES
('1015', 'Kai', '2024-04-11', '18:46:23', '1'),
('1016', 'Kai', '2024-04-11', '22:27:46', '0'),
('1017', 'Kai', '2024-04-11', '22:27:51', '0'),
('1018', 'Kai', '2024-04-11', '22:45:08', '1'),
('1019', 'Kai', '2024-04-11', '22:55:06', '0'),
('1020', 'Kai', '2024-04-11', '22:58:51', '0'),
('1021', 'Kai', '2024-04-11', '23:13:00', '0'),
('1022', 'Kai', '2024-04-11', '23:34:10', '2'),
('1023', 'Kai', '2024-04-11', '23:34:14', '0'),
('1024', 'Kai', '2024-04-13', '10:35:37', '1'),
('1025', 'Kai', '2024-04-13', '15:52:32', '0'),
('1026', 'Kai', '2024-04-13', '15:52:36', '0'),
('1027', 'User1', '2024-04-13', '16:09:11', '0'),
('1028', 'Kai', '2024-04-14', '23:35:17', '1'),
('1029', 'Kai', '2024-04-14', '23:36:04', '0'),
('1030', 'Kai', '2024-04-14', '23:36:16', '0'),
('1031', 'Kai', '2024-04-14', '23:36:33', '0'),
('1032', 'Kai', '2024-04-14', '23:36:48', '0'),
('1033', 'Kai', '2024-04-14', '23:36:54', '0'),
('1034', 'Kai', '2024-04-15', '11:05:38', '2'),
('1035', 'Kai', '2024-04-15', '11:06:22', '0'),
('1036', 'Kai', '2024-04-15', '11:07:01', '0'),
('1037', 'Kai', '2024-04-15', '11:11:39', '0'),
('1038', 'Kai', '2024-04-15', '11:12:53', '0'),
('1039', 'Kai', '2024-04-15', '11:15:04', '1'),
('1040', 'Kai', '2024-04-15', '22:45:53', '2'),
('1041', 'Kai', '2024-04-17', '14:07:27', '0'),
('1042', 'Kai', '2024-04-17', '14:07:34', '0'),
('1043', 'Kai', '2024-04-17', '14:07:54', '0'),
('1044', 'Kai', '2024-04-17', '14:08:06', '0'),
('1045', 'Kai', '2024-04-17', '14:08:13', '0'),
('1046', 'Kai', '2024-04-17', '14:08:58', '0'),
('1047', 'Kai', '2024-04-17', '14:09:08', '0'),
('1048', 'Kai', '2024-04-17', '14:09:43', '0'),
('1049', 'Kai', '2024-04-17', '14:12:20', '0'),
('1050', 'Kai', '2024-04-17', '14:12:40', '0'),
('1051', 'Kai', '2024-04-17', '14:13:14', '0'),
('1052', 'Kai', '2024-04-17', '14:21:23', '0'),
('1053', 'Kai', '2024-04-17', '14:22:47', '0'),
('1054', 'Kai', '2024-04-17', '14:23:29', '0'),
('1055', 'Kai', '2024-04-17', '14:30:10', '0'),
('1056', 'Kai', '2024-04-17', '14:30:37', '0'),
('1057', 'Kai', '2024-04-17', '14:32:48', '0'),
('1058', 'Kai', '2024-04-17', '14:50:33', '0'),
('1059', 'Kai', '2024-04-17', '14:53:25', '1'),
('1060', 'Kai', '2024-04-17', '14:56:17', '0'),
('1061', 'Kai', '2024-04-17', '14:58:49', '1'),
('1062', 'Kai', '2024-04-17', '15:17:55', '0'),
('1063', 'Kai', '2024-04-17', '15:18:03', '0'),
('1064', 'Kai', '2024-04-17', '15:19:22', '1'),
('1065', 'Kai', '2024-04-17', '15:21:27', '1'),
('1066', 'Kai', '2024-04-17', '15:22:43', '0'),
('1067', 'Kai', '2024-04-17', '15:27:46', '1'),
('1068', 'Kai', '2024-04-17', '15:42:00', '1'),
('1069', 'Kai', '2024-04-17', '15:47:20', '0'),
('1070', 'Kai', '2024-04-17', '16:03:31', '1'),
('1071', 'Kai', '2024-04-17', '16:11:00', '0'),
('1072', 'Kai', '2024-04-24', '10:46:27', '1');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
