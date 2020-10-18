--1
CREATE TABLE EMP_DDA AS SELECT * FROM employees;
CREATE TABLE DEPT_DDA AS SELECT * FROM departments;

--2. Listati structura tabelelor sursa si a celor create anterior. Ce se observa?
DESC employees;
DESC emp_dda;

DESC departments;
DESC dept_dda;
--Nu mai avem constrangerile aplicate asupra cheilor primare

--3. Listati continutul tabelelor create anterior
SELECT *
FROM emp_dda;

SELECT *
FROM dept_dda;

--4
ALTER TABLE emp_dda
ADD CONSTRAINT pk_emp_dda PRIMARY KEY(employee_id);

ALTER TABLE dept_dda
ADD CONSTRAINT pk_dept_dda PRIMARY KEY(department_id);

ALTER TABLE emp_dda
ADD CONSTRAINT fk_emp_dda
    FOREIGN KEY(department_id) REFERENCES dept_dda(department_id);
    
    
--5. Sa se insereze departamentul 300, cu numele Programare in DEPT_pnu. Pentru a anula efectul instructiunii precedente utilizati comanda ROLLBACK.
INSERT INTO dept_dda(department_id, department_name)
VALUES(300, 'Programare');

ROLLBACK;

--6. Sa se insereze un angajat corespunzator departamentului introdus anterior in tabelul EMP_pnu, precizand valoarea NULL pentru coloanele 
-- a caror valoare nu este cunoscuta la inserare (metoda implicita de inserare). Efectele instructiunii sa devina permanente.
INSERT INTO emp_dda(employee_id, first_name, last_name, email, hire_date, job_id, department_id)
VALUES (207, 'Petrican', 'Andrei', 'petrican.andrei@gmail.ro', sysdate - 15, 'AC_ACCOUNT' ,300);

COMMIT;

--7. Sa se mai introduca un angajat corespunzator departamentului 300, precizand dupa numele tabelului lista coloanelor in care se introduc valori 
-- (metoda explicita de inserare). Se presupune ca data angajarii acestuia este cea curent? (SYSDATE). Salvati înregistrarea.
INSERT INTO emp_dda(employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id)
VALUES (208, 'Petrican', 'Alexandra', 'petricanu@gmail.ro', null, sysdate - 15, 'AD_PRES', null, null, null, 300);

COMMIT;

--8. Este posibila introducerea de inregistrari prin intermediul subcererilor (specificate in locul tabelului).
-- Ce reprezinta, de fapt, aceste subcereri? (view) 
-- Incercati daca este posibila introducerea unui angajat, precizand pentru valoarea employee_id o subcerere care returneaz? (codul maxim +1).
INSERT INTO emp_dda(employee_id, last_name, email, hire_date, job_id, department_id)
VALUES ((SELECT MAX(employee_id) FROM emp_dda) + 1, 'Paul', 'ppaul015@gmail.ro', sysdate, 'SOFT_DEV' , 300);

COMMIT;

--9. Creati un nou tabel, numit EMP1_PNU(p = prenume, nu = nume), care va avea aceeasi structura ca si EMPLOYEES, dar nici o înregistrare.
-- Copiati in tabelul EMP1_PNU salariatii (din tabelul EMPLOYEES) al caror comision depaseste 25% din salariu.
DESC employees;

CREATE TABLE emp1_dda (
    employee_id NUMBER(6) PRIMARY KEY,
    first_name VARCHAR2(20),
    LAST_NAME  VARCHAR2(25) NOT NULL, 
    EMAIL VARCHAR2(25) NOT NULL, 
    PHONE_NUMBER  VARCHAR2(20), 
    HIRE_DATE DATE NOT NULL,         
    JOB_ID VARCHAR2(10) NOT NULL,  
    SALARY NUMBER(8,2), 
    COMMISSION_PCT NUMBER(2,2),  
    MANAGER_ID NUMBER(6),    
    DEPARTMENT_ID NUMBER(4)
);

INSERT INTO emp1_dda
SELECT *
FROM employees
WHERE commission_pct IS NOT NULL AND commission_pct > 0.25;

