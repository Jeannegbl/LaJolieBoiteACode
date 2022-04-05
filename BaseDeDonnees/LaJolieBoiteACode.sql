-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost:3306
-- Généré le : mar. 05 avr. 2022 à 14:08
-- Version du serveur :  10.3.34-MariaDB-0ubuntu0.20.04.1
-- Version de PHP : 7.4.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `LaJolieBoiteACode`
--

-- --------------------------------------------------------

--
-- Structure de la table `commentaire`
--

CREATE TABLE `commentaire` (
  `utilisateur_id` int(11) NOT NULL,
  `contact_id` int(11) NOT NULL,
  `description` varchar(500) DEFAULT NULL,
  `date_creation` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `commentaire`
--

INSERT INTO `commentaire` (`utilisateur_id`, `contact_id`, `description`, `date_creation`) VALUES
(1, 1, 'Contrat en cours pour faire notre projet Python', '2022-03-31 12:28:35'),
(1, 1, 'Je suis un test', '2022-04-02 22:40:10');

-- --------------------------------------------------------

--
-- Structure de la table `contact`
--

CREATE TABLE `contact` (
  `id` int(11) NOT NULL,
  `nom` varchar(30) DEFAULT NULL,
  `prenom` varchar(30) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `poste` varchar(50) DEFAULT NULL,
  `telephone` int(11) DEFAULT NULL,
  `statut` tinyint(4) DEFAULT NULL,
  `prospect_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `contact`
--

INSERT INTO `contact` (`id`, `nom`, `prenom`, `email`, `poste`, `telephone`, `statut`, `prospect_id`) VALUES
(1, 'DUCLOS', 'Erwann', 'erwann@duclos.fr', 'Professeur', 111111111, 1, 1),
(2, 'PANNETIER', 'Magali', 'magali@pannetier.fr', 'Directrice', 111111110, 0, 1),
(11, 'test', 'test', 'test@test.com', 'test', 123456789, 1, 1);

-- --------------------------------------------------------

--
-- Structure de la table `entreprise`
--

CREATE TABLE `entreprise` (
  `id` int(11) NOT NULL,
  `nom` varchar(30) DEFAULT NULL,
  `numero_siren` varchar(20) DEFAULT NULL,
  `adresse_postale` varchar(50) DEFAULT NULL,
  `code_postal` int(11) DEFAULT NULL,
  `ville` varchar(45) DEFAULT NULL,
  `cedex` int(11) DEFAULT NULL,
  `telephone` int(11) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `IBAN` varchar(40) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `entreprise`
--

INSERT INTO `entreprise` (`id`, `nom`, `numero_siren`, `adresse_postale`, `code_postal`, `ville`, `cedex`, `telephone`, `email`, `IBAN`) VALUES
(1, 'La jolie boite à code', '123 456 7890', '123 Rue du Soleil', 75009, 'Paris', 9, 123456789, 'lajolieboiteacode@gmail.com', 'FR12 1234 1234 1234 1234 1234 123');

-- --------------------------------------------------------

--
-- Structure de la table `facture`
--

CREATE TABLE `facture` (
  `id` int(11) NOT NULL,
  `numero_facture` int(11) DEFAULT NULL,
  `date_emission` datetime DEFAULT NULL,
  `montant` int(11) NOT NULL,
  `contact_id` int(11) NOT NULL,
  `prospect_id` int(11) NOT NULL,
  `entreprise_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `facture`
--

INSERT INTO `facture` (`id`, `numero_facture`, `date_emission`, `montant`, `contact_id`, `prospect_id`, `entreprise_id`) VALUES
(1, 1, '2022-03-31 12:29:37', 1500, 1, 1, 1);

-- --------------------------------------------------------

--
-- Structure de la table `prospect`
--

CREATE TABLE `prospect` (
  `id` int(11) NOT NULL,
  `nom` varchar(30) DEFAULT NULL,
  `numero_siret` varchar(20) DEFAULT NULL,
  `adresse_postale` varchar(50) DEFAULT NULL,
  `code_postal` int(11) DEFAULT NULL,
  `ville` varchar(45) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `url` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `prospect`
--

INSERT INTO `prospect` (`id`, `nom`, `numero_siret`, `adresse_postale`, `code_postal`, `ville`, `description`, `url`) VALUES
(1, 'EPSI', '111 111 1111', '123 Rue de l\'EPSI', 35000, 'Rennes', 'École de programmation de l\'EPSI à Rennes', 'https://www.epsi.fr/'),
(3, 'Saint Martin', '111 111 1110', '123 Rue de Saint Mart', 35000, 'Rennes', 'Lycée St Martin', 'https://www.saintmartin-rennes.org/');

-- --------------------------------------------------------

--
-- Structure de la table `utilisateur`
--

CREATE TABLE `utilisateur` (
  `id` int(11) NOT NULL,
  `login` varchar(30) DEFAULT NULL,
  `mot_de_passe` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `utilisateur`
--

INSERT INTO `utilisateur` (`id`, `login`, `mot_de_passe`) VALUES
(1, 'admin', 'admin');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `commentaire`
--
ALTER TABLE `commentaire`
  ADD KEY `fk_utilisateur_has_contact_contact1_idx` (`contact_id`),
  ADD KEY `fk_utilisateur_has_contact_utilisateur_idx` (`utilisateur_id`);

--
-- Index pour la table `contact`
--
ALTER TABLE `contact`
  ADD PRIMARY KEY (`id`) USING BTREE,
  ADD KEY `fk_contact_prospect1_idx` (`prospect_id`);

--
-- Index pour la table `entreprise`
--
ALTER TABLE `entreprise`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `facture`
--
ALTER TABLE `facture`
  ADD PRIMARY KEY (`id`) USING BTREE,
  ADD KEY `fk_facture_contact1_idx` (`contact_id`),
  ADD KEY `fk_facture_prospect1_idx` (`prospect_id`),
  ADD KEY `fk_facture_entreprise1_idx` (`entreprise_id`);

--
-- Index pour la table `prospect`
--
ALTER TABLE `prospect`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `utilisateur`
--
ALTER TABLE `utilisateur`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `contact`
--
ALTER TABLE `contact`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT pour la table `entreprise`
--
ALTER TABLE `entreprise`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `facture`
--
ALTER TABLE `facture`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `prospect`
--
ALTER TABLE `prospect`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT pour la table `utilisateur`
--
ALTER TABLE `utilisateur`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `commentaire`
--
ALTER TABLE `commentaire`
  ADD CONSTRAINT `fk_utilisateur_has_contact_contact1` FOREIGN KEY (`contact_id`) REFERENCES `contact` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_utilisateur_has_contact_utilisateur` FOREIGN KEY (`utilisateur_id`) REFERENCES `utilisateur` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Contraintes pour la table `contact`
--
ALTER TABLE `contact`
  ADD CONSTRAINT `fk_contact_prospect1` FOREIGN KEY (`prospect_id`) REFERENCES `prospect` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Contraintes pour la table `facture`
--
ALTER TABLE `facture`
  ADD CONSTRAINT `fk_facture_prospect1` FOREIGN KEY (`prospect_id`) REFERENCES `prospect` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
