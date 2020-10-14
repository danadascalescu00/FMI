--1 a)
SELECT d.department_name, j.job_title, AVG(e.salary)
FROM departments d
JOIN employees e ON d.department_id = e.department_id
JOIN jobs j ON e.job_id = j.job_id
GROUP BY ROLLUP (d.department_name, j.job_title);

--b)
SELECT d.department_name, j.job_title, ROUND(AVG(e.salary), 2) Media,
       GROUPING(d.department_name), GROUPING(j.job_title)
FROM departments d
JOIN employees e ON d.department_id = e.department_id
JOIN jobs j ON e.job_id = j.job_id
GROUP BY ROLLUP (d.department_name, j.job_title);


--2 a)
SELECT d.department_name, j.job_title, ROUND(AVG(e.salary), 2) Media
FROM departments d
JOIN employees e ON d.department_id = e.department_id
JOIN jobs j ON e.job_id = j.job_id
GROUP BY CUBE (d.department_name, j.job_title)
ORDER BY d.department_name;

--b)
SELECT d.department_name, j.job_title, ROUND(AVG(e.salary), 2) Media, DECODE(GROUPING(d.department_name), 0, 'Dep', GROUPING(j.job_title), 0, 'Job')
FROM departments d
JOIN employees e ON d.department_id = e.department_id
JOIN jobs j ON e.job_id = j.job_id
GROUP BY CUBE (d.department_name, j.job_title)
ORDER BY d.department_name;


--3. 
SELECT d.department_id "Departament", j.job_title "Job", e.manager_id "Manager#" , MAX(e.salary), SUM(e.salary) "Total"
FROM employees e
JOIN departments d ON e.department_id = d.department_id
JOIN jobs j USING (job_id)
GROUP BY GROUPING SETS ((d.department_id, j.job_title), (j.job_title, e.manager_id), ());


--4
SELECT MAX(salary)
FROM employees
HAVING MAX(salary) > 15000;


--5 a) Sa se afisezez informatii despre angajatii al caror salariu depaseste valoarea medie a salariilor colegilor sai de departament
SELECT *
FROM employees e
WHERE e.salary > (SELECT AVG(salary)
                  FROM employees
                  WHERE e.department_id = department_id 
                    AND e.employee_id <> employee_id);
                  
-- b) Analog cu cererea precedenta, afisandu-se si numele departamentului si media salariilor acestuia si numarul de angajati
--Varianta 1 - subcerere necorelata in clauza FROM
SELECT department_name, em.medie, em.nr_ang, 
    e.employee_id, e.first_name||' '||e.last_name full_name, e.salary
FROM departments d,
    (SELECT department_id, employee_id, first_name, last_name, salary
     FROM employees) e,
    (SELECT ROUND(AVG(salary), 2) medie,  
        COUNT(employee_id) nr_ang,
        e.department_id
     FROM employees e
     GROUP BY e.department_id) em
WHERE d.department_id = em.department_id
    AND e.department_id = d.department_id
    AND e.salary > em.medie;
    
--Varianta 2 - subcerere corelata in clauza SELECT
SELECT first_name||' '||last_name AS "Nume angajat", e.salary AS "Salariu", 
    e.department_id AS "Dep#", department_name AS "Departament",
    (SELECT ROUND(AVG(salary), 3)
     FROM employees
     WHERE department_id = e. department_id) "Salariu mediu",
    (SELECT COUNT(*)
     FROM employees
     WHERE department_id = e. department_id) "Numar angajati"
FROM employees e, departments d
WHERE e.department_id = d.department_id
    AND salary > (SELECT AVG(salary)
                  FROM employees
                  WHERE department_id = e.department_id);



--6. Sa se afiseze numele si salariul angajatilor al caror salariu este mai mare decat salariile medii din toate departamentele
---Varianta 1
SELECT e.first_name||' '||e.last_name "Nume angajat", e.salary "Salariu"
FROM employees e
WHERE e.salary > ALL (SELECT AVG(salary)
                      FROM employees
                      WHERE e.employee_id <> employee_id);
                      
