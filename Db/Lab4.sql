
--Exemplu operator ROLLUP
--Pentru departamentele avand codul mai mic decat 50:
-- - pentru fiecare departament si pentru fiecare an al angajarii(corespunzator departamentului respectiv), valoarea totala a salariilor angajatiilor in acel an;
-- - valoarea totala a salariilor pe departamente (indiferent de anul angajarii)
-- - valoarea totala a salariilor(indiferent de anul angajarii si de departament)
SELECT department_id, TO_CHAR(hire_date, 'yyyy'), SUM(salary)
FROM employees
WHERE department_id < 50
GROUP BY ROLLUP (department_id,TO_CHAR(hire_date, 'yyyy'));

--Exemplu operator CUBE
--Pentru departamentele avand codul mai mic decat 50:
-- - pentru fiecare departament si pentru fiecare an al angajarii(corespunzator departamentului respectiv), valoarea totala a salariilor angajatiilor in acel an;
-- - valoarea totala a salariilor pe departamente (indiferent de anul angajarii)
-- - valoarea totala a salariilor corespunzatoare fiecarui an(indiferent de departament)
-- - valoarea totala a salariilor(indiferent de anul angajarii si de departament)
SELECT department_id, TO_CHAR(hire_date, 'yyyy'), SUM(salary)
FROM employees
WHERE department_id < 50
GROUP BY CUBE(department_id, TO_CHAR(hire_date, 'yyyy'));


--1
-- a) Inafara de functia COUNT, functiile grup includ valorile NULL in calcule
-- b) In HAVING putem avea comparari cu functii grup, iar in WHERE nu putem

--2
SELECT MAX(salary) "Maxim" ,MIN(salary) "Minim", SUM(salary) "Suma", ROUND(AVG(salary),2) "Media"
FROM employees;

--3.
SELECT j.job_title, MIN(e.salary) AS "Minim", 
    MAX(e.salary) AS "Maxim", 
    ROUND(AVG(salary),2) AS "Media", 
    SUM(salary) AS "Total"
FROM employees e, jobs j
WHERE e.job_id = j.job_id
GROUP BY j.job_title
ORDER BY j.job_title;


--4. Sa se afiseze numarul de angajati pentru fiecare job.
SELECT job_id, COUNT(employee_id)
FROM employees
GROUP BY job_id;


--5. Sa se determine numarul de angajati care sunt sefi.
SELECT COUNT(DISTINCT manager_id) "Nr. manageri"
FROM employees;


--6. Sa se afiseze diferenta dintre cel mai mare si cel mai mic salariu.
SELECT MAX(salary) - MIN(salary)
FROM employees;


--7. Scrieti o cerere pentru a se afisa numele departamentului, locatia, numarul de angajati si salariul mediu pentru angajatii din acel departament. 
SELECT d.department_name, d.location_id, 
    COUNT(e.employee_id) "Numarul de angajati", 
    ROUND(AVG(e.salary), 2) "Media"
FROM departments d, employees e
WHERE d.department_id = e.department_id
GROUP BY d.department_name, d.location_id;


--8. Sa se afiseze codul si numele angajatilor care castiga mai mult decat salariul mediu din firma. Se va sorta rezultatul in ordine descrescatoare a salariilor.
SELECT employee_id, first_name, last_name
FROM employees
WHERE salary > (SELECT AVG(salary)
                FROM employees)
ORDER BY salary DESC;


--9. Pentru fiecare sef, sa se afiseze codul sau si salariul celui mai prost platit subordonat. Se vor exclude cei pentru care codul managerului nu este cunoscut. 
-- De asemenea, se vor exclude grupurile in care salariul minim este mai mic de 1000$. Sortati rezultatul in ordine descrescatoare a salariilor.
SELECT manager_id, MIN(salary)
FROM employees
WHERE manager_id IS NOT NULL
GROUP BY manager_id
HAVING MIN(salary) > 1000
ORDER BY 2 DESC;
    

