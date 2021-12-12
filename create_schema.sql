DROP DATABASE IF EXISTS zbd;
CREATE DATABASE zbd;
USE zbd;

CREATE OR REPLACE TABLE Football_Team (
    Team_id     INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Team_name   VARCHAR(50) NOT NULL,
    Number_of_players  INTEGER NOT NULL,
    Coach_id    INTEGER,
    Manager     INTEGER,
    Home_stadium_id     INTEGER
);

CREATE OR REPLACE TABLE Coach (
    Coach_id      INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    first_name    VARCHAR(50) NOT NULL,
    last_name     VARCHAR(50) NOT NULL,
    phone_number  VARCHAR(50) NOT NULL,
    nationality   VARCHAR(50) NOT NULL
);

CREATE OR REPLACE TABLE Team_manager(
    Manager_id      INTEGER       NOT NULL AUTO_INCREMENT PRIMARY KEY,
    First_name      VARCHAR(50)  NOT NULL,
    Last_name       VARCHAR(50) NOT NULL,
    Phone_number    VARCHAR(25)
);

CREATE OR REPLACE TABLE Players(
    Player_id     Integer NOT NULL AUTO_INCREMENT PRIMARY KEY,
    First_name    VARCHAR(20) NOT NULL,
    Last_name     VARCHAR(20) NOT NULL,
    Phone_number  VARCHAR(20) NOT NULL,
    Team_id       INTEGER,
    Physio_id     INTEGER
);


CREATE OR REPLACE TABLE Budget(
    Team_id    Integer NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Balance    INTEGER NOT NULL,
    Debt       INTEGER,
    Profit     INTEGER NOT NULL,
    Expenses   INTEGER NOT NULL
);

CREATE OR REPLACE TABLE Stadium(
    stadium_id      INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Adress          VARCHAR(25) NOT NULL,
    Number_of_Seats INTEGER NOT NULL
);


CREATE OR REPLACE TABLE Receptionist (
    Receptionist_id    INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    First_name         VARCHAR(20) NOT NULL,
    Last_name          VARCHAR(20) NOT NULL,
    Phone_number       VARCHAR(20) NOT NULL,
    Employee_id        INTEGER NOT NULL AUTO_INCREMENT
);

CREATE OR REPLACE TABLE Employee (
    Employee_id    INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    First_name         VARCHAR(20) NOT NULL,
    Last_name          VARCHAR(20) NOT NULL,
    Phone_number       VARCHAR(20) NOT NULL,
    Team_id        INTEGER NOT NULL AUTO_INCREMENT
);
CREATE OR REPLACE TABLE Physios (
    Physios_id    INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    First_name         VARCHAR(20) NOT NULL,
    Last_name          VARCHAR(20) NOT NULL,
    Phone_number       VARCHAR(20) NOT NULL,
    Physios_type       VARCHAR(20)
);
 
CREATE OR REPLACE TABLE Match_history(
    Match_id    Integer NOT NULL,
    Team1_id    INTEGER NOT NULL,
    Team2_id    INTEGER NOT NULL,
    Team1_score    INTEGER NOT NULL,
    Team2_score    INTEGER NOT NULL,
    Match_date  DATE NOT NULL,
    Stadion_id  INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
);


ALTER TABLE koszyk_produkt ADD CONSTRAINT koszyk_produkt_pk PRIMARY KEY ( uzytkownik_id, produkt_id );


ALTER TABLE zamowienie_produkt ADD CONSTRAINT zamowienie_produkt_pk PRIMARY KEY (produkt_id, zamowienie_id);

ALTER TABLE adres ADD CONSTRAINT adres_uzytkownik_fk FOREIGN KEY ( uzytkownik_id ) REFERENCES uzytkownik ( id ) ON DELETE CASCADE;
ALTER TABLE produkt ADD CONSTRAINT produkt_kategoria_fk FOREIGN KEY ( kategoria ) REFERENCES kategoria ( nazwa ) ON DELETE CASCADE;
ALTER TABLE atrybut ADD CONSTRAINT atrybut_produkt_fk FOREIGN KEY ( produkt_id ) REFERENCES produkt ( id ) ON DELETE CASCADE;

