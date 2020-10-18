--1. Sa se listeze informatii despre angajatii care au lucrat in toate proiectele demarate in primele 6 luni ale anului 2006.
--Varianta 1 - Simularea diviziunii cu ajutorul functiei COUNT
SELECT e.employee_id EMP#, e.first_name||' '||e.last_name EMP, MAX(e.department_id) DEP#
FROM employees e JOIN works_on w
    ON e.employee_id = w.employee_id
WHERE project_id IN (SELECT project_id
                     FROM projects
                     WHERE EXTRACT(YEAR FROM start_date) = 2006
                        AND TO_CHAR(start_date, 'MM') < '07')
GROUP BY e.employee_id, e.first_name||' '||e.last_name
HAVING COUNT(w.project_id) = ( SELECT COUNT(*)
                               FROM projects
                               WHERE EXTRACT(YEAR FROM start_date) = 2006
                                   AND TO_CHAR(start_date, 'MM') < '07');


--Varianta 2 - A include B => B\A = empty_set
SELECT DISTINCT e.employee_id EMP#, e.first_name||' '||e.last_name EMP, 
    e.department_id DEP#, e.manager_id, e.job_id, e.email, e.phone_number
FROM employees e JOIN works_on w
    ON e.employee_id = w.employee_id
WHERE NOT EXISTS ( SELECT project_id
                   FROM projects
                   WHERE EXTRACT(YEAR FROM start_date) = 2006
                       AND TO_CHAR(start_date, 'MM') < '07'
                   MINUS
                   SELECT project_id
                   FROM works_on w2
                   WHERE w2.employee_id = e.employee_id);


--Varianta 3 - Simularea diviziunii utilizand dde doua ori NOT EXISTS
SELECT DISTINCT e.employee_id EMP#, e.first_name||' '||e.last_name EMP, 
    e.department_id DEP#, e.manager_id, e.job_id, e.email, e.phone_number
FROM employees e
WHERE NOT EXISTS( SELECT 1
                  FROM projects p
                  WHERE EXTRACT(YEAR FROM start_date) = 2006
                      AND TO_CHAR(start_date, 'MM') < '07'
                      AND NOT EXISTS( SELECT 'x'
                                      FROM works_on w2
                                      WHERE w2.project_id = p.project_id
                                        AND w2.employee_id = e.employee_id));


--2. Sa se listeze informatii despre proiectele la care au participat toti angajatii care au detinut alte 2 posturi in firma.
SELECT *
FROM projects p
WHERE NOT EXISTS ( SELECT employee_id
                   FROM job_history j
                   GROUP BY employee_id
                   HAVING COUNT(DISTINCT job_id) = 2
                    AND NOT EXISTS ( SELECT '1'
                                     FROM works_on w1
                                     WHERE w1.project_id = p.project_id
                                        AND w1.employee_id = j.employee_id));


--3. Sa se obtina numarul de angajati care au avut cel putin trei job-uri, luandu-se in considerare si job-ul curent.
SELECT SUM(CASE WHEN number_distinct_jobs >=3 THEN 1 ELSE 0 END) 
FROM( SELECT COUNT(*) AS number_distinct_jobs
      FROM(
        SELECT employee_id, job_id
        FROM employees
        UNION                       
        SELECT employee_id, job_id
        FROM job_history)
      GROUP BY employee_id
    );


--4. Pentru fiecare tara, sa se afiseze numarul de angajati din cadrul acesteia.
SELECT l.country_id, COUNT(e.employee_id) no_emp
FROM locations l, departments d, employees e
WHERE l.location_id = d.location_id
    AND d.department_id = e.department_id
GROUP BY l.country_id;


--5. Sa se listeze angajatii(codul si numele acestora) care au lucrat pe cel putin doua proiecte nelivrate la termen.
DESC works_on;
DESC projects;

