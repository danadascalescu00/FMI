--1. Scrieti o cerere pentru a se afisa numele, luna (in litere) si anul angajarii pentru toti salariatii din acelasi departament cu Gates, 
-- al caror nume contine litera “a”. Se va exclude Gates. Se vor da 2 solutii pentru determinarea apari?iei literei “A” în nume. De asemenea, 
-- pentru una din metode se va da ?i varianta join-ului conform standardului SQL99.
--Varianta 1
SELECT e1.first_name||' '||e1.last_name "Nume angajat", 
    TO_CHAR(e1.hire_date, 'MONTH') "Luna angajarii", 
    TO_CHAR(e1.hire_date, 'YYYY') "Anul angajarii"
FROM employees e1, employees e2 
WHERE e1.department_id = e2.department_id
    AND e1.employee_id <> e2.employee_id
    AND UPPER(e2.last_name) = 'GATES'
    AND LOWER(e1.last_name) LIKE '%a%';
    
--Varianta 2
SELECT e1.first_name||' '||e1.last_name nume_angajat, 
    TO_CHAR(e1.hire_date, 'MONTH-YYYY') luna_an_angajare
FROM employees e1 JOIN employees e2
    USING (department_id)
WHERE INITCAP(e2.last_name) = 'Gates'
    AND e1.employee_id <> e2.employee_id
    AND LOWER(e1.last_name) LIKE '%a%';
    
    
--2. Sa se afiseze codul si numele angajatilor care lucreaza in acelasi departament cu cel putin un angajat al carui nume contine litera “t”. 
-- Se vor afisa, de asemenea, codul si numele departamentului respectiv. Rezultatul va fi ordonat alfabetic dupa nume.
--Varianta 1
SELECT DISTINCT e1.employee_id, e1.first_name, e1.last_name, d.department_id, d.department_name
FROM employees e1, employees e2, departments d
WHERE e1.department_id = e2.department_id
    AND e1.employee_id <> e2.employee_id
    AND LOWER(e2.first_name||' '||e2.last_name) LIKE '%t%'
    AND e1.department_id = d.department_id;

--Varianta 2   
SELECT DISTINCT e1.employee_id, e1.last_name
FROM employees e1 JOIN employees e2
    ON (e1.department_id = e2.department_id
        AND e1.employee_id <> e2.employee_id)
WHERE UPPER(e2.last_name) LIKE '%T%'
ORDER BY last_name;


--3. Sa se afiseze numele, salariul, titlul job-ului, orasul si ?ara in care lucreaza angajatii condusi direct de King.
--Varianta 1
SELECT e.first_name, e.last_name, e.salary, j.job_title, l.city, c.country_name
FROM employees e JOIN employees m
    ON (e.manager_id = m.employee_id AND UPPER(m.last_name) = 'KING')
JOIN departments d ON e.department_id = d.department_id
JOIN jobs j ON e.job_id = j.job_id
JOIN locations l ON d.location_id = l.location_id
JOIN countries c ON l.country_id = c.country_id;

--Varianta 2
SELECT e.last_name, e.first_name, e.salary, j.job_title, l.city, c.country_name
FROM employees e, employees m, jobs j, departments d, locations l, countries c
WHERE e.job_id = j.job_id
    AND e.department_id = d.department_id
    AND d.location_id = l.location_id
    AND l.country_id = c.country_id
    AND e.manager_id = m.employee_id
    AND INITCAP(m.last_name) = 'King';
    
    
--4. Sa se afiseze codul departamentului, numele departamentului, numele si job-ul tuturor angajatilor din departamentele al caror nume contine sirul ‘ti’. 
-- De asemenea, se va lista salariul angajatilor, in formatul “$99,999.00”. Rezultatul se va ordona alfabetic dupa numele departamentului, 
-- si in cadrul acestuia, dupa numele angajatilor.

--Exemplu
SELECT TO_CHAR(10000, 'L99G999D99MI', ' NLS_NUMERIC_CHARACTERS = '',.'' NLS_CURRENCY = ''$'' ') "Amount"
FROM dual;

