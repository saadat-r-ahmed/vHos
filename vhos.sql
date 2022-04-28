-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 28, 2022 at 10:50 PM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 8.1.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `vhos`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin_data`
--

CREATE TABLE `admin_data` (
  `admin_id` varchar(5) NOT NULL,
  `password` varchar(60) NOT NULL,
  `name` text NOT NULL,
  `email` varchar(60) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin_data`
--

INSERT INTO `admin_data` (`admin_id`, `password`, `name`, `email`) VALUES
('adm1', '81dc9bdb52d04dc20036dbd8313ed055', 'Saadat', 'saadat.r.ahmed@gmail.com'),
('adm2', '81dc9bdb52d04dc20036dbd8313ed055', 'Rubayet', 'rubayet.shareen@gmail.com'),
('adm3', '81dc9bdb52d04dc20036dbd8313ed055', 'Shuborna', 'shu@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `asp_data`
--

CREATE TABLE `asp_data` (
  `asp_id` varchar(60) NOT NULL,
  `name` varchar(60) NOT NULL,
  `owner` varchar(60) NOT NULL,
  `location` varchar(100) NOT NULL,
  `address` varchar(100) NOT NULL,
  `email` varchar(60) NOT NULL,
  `password` varchar(60) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `asp_data`
--

INSERT INTO `asp_data` (`asp_id`, `name`, `owner`, `location`, `address`, `email`, `password`) VALUES
('asp--01', 'garage1', 'Ateya Shubarna', '-26.235360, 28.456050', 'Adabor 2, Road 2, Dhaka,  Bangladesh', 'contact-us@CarZone.com', '1234'),
('asp_4', 'Car Zone', 'Saadat Rafid Ahmed', '-26.235360, 28.456050', 'Dhanmondi 10/A', 'saadat.rafid.ahmed@g.bracu.ac.bd', '1234'),
('asp_5', 'Car Zone', 'Ateya', '-26.235360, 28.456050', 'Adabor 2, Road 2, Dhaka,  Bangladesh', 'saadat.rafid.ahmed@g.bracu.ac.bd', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `cars`
--

CREATE TABLE `cars` (
  `v_id` varchar(60) NOT NULL,
  `asp_id` varchar(60) NOT NULL,
  `vo_mail` varchar(60) NOT NULL,
  `status` varchar(60) NOT NULL DEFAULT 'Received',
  `bill` varchar(300) NOT NULL DEFAULT 'Not Assigned Yet',
  `review` varchar(20) DEFAULT 'Not Assigned Yet'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `cars`
--

INSERT INTO `cars` (`v_id`, `asp_id`, `vo_mail`, `status`, `bill`, `review`) VALUES
('0', 'asp_4', 'xyz@g.bracu.ac.bd', 'completed-50', 'Not Assigned Yet', 'Not Assigned Yet');

-- --------------------------------------------------------

--
-- Table structure for table `owner`
--

CREATE TABLE `owner` (
  `email` varchar(60) NOT NULL,
  `name` varchar(60) NOT NULL,
  `longitude` varchar(60) NOT NULL,
  `latitude` varchar(60) NOT NULL,
  `password` varchar(60) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `owner`
--

INSERT INTO `owner` (`email`, `name`, `longitude`, `latitude`, `password`) VALUES
('saadat.r.ahmed@gmail.com', 'The Boss - Not so', '1223.1351654', '26.11533', '1234'),
('saadat.rafid@gmail.com', 'Saadat Rafid Ahmed', '1223.1351654', '26.11533', '111'),
('xyz@g.bracu.ac.bd', 'xyz', '1223.1351654', '26.11533', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `regular`
--

CREATE TABLE `regular` (
  `request_id` varchar(60) NOT NULL,
  `vo_id` varchar(60) NOT NULL,
  `asp_id` varchar(60) NOT NULL,
  `service_name` varchar(12) NOT NULL,
  `status` varchar(12) NOT NULL DEFAULT 'Pending',
  `time_slot` varchar(60) NOT NULL DEFAULT 'Not Yet Provided',
  `contact` varchar(20) NOT NULL DEFAULT 'Not Yet Provided'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `regular`
--

INSERT INTO `regular` (`request_id`, `vo_id`, `asp_id`, `service_name`, `status`, `time_slot`, `contact`) VALUES
('0', 'saadat@gmail.com', 'asp1', 'Change Air F', 'Pending', 'Not Yet Provided', 'Not Yet Provided'),
('1', 'saadat@gmail.com', 'asp1', 'Color Motor', 'Accepted', '2022-05-06T12:34', '017771521654'),
('2', 'saadat.r.ahmed@gmail.com', 'asp_4', 'Car Cleaning', 'Accepted', '2022-04-30T03:57', '017771521654'),
('3', 'saadat.r.ahmed@gmail.com', 'asp_4', 'Air Filter', 'Accepted', '2022-04-22T03:02', '017771521654'),
('4', 'saadat.r.ahmed@gmail.com', 'asp_4', 'Car Cleaning', 'Accepted', '2022-05-03T14:03', '017771521654'),
('5', 'xyz@g.bracu.ac.bd', 'asp_4', 'Color Motor ', 'Accepted', '2022-05-07T04:22', '017771521654');

-- --------------------------------------------------------

--
-- Table structure for table `request`
--

CREATE TABLE `request` (
  `request_id` varchar(60) NOT NULL,
  `vo_id` varchar(60) NOT NULL,
  `location` varchar(300) NOT NULL,
  `status` varchar(12) NOT NULL DEFAULT 'Pending',
  `asp_id` varchar(60) NOT NULL DEFAULT 'Request Not Accepted',
  `time` varchar(60) NOT NULL DEFAULT 'Request Not Accepted'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `request`
--

INSERT INTO `request` (`request_id`, `vo_id`, `location`, `status`, `asp_id`, `time`) VALUES
('4', 'saadat@gmail.com', 'asdfasf', 'Accepted', 'asp1', '2022-04-28 18:23:55.080110'),
('5', 'saadat@gmail.com', 'xxls\r\n', 'Pending', 'Request Not Accepted', 'Request Not Accepted'),
('6', 'saadat@gmail.com', 'Adabor 2\r\nCar broke Down \r\nRadiator needs to be fixed | inplace', 'Accepted', 'asp1', '2022-04-28 22:06:41.759164'),
('7', 'saadat.r.ahmed@gmail.com', 'Adabor Road 2\r\n01767442826\r\nIn place tire change', 'Accepted', 'asp_4', '2022-04-29 00:00:14.338862'),
('8', 'xyz@g.bracu.ac.bd', 'Adabor Road 2\r\n0175656565\r\nProbable break fail need in-place service ', 'Accepted', 'asp_4', '2022-04-29 02:25:07.203842');

-- --------------------------------------------------------

--
-- Table structure for table `services`
--

CREATE TABLE `services` (
  `asp_id` varchar(60) NOT NULL,
  `service_name` varchar(30) NOT NULL,
  `price` int(10) NOT NULL,
  `description` varchar(300) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `services`
--

INSERT INTO `services` (`asp_id`, `service_name`, `price`, `description`) VALUES
('asp_4', 'Change Air Filter', 1000, 'All expenses included'),
('asp_4', 'Color Motor Bike', 4000, 'Black, Green available\r\n');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin_data`
--
ALTER TABLE `admin_data`
  ADD PRIMARY KEY (`admin_id`);

--
-- Indexes for table `asp_data`
--
ALTER TABLE `asp_data`
  ADD PRIMARY KEY (`asp_id`);

--
-- Indexes for table `cars`
--
ALTER TABLE `cars`
  ADD PRIMARY KEY (`v_id`,`asp_id`,`vo_mail`),
  ADD KEY `asp_id` (`asp_id`),
  ADD KEY `vo_mail` (`vo_mail`);

--
-- Indexes for table `owner`
--
ALTER TABLE `owner`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `regular`
--
ALTER TABLE `regular`
  ADD PRIMARY KEY (`request_id`);

--
-- Indexes for table `request`
--
ALTER TABLE `request`
  ADD PRIMARY KEY (`request_id`);

--
-- Indexes for table `services`
--
ALTER TABLE `services`
  ADD PRIMARY KEY (`asp_id`,`service_name`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `cars`
--
ALTER TABLE `cars`
  ADD CONSTRAINT `cars_ibfk_1` FOREIGN KEY (`asp_id`) REFERENCES `asp_data` (`asp_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `cars_ibfk_2` FOREIGN KEY (`vo_mail`) REFERENCES `owner` (`email`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `services`
--
ALTER TABLE `services`
  ADD CONSTRAINT `services_ibfk_1` FOREIGN KEY (`asp_id`) REFERENCES `asp_data` (`asp_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