--10. Pentru departamentele in care salariul maxim depaseste 3000$, sa se obtina codul, numele acestor departamente si salariul maxim pe departament.
SELECT d.department_id, d.department_name, MAX(e.salary)
FROM departments d, employees e
WHERE d.department_id = e.department_id
GROUP BY d.department_id, d.department_name
HAVING MAX(e.salary) > 3000;

--11. Care este salariul mediu minim al job-urilor existente?
SELECT MIN(AVG(salary))
FROM employees
GROUP BY job_id;


--12. Sa se afiseze codul, numele departamentului si suma salariilor pe departamente.
SELECT d.department_id, d.department_name, SUM(e.salary)
FROM departments d JOIN employees e
    ON d.department_id = e.department_id
GROUP BY d.department_id, d.department_name;


--13. Sa se afi?eze maximul salariilor medii pe departamente.
SELECT TRUNC(MAX(AVG(salary)), 5)
FROM employees
GROUP BY department_id;


--14. Sa se obtina codul, titlul si salariul mediu al job-ului pentru care salariul mediu este minim.
SELECT job_id, job_title, AVG(salary)
FROM employees 
JOIN jobs USING(job_id)
GROUP BY job_id, job_title
HAVING AVG(employees.salary) = (SELECT MIN(AVG(salary))
                                FROM employees
                                GROUP BY job_id);
                                
--15. Sa se afiseze salariul mediu din firma doar daca acesta este mai mare decat 2500.
SELECT ROUND(AVG(salary),3)
FROM employees
HAVING AVG(salary) > 2500;


--16. Sa se afiseze suma salariilor pe departamente si, in cadrul acestora, pe job-uri
SELECT department_id, job_id, SUM(salary)
FROM employees
GROUP BY GROUPING SETS(department_id, (department_id, job_id))
ORDER BY 1;

--17. Sa se afiseze numele departamentului si cel mai mic salariu din departamentul avand cel mai mare salariu mediu.
SELECT d.department_name, MIN(e.salary) MIN_SALARY
FROM employees e JOIN departments d
    ON e.department_id = d.department_id
GROUP BY d.department_name
HAVING AVG(salary) = ( SELECT MAX(AVG(salary))
                       FROM employees
                       GROUP BY department_id );
                       
--18. Sa se afiseze codul, numele departamentului si numarul de angajati care lucreaza in acel departament pentru:
--a)departamentele in care lucreaza mai putin de 4 angajati;
--Varianta 1 - Se vor afisa si departamentele care nu au niciun angajat
SELECT d.department_id, d.department_name, COUNT(e.employee_id) NUMBER_EMPLOYEES
FROM departments d, employees e
WHERE d.department_id = e.department_id(+)
GROUP BY d.department_id, d.department_name
HAVING COUNT(*) < 4
ORDER BY 3;

--Varianta 2. In acest caz nu for fi luate in considerare departamentele care nu au niciun angajat
SELECT d.department_id, d.department_name, COUNT(*) NUMBER_EMPLOYEES
FROM departments d, employees e
WHERE d.department_id = e.department_id
    AND d.department_id IN (SELECT department_id
                            FROM employees
                            GROUP BY department_id
                            HAVING COUNT(*) < 4)
GROUP BY d.department_id, d.department_name
ORDER BY 3;


--b)departamentul care are numarul maxim de angajati.
SELECT d.department_id, d.department_name, COUNT(*) NUMBER_EMPLOYEES
FROM employees e JOIN departments d
    ON e.department_id = d.department_id
GROUP BY d.department_id, d.department_name
HAVING COUNT(*) = ( SELECT MAX(COUNT(*))
                    FROM employees
                    GROUP BY department_id);


