-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3307
-- Generation Time: Feb 27, 2025 at 09:56 PM
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
-- Database: `flight_ticket_booking_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `admin_id` int(11) NOT NULL,
  `admin_name` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`admin_id`, `admin_name`, `password`) VALUES
(1, 'jay', '123');

-- --------------------------------------------------------

--
-- Table structure for table `flights`
--

CREATE TABLE `flights` (
  `flight_number` varchar(20) NOT NULL,
  `flight_name` varchar(100) NOT NULL,
  `departure_location` varchar(100) NOT NULL,
  `arrival_location` varchar(100) NOT NULL,
  `departure_airport` varchar(100) NOT NULL,
  `arrival_airport` varchar(100) NOT NULL,
  `departure_date` date NOT NULL,
  `departure_time` time NOT NULL,
  `arrival_date` date NOT NULL,
  `arrival_time` time NOT NULL,
  `duration` varchar(50) NOT NULL,
  `flight_type` enum('Domestic','International') NOT NULL,
  `total_seats` int(11) NOT NULL,
  `available_seats` int(11) NOT NULL,
  `economy_seats` int(11) NOT NULL,
  `business_seats` int(11) NOT NULL,
  `first_class_seats` int(11) NOT NULL,
  `economy_price` decimal(10,2) NOT NULL,
  `business_price` decimal(10,2) NOT NULL,
  `first_class_price` decimal(10,2) NOT NULL,
  `status` enum('Scheduled','Delayed','Cancelled') DEFAULT 'Scheduled'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `flights`
--

INSERT INTO `flights` (`flight_number`, `flight_name`, `departure_location`, `arrival_location`, `departure_airport`, `arrival_airport`, `departure_date`, `departure_time`, `arrival_date`, `arrival_time`, `duration`, `flight_type`, `total_seats`, `available_seats`, `economy_seats`, `business_seats`, `first_class_seats`, `economy_price`, `business_price`, `first_class_price`, `status`) VALUES
('6E702', 'IndiGo 702', 'Chennai', 'Hyderabad', 'Chennai Intl', 'Rajiv Gandhi Intl', '2025-03-05', '09:30:00', '2025-03-05', '11:00:00', '1h 30m', 'Domestic', 180, 180, 160, 10, 10, 3500.00, 9000.00, 16000.00, 'Scheduled'),
('6E703', 'IndiGo 703', 'Hyderabad', 'Chennai', 'Rajiv Gandhi Intl', 'Chennai Intl', '2025-03-05', '13:30:00', '2025-03-05', '15:00:00', '1h 30m', 'Domestic', 180, 180, 160, 10, 10, 3500.00, 9000.00, 16000.00, 'Scheduled'),
('6E707', 'IndiGo 707', 'Lucknow', 'Hyderabad', 'Chaudhary Charan Singh Intl', 'Rajiv Gandhi Intl', '2025-03-10', '10:45:00', '2025-03-10', '13:15:00', '2h 30m', 'Domestic', 180, 180, 160, 10, 10, 3600.00, 8800.00, 15500.00, 'Scheduled'),
('6E708', 'IndiGo 708', 'Hyderabad', 'Lucknow', 'Rajiv Gandhi Intl', 'Chaudhary Charan Singh Intl', '2025-03-10', '14:45:00', '2025-03-10', '17:15:00', '2h 30m', 'Domestic', 180, 180, 160, 10, 10, 3600.00, 8800.00, 15500.00, 'Scheduled'),
('6E808', 'IndiGo 808', 'Bangalore', 'Pune', 'Kempegowda Intl', 'Pune Intl', '2025-03-15', '09:45:00', '2025-03-15', '11:15:00', '1h 30m', 'Domestic', 180, 180, 160, 10, 10, 3500.00, 8900.00, 16000.00, 'Scheduled'),
('6E809', 'IndiGo 809', 'Pune', 'Bangalore', 'Pune Intl', 'Kempegowda Intl', '2025-03-15', '12:45:00', '2025-03-15', '14:15:00', '1h 30m', 'Domestic', 180, 180, 160, 10, 10, 3500.00, 8900.00, 16000.00, 'Scheduled'),
('AF302', 'Air France 302', 'Paris', 'New York', 'Charles de Gaulle', 'JFK Intl', '2025-02-23', '10:00:00', '2025-02-23', '13:30:00', '8h 30m', 'International', 280, 280, 260, 10, 10, 32000.00, 60000.00, 100000.00, 'Scheduled'),
('AI101', 'qq', 'qq', 'qq', 'qq', 'qq', '1111-11-11', '11:11:11', '1111-11-11', '11:11:11', '2h 3m', 'Domestic', 100, 93, 76, 9, 8, 1000.00, 2000.00, 3000.00, 'Delayed'),
('AI102', 'air india', 'delhi', 'mumbai', 'delhi airport', 'mumbai airport', '2025-02-27', '12:00:00', '2025-02-28', '13:12:00', '5h 4m', 'Domestic', 100, 63, 60, 0, 3, 5000.00, 20000.00, 40000.00, 'Scheduled'),
('AI103', 'air india', 'Mumbai', 'Delhi', 'mumbai airport', 'delhi airport', '2025-01-01', '12:00:00', '2025-01-02', '22:00:00', '5h 3m', 'Domestic', 100, 85, 75, 4, 6, 5000.00, 15000.00, 30000.00, 'Scheduled'),
('AI104', 'Air India 101', 'Mumbai', 'Delhi', 'Chhatrapati Shivaji Intl', 'Indira Gandhi Intl', '2025-03-01', '08:00:00', '2025-03-01', '10:30:00', '2h 30m', 'Domestic', 150, 129, 120, 9, 10, 5000.00, 12000.00, 20000.00, 'Scheduled'),
('AI201', 'Air India 201', 'Mumbai', 'Delhi', 'Chhatrapati Shivaji Intl', 'Indira Gandhi Intl', '2025-02-15', '07:00:00', '2025-02-15', '09:30:00', '2h 30m', 'Domestic', 180, 180, 160, 10, 10, 4500.00, 11000.00, 19000.00, 'Scheduled'),
('AI202', 'Air India 202', 'Hyderabad', 'Bangalore', 'Rajiv Gandhi Intl', 'Kempegowda Intl', '2025-02-20', '08:30:00', '2025-02-20', '10:00:00', '1h 30m', 'Domestic', 180, 180, 160, 10, 10, 3200.00, 8500.00, 15000.00, 'Scheduled'),
('AI303', 'Air India 303', 'Mumbai', 'Singapore', 'Chhatrapati Shivaji Intl', 'Changi Intl', '2025-02-27', '08:20:00', '2025-02-27', '16:30:00', '6h 10m', 'International', 220, 220, 200, 10, 10, 25000.00, 47000.00, 85000.00, 'Scheduled'),
('AI401', 'Air India 401', 'Delhi', 'Bangalore', 'Indira Gandhi Intl', 'Kempegowda Intl', '2025-03-03', '06:00:00', '2025-03-03', '08:45:00', '2h 45m', 'Domestic', 180, 180, 160, 10, 10, 4500.00, 10000.00, 18000.00, 'Scheduled'),
('AI402', 'Air India 402', 'Bangalore', 'Delhi', 'Kempegowda Intl', 'Indira Gandhi Intl', '2025-03-03', '10:00:00', '2025-03-03', '12:45:00', '2h 45m', 'Domestic', 180, 180, 160, 10, 10, 4500.00, 10000.00, 18000.00, 'Scheduled'),
('AI505', 'Air India 505', 'Bangalore', 'Chandigarh', 'Kempegowda Intl', 'Chandigarh Intl', '2025-03-08', '08:00:00', '2025-03-08', '10:45:00', '2h 45m', 'Domestic', 180, 180, 160, 10, 10, 5000.00, 10500.00, 19000.00, 'Scheduled'),
('AI506', 'Air India 506', 'Chandigarh', 'Bangalore', 'Chandigarh Intl', 'Kempegowda Intl', '2025-03-08', '11:00:00', '2025-03-08', '13:45:00', '2h 45m', 'Domestic', 180, 180, 160, 10, 10, 5000.00, 10500.00, 19000.00, 'Scheduled'),
('AI606', 'Air India 606', 'Ahmedabad', 'Kolkata', 'Sardar Vallabhbhai Patel Intl', 'Netaji Subhash Chandra Bose Intl', '2025-03-13', '07:30:00', '2025-03-13', '10:15:00', '2h 45m', 'Domestic', 180, 180, 160, 10, 10, 4400.00, 9900.00, 17500.00, 'Scheduled'),
('AI607', 'Air India 607', 'Kolkata', 'Ahmedabad', 'Netaji Subhash Chandra Bose Intl', 'Sardar Vallabhbhai Patel Intl', '2025-03-13', '13:30:00', '2025-03-13', '16:15:00', '2h 45m', 'Domestic', 180, 180, 160, 10, 10, 4400.00, 9900.00, 17500.00, 'Scheduled'),
('AI707', 'Air India 707', 'Delhi', 'Mumbai', 'Indira Gandhi Intl', 'Chhatrapati Shivaji Intl', '2025-03-18', '15:30:00', '2025-03-18', '18:00:00', '2h 30m', 'Domestic', 180, 180, 160, 10, 10, 4700.00, 10200.00, 18000.00, 'Scheduled'),
('AI708', 'Air India 708', 'Mumbai', 'Delhi', 'Chhatrapati Shivaji Intl', 'Indira Gandhi Intl', '2025-03-18', '18:30:00', '2025-03-18', '21:00:00', '2h 30m', 'Domestic', 180, 180, 160, 10, 10, 4700.00, 10200.00, 18000.00, 'Scheduled'),
('BA250', 'British Airways 250', 'Delhi', 'London', 'Indira Gandhi Intl', 'Heathrow Intl', '2025-03-05', '22:00:00', '2025-03-06', '06:00:00', '9h 30m', 'International', 200, 180, 170, 20, 10, 25000.00, 45000.00, 80000.00, 'Scheduled'),
('BA305', 'British Airways 305', 'Delhi', 'London', 'Indira Gandhi Intl', 'Heathrow Intl', '2025-02-16', '23:30:00', '2025-02-17', '07:00:00', '9h 30m', 'International', 250, 250, 230, 10, 10, 26000.00, 48000.00, 85000.00, 'Scheduled'),
('BA306', 'British Airways 306', 'Mumbai', 'London', 'Chhatrapati Shivaji Intl', 'Heathrow Intl', '2025-02-21', '22:45:00', '2025-02-22', '06:30:00', '9h 45m', 'International', 260, 260, 240, 10, 10, 26500.00, 49000.00, 87000.00, 'Scheduled'),
('BA509', 'British Airways 509', 'London', 'New York', 'Heathrow Intl', 'JFK Intl', '2025-02-28', '11:15:00', '2025-02-28', '14:30:00', '7h 15m', 'International', 270, 270, 250, 10, 10, 35000.00, 62000.00, 110000.00, 'Scheduled'),
('CX411', 'Cathay Pacific 411', 'Hong Kong', 'San Francisco', 'Hong Kong Intl', 'SFO Intl', '2025-03-01', '23:30:00', '2025-03-02', '14:00:00', '12h 30m', 'International', 300, 300, 280, 10, 10, 37000.00, 64000.00, 105000.00, 'Scheduled'),
('DL610', 'Delta Airlines 610', 'Los Angeles', 'Tokyo', 'LAX Intl', 'Narita Intl', '0000-00-00', '09:00:00', '0000-00-00', '17:30:00', '11h 30m', 'International', 280, 280, 260, 10, 10, 39000.00, 68000.00, 115000.00, 'Scheduled'),
('EK305', 'Emirates 305', 'Dubai', 'Singapore', 'Dubai Intl', 'Changi Intl', '2025-02-25', '22:50:00', '2025-02-26', '11:00:00', '8h 10m', 'International', 260, 260, 240, 10, 10, 27000.00, 51000.00, 88000.00, 'Scheduled'),
('EK501', 'Emirates 501', 'Mumbai', 'Dubai', 'Chhatrapati Shivaji Intl', 'Dubai Intl', '2025-03-12', '21:30:00', '2025-03-13', '00:30:00', '3h 00m', 'International', 250, 229, 220, 19, 10, 15000.00, 30000.00, 60000.00, 'Scheduled'),
('EK802', 'Emirates 802', 'Bangalore', 'Dubai', 'Kempegowda Intl', 'Dubai Intl', '2025-02-18', '22:00:00', '2025-02-19', '01:30:00', '3h 30m', 'International', 220, 220, 200, 10, 10, 15500.00, 32000.00, 62000.00, 'Scheduled'),
('G8104', 'GoAir 104', 'Mumbai', 'Ahmedabad', 'Chhatrapati Shivaji Intl', 'Sardar Vallabhbhai Patel Intl', '2025-03-07', '13:45:00', '2025-03-07', '15:15:00', '1h 30m', 'Domestic', 180, 180, 160, 10, 10, 3000.00, 8200.00, 15000.00, 'Scheduled'),
('G8105', 'GoAir 105', 'Ahmedabad', 'Mumbai', 'Sardar Vallabhbhai Patel Intl', 'Chhatrapati Shivaji Intl', '2025-03-07', '18:45:00', '2025-03-07', '20:15:00', '1h 30m', 'Domestic', 180, 180, 160, 10, 10, 3000.00, 8200.00, 15000.00, 'Scheduled'),
('G8110', 'GoAir 110', 'Bangalore', 'Chennai', 'Kempegowda Intl', 'Chennai Intl', '2025-03-12', '18:30:00', '2025-03-12', '20:00:00', '1h 30m', 'Domestic', 180, 180, 160, 10, 10, 2800.00, 8100.00, 14500.00, 'Scheduled'),
('G8111', 'GoAir 111', 'Chennai', 'Bangalore', 'Chennai Intl', 'Kempegowda Intl', '2025-03-12', '22:30:00', '2025-03-12', '00:00:00', '1h 30m', 'Domestic', 180, 180, 160, 10, 10, 2800.00, 8100.00, 14500.00, 'Scheduled'),
('G8120', 'GoAir 120', 'Chennai', 'Bangalore', 'Chennai Intl', 'Kempegowda Intl', '2025-03-17', '20:00:00', '2025-03-17', '21:30:00', '1h 30m', 'Domestic', 180, 180, 160, 10, 10, 3100.00, 8300.00, 15000.00, 'Scheduled'),
('G8121', 'GoAir 121', 'Bangalore', 'Chennai', 'Kempegowda Intl', 'Chennai Intl', '2025-03-17', '07:00:00', '2025-03-17', '08:30:00', '1h 30m', 'Domestic', 180, 180, 160, 10, 10, 3100.00, 8300.00, 15000.00, 'Scheduled'),
('LH508', 'Lufthansa 508', 'Frankfurt', 'Toronto', 'Frankfurt Intl', 'Pearson Intl', '2025-02-26', '13:30:00', '2025-02-26', '16:45:00', '8h 15m', 'International', 240, 240, 220, 10, 10, 31000.00, 57000.00, 96000.00, 'Scheduled'),
('LH721', 'Lufthansa 721', 'Delhi', 'Munich', 'Indira Gandhi Intl', 'Munich Intl', '2025-02-19', '13:15:00', '2025-02-19', '19:15:00', '8h 00m', 'International', 230, 230, 210, 10, 10, 28000.00, 52000.00, 92000.00, 'Scheduled'),
('LH760', 'Lufthansa 760', 'Delhi', 'Frankfurt', 'Indira Gandhi Intl', 'Frankfurt Intl', '2025-03-15', '13:00:00', '2025-03-15', '19:00:00', '8h 00m', 'International', 220, 200, 190, 20, 10, 27000.00, 50000.00, 90000.00, 'Scheduled'),
('QF101', 'Qantas 101', 'Sydney', 'Los Angeles', 'Sydney Intl', 'LAX Intl', '2025-02-22', '20:30:00', '2025-02-22', '10:30:00', '14h 00m', 'International', 300, 300, 280, 10, 10, 45000.00, 75000.00, 125000.00, 'Scheduled'),
('QR507', 'Qatar Airways 507', 'Doha', 'London', 'Hamad Intl', 'Heathrow Intl', '2025-02-24', '01:15:00', '2025-02-24', '06:45:00', '6h 30m', 'International', 250, 250, 230, 10, 10, 29000.00, 54000.00, 95000.00, 'Scheduled'),
('SG401', 'SpiceJet 401', 'Bangalore', 'Kolkata', 'Kempegowda Intl', 'Netaji Subhash Chandra Bose Intl', '2025-03-10', '06:30:00', '2025-03-10', '09:15:00', '2h 45m', 'Domestic', 180, 150, 140, 20, 20, 4000.00, 10000.00, 18000.00, 'Scheduled'),
('SG510', 'SpiceJet 510', 'Chennai', 'Kolkata', 'Chennai Intl', 'Netaji Subhash Chandra Bose Intl', '2025-02-17', '06:45:00', '2025-02-17', '09:15:00', '2h 30m', 'Domestic', 180, 180, 160, 10, 10, 4200.00, 9500.00, 17000.00, 'Scheduled'),
('SG601', 'SpiceJet 601', 'Kolkata', 'Mumbai', 'Netaji Subhash Chandra Bose Intl', 'Chhatrapati Shivaji Intl', '2025-03-04', '07:15:00', '2025-03-04', '10:00:00', '2h 45m', 'Domestic', 180, 180, 160, 10, 10, 4000.00, 9500.00, 17000.00, 'Scheduled'),
('SG602', 'SpiceJet 602', 'Mumbai', 'Kolkata', 'Chhatrapati Shivaji Intl', 'Netaji Subhash Chandra Bose Intl', '2025-03-04', '11:15:00', '2025-03-04', '14:00:00', '2h 45m', 'Domestic', 180, 180, 160, 10, 10, 4000.00, 9500.00, 17000.00, 'Scheduled'),
('SG606', 'SpiceJet 606', 'Jaipur', 'Mumbai', 'Jaipur Intl', 'Chhatrapati Shivaji Intl', '2025-03-09', '06:30:00', '2025-03-09', '08:30:00', '2h 00m', 'Domestic', 180, 180, 160, 10, 10, 4000.00, 9200.00, 17000.00, 'Scheduled'),
('SG607', 'SpiceJet 607', 'Mumbai', 'Jaipur', 'Chhatrapati Shivaji Intl', 'Jaipur Intl', '2025-03-09', '08:30:00', '2025-03-09', '10:30:00', '2h 00m', 'Domestic', 180, 180, 160, 10, 10, 4000.00, 9200.00, 17000.00, 'Scheduled'),
('SG707', 'SpiceJet 707', 'Mumbai', 'Delhi', 'Chhatrapati Shivaji Intl', 'Indira Gandhi Intl', '2025-03-14', '12:00:00', '2025-03-14', '14:30:00', '2h 30m', 'Domestic', 180, 179, 160, 9, 10, 4600.00, 10300.00, 18500.00, 'Scheduled'),
('SG708', 'SpiceJet 708', 'Delhi', 'Mumbai', 'Indira Gandhi Intl', 'Chhatrapati Shivaji Intl', '2025-03-14', '17:00:00', '2025-03-14', '19:30:00', '2h 30m', 'Domestic', 180, 173, 158, 6, 9, 4600.00, 10300.00, 18500.00, 'Scheduled'),
('SG808', 'SpiceJet 808', 'Kolkata', 'Hyderabad', 'Netaji Subhash Chandra Bose Intl', 'Rajiv Gandhi Intl', '2025-03-19', '11:30:00', '2025-03-19', '14:00:00', '2h 30m', 'Domestic', 180, 180, 160, 10, 10, 4200.00, 9500.00, 17000.00, 'Scheduled'),
('SG809', 'SpiceJet 809', 'Hyderabad', 'Kolkata', 'Rajiv Gandhi Intl', 'Netaji Subhash Chandra Bose Intl', '2025-03-19', '15:30:00', '2025-03-19', '18:00:00', '2h 30m', 'Domestic', 180, 180, 160, 10, 10, 4200.00, 9500.00, 17000.00, 'Scheduled'),
('SQ512', 'Singapore Airlines 512', 'Singapore', 'Sydney', 'Changi Intl', 'Sydney Intl', '2025-03-02', '18:45:00', '2025-03-03', '07:00:00', '8h 15m', 'International', 290, 290, 270, 10, 10, 36000.00, 63000.00, 102000.00, 'Scheduled'),
('UK803', 'Vistara 803', 'Pune', 'Delhi', 'Pune Intl', 'Indira Gandhi Intl', '2025-03-06', '21:00:00', '2025-03-06', '23:30:00', '2h 30m', 'Domestic', 180, 178, 159, 10, 9, 4800.00, 10200.00, 18500.00, 'Scheduled'),
('UK804', 'Vistara 804', 'Delhi', 'Pune', 'Indira Gandhi Intl', 'Pune Intl', '2025-03-06', '16:00:00', '2025-03-06', '18:30:00', '2h 30m', 'Domestic', 180, 178, 160, 8, 10, 4800.00, 10200.00, 18500.00, 'Scheduled'),
('UK808', 'Vistara 808', 'Delhi', 'Goa', 'Indira Gandhi Intl', 'Goa Intl', '2025-03-11', '16:15:00', '2025-03-11', '18:45:00', '2h 30m', 'Domestic', 180, 176, 159, 8, 9, 4700.00, 10100.00, 18000.00, 'Scheduled'),
('UK809', 'Vistara 809', 'Goa', 'Delhi', 'Goa Intl', 'Indira Gandhi Intl', '2025-03-11', '19:15:00', '2025-03-11', '21:45:00', '2h 30m', 'Domestic', 180, 178, 160, 8, 10, 4700.00, 10100.00, 18000.00, 'Scheduled'),
('UK909', 'Vistara 909', 'Hyderabad', 'Delhi', 'Rajiv Gandhi Intl', 'Indira Gandhi Intl', '2025-03-16', '22:30:00', '2025-03-16', '01:00:00', '2h 30m', 'Domestic', 180, 180, 160, 10, 10, 4500.00, 9800.00, 17200.00, 'Scheduled'),
('UK910', 'Vistara 910', 'Delhi', 'Hyderabad', 'Indira Gandhi Intl', 'Rajiv Gandhi Intl', '2025-03-16', '01:30:00', '2025-03-16', '04:00:00', '2h 30m', 'Domestic', 180, 180, 160, 10, 10, 4500.00, 9800.00, 17200.00, 'Scheduled');

-- --------------------------------------------------------

--
-- Table structure for table `tickets`
--

CREATE TABLE `tickets` (
  `ticket_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `flight_number` varchar(20) NOT NULL,
  `booking_date` date NOT NULL,
  `booking_time` time NOT NULL,
  `seat_class` enum('Economy','Business','First Class') NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `seat_number` varchar(10) NOT NULL,
  `ticket_status` enum('Confirmed','Cancelled') DEFAULT 'Confirmed'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tickets`
--

INSERT INTO `tickets` (`ticket_id`, `user_id`, `flight_number`, `booking_date`, `booking_time`, `seat_class`, `price`, `seat_number`, `ticket_status`) VALUES
(6, 2, 'AI101', '2025-02-26', '17:06:16', 'Economy', 1000.00, 'C1', 'Confirmed'),
(7, 2, 'AI101', '2025-02-26', '17:06:16', 'First Class', 3000.00, 'A2', 'Cancelled'),
(8, 2, 'AI101', '2025-02-26', '17:06:16', 'Economy', 1000.00, 'H3', 'Confirmed'),
(9, 2, 'AI101', '2025-02-26', '17:06:16', 'First Class', 3000.00, 'A1', 'Confirmed'),
(14, 2, 'AI102', '2025-02-26', '18:43:27', 'Economy', 5000.00, 'C1', 'Confirmed'),
(15, 2, 'AI103', '2025-02-26', '18:43:27', 'First Class', 30000.00, 'A1', 'Cancelled'),
(18, 2, 'AI102', '2025-02-26', '19:16:55', 'Economy', 5000.00, 'C2', 'Confirmed'),
(19, 2, 'AI103', '2025-02-26', '19:16:55', 'Economy', 5000.00, 'C1', 'Confirmed'),
(23, 2, 'AI102', '2025-02-26', '19:31:39', 'First Class', 40000.00, 'A1', 'Confirmed'),
(24, 2, 'AI102', '2025-02-26', '19:31:39', 'Economy', 5000.00, 'C3', 'Confirmed'),
(25, 2, 'AI103', '2025-02-26', '19:31:39', 'First Class', 30000.00, 'A1', 'Confirmed'),
(26, 2, 'AI102', '2025-02-26', '19:31:39', 'Business', 20000.00, 'B1', 'Confirmed'),
(73, 2, 'AI102', '2025-02-27', '09:57:35', 'Economy', 5000.00, 'C4', 'Confirmed'),
(74, 2, 'AI102', '2025-02-27', '10:00:18', 'Economy', 5000.00, 'C5', 'Confirmed'),
(75, 2, 'AI102', '2025-02-27', '10:02:31', 'Economy', 5000.00, 'C6', 'Confirmed'),
(76, 2, 'AI102', '2025-02-27', '10:08:05', 'Economy', 5000.00, 'C7', 'Confirmed'),
(77, 2, 'AI102', '2025-02-27', '10:13:58', 'Economy', 5000.00, 'C8', 'Confirmed'),
(78, 2, 'AI102', '2025-02-27', '10:17:23', 'Economy', 5000.00, 'C9', 'Confirmed'),
(79, 2, 'AI102', '2025-02-27', '10:21:31', 'Economy', 5000.00, 'C10', 'Confirmed'),
(80, 2, 'AI102', '2025-02-27', '10:41:34', 'First Class', 40000.00, 'A2', 'Confirmed'),
(81, 2, 'AI103', '2025-02-27', '10:41:34', 'Business', 15000.00, 'B1', 'Confirmed'),
(82, 2, 'AI102', '2025-02-27', '10:44:13', 'Economy', 5000.00, 'D1', 'Confirmed'),
(83, 2, 'AI103', '2025-02-27', '10:44:13', 'Business', 15000.00, 'B2', 'Confirmed'),
(86, 2, 'AI102', '2025-02-27', '12:12:47', 'Economy', 5000.00, 'D2', 'Confirmed'),
(87, 2, 'AI103', '2025-02-27', '12:12:47', 'Business', 15000.00, 'B3', 'Confirmed'),
(88, 2, 'AI102', '2025-02-27', '12:12:47', 'Economy', 5000.00, 'D3', 'Confirmed'),
(89, 2, 'AI102', '2025-02-27', '12:12:47', 'Business', 20000.00, 'B2', 'Confirmed'),
(90, 2, 'AI102', '2025-02-27', '12:12:47', 'Business', 20000.00, 'B3', 'Confirmed'),
(91, 2, 'AI102', '2025-02-27', '12:12:47', 'Business', 20000.00, 'B4', 'Confirmed'),
(92, 2, 'AI102', '2025-02-27', '12:12:47', 'First Class', 40000.00, 'A3', 'Confirmed'),
(93, 2, 'AI102', '2025-02-27', '12:12:47', 'Economy', 5000.00, 'D4', 'Confirmed'),
(94, 2, 'AI103', '2025-02-27', '12:12:47', 'First Class', 30000.00, 'A2', 'Confirmed'),
(95, 2, 'AI102', '2025-02-27', '12:12:47', 'Business', 20000.00, 'B5', 'Confirmed'),
(96, 2, 'AI103', '2025-02-27', '12:12:47', 'Economy', 5000.00, 'C2', 'Confirmed'),
(97, 2, 'AI102', '2025-02-27', '12:12:47', 'First Class', 40000.00, 'A4', 'Confirmed'),
(99, 2, 'AI102', '2025-02-27', '12:45:27', 'Business', 20000.00, 'B6', 'Confirmed'),
(101, 2, 'AI103', '2025-02-27', '12:54:41', 'First Class', 30000.00, 'A3', 'Confirmed'),
(103, 2, 'AI103', '2025-02-27', '12:54:41', 'Economy', 5000.00, 'C3', 'Confirmed'),
(104, 2, 'AI102', '2025-02-27', '13:09:56', 'Economy', 5000.00, 'D5', 'Cancelled'),
(105, 2, 'AI103', '2025-02-27', '13:09:56', 'Economy', 5000.00, 'C4', 'Cancelled'),
(106, 2, 'AI102', '2025-02-28', '00:27:23', 'Economy', 5000.00, 'H1', 'Confirmed'),
(107, 2, 'AI102', '2025-02-28', '00:36:28', 'Economy', 5000.00, 'D5', 'Confirmed'),
(108, 2, 'AI103', '2025-02-28', '00:36:28', 'First Class', 30000.00, 'A4', 'Confirmed'),
(109, 2, 'AI102', '2025-02-28', '00:36:28', 'First Class', 40000.00, 'A5', 'Confirmed'),
(110, 2, 'EK501', '2025-02-28', '00:36:28', 'Business', 30000.00, 'B1', 'Confirmed'),
(111, 3, 'UK808', '2025-02-28', '01:14:55', 'First Class', 18000.00, 'A1', 'Confirmed'),
(112, 3, 'UK809', '2025-02-28', '01:14:55', 'Business', 10100.00, 'B1', 'Confirmed'),
(113, 3, 'UK808', '2025-02-28', '01:14:55', 'Economy', 4700.00, 'C1', 'Confirmed'),
(114, 3, 'SG708', '2025-02-28', '01:14:55', 'Business', 10300.00, 'B1', 'Confirmed'),
(115, 3, 'SG708', '2025-02-28', '01:52:30', 'Economy', 4600.00, 'C1', 'Confirmed'),
(116, 3, 'SG708', '2025-02-28', '01:58:21', 'First Class', 18500.00, 'A1', 'Confirmed'),
(117, 3, 'SG708', '2025-02-28', '01:58:21', 'Economy', 4600.00, 'C2', 'Confirmed'),
(118, 3, 'SG707', '2025-02-28', '01:58:21', 'Business', 10300.00, 'B1', 'Confirmed'),
(119, 3, 'UK808', '2025-02-28', '01:58:21', 'Business', 10100.00, 'B1', 'Confirmed'),
(120, 3, 'UK809', '2025-02-28', '01:58:21', 'Business', 10100.00, 'B2', 'Confirmed'),
(121, 3, 'UK804', '2025-02-28', '01:58:21', 'Business', 10200.00, 'B1', 'Confirmed'),
(122, 3, 'UK803', '2025-02-28', '01:58:21', 'First Class', 18500.00, 'A1', 'Confirmed'),
(123, 3, 'UK803', '2025-02-28', '01:58:21', 'Economy', 4800.00, 'C1', 'Confirmed'),
(124, 3, 'UK804', '2025-02-28', '01:58:21', 'Business', 10200.00, 'B2', 'Confirmed'),
(125, 3, 'UK808', '2025-02-28', '01:58:21', 'Business', 10100.00, 'B2', 'Confirmed'),
(126, 3, 'SG708', '2025-02-28', '01:58:21', 'Business', 10300.00, 'B2', 'Confirmed'),
(127, 3, 'SG708', '2025-02-28', '01:58:21', 'Business', 10300.00, 'B2', 'Confirmed'),
(128, 3, 'AI708', '2025-02-28', '01:58:21', 'Business', 10200.00, 'B1', 'Cancelled');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `user_name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `phone_number` varchar(15) NOT NULL,
  `passport_number` varchar(20) DEFAULT NULL,
  `gender` enum('Male','Female','Other') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `user_name`, `email`, `password`, `address`, `phone_number`, `passport_number`, `gender`) VALUES