SELECT e.employee_id, e.first_name||' '||e.last_name EMPLOYEE
FROM employees e
WHERE e.employee_id IN ( SELECT w.employee_id
                         FROM works_on w, projects p
                         WHERE w.project_id = p.project_id
                            AND p.deadline < p.delivery_date
                         GROUP BY w.employee_id
                         HAVING COUNT(p.project_id) >= 2);
                         
                         
--6. Sa se listeze codurile angajatilor si codurile proiectelor pe care au lucrat. Listarea va cuprinde si angajatii care nu au lucrat pe nici un proiect.
SELECT e.employee_id, w.project_id
FROM employees e, works_on w
WHERE e.employee_id = w.employee_id(+);


--7. Sa se afiseze angajatii care lucreaza in acelasi departament cu cel putin un manager de proiect.
SElECT *
FROM employees e
WHERE EXISTS ( SELECT 'x'
               FROM employees e2, projects p
               WHERE e2.department_id = e.department_id
                AND e2.employee_id = p.project_manager
                AND e2.employee_id <> e.employee_id);
                

--8. Sa se afiseze angajatii care nu lucreaza in acelasi departament cu nici un manager de proiect.
WITH 
    manager AS (SELECT project_manager employee_id
                FROM projects)

SELECT DISTINCT *
FROM employees 
WHERE department_id NOT IN (SELECT DISTINCT e.department_id
                            FROM employees e
                            INNER JOIN manager m
                                USING(employee_id));
                                
                                
--9. Sa se determine departamentele avand media salariilor mai mare decat un numar dat.
ACCEPT val PROMPT "Introduceti valoarea:";
PRINT &val;

SELECT d.department_id, MIN(d.department_name) DEPARTMENT
FROM departments d
JOIN employees e ON d.department_id = e.department_id
GROUP BY d.department_id
HAVING AVG(e.salary) > &val;

UNDEFINE val;


--10. Se cer informaii(nume, prenume, salariu, numar proiecte) despre managerii de proiect care au condus mai mult de 2 proiecte.
WITH 
    manager AS (SELECT project_manager employee_id, COUNT(project_id) no_projects
                FROM projects
                GROUP BY project_manager
                HAVING COUNT(project_id) >= 2)
            
SELECT e.employee_id, e.last_name, e.first_name, e.salary, m.no_projects
FROM employees e
INNER JOIN manager m ON e.employee_id = m.employee_id;


--11. Sa se afiseze lista angajatilor care au lucrat numai pe proiecte conduse de managerul de proiect având codul 102.
SELECT *
FROM employees
INNER JOIN works_on USING (employee_id)
INNER JOIN projects p USING (project_id)
WHERE p.project_manager = 102;


--12. a) Sa se obtin? numele angajatilor care au lucrat cel putin pe aceleasi proiecte ca si angajatul avand codul 200.
SELECT e.last_name||' '||e.first_name name
FROM employees e
WHERE NOT EXISTS ( SELECT project_id
                   FROM works_on
                   WHERE employee_id = 200
                   MINUS
                   SELECT project_id
                   FROM works_on
                   WHERE e.employee_id = employee_id);
                
-- b) Sa se obtina numele angajatilor care au lucrat cel mult pe aceleasi proiecte ca si angajatul avand codul 200.
SELECT e.last_name||' '||e.first_name name
FROM employees e
WHERE NOT EXISTS ( SELECT project_id
                   FROM works_on
                   WHERE employee_id = e.employee_id
                   MINUS
                   SELECT project_id
                   FROM works_on
                   WHERE employee_id = 200);
                
                
--13. Sa se obtina angajatii care au lucrat pe aceleaai proiecte ca si angajatul avand codul 200.
SELECT *
FROM employees e
WHERE NOT EXISTS ( SELECT w.project_id
                   FROM works_on w
                   WHERE w.employee_id = e.employee_id
                   MINUS
                   SELECT project_id
                   FROM works_on 
                   WHERE employee_id = 200)
AND NOT EXISTS ( SELECT project_id
                 FROM works_on
                 WHERE employee_id = 200
                 MINUS
                 SELECT project_id
                 FROM works_on
                 WHERE employee_id = e.employee_id)
AND employee_id <> 200;