COMMIT;

--10. Inserati o noua inregistrare in tabelul EMP_PNU care sa totalizeze salariile, sa faca media comisioanelor, iar campurile de tip data 
-- sa contina data curenta si campurile de tip caracter sa contina textul 'TOTAL'. Numele si prenumele angajatului sa corespunda utilizatorului curent (USER).
-- Pentru campul employee_id se va introduce valoarea 0, iar pentru manager_id si department_id se va da valoarea null.
SELECT Username FROM USER_USERS;

DROP TABLE emp1_dda;

CREATE TABLE emp1_dda (
    employee_id NUMBER(6) PRIMARY KEY,
    first_name VARCHAR2(20),
    LAST_NAME  VARCHAR2(25) NOT NULL, 
    EMAIL VARCHAR2(25) NOT NULL, 
    PHONE_NUMBER  VARCHAR2(20), 
    HIRE_DATE DATE NOT NULL,         
    JOB_ID VARCHAR2(10) NOT NULL,  
    SALARY NUMBER(8,2), 
    COMMISSION_PCT NUMBER(2,2),  
     MANAGER_ID NUMBER(6),    
    DEPARTMENT_ID NUMBER(4),
    TOTAL NUMBER(8,2),
    AVERAGE_COMMISSION NUMBER(8,2)
);

INSERT INTO emp1_dda (employee_id, first_name, last_name, email, hire_date, job_id, manager_id, department_id, total, average_commission)
VALUES(0,'DANA', 'DASCALESCU', 'TOTAL:', sysdate, 'SA_REP', null, null, (SELECT SUM(salary) FROM emp1_dda), (SELECT AVG(NVL(commission_pct,0)) FROM emp1_dda));


--12. Creati 2 tabele emp2_pnu si emp3_pnu cu aceeasi structura ca tabelul EMPLOYEES, dar fara inregistrari.
-- Prin intermediul unei singure comenzi, copiati din tabelul EMPLOYEES:
--- in tabelul EMP1_PNU salariatii care au salariul mai mic decat 5000;
--- in tabelul EMP2_PNU salariatii care au salariul cuprins între 5000 si 10000;
--- in tabelul EMP3_PNU salariatii care au salariul mai mare decât 10000.
--Verificati rezultatele, apoi stergeti toate inregistrarile din aceste tabele.
DROP TABLE emp1_dda;

CREATE TABLE emp1_dda (
    employee_id NUMBER(6) PRIMARY KEY,
    first_name VARCHAR2(20),
    LAST_NAME  VARCHAR2(25) NOT NULL, 
    EMAIL VARCHAR2(25) NOT NULL, 
    PHONE_NUMBER  VARCHAR2(20), 
    HIRE_DATE DATE NOT NULL,         
    JOB_ID VARCHAR2(10) NOT NULL,  
    SALARY NUMBER(8,2), 
    COMMISSION_PCT NUMBER(2,2),  
    MANAGER_ID NUMBER(6),    
    DEPARTMENT_ID NUMBER(4)
);


CREATE TABLE emp2_dda (
    employee_id NUMBER(6) PRIMARY KEY,
    first_name VARCHAR2(20),
    LAST_NAME  VARCHAR2(25) NOT NULL, 
    EMAIL VARCHAR2(25) NOT NULL, 
    PHONE_NUMBER  VARCHAR2(20), 
    HIRE_DATE DATE NOT NULL,         
    JOB_ID VARCHAR2(10) NOT NULL,  
    SALARY NUMBER(8,2), 
    COMMISSION_PCT NUMBER(2,2),  
    MANAGER_ID NUMBER(6),    
    DEPARTMENT_ID NUMBER(4)
);


CREATE TABLE emp3_dda (
    employee_id NUMBER(6) PRIMARY KEY,
    first_name VARCHAR2(20),
    LAST_NAME  VARCHAR2(25) NOT NULL, 
    EMAIL VARCHAR2(25) NOT NULL, 
    PHONE_NUMBER  VARCHAR2(20), 
    HIRE_DATE DATE NOT NULL,         
    JOB_ID VARCHAR2(10) NOT NULL,  
    SALARY NUMBER(8,2), 
    COMMISSION_PCT NUMBER(2,2),  
    MANAGER_ID NUMBER(6),    
    DEPARTMENT_ID NUMBER(4)
);

