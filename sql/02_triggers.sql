USE hospital_db;
DELIMITER $$

CREATE TRIGGER bed_occupy
AFTER INSERT ON Admissions
FOR EACH ROW
BEGIN
    UPDATE Beds SET is_occupied = TRUE WHERE bed_id = NEW.bed_id;
END $$

CREATE TRIGGER bed_free
AFTER UPDATE ON Admissions
FOR EACH ROW
BEGIN
    IF NEW.discharge_time IS NOT NULL THEN
        UPDATE Beds SET is_occupied = FALSE WHERE bed_id = NEW.bed_id;
    END IF;
END $$

CREATE TRIGGER alert_low_beds
AFTER INSERT ON Admissions
FOR EACH ROW
BEGIN
    DECLARE free_count INT;
    DECLARE threshold INT;

    SELECT COUNT(*) INTO free_count FROM Beds WHERE is_occupied = FALSE;
    SELECT min_free_beds INTO threshold FROM Thresholds WHERE id = 1;

    IF free_count <= threshold THEN
        INSERT INTO Alerts (alert_type, message)
        VALUES ('LOW_FREE_BEDS', CONCAT('Only ', free_count, ' beds left!'));
    END IF;

END $$
DELIMITER ;
