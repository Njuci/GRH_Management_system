-- Suppression de la base de données si elle existe
DROP DATABASE IF EXISTS Gestion_Ressources_Humaines;

-- Création de la base de données
CREATE DATABASE IF NOT EXISTS Gestion_Ressources_Humaines;
USE Gestion_Ressources_Humaines;

-- Création de la table Sequence pour gérer les identifiants automatiques
CREATE TABLE IF NOT EXISTS Sequence (
    table_name VARCHAR(50) PRIMARY KEY,
    prefix VARCHAR(10) NOT NULL,
    current_value INT NOT NULL DEFAULT 0
);

CREATE TABLE table_name_id (
   name_table VARCHAR(255),
   ancienne_cle INT,
   nouvelle_cle INT,
   variable_name INT  -- Ajout de la colonne variable_name
);

-- Création de la fonction de génération d'ID
DELIMITER //

CREATE FUNCTION generate_id(table_name VARCHAR(50))
RETURNS VARCHAR(10)
BEGIN
    DECLARE new_id VARCHAR(10);
    DECLARE prefix VARCHAR(10);
    DECLARE current_value INT;

    -- Récupérer le préfixe et la valeur actuelle
    SELECT prefix, current_value INTO prefix, current_value 
    FROM Sequence 
    WHERE table_name = table_name;

    -- Incrémenter la valeur actuelle
    SET current_value = current_value + 1;

    -- Mettre à jour la séquence
    UPDATE Sequence SET current_value = current_value WHERE table_name = table_name;

    -- Générer l'ID sous la forme PREFIX000
    SET new_id = CONCAT(prefix, LPAD(current_value, 3, '0'));

    RETURN new_id;
END //

DELIMITER ;