SAVEPOINT a;

INSERT ALL
WHEN salary < 5000 THEN INTO emp1_dda
WHEN salary >= 5000 AND salary < 10000 THEN INTO emp2_dda
WHEN salary >= 10000 THEN INTO emp3_dda
SELECT * FROM employees;

SELECT MAX(salary)
FROM emp1_dda;

SELECT MIN(salary), MAX(salary)
FROM emp2_dda;

SELECT MIN(salary)
FROM emp3_dda;

ROLLBACK TO a;

--13. Sa se creeze tabelul EMP0_PNU cu aceeasi structura ca tabelul EMPLOYEES (fara constrangeri), dar fara nici o inregistrare. Copiati din tabelul EMPLOYEES:
--    - in tabelul EMP0_PNU salariatii care lucreaza in departamentul 80;
--    - in tabelul EMP1_PNU salariatii care au salariul mai mic decat 5000;
--    - in tabelul EMP2_PNU salariatii care au salariul cuprins intre 5000 si 10000;
--    - in tabelul EMP3_PNU salariatii care au salariul mai mare decat 10000.
--    Daca un salariat se incadreaza in tabelul emp0_pnu atunci acesta nu va mai fi inserat si in alt tabel(tabelul corespunzator salariului sau).

CREATE TABLE emp0_dda (
    employee_id NUMBER(6) PRIMARY KEY,
    first_name VARCHAR2(20),
    LAST_NAME  VARCHAR2(25) NOT NULL, 
    EMAIL VARCHAR2(25) NOT NULL, 
    PHONE_NUMBER  VARCHAR2(20), 
    HIRE_DATE DATE NOT NULL,         
    JOB_ID VARCHAR2(10) NOT NULL,  
    SALARY NUMBER(8,2), 
    COMMISSION_PCT NUMBER(2,2),  
    MANAGER_ID NUMBER(6),    
    DEPARTMENT_ID NUMBER(4)
);

INSERT FIRST
WHEN department_id = 80 THEN INTO emp0_dda
WHEN salary < 5000 THEN INTO emp1_dda
WHEN salary >= 5000 AND salary < 10000 THEN INTO emp2_dda
WHEN salary > 10000 THEN INTO emp3_dda
SELECT * FROM employees;

--14. Mariti salariul tuturor angajatilor din tabelul EMP_PNU cu 5%. Vizualizati, iar apoi anulati modificarile.
COMMIT; 

UPDATE emp_dda
SET salary = salary * 1.05;

ROLLBACK;

--15. Schimba?i jobul tuturor salaria?ilor din departamentul 80 care au comision în 'SA_REP'. Anulati modificarile
UPDATE emp_dda
SET job_id = 'SA_REP'
WHERE department_id = 80;

ROLLBACK;

--16. Sa se promoveze Douglas Grant la manager in departamentul 20, avand o crestere de salariucu 1000$. Se poate realiza modificarea prin intermediul unei singure comenzi?

UPDATE emp_dda
SET manager_id = ( SELECT employee_id
                   FROM emp_dda
                   WHERE UPPER(first_name) = 'DOUGLAS' AND UPPER(last_name) = 'GRANT')
WHERE department_id = 20;

UPDATE emp_dda
SET salary = salary + 1000
WHERE UPPER(first_name) = 'DOUGLAS' AND UPPER(last_name) = 'GRANT';


--17. Schimba?i salariul si comisionul celui mai prost platit salariat din firma, astfel incat sa fie egale cu salariul si comisionul sefului sau.

UPDATE emp_dda
SET (salary, commission_pct) = ( SELECT salary, commission_pct
                                 FROM emp_dda
                                 WHERE employee_id = ( SELECT manager_id
                                                       FROM emp_dda
                                                       WHERE salary = ( SELECT MIN(salary)
                                                                        FROM emp_dda)))
