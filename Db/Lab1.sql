-- 1.
DESCRIBE employees;
DESCRIBE departments;
DESCRIBE jobs;
DESCRIBE job_history;
DESCRIBE job_grades;
DESCRIBE locations;
DESCRIBE countries;
DESCRIBE regions;

--2.
SELECT * FROM employees;

--3.
SELECT employee_id, first_name||' '||last_name AS name, job_id, hire_date
FROM employees;

--4.
SELECT job_id FROM employees;
SELECT DISTINCT job_id FROM employees;

--5.
SELECT first_name||' '||last_name||', '||job_id AS "Angajat si titlu"
FROM employees;

--6.
SELECT first_name||' '||last_name AS name, salary
FROM employees
WHERE salary > 2850;

--7.
SELECT first_name||' '||last_name AS  name, department_id
FROM employees
WHERE employee_id = 104;

--8.
SELECT first_name||' '||last_name AS name, salary
FROM employees
WHERE salary NOT BETWEEN 1500 AND 2850
ORDER BY 2 ASC;

--9.
SELECT first_name||' '||last_name AS name, job_id, hire_date
FROM employees
WHERE hire_date BETWEEN '20-FEB-87' AND '1-MAY-89'
ORDER BY hire_date;

SELECT first_name, last_name, department_id
FROM employees
WHERE department_id IN (10, 30)
ORDER BY 2;

--10.
SELECT first_name||' '||last_name AS name, salary
FROM employees
WHERE salary > 3500
    AND department_id IN (10, 30);
    
--11.
SELECT SYSDATE FROM DUAL;

--12.
--Varianta 1:
SELECT first_name, last_name, hire_date
FROM employees
WHERE hire_date LIKE ('%87%');

--Varianta 2:
SELECT first_name, last_name, hire_date
FROM employees
WHERE TO_CHAR(hire_date, 'YYYY') = '1987';

--13.
SELECT first_name||' '||last_name AS name, job_id
FROM employees
WHERE manager_id IS NULL;

--14.
SELECT first_name||' '||last_name AS name, salary, commission_pct
FROM employees
WHERE commission_pct IS NOT NULL
ORDER BY salary DESC, commission_pct DESC;

--15.
--Varianta 1
SELECT last_name||' '||first_name AS "Nume angajat"
FROM employees
WHERE UPPER(last_name||' '||first_name) LIKE '__A%';

--Varianta 2
SELECT last_name||' '||first_name AS "Nume angajat"
FROM employees
WHERE INSTR(UPPER(last_name||' '||first_name), 'A') = 3;

--16.
SELECT last_name||' '||first_name AS "Nume angajat"
FROM employees
WHERE (UPPER(last_name||' '||first_name) LIKE '%L%L%' AND department_id = 30)
    OR (UPPER(last_name||' '||first_name) LIKE '%L%L%' AND manager_id = 101);
    
--17.
SELECT DISTINCT e.last_name||' '||e.first_name AS name, j.job_title, salary
FROM employees e
INNER JOIN jobs j ON e.job_id = j.job_id
WHERE (UPPER(j.job_title) LIKE '%CLERK%' AND salary NOT IN (1000, 2000, 3000))
    OR (UPPER(j.job_title) LIKE '%REP%' AND salary NOT IN (1000, 2000, 3000));
    
--18
SELECT first_name, last_name, salary, commission_pct
FROM employees 
WHERE 5*commission_pct*salary < salary;   





