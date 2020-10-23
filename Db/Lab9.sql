--1. Creati un tabel temporar TEMP_TRANZ_PNU, cu datele persistente doar pe durata unei tranzactii.
--Acest tabel va con?ine o singura coloana x, de tip NUMBER. Introduceti o inregistrare in tabel.
--Listati continutul tabelului. Permanentizati tranzactia si listati din nou continutul tabelului.
CREATE GLOBAL TEMPORARY TABLE TEMP_TRANZ_DDA (
    x NUMBER
)ON COMMIT DELETE ROWS;

INSERT INTO temp_tranz_dda
VALUES (1);

SELECT *
FROM temp_tranz_dda;

--Incheierea tranzactiei
COMMIT;

SELECT *
FROM temp_tranz_dda;

--2. Creati un tabel temporar TEMP_SESIUNE_PNU, cu datele persistente pe durata sesiunii. Cerintele sunt cele de la punctul 1.
CREATE GLOBAL TEMPORARY TABLE TEMP_SESIUNE_DDA (
    x NUMBER
)ON COMMIT PRESERVE ROWS;

INSERT INTO temp_sesiune_dda
VALUES (1);

SELECT *
FROM TEMP_SESIUNE_DDA;

COMMIT;

SELECT *
FROM TEMP_SESIUNE_DDA;

--3. Initiati inca o sesiune. Listati structura si continutul tabelelor create anterior. Introduceti inca o linie in fiecare din cele doua tabele.
DESC temp_tranz_dda;
DESC temp_sesiune_dda;

--Intrucat am incheiat sesiunea, liniile din vizualizarea temp_sesiune_dda au fost sterse
SELECT *
FROM temp_sesiune_dda;

INSERT INTO temp_tranz_dda
VALUES (1);

INSERT INTO temp_sesiune_dda
VALUES (2);

--4. Stergeti tabelele create anterior. Cum se poate realiza acest lucru?
DROP TABLE temp_tranz_dda;

--Pentru a sterge un tabel ce persista pe intreaga sesiune, mai intai trebuie sa detasam sesiune curenta de tabel
TRUNCATE TABLE temp_sesiune_dda;
DROP TABLE temp_sesiune_dda;

--5. Sa se creeze un tabel temporar angajati_azi_pnu. Sesiunea fiecarui utilizator care se ocupa de angajari va permite stocarea in acest tabel a angajatilor 
-- pe care i-a recrutat la data curenta. La sfarsitul sesiunii, aceste date vor fi sterse. Se aloca spatiu acestui tabel la creare?
DESC emp_dda;

-- Se aloca spatiu acestui tabel al creeare deoarece s-a folosit clauza AS subcerere
CREATE GLOBAL TEMPORARY TABLE ANGAJATI_AZI_DDA
ON COMMIT PRESERVE ROWS
    AS ( SELECT *
         FROM emp_dda
         WHERE hire_date = sysdate);
         
--6. Inserati o noua inregistrare in tabelul angajati_azi_pnu. Incercati actualizarea tipului de date al coloanei last_name a tabelului angajati_azi_pnu.
DESC angajati_azi_dda;

INSERT INTO ANGAJATI_AZI_DDA(EMPLOYEE_ID, LAST_NAME, EMAIL, HIRE_DATE, JOB_ID)
VALUES (1, 'Nume', 'nume@gmail.com', sysdate, 'PU_MAN');

COMMIT;

-- Nu se poate modifica o tabela ce este  utilizata de alta tranzactie in aceeasi sesiune
ALTER TABLE angajati_azi_dda
MODIFY last_name VARCHAR2(28);


--7. Sa se creeze o vizualizare VIZ_EMP30_PNU, care contine codul, numele, email-ul si salariul angajatilor din departamentul 30. 
-- Sa se analizeze structura si con?inutul vizualizarii. Ce se observa referitor la constrangeri? Ce se obtine de fapt la interogarea continutului vizualizarii ?
-- Inserati o linie prin intermediul acestei vizualizari; comentati!
DESC emp_dda;
CREATE OR REPLACE VIEW viz_emp30_dda
AS (SELECT employee_id, last_name, email, salary,
        department_id
    FROM employees
    WHERE department_id = 30);
    
