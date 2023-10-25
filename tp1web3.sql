-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : mer. 25 oct. 2023 à 19:26
-- Version du serveur : 8.0.31
-- Version de PHP : 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `tp1web3`
--

-- --------------------------------------------------------

--
-- Structure de la table `categories`
--

DROP TABLE IF EXISTS `categories`;
CREATE TABLE IF NOT EXISTS `categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `description` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `description_UNIQUE` (`description`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `objets`
--

DROP TABLE IF EXISTS `objets`;
CREATE TABLE IF NOT EXISTS `objets` (
  `id` int NOT NULL AUTO_INCREMENT,
  `titre` varchar(50) NOT NULL,
  `description` varchar(2000) NOT NULL,
  `photo` varchar(50) DEFAULT NULL,
  `categorie` int NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `objets`
--

INSERT INTO `objets` (`id`, `titre`, `description`, `photo`, `categorie`, `date`) VALUES
(18, 'Objet sans image', 'Il n\'y a pas d\'image.', '/static/images/ajouts/vide.jpg', 1, '2023-09-22'),
(15, 'Nintendo DS', 'Une super console.', '/static/images/ajouts/1695730657.555625.jpg', 1, '2023-09-22'),
(14, 'GTA VI', 'Jeu pas encore sortie.', '/static/images/ajouts/1695645173.605646.jpg', 1, '2023-09-22'),
(13, 'GTA V', 'Un bon jeu.', '/static/images/ajouts/1695426758.106544.jpg', 2, '2023-09-22'),
(12, 'Toupie et Binou', 'Un filme.', '/static/images/ajouts/1695426730.673883.jpg', 3, '2023-09-22'),
(19, 'Titre', 'Description', '/static/images/ajouts/1695643516.311346.jpg', 1, '2023-09-25'),
(10, 'Un jeu', 'Voici une description.', '/static/images/ajouts/1695426682.624962.jpg', 2, '2023-09-22');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
