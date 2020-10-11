--1
SELECT first_name||' '||last_name||' castiga '||salary||' lunar, dar doreste '||salary*3 "Salariul ideal"
FROM employees;


--2. Scrieti o cerere prin care sa se afiseze prenumele salariatului cu prima litera majuscula si toate celelalte litere mici, numele acestuia cu majuscule si lungimea numelui, 
-- pentru angajatii al caror nume incepe cu J sau M sau care au a treia litera din nume A. Rezultatul va fi ordonat descresc?tor dup? lungimea numelui.
--Varianta 1
--Varianta 1
SELECT INITCAP(last_name) prenume,
    UPPER(first_name) nume, 
    LENGTH(first_name) lungime
FROM employees
WHERE UPPER(first_name) LIKE ('J%')
    OR UPPER(first_name) LIKE ('M%')
    OR UPPER(first_name) LIKE ('__A%')
ORDER BY lungime DESC;

--Varianta 2
SELECT INITCAP(last_name) prenume,
    UPPER(first_name) nume, 
    LENGTH(first_name) lungime
FROM employees
WHERE SUBSTR(UPPER(first_name), 1, 1) = 'J'
OR SUBSTR(UPPER(first_name), 1, 1) = 'M'
OR SUBSTR(UPPER(first_name), 3, 1) = 'A'
ORDER BY lungime DESC;


--3 Sa se afiseze pentru angajatii cu prenumele „Steven”, codul, numele ?i codul departamentului in care lucreaza. 
-- Cautarea trebuie sa nu fie case-sensitive, iar eventualele blank-uri care preced sau urmeaza numelui trebuie ignorate.
--Varianta 1
SELECT employee_id, first_name||' '||last_name AS name, department_id
FROM employees
WHERE LTRIM(RTRIM(INITCAP(first_name))) = 'Steven';

--Varianta 2
SELECT employee_id, first_name||' '||last_name AS name, department_id
FROM employees
WHERE TRIM(BOTH ' ' FROM INITCAP(first_name)) = 'Steven';


--4.
--Varianta 1
SELECT employee_id, first_name||' '||last_name AS name, 
    INSTR(LOWER(last_name), 'a') "Position of first 'a' in name"
FROM employees
WHERE UPPER(last_name) LIKE '%E';

--Varianta 2
SELECT employee_id, first_name||' '||last_name AS name, 
    INSTR(LOWER(last_name), 'a') "Position of first 'a' in name"
FROM employees
WHERE SUBSTR(LOWER(last_name), -1, 1) = 'e';


--5.
SELECT *
FROM employees
WHERE MOD(ROUND(sysdate - hire_date), 7) = 0;

--6. Sa se afiseze codul salariatului, numele, salariul, salariul marit cu 15%, exprimat cu doua zecimale si numarul de sute al salariului nou rotunjit la 2 zecimale. 
-- Se vor lua în considerare salariatii al caror salariu nu este divizibil cu 1000.
SELECT employee_id, first_name||' '||last_name "Nume angajat",
        TRUNC(salary*1.15,2) "Salariu nou",
        ROUND(TRUNC(salary*1.15,2)/100, 2) "Numar sute"
FROM employees
WHERE MOD(salary, 1000) <> 1000;


--7. S? se listeze numele ?i data angaj?rii salaria?ilor care câ?tig? comision. Pentru a nu ob?ine alias-ul datei angaj?rii trunchiat, utiliza?i func?ia RPAD.
SELECT first_name||' '||last_name AS "Nume angajat", RPAD(hire_date, 14, ' ') AS "Data angajarii"
FROM employees
WHERE commission_pct IS NOT NULL;


--8. S? se afi?eze data (numele lunii, ziua, anul, ora, minutul si secunda) de peste 30 zile.
SELECT TO_CHAR(sysdate + 30, 'MONTH DAY YYYY HH24:MI:SS') "Data de peste 30 de zile"
FROM dual;

--9. S? se afi?eze numarul de zile ramase pana la sfarsitul anului.
--Varianta 1
SELECT ROUND(ADD_MONTHS(TRUNC(sysdate, 'YEAR'), 12) - 1 - sysdate)
FROM dual;

--Varianta 2
SELECT ROUND(TO_DATE('31/DEC/2020', 'DD/MON/YYYY') - sysdate)
FROM dual;