SELECT *
FROM viz_emp30_dda;

-- Daca vrem sa inseram in tabela de baza prin intermediul vizualizarii trebuie introduse coloanele care au constrangerea NOT NULL in tabela de baza,
-- altfel, chiar daca tipul vizualizarii permite efectuarea operatiilor LMD, acestea nu vor fi posibile din cauza constrangerilor NOT NULL.

--INSERT INTO viz_emp30_dda
--VALUES (1, 'Koo', 'koo@email.com', 3000, 30);  -- aceasta cerere va intoarce o eroare

SELECT *
FROM USER_UPDATABLE_COLUMNS
WHERE TABLE_NAME = 'VIZ_EMP30_DDA';


--8. Modificati VIZ_EMP30_PNU astfel incat sa fie posibila inserarea/modificarea continutului tabelului
--de baza prin intermediul ei. Inserati si actualizati o linie prin intermediul acestei vizualizari.
CREATE OR REPLACE VIEW viz_emp30_dda
AS (SELECT employee_id, last_name, email, salary,
        department_id, hire_date, job_id
    FROM employees
    WHERE department_id = 30);
    
SELECT *
FROM viz_emp30_dda;

INSERT INTO viz_emp30_dda
VALUES (1, 'Nume', 'nume@email.com', 3000, 
        30, SYSDATE, 'PU_MAN');

SELECT *
FROM employees
WHERE employee_id = 1;

ROLLBACK;

--9. Sa se creeze o vizualizare, VIZ_EMPSAL50_PNU, care contine coloanele cod_angajat, nume,
--email, functie, data_angajare si sal_anual corespunzatoare angajatilor din departamentul 50.
--Analizati structura si continutul vizualizarii.

CREATE OR REPLACE VIEW viz_empsal50_dda
    AS (SELECT employee_id, last_name, email, job_id, hire_date, salary*12 sal_anual
        FROM employees
        WHERE department_id = 50);
        
DESC viz_empsal50_dda;

SELECT *
FROM viz_empsal50_dda;


--10
--a) Inserati o linie prin intermediul vizualizarii precedente. Comentati.
-- Se poate insera o linie prin intermediul vizualizarii precedente deoarece toate coloanele care au constrangerea NOT NULL in tabela de baza sunt adaugate in vizualizare
INSERT INTO viz_empsal50_dda(employee_id, last_name, email, job_id, hire_date)
VALUES (321, 'Nume2', 'nume2@gmail.ro', 'PU_MAN', sysdate);

--b) Nu este actualizabila coloana sal_anual deoarece a rezultat in urma efectuarii unui calcul
SELECT *
FROM USER_UPDATABLE_COLUMNS
WHERE LOWER(TABLE_NAME) = 'viz_empsal50_dda';


--c) Inserati o linie precizand valori doar pentru coloanele actualizabile
INSERT INTO viz_empsal50_dda(employee_id, last_name, email, job_id, hire_date)
VALUES (321, 'Nume2', 'nume2@gmail.ro', 'PU_MAN', sysdate);


--11.
--a) Sa se creeze vizualizarea VIZ_EMP_DEP30_PNU, astfel incat aceasta sa includa coloanele vizualizarii VIZ_EMP_30_PNU, 
-- precum si numele si codul departamentului. Sa se introduca aliasuri pentru coloanele vizualizarii. 
-- Asigurati-va ca exista constrangerea de cheie externa intre tabelele de baza ale acestei vizualizari.
DESC viz_emp30_dda;