--19. Sa se afiseze salariatii care au fost angajati în aceea?i zi a lunii în care cei mai multi dintre salariati au fost angajati.
SELECT employee_id, first_name, last_name, hire_date, department_id
FROM employees
WHERE TO_CHAR(hire_date, 'DD') = ( SELECT TO_CHAR(hire_date, 'DD')
                                    FROM employees
                                    GROUP BY TO_CHAR(hire_date, 'DD')
                                    HAVING COUNT(employee_id) = (   SELECT MAX(COUNT(employee_id))
                                                                    FROM employees
                                                                    GROUP BY TO_CHAR(hire_date, 'DD') ) );
                                                                
--20. Sa se obtina numarul departamentelor care au cel putin 15 angajati.
SELECT COUNT(COUNT(department_id))
FROM employees 
GROUP BY department_id
HAVING COUNT(*) >= 15;


--21. Sa se obtina codul departamentelor si suma salariilor angajatilor care lucreaza in acestea, in ordine crescatoare. 
-- Se considera departamentele care au mai mult de 10 angajati si al caror cod este diferit de 30.
SELECT department_id, SUM(salary)
FROM employees
GROUP BY department_id
HAVING department_id <> 30
    AND COUNT(DISTINCT employee_id)  > 10;
    
    
--22. Sa se afiseze codul, numele departamentului, numarul de angajati si salariul mediu din departamentul respectiv, 
-- impreuna cu numele, salariul si jobul angajatilor din acel departament. Se vor afisa si departamentele fara angajati
SELECT d.department_id, d.department_name, 
    e.first_name||' '||e.last_name name, e.salary, e.job_id,
    (SELECT COUNT(*) FROM employees WHERE department_id = d.department_id) num_emp,
    NVL(ROUND((SELECT AVG(salary) FROM employees WHERE department_id = d.department_id), 2), 0) avg_salary
FROM departments d LEFT OUTER JOIN employees e
   ON d.department_id = e.department_id
GROUP BY d.department_id, d.department_name, e.first_name||' '||e.last_name, e.salary, e.job_id;


--23.
SELECT d.department_name, l.city, e.job_id, SUM(salary)
FROM employees e, departments d, locations l
WHERE e.department_id = d.department_id
    AND d.location_id = l.location_id
    AND d.department_id > 80
GROUP BY GROUPING SETS ((d.department_name, e.job_id), l.city, ());


--24. Care sunt angajatii care au mai avut cel putin doua joburi?
SELECT j.employee_id "Cod angajat", e.last_name||' '||e.first_name "Nume angajat"
FROM job_history j
JOIN employees e ON j.employee_id = e.employee_id
GROUP BY j.employee_id, e.last_name||' '||e.first_name
HAVING COUNT(j.employee_id) >= 2;


--25. S? se calculeze comisionul mediu din firm?, luând în considerare toate liniile din tabel.
--Varianta 1
SELECT TRUNC(AVG(NVL(commission_pct, 0)), 3)
FROM employees;

--Varianta 2
SELECT SUM(commission_pct) / COUNT(*)
FROM employees;

--26. In cazul operatorului ROLLUP conteaza ordinea parametriilor, in schimb la operatorul CUBE NU conteaza

--27. Scrieti o cerere pentru a afisa job-ul, salariul total pentru job-ul respectiv pe departamente si salariul total pentru job-ul respectiv pe departamentele 30, 50, 80.
-- Varianta 1
SELECT j.job_id job, (SELECT DECODE(d.department_id, 30, SUM(salary))
                      FROM employees
                      WHERE j.job_id = job_id) dep30,
                    (SELECT DECODE(d.department_id, 50, SUM(salary))
                    FROM employees
                    WHERE j.job_id = job_id) dep50,
                    (SELECT DECODE(d.department_id, 80, SUM(salary))
                    FROM employees
                    WHERE j.job_id = job_id) dep80,
    SUM(salary) total
FROM jobs j, departments d, employees e
WHERE j.job_id = e.job_id
AND d.department_id = e.department_id
GROUP BY j.job_id, d.department_id;