ALTER TABLE tag_produkt ADD CONSTRAINT tp_produkt_fk FOREIGN KEY ( produkt_id ) REFERENCES produkt ( id ) ON DELETE CASCADE;
ALTER TABLE tag_produkt ADD CONSTRAINT tp_tag_fk FOREIGN KEY ( tag_nazwa ) REFERENCES tag ( nazwa ) ON DELETE CASCADE;

ALTER TABLE kategoria ADD CONSTRAINT kategoria_kategoria_fk FOREIGN KEY ( rodzic ) REFERENCES kategoria ( nazwa ) ON DELETE SET NULL;

ALTER TABLE punkt_dostawy ADD CONSTRAINT produkt_dostawy_metoda_dostawy_fk FOREIGN KEY ( metoda_dostawy_nazwa ) REFERENCES metoda_dostawy ( nazwa ) ON DELETE CASCADE;

ALTER TABLE koszyk ADD CONSTRAINT koszyk_uzytkownik_fk FOREIGN KEY ( uzytkownik_id ) REFERENCES uzytkownik ( id ) ON DELETE CASCADE;
ALTER TABLE koszyk_produkt ADD CONSTRAINT koszyk_produkt_uzytkownik_fk FOREIGN KEY ( uzytkownik_id ) REFERENCES uzytkownik ( id ) ON DELETE CASCADE;
ALTER TABLE koszyk_produkt ADD CONSTRAINT koszyk_produkt_produkt_fk FOREIGN KEY ( produkt_id ) REFERENCES produkt ( id ) ON DELETE CASCADE;

ALTER TABLE zamowienie ADD CONSTRAINT zamowienie_uzytkownik_fk FOREIGN KEY ( uzytkownik_id ) REFERENCES uzytkownik ( id ) ON DELETE CASCADE;
ALTER TABLE zamowienie ADD CONSTRAINT zamowienie_metoda_dostawy_fk FOREIGN KEY ( metoda_dost ) REFERENCES metoda_dostawy ( nazwa ) ON DELETE SET NULL;
ALTER TABLE zamowienie ADD CONSTRAINT zamowienie_punkt_dostawy_fk FOREIGN KEY ( punkt_dost ) REFERENCES punkt_dostawy ( id ) ON DELETE SET NULL;
ALTER TABLE zamowienie ADD CONSTRAINT zamowienie_adres_fk FOREIGN KEY ( adres_id ) REFERENCES adres ( id ) ON DELETE SET NULL;
ALTER TABLE zamowienie ADD CONSTRAINT zamowienie_rabat_fk FOREIGN KEY ( rabat_kod ) REFERENCES rabat ( kod ) ON DELETE SET NULL;

ALTER TABLE zamowienie_produkt ADD CONSTRAINT zamowienie_produkt_produkt_fk FOREIGN KEY ( produkt_id ) REFERENCES produkt ( id ) ON DELETE CASCADE;
ALTER TABLE zamowienie_produkt ADD CONSTRAINT zamowienie_produkt_zamowienie_fk FOREIGN KEY ( zamowienie_id ) REFERENCES zamowienie ( id ) ON DELETE CASCADE;

DELIMITER //

CREATE OR REPLACE TRIGGER trig_koszyk
    AFTER UPDATE ON koszyk_produkt FOR EACH ROW
    UPDATE koszyk SET koszyk.data_waznosci = (NOW() + INTERVAL 7 DAY) WHERE koszyk.uzytkownik_id = NEW.uzytkownik_id;
//

CREATE OR REPLACE TRIGGER delete_tag AFTER DELETE ON tag_produkt FOR EACH ROW
BEGIN
	DECLARE vCount INTEGER;
	SELECT count(*) INTO vCount FROM tag_produkt WHERE tag_nazwa = OLD.tag_nazwa;
	IF vCount = 0 THEN
		DELETE FROM tag WHERE nazwa = OLD.tag_nazwa;
	END IF;
END
//

CREATE PROCEDURE InsertTag (vName VARCHAR(25), vProductId INTEGER)
MODIFIES SQL DATA
BEGIN
	INSERT INTO tag (nazwa) VALUES (vName) ON DUPLICATE KEY UPDATE nazwa=vName;
	INSERT INTO tag_produkt (tag_nazwa, produkt_id) VALUES (vName, vProductId);
END
//