---Varianta 2
SELECT e.first_name||' '||e.last_name "Nume angajat"
FROM employees e
WHERE e.salary > (SELECT MAX(AVG(salary)) 
                   FROM employees
                   WHERE employee_id <> e.employee_id
                   GROUP BY department_id);
                   
                   
--7. Sa se afiseze numele si salariul celor mai prost platiti angajati din fiecare departament.
-- Subcerere sincronizata
SELECT e.first_name||' '||e.last_name "Nume angajat", e.salary "Salariu", e.department_id "Dep#"
FROM employees e
WHERE e.salary = (SELECT MIN(salary)
                  FROM employees
                  WHERE e.department_id = department_id);
                                     
-- Subcerere nesincronizare
SELECT e.first_name||' '||e.last_name "Nume angajat", e.department_id "Departament", e.salary "Salariu"
FROM employees e
WHERE (e.department_id, e.salary) IN (SELECT department_id, MIN(salary)
                                      FROM employees
                                      GROUP BY department_id);                                      
                                      
--Subcerere in clauza FROM
SELECT e1.first_name||' '||e1.last_name "Nume angajat", e1.department_id "Dep#", em.salariu
FROM employees e1, (SELECT department_id, MIN(salary) salariu
                    FROM employees 
                    GROUP BY department_id) em
WHERE e1.department_id = em.department_id;


--8 Pentru fiecare departament, sa se obtina numele salariatului avand cea mai mare vechime din departament.
--Varianta 1 - Subcerere sincronizata
SELECT e.first_name||' '||e.last_name "Nume angajat"
FROM employees e
WHERE sysdate - hire_date = (SELECT MAX(sysdate - hire_date)
                              FROM employees
                              WHERE department_id = e.department_id);
                              
--Varianta 2
SELECT e.first_name||' '||e.last_name "Nume angajat"
FROM employees e
WHERE MONTHS_BETWEEN(SYSDATE, hire_date) = (SELECT MAX(MONTHS_BETWEEN(SYSDATE, hire_date))
                                            FROM employees
                                            WHERE department_id = e.department_id
                                            GROUP BY department_id);
                              
                              
--9 Sa se obtina numele salariatilor care lucreaza intr-un departament in care exista cel putin un
-- angajat cu salariul egal cu salariul maxim din departamentul 30(operatorul exists).
SELECT e.first_name||' '||e.last_name "Nume angajat"
FROM employees e
WHERE EXISTS (SELECT 1
              FROM employees e1
              WHERE e1.salary = (SELECT MAX(salary)
                                 FROM employees e2
                                 WHERE e2.department_id = 30)
              AND e.department_id = e1.department_id);
              
--10. Sa se obtina numele primilor 3 angajati avand salariul maxim.
--Varianta 1
SELECT *
FROM (SELECT first_name||' '||last_name full_name, job_id, salary
      FROM employees
      ORDER BY salary DESC)
WHERE ROWNUM <= 3;

--Varianta 2
SELECT first_name||' '||last_name full_name, job_id, salary
FROM employees e
WHERE 3 > (SELECT COUNT(*)
           FROM employees
           WHERE salary > e.salary)
ORDER BY salary DESC;


--11. Sa se afiseze codul, numele si prenumele angajatilor care au cel putin doi subalterni.
SELECT e.employee_id "Cod", e.last_name "Nume", e.first_name "Prenume"
FROM employees e
WHERE 2 < (SELECT COUNT(*)
           FROM employees
           WHERE manager_id = e.employee_id);
     
           
--12. Sa se determine locatiile în care se afla cel pu?in un departament.
SELECT l.street_address||' '||l.postal_code||' '||l.city||' '||l.state_province||' '||c.country_name "Adresa"
FROM locations l
JOIN countries c ON l.country_id = c.country_id
WHERE EXISTS ( SELECT 1
               FROM departments d
               WHERE d.location_id = l.location_id);
               
--13. Sa se determine departamentele in care nu exista nici un angajat.
SELECT d.department_id, d.department_name
FROM departments d
WHERE NOT EXISTS ( SELECT 1
                   FROM employees e
                   WHERE d.department_id = e.department_id );

