
CREATE DATABASE IF NOT EXISTS 'mundial';
USE mundial;

CREATE TABLE IF NOT EXISTS fixture (
    id_fixture               INT AUTO_INCREMENT PRIMARY KEY,
    local            VARCHAR(255) DEFAULT NULL,
    visitante        VARCHAR(255) DEFAULT NULL,
    estadio          VARCHAR(255) NOT NULL,
    ciudad           VARCHAR(255) NOT NULL,
    fecha            DATE         NOT NULL,
    fase             VARCHAR(255) NOT NULL,
    goles_local      INT          DEFAULT NULL,
    goles_visitante  INT          DEFAULT NULL
);

-- FASE DE GRUPOS
INSERT INTO fixture (local, visitante, estadio, ciudad, fecha, fase) VALUES
-- Jornada 1
('Mexico', 'Sudafrica', 'Estadio Azteca', 'Ciudad de Mexico', '2026-06-11', 'Fase de grupos'),
('Corea del Sur', 'Republica Checa', 'Estadio Guadalajara', 'Guadalajara', '2026-06-11', 'Fase de grupos'),
('Canada', 'Bosnia y Herzegovina', 'BMO Field', 'Toronto', '2026-06-12', 'Fase de grupos'),
('Estados Unidos', 'Paraguay', 'SoFi Stadium', 'Los Angeles', '2026-06-12', 'Fase de grupos'),
('Qatar', 'Suiza', 'Levi''s Stadium', 'San Francisco', '2026-06-13', 'Fase de grupos'),
('Brasil', 'Marruecos', 'MetLife Stadium', 'Nueva York', '2026-06-13', 'Fase de grupos'),
('Haiti', 'Escocia', 'Gillette Stadium', 'Boston', '2026-06-13', 'Fase de grupos'),
('Australia', 'Turquia', 'BC Place', 'Vancouver', '2026-06-13', 'Fase de grupos'),
('Alemania', 'Curazao', 'NRG Stadium', 'Houston', '2026-06-14', 'Fase de grupos'),
('Paises Bajos', 'Japon', 'AT&T Stadium', 'Dallas', '2026-06-14', 'Fase de grupos'),
('Costa de Marfil', 'Ecuador', 'Lincoln Financial Field', 'Philadelphia', '2026-06-14', 'Fase de grupos'),
('Suecia', 'Tunez', 'Estadio BBVA', 'Monterrey', '2026-06-14', 'Fase de grupos'),
('Espana', 'Cabo Verde', 'Mercedes-Benz Stadium', 'Atlanta', '2026-06-15', 'Fase de grupos'),
('Belgica', 'Egipto', 'Lumen Field', 'Seattle', '2026-06-15', 'Fase de grupos'),
('Arabia Saudita', 'Uruguay', 'Hard Rock Stadium', 'Miami', '2026-06-15', 'Fase de grupos'),
('Iran', 'Nueva Zelanda', 'SoFi Stadium', 'Los Angeles', '2026-06-15', 'Fase de grupos'),
('Francia', 'Senegal', 'MetLife Stadium', 'Nueva York', '2026-06-16', 'Fase de grupos'),
('Irak', 'Noruega', 'Gillette Stadium', 'Boston', '2026-06-16', 'Fase de grupos'),
('Argentina', 'Argelia', 'Arrowhead Stadium', 'Kansas City', '2026-06-16', 'Fase de grupos'),
('Austria', 'Jordania', 'Levi''s Stadium', 'San Francisco', '2026-06-16', 'Fase de grupos'),
('Portugal', 'Rep. Democratica del Congo', 'NRG Stadium', 'Houston', '2026-06-17', 'Fase de grupos'),
('Inglaterra', 'Croacia', 'AT&T Stadium', 'Dallas', '2026-06-17', 'Fase de grupos'),
('Ghana', 'Panama', 'BMO Field', 'Toronto', '2026-06-17', 'Fase de grupos'),
('Uzbekistan', 'Colombia', 'Estadio Azteca', 'Ciudad de Mexico', '2026-06-17', 'Fase de grupos'),