WHERE salary = ( SELECT MIN(salary)
                 FROM emp_dda);
                 
--18. Sa se modifice adresa de e-mail pentru angajatii care câstiga cel mai mult in departamentul in care lucreaza astfel incat acesta 
--sa devina initiala numelui concatenata cu prenumele. Daca nu are prenume atunci in loc de acesta apare caracterul ‘.’. Anulati modificarile.
UPDATE emp_dda e
SET email = ( SELECT SUBSTR(NVL(first_name, '.'), 1, 1) ||'.'|| last_name
              FROM emp_dda
              WHERE e.employee_id = employee_id)
WHERE salary = ( SELECT MAX(salary)
                 FROM emp_dda
                 WHERE e.department_id = department_id);

ROLLBACK;

--19. Pentru fiecare departament sa se modifice salariul celor care au fost angajati primii astfel incat sa devina media salariilor din companie. 
DESC emp_dda;

UPDATE emp_dda e
SET salary = ( SELECT ROUND(AVG(salary),2)
               FROM emp_dda)
WHERE employee_id IN ( SELECT employee_id
                       FROM emp_dda e1
                       WHERE hire_date = ( SELECT MIN(hire_date)
                                           FROM emp_dda));
                                          
                                          
--20. Sa se modifice jobul si departamentul angajatului avand codul 114, astfel incat sa fie la fel cu cele ale angajatului avand codul 205.
UPDATE emp_dda
SET (department_id, job_id) = ( SELECT department_id, job_id
                                FROM emp_dda
                                WHERE employee_id = 205)
WHERE employee_id = 114;


--21. Stergeti toate inregistrarile din tabelul DEPT_PNU. Ce inregistr?ri se pot ?terge?
-- Se pot sterge toate inregistrarile din dept_dda care nu apar ca si cheie straina
DELETE FROM dept_dda;

--22. Stergeti angajatii care nu au comision. Anulati modificarile.
DELETE FROM emp_dda
WHERE commission_pct IS NOT NULL;

ROLLBACK;

--23. Suprimati departamentele care un au nici un angajat. Anulati modificarile.
DELETE FROM dept_dda
WHERE department_id NOT IN ( SELECT DISTINCT department_id
                             FROM emp_dda);
ROLLBACK;

--24 -> 27
--24. Sa se marcheze un punct intermediar in procesarea tranzactiei.
--28. Sa se stearg? tot continutul tabelului emp_pnu. Listati continutul tabelului.
--29. Sa se renunte la cea mai recenta operatie de stergere.
--30. Listati continutul tabelului. Determinati ca modificarile sa devina permanente.

SAVEPOINT b;

DELETE FROM emp_dda;

SELECT *
FROM emp_dda;

ROLLBACK TO b;

SELECT *
FROM emp_dda;

COMMIT;


--31. Sa se stearga din tabelul EMP_PNU toti angajatii care castiga comision. Sa se introduc? sau sa se actualizeze datele din tabelul EMP_PNU pe baza tabelului employees.
DELETE FROM emp_dda
WHERE commission_pct IS NOT NULL;

MERGE INTO emp_dda
USING employees b
ON (emp_dda.employee_id = b.employee_id)
WHEN MATCHED THEN 
    UPDATE SET 
        first_name=b.first_name,
        last_name=b.last_name,
        email=b.email,
        phone_number=b.phone_number,
        hire_date=b.hire_date,
        job_id=b.job_id,
        salary=b.salary,
        COMMISSION_PCT=b.COMMISSION_PCT,
        MANAGER_ID=b.MANAGER_ID,
        department_id=b.department_id
WHEN NOT MATCHED THEN 
    INSERT (employee_id, first_name,last_name,
        email, phone_number, hire_date, job_id,
        salary, COMMISSION_PCT, MANAGER_ID,
        department_id)
    VALUES (b.employee_id, b.first_name, b.last_name,
        b.email, b.phone_number, b.hire_date, b.job_id,
        b.salary, b.COMMISSION_PCT, b.MANAGER_ID,
        b.department_id);