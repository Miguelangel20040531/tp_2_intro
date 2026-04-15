
CREATE DATABASE IF NOT EXISTS 'mundial';
USE mundial;

CREATE TABLE IF NOT EXISTS fixture (
    id INT AUTO_INCREMENT PRIMARY KEY,
    local VARCHAR(255) NOT NULL,
    visitante VARCHAR(255) NOT NULL,
    estadio VARCHAR(255) NOT NULL,
    ciudad VARCHAR(255) NOT NULL,
    fecha DATE NOT NULL,
    fase VARCHAR(255) NOT NULL,
    goles_local INT NOT NULL,
    goles_visitante INT NOT NULL
)

INSERT INTO fixture (local, visitante, estadio, ciudad, fecha, fase) VALUES
(Mexico, Sudafrica, Estadio Azteca, Ciudad de Mexico, '2010-06-11', 'Fase de grupos')