-- Jornada 2
('Republica Checa', 'Sudafrica', 'Mercedes-Benz Stadium', 'Atlanta', '2026-06-18', 'Fase de grupos'),
('Suiza', 'Bosnia y Herzegovina', 'SoFi Stadium', 'Los Angeles', '2026-06-18', 'Fase de grupos'),
('Canada', 'Qatar', 'BC Place', 'Vancouver', '2026-06-18', 'Fase de grupos'),
('Mexico', 'Corea del Sur', 'Estadio Guadalajara', 'Guadalajara', '2026-06-18', 'Fase de grupos'),
('Estados Unidos', 'Australia', 'Lumen Field', 'Seattle', '2026-06-19', 'Fase de grupos'),
('Escocia', 'Marruecos', 'Gillette Stadium', 'Boston', '2026-06-19', 'Fase de grupos'),
('Brasil', 'Haiti', 'Lincoln Financial Field', 'Philadelphia', '2026-06-19', 'Fase de grupos'),
('Turquia', 'Paraguay', 'Levi''s Stadium', 'San Francisco', '2026-06-19', 'Fase de grupos'),
('Paises Bajos', 'Suecia', 'NRG Stadium', 'Houston', '2026-06-20', 'Fase de grupos'),
('Alemania', 'Costa de Marfil', 'BMO Field', 'Toronto', '2026-06-20', 'Fase de grupos'),
('Ecuador', 'Curazao', 'Arrowhead Stadium', 'Kansas City', '2026-06-20', 'Fase de grupos'),
('Tunez', 'Japon', 'Estadio BBVA', 'Monterrey', '2026-06-20', 'Fase de grupos'),
('Espana', 'Arabia Saudita', 'Mercedes-Benz Stadium', 'Atlanta', '2026-06-21', 'Fase de grupos'),
('Belgica', 'Iran', 'SoFi Stadium', 'Los Angeles', '2026-06-21', 'Fase de grupos'),
('Uruguay', 'Cabo Verde', 'Hard Rock Stadium', 'Miami', '2026-06-21', 'Fase de grupos'),
('Nueva Zelanda', 'Egipto', 'BC Place', 'Vancouver', '2026-06-21', 'Fase de grupos'),
('Argentina', 'Austria', 'AT&T Stadium', 'Dallas', '2026-06-22', 'Fase de grupos'),
('Francia', 'Irak', 'Lincoln Financial Field', 'Philadelphia', '2026-06-22', 'Fase de grupos'),
('Noruega', 'Senegal', 'MetLife Stadium', 'Nueva York', '2026-06-22', 'Fase de grupos'),
('Jordania', 'Argelia', 'Levi''s Stadium', 'San Francisco', '2026-06-22', 'Fase de grupos'),
('Portugal', 'Uzbekistan', 'NRG Stadium', 'Houston', '2026-06-23', 'Fase de grupos'),
('Inglaterra', 'Ghana', 'Gillette Stadium', 'Boston', '2026-06-23', 'Fase de grupos'),
('Panama', 'Croacia', 'BMO Field', 'Toronto', '2026-06-23', 'Fase de grupos'),
('Colombia', 'Rep. Democratica del Congo', 'Estadio Guadalajara', 'Guadalajara', '2026-06-23', 'Fase de grupos'),

-- Jornada 3
('Suiza', 'Canada', 'BC Place', 'Vancouver', '2026-06-24', 'Fase de grupos'),
('Bosnia y Herzegovina', 'Qatar', 'Lumen Field', 'Seattle', '2026-06-24', 'Fase de grupos'),
('Escocia', 'Brasil', 'Hard Rock Stadium', 'Miami', '2026-06-24', 'Fase de grupos'),
('Marruecos', 'Haiti', 'Mercedes-Benz Stadium', 'Atlanta', '2026-06-24', 'Fase de grupos'),
('Republica Checa', 'Mexico', 'Estadio Azteca', 'Ciudad de Mexico', '2026-06-24', 'Fase de grupos'),
('Sudafrica', 'Corea del Sur', 'Estadio BBVA', 'Monterrey', '2026-06-24', 'Fase de grupos'),
('Ecuador', 'Alemania', 'MetLife Stadium', 'Nueva York', '2026-06-25', 'Fase de grupos'),
('Curazao', 'Costa de Marfil', 'Lincoln Financial Field', 'Philadelphia', '2026-06-25', 'Fase de grupos'),
('Tunez', 'Paises Bajos', 'Arrowhead Stadium', 'Kansas City', '2026-06-25', 'Fase de grupos'),
('Japon', 'Suecia', 'AT&T Stadium', 'Dallas', '2026-06-25', 'Fase de grupos'),
('Turquia', 'Estados Unidos', 'SoFi Stadium', 'Los Angeles', '2026-06-25', 'Fase de grupos'),
('Paraguay', 'Australia', 'Levi''s Stadium', 'San Francisco', '2026-06-25', 'Fase de grupos'),
('Noruega', 'Francia', 'Gillette Stadium', 'Boston', '2026-06-26', 'Fase de grupos'),
('Senegal', 'Irak', 'BMO Field', 'Toronto', '2026-06-26', 'Fase de grupos'),
('Uruguay', 'Espana', 'Estadio Guadalajara', 'Guadalajara', '2026-06-26', 'Fase de grupos'),
('Cabo Verde', 'Arabia Saudita', 'NRG Stadium', 'Houston', '2026-06-26', 'Fase de grupos'),
('Nueva Zelanda', 'Belgica', 'BC Place', 'Vancouver', '2026-06-26', 'Fase de grupos'),
('Egipto', 'Iran', 'Lumen Field', 'Seattle', '2026-06-26', 'Fase de grupos'),
('Panama', 'Inglaterra', 'MetLife Stadium', 'Nueva York', '2026-06-27', 'Fase de grupos'),
('Croacia', 'Ghana', 'Lincoln Financial Field', 'Philadelphia', '2026-06-27', 'Fase de grupos'),
('Colombia', 'Portugal', 'Hard Rock Stadium', 'Miami', '2026-06-27', 'Fase de grupos'),
('Rep. Democratica del Congo', 'Uzbekistan', 'Mercedes-Benz Stadium', 'Atlanta', '2026-06-27', 'Fase de grupos'),
('Jordania', 'Argentina', 'AT&T Stadium', 'Dallas', '2026-06-27', 'Fase de grupos'),
('Argelia', 'Austria', 'Arrowhead Stadium', 'Kansas City', '2026-06-27', 'Fase de grupos');


