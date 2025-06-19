-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 19, 2025 at 01:03 PM
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
-- Database: `cardio_app`
--

-- --------------------------------------------------------

--
-- Table structure for table `diagnosis`
--

CREATE TABLE `diagnosis` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `age` float DEFAULT NULL,
  `gender` tinyint(4) DEFAULT NULL,
  `heart_rate` float DEFAULT NULL,
  `systolic_bp` float DEFAULT NULL,
  `diastolic_bp` float DEFAULT NULL,
  `blood_sugar` float DEFAULT NULL,
  `ck_mb` float DEFAULT NULL,
  `troponin` float DEFAULT NULL,
  `result` varchar(100) DEFAULT NULL,
  `cluster` int(11) DEFAULT NULL,
  `risk_level` varchar(50) DEFAULT NULL,
  `recommendation` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `diagnosis`
--

INSERT INTO `diagnosis` (`id`, `user_id`, `age`, `gender`, `heart_rate`, `systolic_bp`, `diastolic_bp`, `blood_sugar`, `ck_mb`, `troponin`, `result`, `cluster`, `risk_level`, `recommendation`, `created_at`) VALUES
(1, 1, 23, 1, 120, 65, 23, 90, 32, 12, 'Negative', 2, 'High Risk', 'RUJUK SEGERA ke spesialis jantung. Kondisi berisiko tinggi!', '2025-06-08 06:21:25'),
(2, 1, 23, 1, 120, 65, 23, 90, 32, 12, 'Negative', 2, 'High Risk', 'RUJUK SEGERA ke spesialis jantung. Kondisi berisiko tinggi!', '2025-06-08 06:22:38'),
(3, 1, 32, 1, 42, 12, 12, 12, 12, 12, 'Negative', 2, 'High Risk', 'RUJUK SEGERA ke spesialis jantung. Kondisi berisiko tinggi!', '2025-06-08 07:20:35'),
(4, 1, 24, 1, 94, 95, 83, 120, 1, 0, 'Negative', 0, 'Low Risk', 'Tidak memerlukan rujukan spesialis jantung. Rutin pemeriksaan kesehatan umum.', '2025-06-08 07:26:44'),
(5, 1, 32, 0, 120, 160, 83, 120, 1.3, 0.021, 'Negative', 1, 'Moderate Risk', 'Direkomendasikan rujukan ke spesialis jantung untuk evaluasi lebih lanjut.', '2025-06-08 07:29:52'),
(6, 1, 32, 0, 120, 160, 83, 120, 1.3, 0.021, 'Negative', 1, 'Moderate Risk', 'Direkomendasikan rujukan ke spesialis jantung untuk evaluasi lebih lanjut.', '2025-06-08 07:31:01'),
(7, 1, 32, 0, 120, 160, 83, 120, 1.3, 0.021, 'Negative', 1, 'Moderate Risk', 'Direkomendasikan rujukan ke spesialis jantung untuk evaluasi lebih lanjut.', '2025-06-08 07:32:48'),
(8, 1, 32, 0, 120, 160, 83, 120, 1.3, 0.021, 'Negative', 1, 'Moderate Risk', 'Direkomendasikan rujukan ke spesialis jantung untuk evaluasi lebih lanjut.', '2025-06-08 07:34:15'),
(9, 1, 32, 0, 120, 160, 83, 120, 1.3, 0.021, 'Negative', 1, 'Moderate Risk', 'Direkomendasikan rujukan ke spesialis jantung untuk evaluasi lebih lanjut.', '2025-06-08 07:34:30'),
(10, 1, 32, 0, 120, 160, 83, 120, 1.3, 0.021, 'Negative', 1, 'Moderate Risk', 'Direkomendasikan rujukan ke spesialis jantung untuk evaluasi lebih lanjut.', '2025-06-08 07:36:07'),
(11, 1, 32, 0, 120, 160, 83, 120, 1.3, 0.021, 'Negative', 1, 'Moderate Risk', 'Direkomendasikan rujukan ke spesialis jantung untuk evaluasi lebih lanjut.', '2025-06-08 07:36:30'),
(12, 1, 32, 0, 120, 160, 83, 120, 1.3, 0.021, 'Negative', 1, 'Moderate Risk', 'Direkomendasikan rujukan ke spesialis jantung untuk evaluasi lebih lanjut.', '2025-06-08 07:36:36'),
(13, 1, 32, 0, 120, 160, 83, 120, 1.3, 0.021, 'Negative', 1, 'Moderate Risk', 'Direkomendasikan rujukan ke spesialis jantung untuk evaluasi lebih lanjut.', '2025-06-08 07:36:41'),
(14, 1, 32, 0, 120, 160, 83, 120, 1.3, 0.021, 'Negative', 1, 'Moderate Risk', 'Direkomendasikan rujukan ke spesialis jantung untuk evaluasi lebih lanjut.', '2025-06-08 07:36:50'),
(15, 1, 32, 0, 120, 160, 83, 120, 1.3, 0.021, 'Negative', 1, 'Moderate Risk', 'Direkomendasikan rujukan ke spesialis jantung untuk evaluasi lebih lanjut.', '2025-06-08 07:37:15'),
(16, 1, 32, 0, 120, 160, 83, 120, 1.3, 0.021, 'Negative', 1, 'Moderate Risk', 'Direkomendasikan rujukan ke spesialis jantung untuk evaluasi lebih lanjut.', '2025-06-08 07:37:21'),
(17, 1, 32, 0, 120, 160, 83, 120, 1.3, 0.021, 'Negative', 1, 'Moderate Risk', 'Direkomendasikan rujukan ke spesialis jantung untuk evaluasi lebih lanjut.', '2025-06-08 07:37:27'),
(18, 1, 231, 1, 12, 321, 32, 32, 12, 23, 'Negative', 2, 'High Risk', 'RUJUK SEGERA ke spesialis jantung. Kondisi berisiko tinggi!', '2025-06-08 07:49:50'),
(19, 1, 231, 1, 12, 321, 32, 32, 12, 23, 'Negative', 2, 'High Risk', 'RUJUK SEGERA ke spesialis jantung. Kondisi berisiko tinggi!', '2025-06-08 07:50:46'),
(20, 1, 231, 1, 12, 321, 32, 32, 12, 23, 'Negative', 2, 'High Risk', 'RUJUK SEGERA ke spesialis jantung. Kondisi berisiko tinggi!', '2025-06-08 07:53:43'),
(21, 1, 231, 1, 12, 321, 32, 32, 12, 23, 'Negative', 2, 'High Risk', 'RUJUK SEGERA ke spesialis jantung. Kondisi berisiko tinggi!', '2025-06-08 07:54:11'),
(22, 1, 132, 1, 213, 12, 23, 23, 4, 21, 'Negative', 2, 'High Risk', 'RUJUK SEGERA ke spesialis jantung. Kondisi berisiko tinggi!', '2025-06-08 08:53:12'),
(23, 1, 123, 1, 241, 241, 124, 241, 214, 24, '124', 2, 'High Risk', 'RUJUK SEGERA ke spesialis jantung. Kondisi berisiko tinggi!', '2025-06-08 14:55:17'),
(24, 1, 231, 1, 321, 321, 231, 213, 231, 213, '231', 2, 'High Risk', 'RUJUK SEGERA ke spesialis jantung. Kondisi berisiko tinggi!', '2025-06-08 16:39:43'),
(25, 1, 231, 1, 321, 321, 231, 213, 231, 213, '231', 2, 'High Risk', 'RUJUK SEGERA ke spesialis jantung. Kondisi berisiko tinggi!', '2025-06-08 16:48:33'),
(26, 1, 231, 1, 321, 321, 231, 213, 231, 213, '231', 2, 'High Risk', 'RUJUK SEGERA ke spesialis jantung. Kondisi berisiko tinggi!', '2025-06-08 16:49:15'),
(27, 1, 31, 1, 312, 312, 123, 123, 231, 312, 'Negative', 2, 'High Risk', 'RUJUK SEGERA ke spesialis jantung. Kondisi berisiko tinggi!', '2025-06-13 01:24:17'),
(28, 1, 21, 1, 32, 43, 53, 23, 324, 342, 'Negative', 2, 'High Risk', 'RUJUK SEGERA ke spesialis jantung. Kondisi berisiko tinggi!', '2025-06-19 10:20:21'),
(29, 1, 21, 1, 2, 32, 32, 1, 2, 2, 'Negative', 0, 'Low Risk', 'Tidak memerlukan rujukan spesialis jantung. Rutin pemeriksaan kesehatan umum.', '2025-06-19 10:26:15'),
(30, 1, 21, 1, 2, 32, 32, 1, 2, 2, 'Negative', 0, 'Low Risk', 'Tidak memerlukan rujukan spesialis jantung. Rutin pemeriksaan kesehatan umum.', '2025-06-19 10:27:12'),
(31, 1, 21, 1, 2, 32, 32, 1, 2, 2, 'Negative', 0, 'Low Risk', 'Tidak memerlukan rujukan spesialis jantung. Rutin pemeriksaan kesehatan umum.', '2025-06-19 10:36:55'),
(32, 1, 21, 1, 2, 32, 32, 1, 2, 2, 'Negative', 0, 'Low Risk', 'Tidak memerlukan rujukan spesialis jantung. Rutin pemeriksaan kesehatan umum.', '2025-06-19 10:37:33'),
(33, 1, 21, 1, 2, 32, 32, 1, 2, 2, 'Negative', 0, 'Low Risk', 'Tidak memerlukan rujukan spesialis jantung. Rutin pemeriksaan kesehatan umum.', '2025-06-19 10:37:54'),
(34, 1, 21, 1, 2, 32, 32, 1, 2, 2, 'Negative', 0, 'Low Risk', 'Tidak memerlukan rujukan spesialis jantung. Rutin pemeriksaan kesehatan umum.', '2025-06-19 10:38:03'),
(35, 1, 21, 1, 2, 32, 32, 1, 2, 2, 'Negative', 0, 'Low Risk', 'Tidak memerlukan rujukan spesialis jantung. Rutin pemeriksaan kesehatan umum.', '2025-06-19 10:38:24'),
(36, 1, 21, 1, 2, 32, 32, 1, 2, 2, 'Negative', 0, 'Low Risk', 'Tidak memerlukan rujukan spesialis jantung. Rutin pemeriksaan kesehatan umum.', '2025-06-19 10:38:43'),
(37, 1, 21, 1, 2, 32, 32, 1, 2, 2, 'Negative', 0, 'Low Risk', 'Tidak memerlukan rujukan spesialis jantung. Rutin pemeriksaan kesehatan umum.', '2025-06-19 10:38:47'),
(38, 1, 21, 1, 2, 32, 32, 1, 2, 2, 'Negative', 0, 'Low Risk', 'Tidak memerlukan rujukan spesialis jantung. Rutin pemeriksaan kesehatan umum.', '2025-06-19 10:40:34'),
(39, 1, 21, 1, 2, 32, 32, 1, 2, 2, 'Negative', 0, 'Low Risk', 'Tidak memerlukan rujukan spesialis jantung. Rutin pemeriksaan kesehatan umum.', '2025-06-19 10:40:53'),
(40, 1, 21, 1, 2, 32, 32, 1, 2, 2, 'Negative', 0, 'Low Risk', 'Tidak memerlukan rujukan spesialis jantung. Rutin pemeriksaan kesehatan umum.', '2025-06-19 10:41:30'),
(41, 1, 21, 1, 2, 32, 32, 1, 2, 2, 'Negative', 0, 'Low Risk', 'Tidak memerlukan rujukan spesialis jantung. Rutin pemeriksaan kesehatan umum.', '2025-06-19 10:42:00'),
(42, 1, 21, 1, 2, 32, 32, 1, 2, 2, 'Negative', 0, 'Low Risk', 'Tidak memerlukan rujukan spesialis jantung. Rutin pemeriksaan kesehatan umum.', '2025-06-19 10:42:08');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `is_admin` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `password_hash`, `is_admin`) VALUES
(1, 'ara', 'pbkdf2:sha256:600000$Xgw9TJtmNbzEKbYR$019582de8b6f15002f1677797008069f7f0b8ceb7f306832b0305fedf0afe561', 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `diagnosis`
--
ALTER TABLE `diagnosis`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `diagnosis`
--
ALTER TABLE `diagnosis`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `diagnosis`
--
ALTER TABLE `diagnosis`
  ADD CONSTRAINT `diagnosis_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
