-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema PyPies
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema PyPies
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `PyPies` DEFAULT CHARACTER SET utf8 ;
USE `PyPies` ;

-- -----------------------------------------------------
-- Table `PyPies`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `PyPies`.`users` ;

CREATE TABLE IF NOT EXISTS `PyPies`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL,
  `last_name` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `PyPies`.`pies`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `PyPies`.`pies` ;

CREATE TABLE IF NOT EXISTS `PyPies`.`pies` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `filling` VARCHAR(255) NULL,
  `crust` VARCHAR(255) NULL,
  `votes` INT NULL DEFAULT 0,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_pies_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_pies_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `PyPies`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `PyPies`.`vote_status`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `PyPies`.`vote_status` ;

CREATE TABLE IF NOT EXISTS `PyPies`.`vote_status` (
  `user_id` INT NOT NULL,
  `pie_id` INT NOT NULL,
  INDEX `fk_vote_status_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_vote_status_pies1_idx` (`pie_id` ASC) VISIBLE,
  CONSTRAINT `fk_vote_status_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `PyPies`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_vote_status_pies1`
    FOREIGN KEY (`pie_id`)
    REFERENCES `PyPies`.`pies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