SELECT d.department_id, d.department_name, e.first_name||' '||e.last_name NAME, e.job_id,
    TO_CHAR(salary, 'L99G999D99MI', ' NLS_NUMERIC_CHARACTERS = '',.'' NLS_CURRENCY = ''$'' ') SALARY
FROM departments d, employees e
WHERE e.department_id = d.department_id
    AND LOWER(d.department_name) LIKE '%ti%'
ORDER BY 2, 3;


--5.
SELECT e.first_name||' '||e.last_name AS "Name", e.employee_id AS "Employee Id", j.job_title AS "Job title", 
    d.department_id AS "Department id", d.department_name AS "Department name"
FROM employees e
INNER JOIN jobs j ON e.job_id = j.job_id
INNER JOIN departments d ON e.department_id = d.department_id
INNER JOIN locations a ON d.location_id = a.location_id
INNER JOIN countries c ON a.country_id = c.country_id
WHERE UPPER(a.city) LIKE '%OXFORD%';

--6. Afisati codul, numele si salariul tuturor angajatilor care castiga mai mult decat salariul
-- mediu pentru job-ul corespunzator si lucreaza intr-un departament cu cel putin unul din
-- angajatii al caror nume contine litera “t”.
--Varianta 1
SELECT DISTINCT e1.employee_id, e1.first_name, e1.last_name, e1.salary
FROM employees e1, jobs j, employees e2
WHERE e1.job_id = j.job_id
    AND e1.salary > (j.min_salary + j.max_salary) / 2
    AND e1.department_id = e2.department_id 
    AND e1.employee_id <> e2.employee_id 
    AND LOWER(e2.last_name) LIKE '%t%';
    
--Varianta 2
SELECT DISTINCT e.employee_id, e.first_name, e.last_name, e.salary
FROM employees e
WHERE e.department_id IN ( SELECT department_id
                           FROM employees
                           WHERE TRIM(BOTH ' ' FROM UPPER(last_name)) LIKE '%T%'
                            AND employee_id <> e.employee_id)
    AND e.salary > ( SELECT (j.min_salary + j.max_salary) / 2
                     FROM jobs j
                     WHERE j.job_id = e.job_id )
ORDER BY 1;

--7.
SELECT first_name, last_name, department_name
FROM departments d RIGHT OUTER JOIN employees e
    ON (d.department_id = e.department_id);
    
SELECT first_name, last_name, department_name
FROM employees e, departments d
WHERE d.department_id (+) = e.department_id;


--8. Sa se afiseze numele departamentelor si numele salariatilor care lucreaza in ele. Se vor afisa si departamentele care nu au salariati.
--Varianta 1
SELECT d.department_name, e.first_name||' '||e.last_name empName
FROM departments d, employees e
WHERE d.department_id = e.department_id(+);

--Varianta 2
SELECT d.department_name, e.first_name||' '||e.last_name empName
FROM departments d LEFT OUTER JOIN employees e
    ON d.department_id = e.department_id;
    

--9. Cum se poate implementa full outer join?
-- Full outer join se poate realiza fie prin reuniunea rezultatelor lui right outer join ?i left outer join, fie utilizând sintaxa introdus? de standardul SQL99.

--Varianta 1
SELECT first_name, last_name, department_name
FROM employees e, departments d
WHERE d.department_id (+) = e.department_id
UNION
SELECT d.department_name, e.first_name, e.last_name 
FROM departments d, employees e
WHERE d.department_id = e.department_id(+);


--Varianta 2
SELECT d.department_name, e.first_name||' '||e.last_name empName
FROM departments d FULL OUTER JOIN employees e
    ON d.department_id = e.department_id;
    
    
--10. Se cer codurile departamentelor al caror nume contine sirul “re” sau in care lucreaza angajati avand codul job-ului “SA_REP”. Cum este ordonat rezultatul?
-- R: Rezultatul este ordonat crescator dupa rezultatul primei coloane din clauza SELECT(in cazul nostru dupa department_id)
SELECT department_id
FROM departments
WHERE LOWER(department_name) LIKE '%re%'
UNION 
SELECT department_id
FROM employees
WHERE TRIM(BOTH ' ' FROM UPPER(job_id)) = 'SA_REP';