CREATE VIEW viz_emp_dep30_dda
    AS ( SELECT v.employee_id, v.last_name, v.email, v.salary, 
            v.department_id, v.hire_date, v.job_id, d.department_name
         FROM viz_emp30_dda v
         JOIN departments d 
            ON v.department_id = d.department_id);
         
DESC viz_emp_dep30_dda;

--b) Inserati o linie prin intermediul acestei vizualizari.
-- Pentru vizualizarile bazate pe mai multe tabele, orice operatie INSERT, UPDATE sau DELETE poate modifica datele doar din unul din tabelele de baza. 
-- Acest tabel este partajat prin cheie(key preserved).


--12. Sa se creeze vizualizarea VIZ_DEPT_SUM_PNU, care contine codul departamentului si pentru fiecare
--departament salariul minim, maxim si media salariilor. Ce fel de vizualizare se obtine (complexa sau simpla)? 
--Se poate actualiza vreo coloana prin intermediul acestei vizualizari?
CREATE OR REPLACE VIEW VIZ_DEPT_SUM_DDA (dept_id, min_sal, max_sal, med_sal)
AS (SELECT department_id, MIN(salary), MAX(salary),
        ROUND(AVG(salary), 2)
    FROM emp_dda
    GROUP BY department_id);

-- S-a obtinut o vizualizare complexa. Nu se pot actualiza coloanele prin intermediul vizualizarii, deoarce contine
-- clauza GROUP BY si deci nu sunt permise operatiile  LMD asupra acestei vizualizari
SELECT *
FROM USER_UPDATABLE_COLUMNS
WHERE TABLE_NAME = 'VIZ_DEPT_SUM_DDA';


--13. Modificati vizualizarea VIZ_EMP30_PNU astfel incat sa nu permita modificarea sau inserarea de
--linii ce nu sunt accesibile ei. Vizualizarea va selecta si coloana department_id. Dati un nume
--constrangerii si regasiti-o in vizualizarea USER_CONSTRAINTS din dictionarul datelor. Incercati sa
--modificati si sa inserati linii ce nu indeplinesc conditia department_id = 30.
CREATE OR REPLACE VIEW viz_emp30_dda
AS (SELECT employee_id, last_name, email, salary,
        department_id, hire_date, job_id
    FROM emp_dda
    WHERE department_id = 30)
WITH CHECK OPTION CONSTRAINT noua_constrangere;

DESC USER_CONSTRAINTS;

SELECT OWNER, CONSTRAINT_TYPE, TABLE_NAME
FROM USER_CONSTRAINTS
WHERE CONSTRAINT_NAME = 'NOUA_CONSTRANGERE';

--14
--a) Definiti o vizualizare, VIZ_EMP_S_PNU, care sa contina detalii despre angajatii corespunzatori departamentelor 
-- care incep cu litera S. Se pot insera/actualiza linii prin intermediul acestei vizualizari? În care dintre tabele? 
-- Ce se intampla la stergerea prin intermediul vizualizarii?
DESC employees;

CREATE OR REPLACE VIEW VIZ_EMP_S_DDA
AS ( SELECT e.employee_id, e.last_name, e.email, e.hire_date, e.job_id, e.department_id
     FROM emp_dda e
     JOIN departments d ON e.department_id = d.department_id
     WHERE d.department_name LIKE 'S%');

-- Se pot actualiza/insera linii prin intermediul acestei vizualizari doar in tabela employees
INSERT INTO VIZ_EMP_S_DDA (employee_id, last_name, email, hire_date, job_id, department_id)
VALUES (529, 'Nume4', 'nume4@gmail.com', sysdate - 4, 'ST_MAN', 50);

COMMIT;

SELECT *
FROM emp_dda
WHERE employee_id = 529;

--Pentru inserarea in tabela departments trebuie definit un trigger de tip INSTEAD OF

DELETE FROM viz_emp_s_dda -- Se pot sterge date prin intermediul vizualizarii(fiind o vizualizare simpla se permit operatiile LMD)
WHERE employee_id = 529;


