--1. Sa se creeze tabelul ANGAJATI_pnu (pnu se alcatuieste din prima litera din prenume si primele dou? din numele studentului) 
-- corespunzator schemei relationale: ANGAJATI_pnu(cod_ang number(4), nume varchar2(20), prenume varchar2(20), email char(15),
-- data_ang date, job varchar2(10), cod_sef number(4), salariu number(8, 2), cod_dep number(2))
-- in urm?toarele moduri:
--a) fara precizarea vreunei chei sau constrangeri
CREATE TABLE angajati_dda(
    cod_ang NUMBER(4),
    nume VARCHAR2(20),
    prenume VARCHAR2(20),
    email CHAR(15),
    data_ang DATE DEFAULT sysdate,
    job VARCHAR2(10),
    cod_sef NUMBER(4),
    salariu NUMBER(8,2),
    cod_dep NUMBER(2) 
);

--b) cu precizarea cheilor primare la nivel de coloana si a constrangerilor NOT NULL pentru coloanele nume si salariu;
CREATE TABLE angajati_dda(
    cod_ang NUMBER(4) PRIMARY KEY,
    nume VARCHAR2(20) NOT NULL,
    prenume VARCHAR2(20),
    email CHAR(15),
    data_ang DATE DEFAULT sysdate,
    job VARCHAR2(10),
    cod_sef NUMBER(4),
    salariu NUMBER(8,2) NOT NULL,
    cod_dep NUMBER(2)  
);

--c) cu precizarea cheii primare la nivel de tabel si a constrangerilor NOT NULL pentru coloanele nume si salariu.
CREATE TABLE angajati_dda(
    cod_ang NUMBER(4),
    nume VARCHAR2(20) NOT NULL,
    prenume VARCHAR2(20),
    email CHAR(15),
    data_ang DATE DEFAULT sysdate,
    job VARCHAR2(10),
    cod_sef NUMBER(4),
    salariu NUMBER(8,2) NOT NULL,
    cod_dep NUMBER(2),
    CONSTRAINT pk_cod_angajat PRIMARY KEY(cod_ang)
);


--2
INSERT INTO ANGAJATI_DDA (cod_ang, nume, prenume, 
                          job, salariu, cod_dep)
VALUES ( 100, 'Nume1', 'Prenume1', 
    'Director', 20000, 10);


INSERT INTO ANGAJATI_DDA(cod_ang, nume, prenume, data_ang,
                          job, cod_sef, salariu, cod_dep)
VALUES ( 101, 'Nume2', 'Prenume2',
    TO_DATE('02-02-2004', 'DD-MM-YYYY'), 'Inginer',
    100, 10000, 10);

INSERT INTO ANGAJATI_DDA(cod_ang, nume, prenume, data_ang,
                         job, cod_sef, salariu, cod_dep)
VALUES ( 102, 'Nume3', 'Prenume2',
    TO_DATE('05-06-2000', 'DD-MM-YYYY'), 'Analist', 
    101, 5000, 20);

INSERT INTO ANGAJATI_DDA (cod_ang, nume, prenume, 
                          job, cod_sef, salariu, 
                          cod_dep)
VALUES ( 103, 'Nume4', 'Prenume4', 
    'Inginer', 100, 9000, 20);

INSERT INTO ANGAJATI_DDA(cod_ang, nume, prenume, data_ang,
                         job, cod_sef, salariu, cod_dep)
VALUES ( 104, 'Nume5', 'Prenume5', 
    NULL, 'Analist', 
    101, 3000, 30);
   
    
--3. Creati tabelul ANGAJATI10_pnu, prin copierea angajatilor din departamentul 10 din tabelul ANGAJATI_pnu. Listati structura noului tabel. Ce se observa?
CREATE TABLE angajati10_dda
    AS (SELECT *
        FROM angajati_dda
        WHERE cod_dep = 10);
        
DESC angajati10_dda;  -- Observam ca nu s-a pastrat constrangerea de cheie primara in tabela copiata
        
--4. Introduceti coloana comision in tabelul ANGAJATI_pnu. Coloana va avea tipul de date NUMBER(4,2).
ALTER TABLE angajati_dda
ADD comision NUMBER(4,2);

--5. Este posibila modificarea tipului coloanei salariu în NUMBER(6,2)?
--NU, PENTRU CA AVEM DATE PE COLOANA RESPECTIVA DIFERITE DE NULL => NU SE POATE MICSORA DIMENSIUNEA