--11. Ce se întâmpl? dac? înlocuim UNION cu UNION ALL în comanda precedent?? R: Vom obtine un rezultat ce contine duplicate

--12. Sa se obtina codurile departamentelor in care nu lucreaza nimeni (nu este introdus niciun salariat in tabelul employees).
--Varianta 1
SELECT department_id
FROM departments
MINUS 
SELECT department_id
FROM employees;

--Varianta 2.
SELECT d.department_id
FROM departments d
WHERE ( SELECT COUNT(employee_id)
        FROM employees 
        WHERE department_id = d.department_id ) = 0;
        
--Varianta 3
SELECT d.department_id
FROM departments d
WHERE NOT EXISTS ( SELECT 1
                   FROM employees
                   WHERE department_id = d.department_id )
ORDER BY 1;

--Varianta 4
SELECT d.department_id
FROM departments d
WHERE d.department_id NOT IN ( SELECT department_id
                               FROM employees
                               WHERE department_id = d.department_id )
ORDER BY 1;

--Varianta 5
SELECT d.department_id 
FROM departments d
LEFT JOIN employees e ON d.department_id = e.department_id
WHERE e.department_id is NULL
ORDER BY d.department_id;

--Varianta 6
SELECT d.department_id
FROM departments d, employees e 
WHERE d.department_id = e.department_id(+) 
    AND e.department_id is NULL
ORDER BY d.department_id;


--13. Se cer codurile departamentelor al caror nume contine sirul “re” si in care lucreaza angajati avand codul job-ului “HR_REP”.
SELECT department_id
FROM departments
WHERE LOWER(department_name) LIKE '%re%'
INTERSECT
SELECT department_id
FROM employees
WHERE TRIM(BOTH ' ' FROM UPPER(job_id)) = 'HR_REP';


--14. Sa se determine codul angajatilor, codul job-urilor si numele celor al caror salariu este mai mare decat 3000 sau 
-- este egal cu media dintre salariul minim si cel maxim pentru job-ul respectiv.
--Varianta 1
SELECT employee_id, job_id, first_name||' '||last_name AS name
FROM employees 
WHERE salary > 3000
UNION
SELECT e.employee_id, j.job_id, last_name
FROM employees e, jobs j
WHERE e.job_id = j.job_id
AND salary = (min_salary + max_salary) / 2;

--Varianta 2
SELECT e.employee_id, e.job_id, e.first_name||' '||e.last_name AS name
FROM employees e
JOIN jobs j ON e.job_id = j.job_id
WHERE e.salary > 3000 OR e.salary = (j.max_salary - j.min_salary) / 2;


--15. Folosind subcereri, sa se afiseze numele si data angajarii pentru salariatii care au fost angajati dupa Gates.
SELECT first_name, last_name, hire_date
FROM employees
WHERE hire_date > ( SELECT hire_date
                    FROM employees
                    WHERE TRIM(BOTH ' ' FROM UPPER(last_name)) = 'GATES' ) --Subcerere nesincronizata
ORDER BY hire_date;


--16. Folosind subcereri, scrie?i o cerere pentru a afi?a numele ?i salariul pentru to?i colegii de departament a lui Gates.
SELECT e.first_name||' '||e.last_name name, e.salary
FROM employees e
WHERE e.department_id = ( SELECT department_id
                          FROM employees
                          WHERE TRIM(BOTH ' ' FROM INITCAP(last_name)) = 'Gates')
    AND TRIM(BOTH ' ' FROM INITCAP(e.last_name)) <> 'Gates';
                            
                            
--17. Folosind subcereri, sa se afiseze numele si salariul angajatilor condusi direct de presedintele companiei.
SELECT first_name||' '||last_name AS name, salary
FROM employees
WHERE manager_id = ( SELECT employee_id
                     FROM employees
                     WHERE manager_id IS null);
                     