-- Création des tables
CREATE TABLE IF NOT EXISTS Departement (
    id_departement VARCHAR(10) PRIMARY KEY,
    nom_depart VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Fonction (
    id_fonction VARCHAR(10) PRIMARY KEY,
    nom_fonction VARCHAR(100) NOT NULL,
    id_departement VARCHAR(10),
    CONSTRAINT fk_fonction_departement FOREIGN KEY (id_departement) REFERENCES Departement(id_departement)
);

CREATE TABLE IF NOT EXISTS Bareme_salariale (
    id_bareme VARCHAR(10) PRIMARY KEY,
    date_fixation DATE NOT NULL DEFAULT (CURRENT_DATE),
    salaire_horaire DECIMAL(10, 2) NOT NULL,
    id_fonction VARCHAR(10),
    CONSTRAINT fk_bareme_fonction FOREIGN KEY (id_fonction) REFERENCES Fonction(id_fonction)
);

CREATE TABLE IF NOT EXISTS Agent (
    id_agent VARCHAR(10) PRIMARY KEY,   
    nom VARCHAR(100) NOT NULL,
    sexe VARCHAR(10),
    date_naissance DATE,
    lieu_naissance VARCHAR(100),
    etat_civil VARCHAR(50),
    adresse VARCHAR(255),
    nombre_enfant INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS Affecter (
    id_affectation VARCHAR(10) PRIMARY KEY,
    date_debut DATE NOT NULL,
    date_fin DATE NULL, 
    id_agent VARCHAR(10),
    id_fonction VARCHAR(10),
    CONSTRAINT fk_affecter_agent FOREIGN KEY (id_agent) REFERENCES Agent(id_agent),
    CONSTRAINT fk_affecter_fonction FOREIGN KEY (id_fonction) REFERENCES Fonction(id_fonction)
);

CREATE TABLE IF NOT EXISTS Presence (
    id_presence VARCHAR(10) PRIMARY KEY,
    date_presence DATE NOT NULL,
    id_agent VARCHAR(10),
    CONSTRAINT fk_presence_agent FOREIGN KEY (id_agent) REFERENCES Agent(id_agent)
);

CREATE TABLE IF NOT EXISTS Pointer (
    id_pointer VARCHAR(10) PRIMARY KEY,
    heure_arrive TIME NOT NULL,
    heure_sortie TIME NOT NULL,
    id_presence VARCHAR(10),
    id_agent VARCHAR(10),
    CONSTRAINT fk_pointer_presence FOREIGN KEY (id_presence) REFERENCES Presence(id_presence),
    CONSTRAINT fk_pointer_agent FOREIGN KEY (id_agent) REFERENCES Agent(id_agent)
);

CREATE TABLE IF NOT EXISTS Performance (
    id_performance VARCHAR(10) PRIMARY KEY,
    annee INT NOT NULL,
    note DECIMAL(5, 2),
    observation VARCHAR(255),
    id_agent VARCHAR(10),
    CONSTRAINT fk_performance_agent FOREIGN KEY (id_agent) REFERENCES Agent(id_agent)
);

CREATE TABLE IF NOT EXISTS GRH (
    id_grh VARCHAR(10) PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    mdp VARCHAR(255) NOT NULL
);

USE Gestion_Ressources_Humaines;

DELIMITER //

-- Trigger pour la table Departement
CREATE TRIGGER avant_insertion_departement
BEFORE INSERT ON Departement
FOR EACH ROW
BEGIN
    DECLARE max_nouvelle_cle INT DEFAULT 0;
    DECLARE variable_name INT DEFAULT 1;

    -- Récupère la plus grande valeur de nouvelle_cle pour Departement
    SELECT COALESCE(MAX(nouvelle_cle), 0) INTO max_nouvelle_cle 
    FROM table_name_id 
    WHERE name_table = 'Departement';

    -- Incrémente la valeur maximale pour le nouvel ID
    SET variable_name = max_nouvelle_cle + 1;

    -- Définit le nouvel id_departement
    SET NEW.id_departement = CONCAT('DEP', LPAD(variable_name, 3, '0'));

    -- Insère le nouvel ID dans table_name_id
    INSERT INTO table_name_id (name_table, nouvelle_cle, variable_name) 
    VALUES ('Departement', variable_name, variable_name);
END //

-- Trigger pour la table Fonction
CREATE TRIGGER avant_insertion_fonction
BEFORE INSERT ON Fonction
FOR EACH ROW
BEGIN
    DECLARE max_nouvelle_cle INT DEFAULT 0;
    DECLARE variable_name INT DEFAULT 1;

    -- Récupère la plus grande valeur de nouvelle_cle pour Fonction
    SELECT COALESCE(MAX(nouvelle_cle), 0) INTO max_nouvelle_cle 
    FROM table_name_id 
    WHERE name_table = 'Fonction';

    -- Incrémente la valeur maximale pour le nouvel ID
    SET variable_name = max_nouvelle_cle + 1;

    -- Définit le nouvel id_fonction
    SET NEW.id_fonction = CONCAT('FCT', LPAD(variable_name, 3, '0'));

    -- Insère le nouvel ID dans table_name_id
    INSERT INTO table_name_id (name_table, nouvelle_cle, variable_name) 
    VALUES ('Fonction', variable_name, variable_name);
END //

-- Trigger pour la table Bareme_salariale
CREATE TRIGGER avant_insertion_bareme_salariale
BEFORE INSERT ON Bareme_salariale
FOR EACH ROW
BEGIN
    DECLARE max_nouvelle_cle INT DEFAULT 0;
    DECLARE variable_name INT DEFAULT 1;

    -- Récupère la plus grande valeur de nouvelle_cle pour Bareme_salariale
    SELECT COALESCE(MAX(nouvelle_cle), 0) INTO max_nouvelle_cle 
    FROM table_name_id 
    WHERE name_table = 'Bareme_salariale';

    -- Incrémente la valeur maximale pour le nouvel ID
    SET variable_name = max_nouvelle_cle + 1;

    -- Définit le nouvel id_bareme
    SET NEW.id_bareme = CONCAT('BAR', LPAD(variable_name, 3, '0'));

    -- Insère le nouvel ID dans table_name_id
    INSERT INTO table_name_id (name_table, nouvelle_cle, variable_name) 
    VALUES ('Bareme_salariale', variable_name, variable_name);
END //

-- Trigger pour la table Agent
CREATE TRIGGER avant_insertion_agent
BEFORE INSERT ON Agent
FOR EACH ROW
BEGIN
    DECLARE max_nouvelle_cle INT DEFAULT 0;
    DECLARE variable_name INT DEFAULT 1;

    -- Récupère la plus grande valeur de nouvelle_cle pour Agent
    SELECT COALESCE(MAX(nouvelle_cle), 0) INTO max_nouvelle_cle 
    FROM table_name_id 
    WHERE name_table = 'Agent';

    -- Incrémente la valeur maximale pour le nouvel ID
    SET variable_name = max_nouvelle_cle + 1;

    -- Définit le nouvel id_agent
    SET NEW.id_agent = CONCAT('AGT', LPAD(variable_name, 3, '0'));

    -- Insère le nouvel ID dans table_name_id
    INSERT INTO table_name_id (name_table, nouvelle_cle, variable_name) 
    VALUES ('Agent', variable_name, variable_name);
END //

-- Trigger pour la table Affecter
CREATE TRIGGER avant_insertion_affecter
BEFORE INSERT ON Affecter
FOR EACH ROW
BEGIN
    DECLARE max_nouvelle_cle INT DEFAULT 0;
    DECLARE variable_name INT DEFAULT 1;

    -- Récupère la plus grande valeur de nouvelle_cle pour Affecter
    SELECT COALESCE(MAX(nouvelle_cle), 0) INTO max_nouvelle_cle 
    FROM table_name_id 
    WHERE name_table = 'Affecter';

    -- Incrémente la valeur maximale pour le nouvel ID
    SET variable_name = max_nouvelle_cle + 1;

    -- Définit le nouvel id_affectation
    SET NEW.id_affectation = CONCAT('AFF', LPAD(variable_name, 3, '0'));

    -- Insère le nouvel ID dans table_name_id
    INSERT INTO table_name_id (name_table, nouvelle_cle, variable_name) 
    VALUES ('Affecter', variable_name, variable_name);
END //

-- Trigger pour la table Presence
CREATE TRIGGER avant_insertion_presence
BEFORE INSERT ON Presence
FOR EACH ROW
BEGIN
    DECLARE max_nouvelle_cle INT DEFAULT 0;
    DECLARE variable_name INT DEFAULT 1;

    -- Récupère la plus grande valeur de nouvelle_cle pour Presence
    SELECT COALESCE(MAX(nouvelle_cle), 0) INTO max_nouvelle_cle 
    FROM table_name_id 
    WHERE name_table = 'Presence';

    -- Incrémente la valeur maximale pour le nouvel ID
    SET variable_name = max_nouvelle_cle + 1;

    -- Définit le nouvel id_presence
    SET NEW.id_presence = CONCAT('PRE', LPAD(variable_name, 3, '0'));

    -- Insère le nouvel ID dans table_name_id
    INSERT INTO table_name_id (name_table, nouvelle_cle, variable_name) 
    VALUES ('Presence', variable_name, variable_name);
END //

-- Trigger pour la table Pointer
CREATE TRIGGER avant_insertion_pointer
BEFORE INSERT ON Pointer
FOR EACH ROW
BEGIN
    DECLARE max_nouvelle_cle INT DEFAULT 0;
    DECLARE variable_name INT DEFAULT 1;

    -- Récupère la plus grande valeur de nouvelle_cle pour Pointer
    SELECT COALESCE(MAX(nouvelle_cle), 0) INTO max_nouvelle_cle 
    FROM table_name_id 
    WHERE name_table = 'Pointer';

    -- Incrémente la valeur maximale pour le nouvel ID
    SET variable_name = max_nouvelle_cle + 1;

    -- Définit le nouvel id_pointer
    SET NEW.id_pointer = CONCAT('PNT', LPAD(variable_name, 3, '0'));

    -- Insère le nouvel ID dans table_name_id
    INSERT INTO table_name_id (name_table, nouvelle_cle, variable_name) 
    VALUES ('Pointer', variable_name, variable_name);
END //

-- Trigger pour la table Performance
CREATE TRIGGER avant_insertion_performance
BEFORE INSERT ON Performance
FOR EACH ROW
BEGIN
    DECLARE max_nouvelle_cle INT DEFAULT 0;
    DECLARE variable_name INT DEFAULT 1;

    -- Récupère la plus grande valeur de nouvelle_cle pour Performance
    SELECT COALESCE(MAX(nouvelle_cle), 0) INTO max_nouvelle_cle 
    FROM table_name_id 
    WHERE name_table = 'Performance';

    -- Incrémente la valeur maximale pour le nouvel ID
    SET variable_name = max_nouvelle_cle + 1;

    -- Définit le nouvel id_performance
    SET NEW.id_performance = CONCAT('PER', LPAD(variable_name, 3, '0'));

    -- Insère le nouvel ID dans table_name_id
    INSERT INTO table_name_id (name_table, nouvelle_cle, variable_name) 
    VALUES ('Performance', variable_name, variable_name);
END //

-- Trigger pour la table GRH
CREATE TRIGGER avant_insertion_grh
BEFORE INSERT ON GRH
FOR EACH ROW
BEGIN
    DECLARE max_nouvelle_cle INT DEFAULT 0;
    DECLARE variable_name INT DEFAULT 1;

    -- Récupère la plus grande valeur de nouvelle_cle pour GRH
    SELECT COALESCE(MAX(nouvelle_cle), 0) INTO max_nouvelle_cle 
    FROM table_name_id 
    WHERE name_table = 'GRH';

    -- Incrémente la valeur maximale pour le nouvel ID
    SET variable_name = max_nouvelle_cle + 1;

    -- Définit le nouvel id_grh
    SET NEW.id_grh = CONCAT('GRH', LPAD(variable_name, 3, '0'));

    -- Insère le nouvel ID dans table_name_id
    INSERT INTO table_name_id (name_table, nouvelle_cle, variable_name) 
    VALUES ('GRH', variable_name, variable_name);
END //

DELIMITER ;