--6. Seta?i o valoare DEFAULT pentru coloana salariu.
ALTER TABLE angajati_dda
MODIFY salariu NUMBER(8,2) DEFAULT 0;


--7. Modificati tipul coloanei comision in NUMBER(2, 2) si al coloanei salariu la NUMBER(10,2), in cadrul aceleiasi instructiuni.
ALTER TABLE angajati_dda
MODIFY (comision NUMBER(2,2), salariu NUMBER(10,2));


--8. Actualizati valoarea coloanei comision, setand-o la valoarea 0.1 pentru salariatii al caror job incepe cu litera A.
UPDATE angajati_dda
SET comision = 0.1
WHERE UPPER(job) LIKE ('A%');


--9. Modificati tipul de date al coloanei email in VARCHAR2
ALTER TABLE angajati_dda
MODIFY email VARCHAR2(15);


--10. Ad?uga?i coloana nr_telefon in tabelul ANGAJATI_pnu, setandu-i o valoare implicita.
ALTER TABLE angajati_dda
ADD nr_telefon VARCHAR2(12) DEFAULT '+40733000000';


--11. Vizualizati înregistrarile existente. Suprimati coloana nr_telefon.
--Ce efect ar avea o comanda ROLLBACK in acest moment?
SELECT *
FROM angajati_dda;

ALTER TABLE angajati_dda
DROP COLUMN nr_telefon;

--Comanda ROLLBACK ar avea niciun efect in acest moment, deoarece comenzile ALTER si DROP, instructiuni LDD, realizeaza un comit implicit


--12. Redenumiti tabelul ANGAJATI_pnu în ANGAJATI3_pnu.
RENAME angajati_dda TO angajati3_dda;

--13. Consultati vizualizarea TAB din dictionarul datelor. Redenumiti angajati3_pnu în angajati_pnu.
DESC tab;

SELECT *
FROM tab;

RENAME angajati3_dda TO angajati_dda;

--14. Suprimati continutul tabelei angajati10_pnu fara a suprima structura acestuia.
TRUNCATE TABLE angajati10_dda;