INSERT INTO fixture (estadio, ciudad, fecha, fase) VALUES
-- 16AVOS DE FINAL
('SoFi Stadium', 'Los Angeles', '2026-06-28', '16avos de final'),
('NRG Stadium', 'Houston', '2026-06-29', '16avos de final'),
('Gillette Stadium', 'Boston', '2026-06-29', '16avos de final'),
('Estadio BBVA', 'Monterrey', '2026-06-29', '16avos de final'),
('AT&T Stadium', 'Dallas', '2026-06-30', '16avos de final'),
('MetLife Stadium', 'Nueva York', '2026-06-30', '16avos de final'),
('Estadio Azteca', 'Ciudad de Mexico', '2026-06-30', '16avos de final'),
('Mercedes-Benz Stadium', 'Atlanta', '2026-07-01', '16avos de final'),
('Lumen Field', 'Seattle', '2026-07-01', '16avos de final'),
('Levis Stadium', 'San Francisco', '2026-07-01', '16avos de final'),
('BMO Field', 'Toronto', '2026-07-02', '16avos de final'),
('SoFi Stadium', 'Los Angeles', '2026-07-02', '16avos de final'),
('BC Place', 'Vancouver', '2026-07-02', '16avos de final'),
('AT&T Stadium', 'Dallas', '2026-07-03', '16avos de final'),
('Hard Rock Stadium', 'Miami', '2026-07-03', '16avos de final'),
('Arrowhead Stadium', 'Kansas City', '2026-07-03', '16avos de final'),

-- OCTAVOS DE FINAL
('NRG Stadium', 'Houston', '2026-07-04', 'Octavos de final'),
('Lincoln Financial Field', 'Philadelphia', '2026-07-04', 'Octavos de final'),
('MetLife Stadium', 'Nueva York', '2026-07-05', 'Octavos de final'),
('Estadio Azteca', 'Ciudad de Mexico', '2026-07-05', 'Octavos de final'),
('AT&T Stadium', 'Dallas', '2026-07-06', 'Octavos de final'),
('Lumen Field', 'Seattle', '2026-07-06', 'Octavos de final'),
('Mercedes-Benz Stadium', 'Atlanta', '2026-07-07', 'Octavos de final'),
('BC Place', 'Vancouver', '2026-07-07', 'Octavos de final'),

-- CUARTOS DE FINAL
('Gillette Stadium', 'Boston', '2026-07-09', 'Cuartos de final'),
('SoFi Stadium', 'Los Angeles', '2026-07-10', 'Cuartos de final'),
('Hard Rock Stadium', 'Miami', '2026-07-11', 'Cuartos de final'),
('Arrowhead Stadium', 'Kansas City', '2026-07-11', 'Cuartos de final'),

-- SEMIFINALES
('AT&T Stadium', 'Dallas', '2026-07-14', 'Semifinal'),
('Mercedes-Benz Stadium', 'Atlanta', '2026-07-15', 'Semifinal'),

-- TERCER PUESTO
('Hard Rock Stadium', 'Miami', '2026-07-18', 'Tercer puesto'),

-- FINAL
('MetLife Stadium', 'Nueva York', '2026-07-19', 'Final');

CREATE TABLE Predicciones(
    id_fixture INT,
    id_usuario INT,
    goles_local INT,
    goles_visitante INT,
    FOREIGN KEY (id_fixture) REFERENCES fixture(id_fixture) ON DELETE CASCADE
);






