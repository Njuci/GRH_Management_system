Drop database if exists Gestion_Ressources_Humaines;
SET GLOBAL log_bin_trust_function_creators = 1;

CREATE DATABASE IF NOT EXISTS Gestion_Ressources_Humaines;
USE Gestion_Ressources_Humaines;

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

-- Table de séquence pour générer des IDs
CREATE TABLE IF NOT EXISTS Sequence (
    table_name VARCHAR(50) PRIMARY KEY,
    prefix VARCHAR(10) NOT NULL,
    current_value INT NOT NULL
);

-- Initialisation des séquences pour chaque table
INSERT INTO Sequence (table_name, prefix, current_value) VALUES 
('Departement', 'DEP', 0),
('Fonction', 'FCT', 0),
('Bareme_salariale', 'BAR', 0),
('Agent', 'AGT', 0),
('Affecter', 'AFT', 0),
('Presence', 'PRS', 0),
('Pointer', 'PTR', 0),
('Performance', 'PER', 0),
('GRH', 'GRH', 0)
ON DUPLICATE KEY UPDATE table_name=table_name;

DELIMITER //

-- Fonction pour générer un ID avec préfixe
CREATE FUNCTION generate_id(table_name VARCHAR(50))
RETURNS VARCHAR(10)
BEGIN
    DECLARE new_id VARCHAR(10);
    DECLARE prefix VARCHAR(10);
    DECLARE current_value INT;
    
    -- Récupérer le préfixe et la valeur actuelle
    SELECT prefix, current_value INTO prefix, current_value 
    FROM Sequence 
    WHERE table_name = table_name FOR UPDATE;
    
    -- Incrémenter la valeur actuelle
    SET current_value = current_value + 1;
    
    -- Mettre à jour la séquence
    UPDATE Sequence SET current_value = current_value WHERE table_name = table_name;
    
    -- Générer l'identifiant sous forme PREFIX000
    SET new_id = CONCAT(prefix, LPAD(current_value, 3, '0'));
    
    RETURN new_id;
END //

-- Création des triggers pour générer les ID

CREATE TRIGGER before_insert_departement
BEFORE INSERT ON Departement
FOR EACH ROW
BEGIN
    SET NEW.id_departement = generate_id('Departement');
END //

CREATE TRIGGER before_insert_fonction
BEFORE INSERT ON Fonction
FOR EACH ROW
BEGIN
    SET NEW.id_fonction = generate_id('Fonction');
END //

CREATE TRIGGER before_insert_bareme_salariale
BEFORE INSERT ON Bareme_salariale
FOR EACH ROW
BEGIN
    SET NEW.id_bareme = generate_id('Bareme_salariale');
END //

CREATE TRIGGER before_insert_agent
BEFORE INSERT ON Agent
FOR EACH ROW
BEGIN
    SET NEW.id_agent = generate_id('Agent');
END //

CREATE TRIGGER before_insert_affecter
BEFORE INSERT ON Affecter
FOR EACH ROW
BEGIN
    SET NEW.id_affectation = generate_id('Affecter');
END //

CREATE TRIGGER before_insert_presence
BEFORE INSERT ON Presence
FOR EACH ROW
BEGIN
    SET NEW.id_presence = generate_id('Presence');
END //

CREATE TRIGGER before_insert_pointer
BEFORE INSERT ON Pointer
FOR EACH ROW
BEGIN
    SET NEW.id_pointer = generate_id('Pointer');
END //

CREATE TRIGGER before_insert_performance
BEFORE INSERT ON Performance
FOR EACH ROW
BEGIN
    SET NEW.id_performance = generate_id('Performance');
END //

CREATE TRIGGER before_insert_grh
BEFORE INSERT ON GRH
FOR EACH ROW
BEGIN
    SET NEW.id_grh = generate_id('GRH');
END //

DELIMITER ;