--14. Modelul HR contine un tabel numit JOB_GRADES, care contine grilele de salarizare ale companiei.
--a) Afisati structura si continutul acestui tabel.
DESC job_grades;

SELECT *
FROM job_grades;

--b) Pentru fiecare angajat, afisati numele, prenumele, salariul si grila de salarizare corespunzatoare.
SELECT DISTINCT last_name, first_name, grade_level
FROM employees e, job_grades j
WHERE e.salary BETWEEN j.lowest_sal AND j.highest_sal
ORDER BY 1;


PAUSE 'Exercitii SQL *PLUS';
--15. Sa se afiseze codul, numele, salariul si codul departamentului din care face parte pentru un angajat al carui cod este introdus de utilizator de la tastatura.
ACCEPT p_cod PROMPT "cod= ";
SELECT employee_id, last_name, salary, department_id
FROM employees 
WHERE employee_id = &p_cod;


--16. Sa se afiseze numele, codul departamentului si salariul anual pentru toti angajatii care au un anumit job.
ACCEPT j_cod PROMPT "Enter a job_cod:";
PRINT &&j_cod;

SELECT first_name, last_name, department_id, salary * 12
FROM employees
WHERE job_id = '&&j_cod';


--17. Sa se afiseze numele, codul departamentului si salariul anual pentru toti angajatii care au fost angajati dupa o anumita data calendaristica.
SELECT hire_date
FROM employees;

ACCEPT data_calendaristica PROMPT "Introduceti o data calendaristica in formatul DD-MON-YY:";

SELECT first_name, last_name, department_id, salary * 12
FROM employees
WHERE hire_date >= TO_DATE('&data_calendaristica', 'DD-MON-YY');


--18. Sa se afiseze o coloana aleasa de utilizator, dintr-un tabel ales de utilizator, ordonand dupa aceeasi
--coloana care se afiseaza. De asemenea, este obligatorie precizarea unei conditii WHERE.
ACCEPT tabel PROMPT "Alege tabel:";
ACCEPT coloana PROMPT "Alege coloana:";
ACCEPT conditie PROMPT "Conditie:";
ACCEPT operator PROMPT "Operator conditie:";

SELECT &&coloana
FROM &&tabel
WHERE &&coloana &&operator &&conditie
ORDER BY &&coloana;


--19. Sa se realizeze un script prin care sa se afiseze numele, job-ul si data angajarii salariatilor care
-- au inceput lucrul intre 2 date calendaristice introduse de utilizator. Sa se concateneze numele si job-ul, 
-- separate prin spatiu si virgula, si sa se eticheteze coloana "Angajati".
-- Se vor folosi comanda ACCEPT si formatul pentru data calendaristica MM/DD/YY.
ACCEPT start_date PROMPT "start_date= ";
ACCEPT end_date PROMPT "end_date= ";
SELECT last_name, job_id, hire_date
FROM employees
WHERE hire_date BETWEEN TO_DATE('&start_date', 'MM/DD/YY') 
    AND TO_DATE('&end_date', 'MM/DD/YY');
SELECT hire_date
FROM employees;


--20. a)Sa se citeasca doua date calendaristice de la tastatura si sa se afiseze zilele dintre aceste dou? date.ACCEPT start_date PROMPT "start_date= ";
ACCEPT end_date PROMPT "end_date= ";
SELECT TO_DATE('&end_date', 'MM/DD/YY') - TO_DATE('&start_date', 'MM/DD/YY')
FROM DUAL;

--b
SELECT SELECT TO_DATE('&end_date', 'MM/DD/YY') - TO_DATE('&start_date', 'MM/DD/YY') - DATEDIFF(week, TO_DATE('&end_date', 'MM/DD/YY'), TO_DATE('&start_date', 'MM/DD/YY'))
FROM DUAL;


DEFINE val; -- Afiseaza variabila, valoarea ei si tipul de data al acesteia.
DEFINE; -- Afiseaza toate variabilele existente in sesiunea curenta, impreuna cu valorile si tipurile lor de date.