--b) Recreati vizualizarea astfel incat sa nu se permita nici o operatie asupra tabelelor de baza prin
-- intermediul ei. Incercati sa introduceti sau sa actualizati inregistrari prin intermediul acestei vizualizari.
CREATE OR REPLACE VIEW VIZ_EMP_S_DDA
AS ( SELECT e.employee_id, e.last_name, e.email, e.hire_date, e.job_id, e.department_id
     FROM emp_dda e
     JOIN departments d ON e.department_id = d.department_id
     WHERE d.department_name LIKE 'S%')
WITH READ ONLY;


--15. Sa se consulte informatii despre vizualizarile utilizatorului curent.
SELECT VIEW_NAME, TEXT
FROM USER_VIEWS;


--16. Sa se selecteze numele, salariul, codul departamentului si salariul maxim din departamentul din
--care face parte, pentru fiecare angajat. Este necesara o vizualizare inline?

--Varianta 1
-- Subcererile însotite de un alias care apar în comenzile SELECT se numesc vizualizari inline, valabile doar pe durata executiei instrcutiunii.
SELECT last_name, salary, department_id, ( SELECT MAX(salary) max_sal
                                           FROM employees em
                                           WHERE em.department_id = e.department_id) max_sal
FROM employees e ;

--Varianta 2
SELECT last_name, salary, department_id, MAX(salary) 
FROM employees
GROUP BY department_id, last_name, salary
ORDER BY 4 DESC;

--17. Sa se creeze o vizualizare VIZ_SAL_PNU, ce contine numele angajatilor, numele, departamentelor, salariile si locatiile pentru toti angajatii. 
--Considerati ca tabele de baza tabelele originale din schema HR. Care sunt coloanele actualizabile?
DESC departments;

CREATE OR REPLACE VIEW VIZ_SAL_DDA
AS ( SELECT e.first_name prenume, e.last_name nume, d.department_name departament, salary salariu, l.city oras
     FROM emp_dda e, departments d, locations l
     WHERE e.department_id = d.department_id AND d.location_id = l.location_id);

SELECT *
FROM USER_UPDATABLE_COLUMNS
WHERE TABLE_NAME = 'VIZ_SAL_DDA';

-- Coloanele actualizabile sunt cele din tabela de baza employees; nu sunt actualizabile coloanele care au fost obtinute din celelalte tabele
-- prin intermediul operatiei JOIN


--18. Sa se creeze vizualizarea V_EMP_PNU asupra tabelului EMP_PNU care contine codul, numele, prenumele, 
-- email-ul si numarul de telefon ale angajatilor companiei. Se va impune unicitatea valorilor coloanei email 
-- si constrangerea de cheie primara pentru coloana corespunzatoare codului angajatului.
CREATE VIEW viz_emp_dda ( employee_id, first_name, last_name,
                          email UNIQUE DISABLE NOVALIDATE, phone_number,
                          CONSTRAINT pk_viz_emp_dda PRIMARY KEY (employee_id) DISABLE NOVALIDATE)
AS SELECT employee_id, first_name, last_name, email, phone_number
FROM emp_dda;


--19. Sa se adauge o constrangere de cheie primara tabelei viz_emp_s_pnu.
DESC viz_emp_s_dda;

ALTER VIEW VIZ_EMP_S_DDA
ADD CONSTRAINT pk_viz_emp_s_dda PRIMARY KEY (employee_id) DISABLE NOVALIDATE;

--20. Creati o secventa pentru generarea codurilor de departamente, SEQ_DEPT_PNU. Secventa va incepe de la 400,
-- va creste cu 10 de fiecare data si va avea valoarea maxima 10000, nu va cicla si nu va incarca nici un numar inainte de cerere.
CREATE SEQUENCE SEQ_DEPT_DDA
START WITH 400
INCREMENT BY 10
MAXVALUE 10000
NOCYCLE
NOCACHE;


