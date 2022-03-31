-- MySQL Script generated by MySQL Workbench
-- jeu. 31 mars 2022 12:03:04
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema LaJolieBoiteACode
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema LaJolieBoiteACode
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `LaJolieBoiteACode` ;
USE `LaJolieBoiteACode` ;

-- -----------------------------------------------------
-- Table `LaJolieBoiteACode`.`prospect`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LaJolieBoiteACode`.`prospect` (
  `id` INT NOT NULL,
  `nom` VARCHAR(30) NULL,
  `numero_siret` VARCHAR(20) NULL,
  `adresse_postale` VARCHAR(50) NULL,
  `code_postale` INT NULL,
  `ville` VARCHAR(45) NULL,
  `description` TEXT(500) NULL,
  `url` VARCHAR(100) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LaJolieBoiteACode`.`contact`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LaJolieBoiteACode`.`contact` (
  `id` INT NOT NULL,
  `nom` VARCHAR(30) NULL,
  `prenom` VARCHAR(30) NULL,
  `email` VARCHAR(50) NULL,
  `poste` VARCHAR(50) NULL,
  `telephone` INT NULL,
  `statut` TINYINT NULL,
  `prospect_id` INT NOT NULL,
  PRIMARY KEY (`id`, `prospect_id`),
  INDEX `fk_contact_prospect1_idx` (`prospect_id` ASC) ,
  CONSTRAINT `fk_contact_prospect1`
    FOREIGN KEY (`prospect_id`)
    REFERENCES `LaJolieBoiteACode`.`prospect` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LaJolieBoiteACode`.`utilisateur`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LaJolieBoiteACode`.`utilisateur` (
  `id` INT NOT NULL,
  `login` VARCHAR(30) NULL,
  `mot_de_passe` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LaJolieBoiteACode`.`entreprise`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LaJolieBoiteACode`.`entreprise` (
  `id` INT NOT NULL,
  `nom` VARCHAR(30) NULL,
  `numero_siret` VARCHAR(20) NULL,
  `adresse_postale` VARCHAR(50) NULL,
  `code_postale` INT NULL,
  `telephone` INT NULL,
  `email` VARCHAR(50) NULL,
  `IBAN` VARCHAR(40) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LaJolieBoiteACode`.`facture`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LaJolieBoiteACode`.`facture` (
  `id` INT NOT NULL,
  `numero_facture` INT NULL,
  `date_emission` DATETIME NULL,
  `contact_id` INT NOT NULL,
  `prospect_id` INT NOT NULL,
  `entreprise_id` INT NOT NULL,
  PRIMARY KEY (`id`, `contact_id`, `prospect_id`, `entreprise_id`),
  INDEX `fk_facture_contact1_idx` (`contact_id` ASC) ,
  INDEX `fk_facture_prospect1_idx` (`prospect_id` ASC) ,
  INDEX `fk_facture_entreprise1_idx` (`entreprise_id` ASC) ,
  CONSTRAINT `fk_facture_contact1`
    FOREIGN KEY (`contact_id`)
    REFERENCES `LaJolieBoiteACode`.`contact` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_facture_prospect1`
    FOREIGN KEY (`prospect_id`)
    REFERENCES `LaJolieBoiteACode`.`prospect` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_facture_entreprise1`
    FOREIGN KEY (`entreprise_id`)
    REFERENCES `LaJolieBoiteACode`.`entreprise` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LaJolieBoiteACode`.`commentaire`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LaJolieBoiteACode`.`commentaire` (
  `utilisateur_id` INT NOT NULL,
  `contact_id` INT NOT NULL,
  `description` VARCHAR(500) NULL,
  `date_creation` DATETIME NULL,
  PRIMARY KEY (`utilisateur_id`, `contact_id`),
  INDEX `fk_utilisateur_has_contact_contact1_idx` (`contact_id` ASC) ,
  INDEX `fk_utilisateur_has_contact_utilisateur_idx` (`utilisateur_id` ASC) ,
  CONSTRAINT `fk_utilisateur_has_contact_utilisateur`
    FOREIGN KEY (`utilisateur_id`)
    REFERENCES `LaJolieBoiteACode`.`utilisateur` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_utilisateur_has_contact_contact1`
    FOREIGN KEY (`contact_id`)
    REFERENCES `LaJolieBoiteACode`.`contact` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;