--15. Creati si tabelul DEPARTAMENTE_pnu, corespunzator schemei rela?ionale:
--DEPARTAMENTE_pnu (cod_dep# number(2), nume varchar2(15), cod_director number(4))
--specificand doar constrangerea NOT NULL pentru nume.
CREATE TABLE departamente_dda (
    cod_dep# NUMBER(2),
    nume VARCHAR2(15) NOT NULL,
    cod_director NUMBER(4)
);

DESC departamente_dda;

--16.
INSERT INTO DEPARTAMENTE_DDA 
VALUES ( 10, 'Administrativ', 100);

INSERT INTO DEPARTAMENTE_DDA 
VALUES ( 20, 'Proiectare', 101);

INSERT INTO  DEPARTAMENTE_DDA
VALUES (30, 'Programare', null);

COMMIT;

--17. Se va preciza apoi cheia primara cod_dep, fara suprimarea si recreerea tabelului (comanda ALTER).
ALTER TABLE departamente_dda
ADD CONSTRAINT pk_departamente PRIMARY KEY(cod_dep#);

--18. Sa se precizeze constrangerea de cheie externa pentru coloana cod_dep din ANGAJATI_pnu:
DESC angajati_dda;
--a) fara suprimarea tabelului
ALTER TABLE angajati_dda
ADD FOREIGN KEY (cod_dep) REFERENCES departamente_dda(cod_dep#);

--b) prin suprimarea si recrearea tabelului, cu precizarea noii constrangeri la nivel de coloana ({DROP, CREATE} TABLE). 
-- De asemenea, se vor mai preciza constrangerile (la nivel de coloana, dac? este posibil):
--  - PRIMARY KEY pentru cod_ang;
--  - FOREIGN KEY pentru cod_sef;
--  - UNIQUE pentru combina?ia nume + prenume;
--  - UNIQUE pentru email;
--  - NOT NULL pentru nume;
--  - verificarea cod_dep >0;
--  - verificarea ca salariul sa fie mai mare decat comisionul*100.
DROP TABLE angajati_dda;

CREATE TABLE angajati_dda(
    cod_ang NUMBER(4) PRIMARY KEY,
    nume VARCHAR2(20) NOT NULL,
    prenume VARCHAR2(20),
    email CHAR(15) UNIQUE,
    date_ang DATE DEFAULT sysdate,
    job VARCHAR2(10),
    cod_sef NUMBER(4),
    salariu NUMBER(8,2) NOT NULL,
    comision NUMBER(2,2),
    cod_dep NUMBER(2),
    FOREIGN KEY (cod_sef) REFERENCES angajati_dda(cod_ang),
    CHECK(cod_dep > 0),
    CHECK(salariu > comision * 100),
    CONSTRAINT pnu UNIQUE (nume,prenume)
);


--19. Suprimati si recreati tabelul, specificand toate constrangerile la nivel de tabel (in masura in care este posibil).
DROP TABLE angajati_dda;

DESC departamente_dda;

CREATE TABLE angajati_dda(
    cod_ang NUMBER(4) PRIMARY KEY,
    nume VARCHAR2(20) NOT NULL,
    prenume VARCHAR2(20),
    email CHAR(15) UNIQUE,
    data_ang DATE DEFAULT sysdate,
    job VARCHAR2(10) NOT NULL,
    cod_sef NUMBER(4),
    salariu NUMBER(8,2) NOT NULL,
    comision NUMBER(2,2) DEFAULT 0,
    cod_dep NUMBER(2),
    FOREIGN KEY (cod_sef) REFERENCES angajati_dda(cod_ang),
    FOREIGN KEY (cod_dep) REFERENCES departamente_dda(cod_dep#),
    CHECK(cod_dep > 0),
    CHECK(salariu > comision * 100),
    CONSTRAINT PNU UNIQUE (nume,prenume)
);


--20. Reintroducerea datelor in tabel
SELECT *
FROM departamente_dda;


INSERT INTO ANGAJATI_DDA(cod_ang, nume, prenume, email, 
                         data_ang, job, salariu, cod_dep)
VALUES ( 101, 'Voinea', 'Andrei', 'andrei@gmail.ro',
    TO_DATE('02-02-2004', 'DD-MM-YYYY'), 'Inginer', 10000, 30);
    
    
INSERT INTO ANGAJATI_DDA(cod_ang, nume, prenume, data_ang,
                          job, cod_sef, salariu, cod_dep)
VALUES (110, 'Oanea', 'Elena',
    TO_DATE('02-02-2006', 'DD-MM-YYYY'), 'Inginer', 
            101, 10000, 20);
            
COMMIT;

--21 Suprimarea tabelului departamente_dda ar fi fost posibila daca nicio linie din acesta nu ar fi avut copii in tabela ANGAJATI_DDA, 
-- adica exista o constrangere de cheie externa ce refera catre tabela departamente_dda.

--22. Sunt utile pentru a afla informatii despre tabelele, constrabgeri etc. din schema curenta.
DESC tab;
DESC user_tables;
DESC user_constraints;

SELECT * FROM tab;

SELECT table_name FROM user_tables;

SELECT * FROM user_constraints;


--23. a)Listati informatiile relevante (cel putin nume, tip si tabel) despre constrangerile asupra tabelelor angajati_pnu si departamente_pnu.
SELECT constraint_name, constraint_type, table_name
FROM user_constraints
WHERE lower(table_name) IN ('angajati_dda', 'departamente_dda');

-- Tipul constrângerilor este marcat prin:
-- • P - pentru cheie primar?
-- • R – pentru constrângerea de integritate referen?ial? (cheie extern?);
-- • U – pentru constrângerea de unicitate (UNIQUE);
-- • C – pentru constrângerile de tip CHECK.

--b) Aflati care sunt coloanele la care se refera constrangerile asupra tabelelor angajati_pnu si departamente_pnu.
SELECT constraint_name, table_name, column_name
FROM user_cons_columns
WHERE lower(table_name) IN ('angajati_dda', 'departamente_dda');

--24. Introduceti constrangerea NOT NULL asupra coloanei email.
TRUNCATE TABLE angajati_dda;

ALTER TABLE angajati_dda
MODIFY email NOT NULL;

--25 (Incercati sa) ad?ugati o noua înregistrare în tabelul ANGAJATI_pnu, care sa corespunda codului de departament 50. Se poate?

SELECT *
FROM departamente_dda;

-- Departamentul cu codul 50 nu se afla in tabela departamente_dda.
-- In tabela ANGAJATI_DDA avem o constrangere de cheie externa pentru coloana cod_dep ce refera la coloana cod_dep#(PK) din tabela DEPARTAMENTE_DDA.
-- Din acest motiv nu putem adauga o noua inregistrare in tabelul ANGAJATI_DDA care sa corespunda codului de departament 50.