--21. Sa se selecteze informatii despre secventele utilizatorului curent (nume, valoare minima, maxima, incrementare, ultimul numar generat).
SELECT sequence_name, min_value, max_value, increment_by, last_number
FROM USER_SEQUENCES;

--22. Creati o secventa pentru generarea codurilor de angajati SEQ_EMP_DDA.
-- implicit INCREMENT BY si START WITH vor fi 1
CREATE SEQUENCE SEQ_EMP_DDA
MAXVALUE 10000
NOCYCLE
NOCACHE;

--23. Sa se modifice toate liniile din EMP_PNU, regenerand codul angajatilor astfel incât sa utilizeze secventa SEQ_EMP_PNU 
-- si sa avem continuitate in codurile angajatilor.
SELECT *
FROM emp_dda;

UPDATE emp_dda
SET employee_id = SEQ_EMP_DDA.NEXTVAL;

--24. Sa se insereze cate o inregistrare noua in EMP_PNU si DEPT_PNU utilizand cele 2 secvente create.
INSERT INTO dept_dda (department_id, department_name)
VALUES (SEQ_DEPT_DDA.NEXTVAL, 'Departament Nou Sequence');

DESC emp_dda;

INSERT INTO emp_dda (employee_id, last_name, email, hire_date, job_id)
VALUES (SEQ_EMP_DDA.NEXTVAL, 'Nume6', 'nume6@email.com', sysdate, 'PU_MAN');


--25. Sa se selecteze valorile curente ale celor doua secvente.
SELECT seq_emp_dda.currval
FROM user_sequences
WHERE ROWNUM <= 1;

SELECT seq_dept_dda.currval
FROM user_sequences
WHERE ROWNUM <= 1;


--26. Stergeti secventa SEQ_DEPT_DDA.
DROP SEQUENCE SEQ_DEPT_DDA;


--27. Sa se creeze un index (normal, neunic) IDX_EMP_LAST_NAME_PNU, asupra coloanei last_name din tabelul emp_pnu.
CREATE INDEX IDX_EMP_LAST_NAME_DDA
ON EMP_DDA(LAST_NAME);


--28. Sa se creeze indecsi unici asupra codului angajatului (employee_id) si 
-- asupra combinatiei last_name, first_name, hire_date prin doua metode (automat si manual).
-- Indexii se creaza automat atunci cand setam o constrangere de tipul PRIMARY KEY sau UNIQUE
SELECT *
FROM USER_CONSTRAINTS
WHERE TABLE_NAME = 'EMP_DDA';

ALTER TABLE emp_dda
DROP CONSTRAINT "PK_EMP_DDA";

ALTER TABLE emp_dda
ADD CONSTRAINT pk_emp_dda PRIMARY KEY(employee_id);

ALTER TABLE emp_dda
ADD CONSTRAINT angajat UNIQUE(last_name, first_name, hire_date);

-- Daca incercam sa creem un index manual pe o cheie primara primim o eroare deoarece coloana respectiva 
-- este deja indexata(automat la crearea constrangerii de cheie primara)
CREATE INDEX IND_EMP_ID1
ON EMP_DDA(employee_id);

-- Asemanator cu exemplul precedent
CREATE UNIQUE INDEX IND_ANGAJAT
ON EMP_DDA(last_name, first_name, hire_date);


--29. Creati un index neunic asupra coloanei department_id din EMP_PNU pentru a eficientiza join-urile dintre acest tabel si DEPT_PNU.
CREATE INDEX IDX_EMP_DDA_DEP_ID
ON EMP_DDA(department_id);


--30. Prespupunand ca se fac foarte des cautari case insensitive asupra numelui departamentului si asupra numelui angajatului, 
-- definiti doi indecsi bazati pe expresiile UPPER(department_name), respectiv LOWER(last_name).
CREATE INDEX IDX_EMP_DDA_LAST_NAME
ON EMP_DDA(LOWER(last_name));