--10.
--a.
SELECT TO_CHAR(sysdate + 1/2, 'DD/MON/YYYY HH24:MI:SS') "Data de peste 12 ore"
FROM dual;

--b.
SELECT TO_CHAR(sysdate + 5/1440, 'DD/MON/YYYY HH24:MI:SS') "Data de peste 5 minute"
FROM dual;


--11. Sa se afiseze numele si prenumele angajatului, data angajarii si data negocierii salariului, care este prima zi de Luni dupa 6 luni de serviciu.
SELECT first_name||' '||last_name AS "Nume", hire_date AS "Data angajarii",
    NEXT_DAY(ADD_MONTHS(hire_date, 6), 'MONDAY') AS "Negociere"
FROM employees;


--12. Pentru fiecare angajat sa se afiseze numele si numarul de luni de la data angajarii. 
-- Sa se ordoneze rezultatul dupa numarul de luni lucrate. Se va rotunji numarul de luni la cel mai apropiat numar intreg.
SELECT first_name||' '||last_name AS "Nume angajat",
    CEIL(MONTHS_BETWEEN(sysdate, hire_date)) AS "Luni lucrate"
FROM employees
ORDER BY 2 DESC;


--13. Sa se afiseze numele, data angajarii si ziua saptamanii in care a inceput lucrul fiecare salariat. Eticheta?i coloana “Zi”. 
-- Ordonati rezultatul dupa ziua saptamanii, începând cu Luni.
--Varianta 1
SELECT first_name||' '||last_name AS "Nume angajat", hire_date AS "Data angajarii"
FROM employees
ORDER BY MOD(TO_CHAR(hire_date, 'D') + 5, 7);

--Varianta 2
SELECT first_name||' '||last_name AS "Nume angajat", hire_date AS "Data angajarii"
FROM employees
ORDER BY 
    CASE TO_CHAR(hire_date, 'D')
        WHEN '1' THEN '8'
        ELSE TO_CHAR(hire_date, 'D')
    END;
    
--Varianta 3
SELECT first_name||' '||last_name "Name", hire_date "Data angajarii",  TO_CHAR(hire_date, 'DAY') AS "Zi"
FROM employees
ORDER BY
    CASE UPPER(TRIM(BOTH ' ' FROM "Zi"))
        WHEN 'MONDAY' THEN 1
        WHEN 'TUESDAY' THEN 2
        WHEN 'WEDNESDAY' THEN 3
        WHEN 'THURSDAY' THEN 4
        WHEN 'FRIDAY' THEN 5
        WHEN 'SATURDAY' THEN 6
        WHEN 'SUNDAY' THEN 7
    END;



--14. Sa se afiseze numele angajatilor si comisionul. Daca un angajat nu castiga comision, sa se scrie “Fara comision”.
SELECT e.first_name||' '||e.last_name "Nume angajat", DECODE(NVL(commission_pct, 0), 0, 'Fara comision', commission_pct) "Comision"
FROM employees e;


--15. Sa se listeze numele, salariul si comisionul tuturor angajatilor al caror venit lunar depaseste 10000$.
SELECT e.first_name||' '||e.last_name "Nume angajat", 
    salary, NVL(commission_pct, 0) "Comision"
FROM employees e
WHERE salary + salary *  NVL(commission_pct, 0) > 10000;


--16.
--Varianta 1
SELECT first_name||' '||last_name AS "Nume angajat", job_id AS "Cod job", salary AS "Salariu",
    DECODE(job_id, 'IT_PROG', salary + salary*0.20, 'SA_REP', salary + salary * 0.25, 'SA_MAN', salary + 0.35) AS "Salariu negociat"
FROM employees;


--Varianta 2
SELECT first_name||' '||last_name AS "Nume angajat", job_id AS "Cod job", salary AS "Salariu",
    CASE job_id
        WHEN 'IT_PROG' THEN salary * 1.20
        WHEN 'SA_REP' THEN salary * 1.25
        WHEN 'SA_MAN' THEN salary * 1.35
        ELSE salary
    END "Salariu negociat"
FROM employees;



--17. Sa se afiseze numele salariatului, codul si numele departamentului pentru toti angajatii.
-- Varianta 1
SELECT employees.last_name||' '||employees.first_name AS "Name", employees.department_id, departments.department_name
FROM employees
LEFT JOIN  departments ON employees.department_id = departments.department_id;

-- Varianta 2
SELECT last_name||' '||first_name AS "Name", department_id, department_name
FROM employees
JOIN departments USING(department_id);