--14. Sa se afiseze codul, numele, data angajarii, salariul si managerul pentru:
-- a) subalternii directi ai lui De Haan.
-- b) ierarhia arborescenta de sub De Haan.

--a
SELECT employee_id, last_name, hire_date, salary, manager_id
FROM employees
WHERE manager_id = (SELECT employee_id
                    FROM employees
                    WHERE UPPER(last_name) = 'DE HAAN');

--b
SELECT LEVEL, employee_id, first_name, last_name, hire_date, salary, manager_id
FROM employees
START WITH manager_id = (SELECT employee_id
                         FROM employees
                         WHERE TRIM(BOTH ' ' FROM UPPER(last_name)) = 'DE HAAN')
CONNECT BY PRIOR employee_id = manager_id;
                   
                   
--15. Sa se ob?in? ierarhia sef-subaltern, considerând ca r?d?cin? angajatul având codul 114.
SELECT *
FROM employees
START WITH employee_id = 114
CONNECT BY PRIOR employee_id = manager_id;

--16. Scrieti o cerere ierarhica pentru a afisa codul salariatului, codul managerului si numele salariatului, pentru angajatii care sunt cu 2 niveluri sub De Haan.
SELECT employee_id, manager_id, salary
FROM employees
WHERE LEVEL = 2
START WITH manager_id = (SELECT employee_id
                         FROM employees
                         WHERE UPPER(last_name) = 'DE HAAN')
CONNECT BY PRIOR employee_id = manager_id;

--17. Pentru fiecare linie din tabelul EMPLOYEES, se va afisa o structura arborescenta in care va aparea angajatul, managerul sau, managerul managerului etc. 
-- Coloanele afisate vor fi: codul angajatului, codul managerului, nivelul în ierarhie si numele angajatului.
SELECT LEVEL, employee_id, first_name||' '||last_name, manager_id
FROM employees
CONNECT BY PRIOR manager_id = employee_id;

--18 Sa se afiseze ierarhia de sub angajatul având salariul maxim, retinând numai angajatii al carorsalariu este mai mare de 5000.
SELECT LEVEL, employee_id, first_name||' '||last_name full_name, salary, manager_id   
FROM employees
START WITH manager_id = (SELECT employee_id
                         FROM employees
                         WHERE salary = (SELECT MAX(salary) FROM employees))
CONNECT BY PRIOR employee_id = manager_id AND salary > 5000;

--19. Sa se scrie o cerere care afiseaza numele departamentelor si valoarea totala a salariilor din cadrul acestora. 
-- Se vor considera departamentele a caror valoare totala a salariilor este mai mare decat media valorilor totale ale salariilor tuturor angajatilor.
---Varianta 1
WITH
    costuri_dept AS (SELECT department_name, SUM(salary) dept_total
                     FROM employees e, departments d
                     WHERE e.department_id = d.department_id
                     GROUP BY department_name)
SELECT *
FROM costuri_dept
WHERE dept_total > (SELECT AVG(dept_total) FROM costuri_dept)
ORDER BY department_name;

---Varianta 2
WITH
    costuri_dept AS (SELECT department_name, SUM(salary) dept_total
                     FROM employees e, departments d
                     WHERE e.department_id = d.department_id
                     GROUP BY department_name),
    medie_costuri_dept AS (SELECT TRUNC(AVG(dept_total), 2) media
                           FROM costuri_dept)
SELECT *
FROM costuri_dept, medie_costuri_dept
WHERE dept_total > media;


--20. Sa se afiseze ierarhic codul, prenumele si numele, codul job-ului si data angajarii, pornind de la subordonatii directi ai lui Steven King 
-- care au cea mai mare vechime. Rezultatul nu va contine salariatii angajati in anul 1970.
WITH
    subordonati_directi AS (SELECT employee_id, hire_date
                            FROM employees 
                            WHERE manager_id = (SELECT employee_id
                                                FROM employees
                                                WHERE UPPER(first_name||' '||last_name) = 'STEVEN KING'))