INSERT INTO ANGAJATI_DDA(cod_ang, nume, prenume, email, data_ang,
                          job, salariu, cod_dep)
VALUES (102, 'Andrei', 'Sorina', 'sorina@yahoo.ro',
        TO_DATE('02-02-2006', 'DD-MM-YYYY'), 'Inginer', 10000, 50);
            
-- Error report- ORA-02291: integrity constraint (GRUPA31.SYS_C00349414) violated - parent key not found

--Pentru a remedia problema vom insera mai intai departamentul cu codul 50 in tabela DEPARTAMENTE_DDA
INSERT INTO DEPARTAMENTE_DDA(cod_dep#,nume, cod_director)
VALUES ('50', 'HUMAN RESOURCES', 102);

INSERT INTO ANGAJATI_DDA(cod_ang, nume, prenume, email, data_ang,
                          job, salariu, cod_dep)
VALUES (102, 'Andrei', 'Sorina', 'sorina@gmail.ro',
        TO_DATE('02-02-2006', 'DD-MM-YYYY'), 'Manager', 10000, 50);
     
        
--26. Adaugati un nou departament, cu numele Analiza, codul 60 si directorul null in DEPARTAMENTE_pnu. COMMIT.
INSERT INTO DEPARTAMENTE_DDA(cod_dep#, nume)
VALUES (60, 'Analiza');

COMMIT;

--27. (Incercati sa) stergeti departamentul 20 din tabelul DEPARTAMENTE_pnu.
--NU putem sa stergem departamentul 20 intrucat incalcam una dintre regulile de intregritate structurala(integritatea referirii).
--In tabela angajatii_dda avem o inregistrare ce corespunde codului de departament 20 si constrangerea:  FOREIGN KEY (cod_dep) REFERENCES departamente_dda(cod_dep#),

SELECT *
FROM angajati_dda
WHERE cod_dep = 20;

--Urmatoarea intructiune va returna eroarea:
--ORA-02292: integrity constraint (GRUPA31.SYS_C00349414) violated - child record found
DELETE FROM departamente_dda
WHERE cod_dep# = 20;  

--28. Stergeti departamentul 60 din DEPARTAMENTE_pnu. ROLLBACK.
DELETE FROM departamente_dda
WHERE cod_dep# = 60;

ROLLBACK;

--29. (Incercati sa) introduceti un nou angajat, specificand valoarea 114 pentru cod_sef. Ce se obtine?
SELECT *
FROM angajati_dda
WHERE cod_ang = 114;

-- NU avem nicio inregistrare in tabela angajati_dda care sa corespunda cod_ang = 114. cod_sef este o cheie externa ce refera la tabela angajati_dda, coloana cod_ang ( SELF JOIN).
-- Deci nu putem introduce niciun angajat al carui sef este angajatul cu codul 114, deoarece acesta nu exista.
ALTER TABLE angajati_dda
MODIFY email VARCHAR(64);

INSERT INTO ANGAJATI_DDA(cod_ang, nume, prenume, email, data_ang,
                         cod_sef, job, salariu, cod_dep)
VALUES ((SELECT MAX(cod_ang) + 1 FROM angajati_dda), 
        'Florea', 'Alexandra', 'florea.alexandra@gmail.ro',
        TO_DATE('02-02-2006', 'DD-MM-YYYY'), 114, 'Analyst', 10000, 60);
        

--30. Adaugati un nou angajat, avand codul 114. Incercati din nou introducerea inregistrarii de la exercitiul 29.
ALTER TABLE angajati_dda
MODIFY email VARCHAR2(64);

INSERT INTO ANGAJATI_DDA(cod_ang, nume, prenume, email, data_ang,
                        job, salariu, cod_dep)
VALUES (114,'Petrican', 'Larisa', 'petrican.larisa@gmail.com',
        sysdate - 4, 'Manager', 12000, 60);
        
INSERT INTO ANGAJATI_DDA(cod_ang, nume, prenume, email, data_ang,
                         cod_sef, job, salariu, cod_dep)
VALUES (115, 'Florea', 'Alexandra', 'floreaa@gmail.ro',
        TO_DATE('02-02-2006', 'DD-MM-YYYY'), 114, 'Analyst', 10000, 60);
COMMIT;
        
-- Care este ordinea de inserare, atunci cand avem constrangeri de cheie externa? Mai intai PK apoi FK.

--31. Se doreste stergerea automata a angajatilor dintr-un departament, odata cu suprimarea departamentului. 
-- Pentru aceasta, este necesara introducerea clauzei ON DELETE CASCADE in definirea constrangerii de cheie externa. 
-- Suprimati constrangerea de cheie externa asupra tabelului ANGAJATI_pnu si reintroduceti aceasta constrangere.

SELECT constraint_name, table_name, column_name
FROM user_cons_columns
WHERE lower(table_name) IN ('angajati_dda');

ALTER TABLE angajati_dda
DROP CONSTRAINT SYS_C00421894;

ALTER TABLE angajati_dda
ADD CONSTRAINT FK_dep FOREIGN KEY (cod_dep) REFERENCES departamente_dda(cod_dep#)
    ON DELETE CASCADE;


--32. Stergeti departamentul 20 din DEPARTAMENTE_pnu. Ce se întâmpla? Rollback.
SELECT * FROM angajati_dda;
SELECT * FROM departamente_dda;

DELETE FROM departamente_dda
WHERE cod_dep# = 20;

SELECT * FROM angajati_dda;
SELECT * FROM departamente_dda;

-- Odata cu stergerea departamentului 20 din tabela departamente_dda se vor sterge si copii din tabela angajati_dda
--( se vor sterge toate inregistrarile cu angajatii care au codul departamentului egal cu 20)
ROLLBACK;

--33. Introduceti constrangerea de cheie externa asupra coloanei cod_director a tabelului DEPARTAMENTE_pnu. Se doreste ca stergerea unui angajat care este director de departament
-- sa atraga dupa sine setarea automata a valorii coloanei cod_director la null.
SELECT constraint_name, constraint_type, table_name, search_condition, status
FROM user_constraints
WHERE constraint_type = 'R';

ALTER TABLE angajati_dda
DROP CONSTRAINT SYS_C00421893;

ALTER TABLE angajati_dda
ADD CONSTRAINT FK_COD_SEF
    FOREIGN KEY (cod_sef)
    REFERENCES angajati_dda(cod_ang)
    ON DELETE SET NULL;
    
ALTER TABLE angajati_dda
ADD UNIQUE (cod_sef);

ALTER TABLE departamente_dda
ADD CONSTRAINT cod_director_fk
    FOREIGN KEY (cod_director)
    REFERENCES ANGAJATI_DDA(cod_ang)
    ON DELETE SET NULL;
     
--34. Actualizati tabelul DEPARTAMENTE_PNU, astfel incât angajatul având codul 102 s? devin?
--directorul departamentului 30. Stergeti angajatul avand codul 102 din tabelul ANGAJATI_pnu.
--Analizati efectele comenzii. Rollback.
DESC departamente_dda;

UPDATE angajati_dda
SET cod_dep = 30
WHERE cod_ang = 102;

UPDATE departamente_dda
SET cod_director = 102
WHERE cod_dep# = 30;

SELECT *
FROM departamente_dda;

SELECT * 
FROM ANGAJATI_DDA;

-- Putem  sterge  angajatul  102  pentru  ca  nu  are  subalterni si in  momentul  stergerii, conform constrangerii ON DELETE SET NULL, cod_director devine NULL
DELETE FROM angajati_dda
WHERE cod_ang = 102;

SELECT *
FROM departamente_dda;

SELECT * 
FROM ANGAJATI_DDA;

--Este posibila suprimarea angajatului având codul 101? Comentati.
--Suprimarea angajatului 101 este posibila doar daca nu are subalterni in momentul stergerii

--35
ALTER TABLE angajati_dda
ADD CONSTRAINT val_sal CHECK(salariu <= 30000);

--36
-- Nu se poate modifica salariul angajatului intrucat avem constrangerea VAL_SAL(salariul nu poate fi mai mare de 30000)
UPDATE angajati_dda
SET salariu = 35000
WHERE cod_ang = 114;

--37
ALTER TABLE angajati_dda
DISABLE CONSTRAINT val_sal;

UPDATE angajati_dda
SET salariu = 35000
WHERE cod_ang = 114;

--Dupa updatarea informatii nu mai putem activa constrangerea
ALTER TABLE angajati_dda
ENABLE CONSTRAINT val_sal;