-- Varianta 3 -- non-standard
SELECT last_name||' '||first_name, department_name, employees.department_id
FROM employees, departments
WHERE employees.department_id = departments.department_id(+);

--18. Sa se listeze titlurile job-urile care exista in departamentul 30.
SELECT DISTINCT jobs.job_title
FROM jobs
INNER JOIN employees ON jobs.job_id = employees.job_id
WHERE employees.department_id = 30;


--19. Sa se afiseze numele angajatului, numele departamentului si locatia pentru toti angajatii care castiga comision.
SELECT employees.last_name||' '||employees.first_name AS "Nume angajat", 
    departments.department_name AS "Departament", 
    locations.city||', '||locations.street_address AS "Locatie"
FROM employees 
LEFT JOIN departments USING(department_id)
LEFT JOIN locations USING(location_id)
WHERE employees.commission_pct IS NOT NULL;


--20. Sa se afiseze numele salariatului si numele departamentului pentru toti salariatii care au litera A inclusa in nume.
--Varianta 1
SELECT employees.first_name||' '||employees.last_name AS "Nume angajat", departments.department_name AS "Departament"
FROM employees
LEFT JOIN departments USING(department_id)
WHERE UPPER(employees.first_name||' '||employees.last_name) LIKE '%A%';

--Varianta 2
SELECT employees.first_name||' '||employees.last_name AS "Nume angajat", departments.department_name AS "Departament"
FROM employees, departments
WHERE employees.department_id = departments.department_id(+) AND
    INSTR(LOWER(employees.first_name||' '||employees.last_name), 'a') <> 0;
    

--21. Sa se afiseze numele, job-ul, codul si numele departamentului pentru toti angajatii care lucreaza in Oxford.
SELECT e.first_name||' '||e.last_name AS "Name", e.employee_id AS "Employee Id", j.job_title AS "Job title", 
    a.street_address||', '||a.postal_code||', '||a.city AS "Address"
FROM employees e
INNER JOIN jobs j ON e.job_id = j.job_id
INNER JOIN departments d ON e.department_id = d.department_id
INNER JOIN locations a ON d.location_id = a.location_id
WHERE UPPER(a.city) LIKE '%OXFORD%';


--22. Sa se afiseze codul angajatului ?i numele acestuia, impreun? cu numele si codul sefului sau direct. Se vor eticheta coloanele Ang#, Angajat, Mgr#, Manager.
SELECT e1.employee_id AS "Ang#", e1.first_name||' '||e1.last_name AS "Angajat",
    m.employee_id AS "Mgr#", m.first_name||' '||m.last_name AS "Manager"
FROM employees e1, employees m
WHERE e1.manager_id = m.employee_id;

--Pentru afisarea tuturor angajatilor, inclusiv cei care nu au sef
SELECT e1.employee_id AS "Ang#", e1.first_name||' '||e1.last_name AS "Angajat",
    m.employee_id AS "Mgr#", m.first_name||' '||m.last_name AS "Manager"
FROM employees e1, employees m
WHERE e1.manager_id = m.employee_id(+);


--23. Creati o cerere care sa afiseze numele angajatului, codul departamentului si toti salariatii care lucreaza in acelasi departament cu el.
SELECT e1.employee_id, e1.first_name||' '||e1.last_name, e2.employee_id, e2.first_name||' '||e2.last_name
FROM employees e1, employees e2
WHERE e1.department_id = e2.department_id AND e1.employee_id <> e2.employee_id
ORDER BY e1.employee_id;


--24. Sa se afiseze numele si data angajarii pentru salariatii care au fost angajati dup? Gates.
SELECT e1.first_name||' '||e1.last_name NAME, e1.hire_date
FROM employees e1, employees e2
WHERE UPPER(e2.last_name) = 'GATES' 
    AND e2.hire_date > e1.hire_date;
    
    
--25. Sa se afiseze numele salariatului si data angajarii impreuna cu numele si data angajarii sefului direct pentru salariatii care au fost angajati inaintea sefilor lor.
SELECT e.employee_id AS "Ang#", e.first_name||' '||e.last_name AS "Angajat",
    m.employee_id AS "Mgr#", m.first_name||' '||m.last_name AS "Manager"
FROM employees e, employees m
WHERE e.manager_id = m.employee_id AND
    e.hire_date < m.hire_date;