SELECT LEVEL, employee_id, first_name||' '||last_name full_name, job_id, hire_date
FROM employees
WHERE TO_CHAR(hire_date, 'yyyy') <> 1970
START WITH employee_id IN (SELECT employee_id
                           FROM subordonati_directi
                           WHERE hire_date = (SELECT MIN(hire_date)
                                              FROM subordonati_directi))
CONNECT BY PRIOR employee_id = manager_id;
        
                    
--21. Sa se detemine primii 10 cei mai bine platiti angajati.
--Varianta 1
SELECT *
FROM (SELECT *
      FROM employees
      ORDER BY salary DESC)
WHERE ROWNUM < 11;

--Varianta 2
SELECT *
FROM employees e
WHERE 10 > (SELECT COUNT(*)
            FROM employees
            WHERE salary > e.salary)
ORDER BY salary DESC;


--22. Sa se determine cele mai prost platite 3 job-uri, din punct de vedere al mediei salariilor.
SELECT *
FROM (SELECT job_title "Job", TRUNC(AVG(salary), 2) "Media salariilor"
      FROM employees e
      JOIN jobs j ON e.job_id = j.job_id
      GROUP BY job_title
      ORDER BY 2)
WHERE ROWNUM <= 3;


--23
SELECT 'Departamentul ' || department_name || ' este condus de ' || 
    NVL(TO_CHAR(d.manager_id), 'nimeni') || ' si ' || 
    CASE COUNT(employee_id)
        WHEN 0 THEN 'nu are salariati'
        ELSE 'are numarul de salariati ' || COUNT(employee_id)
    END info
FROM employees e, departments d
WHERE d.department_id = e.department_id(+)
GROUP BY d.department_id, department_name, d.manager_id;


--24. Sa se afiseze numele, prenumele angajatilor si lungimea numelui pentru inregistrarile in care aceasta este diferita de lungimea prenumelui.
SELECT last_name, first_name, LENGTH(last_name)
FROM employees
WHERE NULLIF(LENGTH(last_name),LENGTH(first_name)) IS NOT NULL;


--25. Sa se afiseze numele, data angajarii, salariul si o coloana reprezentand salariul dupa ce se aplica o marire, astfel: 
-- pentru salariatii angajati in 1989 cresterea este de 20%, pentru cei angajati in 1990 cresterea este de 15%, iar salariul celor angajati in anul 1991 cre?te cu 10%.
-- Pentru salariatii angajati în alti ani valoarea nu se modifica.
--Varianta 1
SELECT first_name||' '||last_name full_name, hire_date, salary,
    CASE TO_CHAR(hire_date, 'yyyy')
        WHEN '1989' THEN salary + salary * 0.20
        WHEN '1990' THEN salary + salary * 0.15
        WHEN '1991' THEN salary + salary * 0.10
        ELSE salary
    END "Marire"
FROM employees;

--Varianta 2
SELECT first_name||' '||last_name full_name, hire_date, salary,
    DECODE(TO_CHAR(hire_date,'yyyy'), '1989', salary * 1.20, '1990', salary * 1.15, '1991', salary * 1.10, salary) "Marire"
FROM employees;


--26. Sa se afiseze:
--    - suma salariilor, pentru job-urile care incep cu litera S;
--    - media generala a salariilor, pentru job-ul avand salariul maxim;
--    - salariul minim, pentru fiecare din celelalte job-uri.
SELECT j.job_id, 
DECODE(INSTR(UPPER(job_title),'S'),  1, '1. ' || SUM(salary), 
    DECODE(MAX(salary), 
           (SELECT MAX(salary)
            FROM employees), '2. ' || AVG(salary), '3. ' || MIN(salary)))
FROM employees e, jobs j
WHERE j.job_id = e.job_id
GROUP BY j.job_id, job_title;


-- TOP 5 departamente din punct de vedere al numarului de angajati
SELECT *
FROM (SELECT d.department_name, COUNT(*) "Numar angajati"
      FROM employees e
      INNER JOIN departments d ON e.department_id = d.department_id
      GROUP BY department_name
      ORDER BY 2 DESC)
WHERE ROWNUM <= 5;