--28. Sa se creeze o cerere prin care sa se afiseze numarul total de angajati ?i, din acest total, numarul celor care au fost angajati in 1997, 1998, 1999 si 2000. 
SELECT COUNT(DISTINCT employee_id) "Numar total de angajati", SUM(DECODE(TO_CHAR(hire_date, 'yyyy'), 1997, 1)) "1997",
                                                              SUM(DECODE(TO_CHAR(hire_date, 'yyyy'), 1998, 1)) "1998",
                                                              SUM(DECODE(TO_CHAR(hire_date, 'yyyy'), 1999, 1))  "1999",
                                                              SUM(DECODE(TO_CHAR(hire_date, 'yyyy'), 2000, 1))  "2000"                                                           
FROM employees e;


--29. Varrianta alternativa pentru pb.22
SELECT d.department_id, d.department_name, (SELECT COUNT(employee_id)
                                            FROM employees
                                            WHERE department_id(+) = d.department_id) "Numar angajati",
                                            ROUND((SELECT AVG(salary)
                                            FROM employees
                                            WHERE department_id(+) = d.department_id), 2) "Salariu mediu",
    e.last_name||' '||e.first_name "Nume angajat", e.salary "Salariu", j.job_title "Job"
FROM departments d, employees e, jobs j
WHERE e.department_id(+) = d.department_id AND e.job_id = j.job_id;


--30. Sa se afiseze codul, numele departamentului si suma salariilor pe departamente.
SELECT d.department_id, d.department_name, s.total_dep
FROM departments d, (SELECT department_id, SUM(salary) total_dep
                     FROM employees
                     GROUP BY department_id) s
WHERE d.department_id = s.department_id
ORDER BY 3;


--31. Sa se afiseze numele si salariul fiecarui salariat, precum si codul departamentului si salariul mediu din departamentul respectiv.
SELECT e.first_name||' '||e.last_name name, e.salary, e.department_id, a.avg_salary
FROM employees e, (SELECT department_id, ROUND(AVG(salary), 2) avg_salary
                   FROM employees
                   GROUP BY department_id) a
WHERE e.department_id = a.department_id;

--32. Modificati cererea anterioara, pentru a determina si listarea numarului de angajati din departamente.
SELECT e.first_name||' '||e.last_name name, e.salary, e.department_id, 
    a.avg_salary, a.count_employees
FROM employees e, (SELECT department_id, 
                      ROUND(AVG(salary), 2) avg_salary,
                      COUNT(*) count_employees
                   FROM employees
                   GROUP BY department_id) a
WHERE e.department_id = a.department_id
ORDER BY 3;

--33. Pentru fiecare departament, sa se afiseze numele acestuia, numele si salariul celor mai prost platiti angajati din cadrul sau.
--Varianta 1 - subcerere in clauza FROM
SELECT d.department_name, emp.full_name, emp.salary
FROM departments d, (SELECT first_name || ' ' || last_name AS full_name, salary, department_id
                     FROM employees 
                     WHERE (department_id, salary) IN (SELECT department_id, MIN(salary)
                                                       FROM employees
                                                       GROUP BY department_id)) emp
WHERE d.department_id = emp.department_id;

--Varianta 2 - subcerere nesincronizata in clauza WHERE
SELECT d.department_name, e.last_name||' '||last_name AS full_name, e.salary
FROM departments d JOIN employees e ON e.department_id = d.department_id
WHERE (d.department_id, e.salary) IN ( SELECT department_id, MIN(salary)
                                       FROM employees
                                       GROUP BY department_id);


--34. Problema 22
SELECT DISTINCT d.department_id, department_name,
    n.nr, 
    m.med,
    last_name, employee_id, job_id
FROM employees e, departments d,
    (SELECT COUNT(employee_id) nr, e1.department_id department_id
     FROM employees e1
     GROUP BY e1.department_id) n,
    (SELECT ROUND(AVG(salary), 2) med, e1.department_id department_id
     FROM employees e1
     GROUP BY e1.department_id) m
WHERE e.department_id (+) = d.department_id
AND m.department_id (+) = d.department_id
AND n.department_id (+) = d.department_id;