--18. Scrieti o cerere pentru a afisa numele, codul departamentului si salariul angajatilor al caror numar de departament si salariu 
-- coincid cu numarul departamentului si salariul unui angajat care castiga comision.
SELECT first_name, last_name, department_id, salary
FROM employees
WHERE (department_id, salary) IN ( SELECT department_id, salary
                                   FROM employees
                                   WHERE commission_pct IS NOT null );
                                   
--19. Scrieti o cerere pentru a afisa angajatii care castiga mai mult decat oricare functionar (job-ul con?ine sirul “CLERK”). 
-- Sortati rezultatele dupa salariu, in ordine descrescatoare. Ce rezultat este returnat daca se inlocuieste “ALL” cu “ANY”?

-- Daca subcererea este precedata de catre cuvântul cheie ALL, atunci conditia va fi adevarata numai daca este satisfacuta de catre toate valorile produse de subcerere. 
-- Daca subcerea este precedata de catre cuvantul cheie ANY, atunci conditia va fi adevarata daca va fi satisfacuta de cel putin una dintre valorile produse de subcerere.
SELECT employee_id, first_name||' '||last_name "Name", department_id, salary
FROM employees
WHERE salary > ALL (SELECT salary
                    FROM employees
                    WHERE UPPER(job_id) LIKE '%CLERK%')
ORDER BY salary DESC;

-- Daca inlocuim ALL cu ANY returnate toate cererile in care salariatii au salariul mai mare decat cel mai mic salariu al unui functionar din tabela employees, 
-- adica angajatii care au salariul mai mare decat 2100

SELECT employee_id, first_name||' '||last_name "Name", department_id, salary
FROM employees
WHERE salary > ANY (SELECT salary
                    FROM employees
                    WHERE UPPER(job_id) LIKE '%CLERK%')
ORDER BY salary;


--20. Scrieti o cerere pentru a afisa numele, numele departamentului si salariul angajatilor care nu castiga comision, 
-- dar al caror sef direct coincide cu seful unui angajat care castiga comision.
SELECT e.last_name||' '||e.first_name NAME, d.department_name, e.salary
FROM employees e
JOIN departments d USING(department_id)
WHERE e.commission_pct IS NULL 
    AND e.manager_id IN ( SELECT manager_id
                          FROM employees
                          WHERE commission_pct IS NOT NULL );
                          
--21. Sa se afiseze numele, departamentul, salariul si job-ul tuturor angajatilor al caror salariu si comision coincid cu salariul si comisionul unui angajat din Oxford.
SELECT e.first_name||' '||e.last_name "Nume", d.department_name "Departament", e.salary "Salariu", j.job_title
FROM employees e, departments d, jobs j
WHERE e.department_id = d.department_id 
    AND e.job_id = j.job_id
    AND (e.salary, NVL(e.commission_pct,0)) IN ( SELECT salary, NVL(commission_pct,0)
                                                 FROM employees, departments, locations
                                                 WHERE employees.department_id = departments.department_id
                                                    AND departments.location_id = locations.location_id
                                                    AND INITCAP(city) LIKE 'Oxford');
                                                    
--22. Sa se afiseze numele angajatilor, codul departamentului si codul job-ului salariatilor al caror departament se afla în Toronto.
-- Varianta 1
SELECT e.last_name||' '||e.first_name AS "Nume", e.department_id AS "Cod departament", e.job_id AS "Cod job"
FROM employees e
JOIN departments d ON e.department_id = d.department_id
JOIN locations l ON d.location_id = l.location_id
WHERE INITCAP(city) LIKE 'Toronto';

-- Varianta 2
SELECT e.last_name||' '||e.first_name AS "Nume", e.department_id AS "Cod departament", e.job_id AS "Cod job"
FROM employees e
WHERE e.department_id IN (  SELECT department_id
                            FROM departments
                            WHERE location_id IN ( SELECT location_id
                                                   FROM locations
                                                   WHERE INITCAP(city) LIKE 'Toronto'));