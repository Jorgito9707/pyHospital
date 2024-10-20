BEGIN TRANSACTION;

--Valores para la tabla PACIENTES
INSERT INTO PACIENTES VALUES(1, 'Juan', 'Fernández', '624237856', 'fjuan@gmail.com', '12-10-1979', 1);
INSERT INTO PACIENTES VALUES(2, 'Harry', 'Potter', '623803195', 'pototo@yahoo.com', '11-07-1992', 2);
INSERT INTO PACIENTES VALUES(3, 'Naruto', 'Uzumaki', '923786543', 'hokage@gmail.com', '20-09-2000', 1);
INSERT INTO PACIENTES VALUES(4, 'Tyrion', 'Lannister', '621785623', 'house_lannister@gmail.com', '18-08-1972', 2);

--Valores para tabla DOCTORES
INSERT INTO DOCTORES VALUES(1, 'Jorge', 'Valdés', '12345', '623403145', 'jlvp@gmail.com', 'True');
INSERT INTO DOCTORES VALUES(2, 'Claudia', 'Umarán', 'cus2000', '624563412', 'claudiasuarez@gmail.com', 'False');

COMMIT;