(2, 'jay', 'jay@gmail.com', '123', '1234sdf', '123123432', '121egev', 'Male'),
(3, 'Rahul Sharma', 'rahul.sharma@example.com', '123', 'Mumbai, India', '9876543210', 'A12345678', 'Male'),
(4, 'Aisha Khan', 'aisha.khan@example.com', '234', 'Delhi, India', '9988776655', 'B98765432', 'Female'),
(5, 'John Doe', 'john.doe@example.com', '345', 'London, UK', '447700900123', 'C12378945', 'Male'),
(6, 'Samantha Lee', 'samantha.lee@example.com', '456', 'New York, USA', '19175551234', 'D56743289', 'Female'),
(7, 'Amit Patel', 'amit.patel@example.com', '567', 'Ahmedabad, India', '9876123456', 'E76543210', 'Male');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`admin_id`);

--
-- Indexes for table `flights`
--
ALTER TABLE `flights`
  ADD PRIMARY KEY (`flight_number`);

--
-- Indexes for table `tickets`
--
ALTER TABLE `tickets`
  ADD PRIMARY KEY (`ticket_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `flight_number` (`flight_number`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `phone_number` (`phone_number`),
  ADD UNIQUE KEY `passport_number` (`passport_number`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tickets`
--
ALTER TABLE `tickets`
  MODIFY `ticket_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=129;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `tickets`
--
ALTER TABLE `tickets`
  ADD CONSTRAINT `tickets_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `tickets_ibfk_2` FOREIGN KEY (`flight_number`) REFERENCES `flights` (`flight_number`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