CREATE INDEX IDX_EMP_DDA_DEPT_NAME
ON DEPT_DDA(UPPER(department_name));


--31. Sa se selecteze din dictionarul datelor numele indexului, numele coloanei, pozitia din lista de coloane a indexului 
-- si proprietatea de unicitate a tuturor indecsilor definiti pe tabelele EMP_PNU si DEPT_PNU.
DESC USER_INDEXES;

SELECT index_name, uniqueness, include_column, blevel
FROM user_indexes
WHERE TABLE_NAME = 'EMP_DDA' OR TABLE_NAME = 'DEPT_DDA';


--32. 
DROP INDEX IDX_EMP_LAST_NAME_DDA;


--33. Creati un cluster denumit angajati_pnu avand cheia denumita angajat si dimensiunea 512 bytes.
--Extensia initial? alocata cluster-ului va avea dimensiunea 100 bytes, iar urmatoarele extensii alocate vor avea 
-- dimensiunea de 50 bytes. Pentru a specifica dimensiunile in kilobytes sau megabytes se foloseste K, respectiv M (de exemplu, 100K sau 100M).
CREATE CLUSTER angajati_dda
(angajat NUMBER(6))
SIZE 512
STORAGE (initial 100 next 50);

--34. Definiti un index pe cheia cluster-ului
CREATE INDEX idx_angajati_dda
ON CLUSTER angajati_dda;

--35. Adaugati cluster-ului urmatoarele trei tabele:
--      ? tabelul ang_1_pnu care va contine angajatii avand salariul mai mic decat 5000;
--      ? tabelul ang_2_pnu care va contine angajatii avand salariul intre 5000 si 10000;
--      ? tabelul ang_3_pnu care va contine angajatii avand salariul mai mare decat 10000.
CREATE TABLE ang_1_dda
CLUSTER angajati_dda(employee_id)
AS SELECT * FROM employees WHERE salary < 5000;

CREATE TABLE ang_2_dda
CLUSTER angajati_dda(employee_id)
AS SELECT * FROM employees WHERE salary BETWEEN 5000 AND 10000;

CREATE TABLE ang_3_dda
CLUSTER angajati_dda(employee_id)
AS SELECT * FROM employees WHERE salary > 10000;


--36. Afisati informatii despre cluster-ele create de utilizatorul curent
SELECT *
FROM USER_CLUSTERS;

--37. Afisati numele cluster-ului din care face parte tabela ang_3_onu.
DESC USER_TABLES;

SELECT cluster_name
FROM user_tables
WHERE LOWER(table_name) = 'ang_3_dda';


--38. Eliminati tabelul ang_3_pnu din cluster.
DROP TABLE ang_3_dda;


--39. Verificati daca tabela ang_3_pnu mai face parte dintr-un cluster.
SELECT cluster_name
FROM user_tables
WHERE table_name = 'ANGAJATI_DDA';


--40. Stergeti tabelul ang_2_pnu. Consultati vizualizarea USER_TABLES afisati numele tabelelor care fac parte din cluster-ul definit.
DROP TABLE ang_2_dda;

SELECT table_name
FROM user_tables
WHERE cluster_name = 'ANGAJATI_DDA';


--41. Stergeti cluster-ul definit anterior eliminand si tabelele create.
DROP CLUSTER angajati_dda
INCLUDING TABLES 
CASCADE CONSTRAINTS;


--42. Creati un sinonim public EMP_PUBLIC_PNU pentru tabelul EMP_PNU.
CREATE PUBLIC SYNONYM EMP_PUBLIC_DDA
FOR EMP_DDA;


--43. Creati un sinonim V30_PNU pentru vizualizarea VIZ_EMP30_PNU.
CREATE SYNONYM V30_DDA
FOR VIZ_EMP30_DDA;


--44. Creati un sinonim pentru DEPT_PNU. Utilizati sinonimul pentru accesarea datelor din tabel.
--Redenumiti tabelul. Incercati din nou sa utilizati sinonimul pentru a accesa datele din tabel. Ce se obtine?
CREATE SYNONYM SD_DDA
FOR DEPT_DDA;

SELECT *
FROM SD_DDA;

RENAME DEPT_DDA TO DEPARTAMENTS_DDA;

-- Nu mai putem accesa datele din tabel prin intermediul sinonimului dupa ce modificam numele tabelului
-- In urma redenumirri unui tabel sunt ivalidatte toate obiectele ce depind de obiectul redenumit, cum ar fi vizualizari, sinonime sau proceduri si functii stocate


--45. Eliminati sinonimele create anterior prin intermediul unui script care sa selecteze numele sinonimelor din USER_SYNONYMS care au termina?ia pnu 
-- si sa genereze un fisier cu comenzile de stergere corespunzatoare.

SET FEEDBACK OFF
SET HEADING OFF
SET TERMOUT OFF     -- suprima afisarea rezultatelor pe ecran( acestea vor fi regasite numai in fisierul specificat in comanda SPOOL
SPOOL "delete_synonym.sql"      -- determina inregistrarea tuturor comenziilor care urmeza si a rezultatelor acestora in fisierul specifica
SELECT 'DROP SYNONYM ' || synonym_name ||'; '
FROM user_synonyms
WHERE lower(synonym_name) LIKE '%dda'
/
SPOOL OFF   -- determina oprirea inregistrarii
SET FEEDBACK ON
SET HEADING ON
SET TERMOUT ON;


--46. Sa se creeze si sa se completeze cu inregistrari o vizualizare materializata care va contine numele joburilor, numele departamentelor si 
-- suma salariilor pentru un job, in cadrul unui departament. Reactualizarile ulterioare ale acestei vizualizari se vor realiza prin reexecutarea cererii din definitie.
-- Vizualizarea creata va putea fi aleasa pentru rescrierea cererilor.

CREATE MATERIALIZED VIEW job_dep_sal_dda
BUILD IMMEDIATE
REFRESH COMPLETE
ENABLE QUERY REWRITE
AS SELECT d.department_name, j.job_title, SUM(salary) suma_salarii
    FROM employees e, departments d, jobs j
    WHERE e.department_id = d. department_id
    AND e.job_id = j.job_id
    GROUP BY d.department_name, j.job_title;
    

--47. Sa se creeze tabelul job_dep_pnu. Acesta va fi utilizat ca tabel sumar preexistent in crearea unei
-- vizualizari materializate ce va permite diferente de precizie si rescrierea cererilor.
CREATE TABLE job_dep_dda (
    job VARCHAR2(10),
    dep NUMBER(4),
    suma_salarii NUMBER
);


CREATE MATERIALIZED VIEW job_dep_dda
ON PREBUILT TABLE WITH REDUCED PRECISION
ENABLE QUERY REWRITE AS (
    SELECT j.job_id, d.department_id, SUM(salary) AS suma_salarii
    FROM employees e
    INNER JOIN departments d
        ON e.department_id = d.department_id
    INNER JOIN jobs j
        ON e.job_id = j.job_id
    GROUP BY d.department_id, j.job_id
);


--48. Sa se creeze o vizualizare materializata care contine informatiile din tabelul dep_pnu, permite
-- reorganizarea acestuia si este reactualizata la momentul crearii, iar apoi la fiecare 5 minute.
CREATE MATERIALIZED VIEW dep_vm_dda
    REFRESH START WITH SYSDATE NEXT SYSDATE + 1/288
    WITH PRIMARY KEY
    AS SELECT * FROM departaments_dda;

--49. Modificarea vizualizarii anterioare
ALTER MATERIALIZED VIEW job_del_sal_dda
    REFRESH FAST NEXT SYSDATE + 7 DISABLE QUERY REWRITE;

--50.
DROP MATERIALIZED VIEW job_dep_sal_dda;
DROP MATERIALIZED VIEW dep_vm_dda;
