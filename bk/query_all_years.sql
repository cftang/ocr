SET SQLFORMAT CSV
SET FEEDBACK OFF
SET HEADING ON
SET PAGESIZE 0
SET TRIMSPOOL ON
SET TERMOUT OFF

COLUMN ts NEW_VALUE ts
SELECT TO_CHAR(SYSDATE, 'YYYYMMDD_HH24MISS') ts FROM dual;

SPOOL hq_&ts..csv



WITH dates AS (
  SELECT TO_DATE('2020-01-02', 'YYYY-MM-DD') as start_2020p1,
         TO_DATE('2020-03-05', 'YYYY-MM-DD') as end_2020p1,
         TO_DATE('2020-03-12', 'YYYY-MM-DD') as start_2020p2,
         TO_DATE('2020-04-30', 'YYYY-MM-DD') as end_2020p2,
         TO_DATE('2021-01-04', 'YYYY-MM-DD') as start_2021p1,
         TO_DATE('2021-03-05', 'YYYY-MM-DD') as end_2021p1,
         TO_DATE('2021-03-12', 'YYYY-MM-DD') as start_2021p2,
         TO_DATE('2021-04-30', 'YYYY-MM-DD') as end_2021p2,
         TO_DATE('2022-01-04', 'YYYY-MM-DD') as start_2022p1,
         TO_DATE('2022-03-04', 'YYYY-MM-DD') as end_2022p1,
         TO_DATE('2022-03-11', 'YYYY-MM-DD') as start_2022p2,
         TO_DATE('2022-04-29', 'YYYY-MM-DD') as end_2022p2,
         TO_DATE('2023-01-03', 'YYYY-MM-DD') as start_2023p1,
         TO_DATE('2023-03-06', 'YYYY-MM-DD') as end_2023p1,
         TO_DATE('2023-03-13', 'YYYY-MM-DD') as start_2023p2,
         TO_DATE('2023-04-28', 'YYYY-MM-DD') as end_2023p2,
         TO_DATE('2024-01-02', 'YYYY-MM-DD') as start_2024p1,
         TO_DATE('2024-03-05', 'YYYY-MM-DD') as end_2024p1,
         TO_DATE('2024-03-12', 'YYYY-MM-DD') as start_2024p2,
         TO_DATE('2024-04-30', 'YYYY-MM-DD') as end_2024p2,
         TO_DATE('2025-01-02', 'YYYY-MM-DD') as start_2025p1,
         TO_DATE('2025-03-05', 'YYYY-MM-DD') as end_2025p1,
         TO_DATE('2025-03-12', 'YYYY-MM-DD') as start_2025p2,
         TO_DATE('2025-04-30', 'YYYY-MM-DD') as end_2025p2,
         TO_DATE('2026-01-05', 'YYYY-MM-DD') as start_2026p1,
         (select max(rq) from hq_baostock )  as end_2026p1
  FROM DUAL
),
p2020_start1 AS (
  SELECT code, close 
  FROM hq_baostock h, dates d 
  WHERE h.rq = d.start_2020p1
),
p2020_end1 AS (
  SELECT code, close 
  FROM hq_baostock h, dates d 
  WHERE h.rq = d.end_2020p1
),
p2020_start2 AS (
  SELECT code, close 
  FROM hq_baostock h, dates d 
  WHERE h.rq = d.start_2020p2
),
p2020_end2 AS (
  SELECT code, close 
  FROM hq_baostock h, dates d 
  WHERE h.rq = d.end_2020p2 
),
p2021_start1 AS (
  SELECT code, close 
  FROM hq_baostock h, dates d 
  WHERE h.rq = d.start_2021p1
),
p2021_end1 AS (
  SELECT code, close 
  FROM hq_baostock h, dates d 
  WHERE h.rq = d.end_2021p1
),
p2021_start2 AS (
  SELECT code, close 
  FROM hq_baostock h, dates d 
  WHERE h.rq = d.start_2021p2
),
p2021_end2 AS (
  SELECT code, close 
  FROM hq_baostock h, dates d 
  WHERE h.rq = d.end_2021p2 
),
p2022_start1 AS (
  SELECT code, close 
  FROM hq_baostock h, dates d 
  WHERE h.rq = d.start_2022p1
),
p2022_end1 AS (
  SELECT code, close 
  FROM hq_baostock h, dates d 
  WHERE h.rq = d.end_2022p1
),
p2022_start2 AS (
  SELECT code, close 
  FROM hq_baostock h, dates d 
  WHERE h.rq = d.start_2022p2
),
p2022_end2 AS (
  SELECT code, close 
  FROM hq_baostock h, dates d 
  WHERE h.rq = d.end_2022p2 
),
p2023_start1 AS (
  SELECT code, close 
  FROM hq_baostock h, dates d 
  WHERE h.rq = d.start_2023p1
),
p2023_end1 AS (
  SELECT code, close 
  FROM hq_baostock h, dates d 
  WHERE h.rq = d.end_2023p1
),
p2023_start2 AS (
  SELECT code, close 
  FROM hq_baostock h, dates d 
  WHERE h.rq = d.start_2023p2
),
p2023_end2 AS (
  SELECT code, close 
  FROM hq_baostock h, dates d 
  WHERE h.rq = d.end_2023p2 
),
p2024_start1 AS (
  SELECT code, close 
  FROM hq_baostock h, dates d 
  WHERE h.rq = d.start_2024p1
),
p2024_end1 AS (
  SELECT code, close 
  FROM hq_baostock h, dates d 
  WHERE h.rq = d.end_2024p1
),
p2024_start2 AS (
  SELECT code, close 
  FROM hq_baostock h, dates d 
  WHERE h.rq = d.start_2024p2
),
p2024_end2 AS (
  SELECT code, close 
  FROM hq_baostock h, dates d 
  WHERE h.rq = d.end_2024p2 
),
p2025_start1 AS (
  SELECT code, close 
  FROM hq_baostock h, dates d 
  WHERE h.rq = d.start_2025p1
),
p2025_end1 AS (
  SELECT code, close 
  FROM hq_baostock h, dates d 
  WHERE h.rq = d.end_2025p1
),
p2025_start2 AS (
  SELECT code, close 
  FROM hq_baostock h, dates d 
  WHERE h.rq = d.start_2025p2
),
p2025_end2 AS (
  SELECT code, close 
  FROM hq_baostock h, dates d 
  WHERE h.rq = d.end_2025p2 
),
p2026_start1 AS (
  SELECT code, close 
  FROM hq_baostock h, dates d 
  WHERE h.rq = d.start_2026p1
),
p2026_end1 AS (
  SELECT code, close 
  FROM hq_baostock h, dates d 
  WHERE h.rq = d.end_2026p1
),
y2020 AS (
SELECT 2020 AS year, p2020s1.code AS code,
  ROUND((p2020e1.close - p2020s1.close) / p2020s1.close * 100, 2) AS period_pct1,
  ROUND((p2020e2.close - p2020s2.close) / p2020s2.close * 100, 2) AS period_pct2,
  p2020s1.close as start_price1, 
  p2020e1.close as end_price1,
  p2020s2.close as start_price2, 
  p2020e2.close as end_price2
FROM p2020_start1 p2020s1
JOIN p2020_end1 p2020e1 ON p2020s1.code = p2020e1.code
JOIN p2020_start2 p2020s2 ON p2020s1.code = p2020s2.code
JOIN p2020_end2 p2020e2 ON p2020s1.code = p2020e2.code
),
y2021 AS (
SELECT 2021 AS year, p2021s1.code AS code,
  ROUND((p2021e1.close - p2021s1.close) / p2021s1.close * 100, 2) AS period_pct1,
  ROUND((p2021e2.close - p2021s2.close) / p2021s2.close * 100, 2) AS period_pct2,
  p2021s1.close as start_price1, 
  p2021e1.close as end_price1,
  p2021s2.close as start_price2, 
  p2021e2.close as end_price2
FROM p2021_start1 p2021s1
JOIN p2021_end1 p2021e1 ON p2021s1.code = p2021e1.code
JOIN p2021_start2 p2021s2 ON p2021s1.code = p2021s2.code
JOIN p2021_end2 p2021e2 ON p2021s1.code = p2021e2.code
),
y2022 AS (
SELECT 2022 AS year, p2022s1.code AS code,
  ROUND((p2022e1.close - p2022s1.close) / p2022s1.close * 100, 2) AS period_pct1,
  ROUND((p2022e2.close - p2022s2.close) / p2022s2.close * 100, 2) AS period_pct2,
  p2022s1.close as start_price1, 
  p2022e1.close as end_price1,
  p2022s2.close as start_price2, 
  p2022e2.close as end_price2
FROM p2022_start1 p2022s1
JOIN p2022_end1 p2022e1 ON p2022s1.code = p2022e1.code
JOIN p2022_start2 p2022s2 ON p2022s1.code = p2022s2.code
JOIN p2022_end2 p2022e2 ON p2022s1.code = p2022e2.code
),
y2023 AS (
SELECT 2023 AS year, p2023s1.code AS code,
  ROUND((p2023e1.close - p2023s1.close) / p2023s1.close * 100, 2) AS period_pct1,
  ROUND((p2023e2.close - p2023s2.close) / p2023s2.close * 100, 2) AS period_pct2,
  p2023s1.close as start_price1, 
  p2023e1.close as end_price1,
  p2023s2.close as start_price2, 
  p2023e2.close as end_price2
FROM p2023_start1 p2023s1
JOIN p2023_end1 p2023e1 ON p2023s1.code = p2023e1.code
JOIN p2023_start2 p2023s2 ON p2023s1.code = p2023s2.code
JOIN p2023_end2 p2023e2 ON p2023s1.code = p2023e2.code
),
y2024 AS (
SELECT 2024 AS year, p2024s1.code AS code,
  ROUND((p2024e1.close - p2024s1.close) / p2024s1.close * 100, 2) AS period_pct1,
  ROUND((p2024e2.close - p2024s2.close) / p2024s2.close * 100, 2) AS period_pct2,
  p2024s1.close as start_price1, 
  p2024e1.close as end_price1,
  p2024s2.close as start_price2, 
  p2024e2.close as end_price2
FROM p2024_start1 p2024s1
JOIN p2024_end1 p2024e1 ON p2024s1.code = p2024e1.code
JOIN p2024_start2 p2024s2 ON p2024s1.code = p2024s2.code
JOIN p2024_end2 p2024e2 ON p2024s1.code = p2024e2.code
),
y2025 AS (
SELECT 2025 AS year, p2025s1.code AS code,
  ROUND((p2025e1.close - p2025s1.close) / p2025s1.close * 100, 2) AS period_pct1,
  ROUND((p2025e2.close - p2025s2.close) / p2025s2.close * 100, 2) AS period_pct2,
  p2025s1.close as start_price1, 
  p2025e1.close as end_price1,
  p2025s2.close as start_price2, 
  p2025e2.close as end_price2
FROM p2025_start1 p2025s1
JOIN p2025_end1 p2025e1 ON p2025s1.code = p2025e1.code
JOIN p2025_start2 p2025s2 ON p2025s1.code = p2025s2.code
JOIN p2025_end2 p2025e2 ON p2025s1.code = p2025e2.code
),
y2026 AS (
SELECT 2026 AS year, p2026s1.code AS code,
  ROUND((p2026e1.close - p2026s1.close) / p2026s1.close * 100, 2) AS period_pct1,
--  ROUND((p2026e2.close - p2026s2.close) / p2026s2.close * 100, 2) AS period_pct2,
  p2026s1.close as start_price1, 
  p2026e1.close as end_price1
--  p2026s2.close as start_price2, 
--  p2026e2.close as end_price2
FROM p2026_start1 p2026s1
JOIN p2026_end1 p2026e1 ON p2026s1.code = p2026e1.code
--JOIN p2026_start2 p2026s2 ON p2026s1.code = p2026s2.code
--JOIN p2026_end2 p2026e2 ON p2026s1.code = p2026e2.code
)
SELECT y2025.code as CODE,
       dm.code_name AS NAME,
       y2020.period_pct1 AS y2020_period_pct1,
       y2020.period_pct2 AS y2020_period_pct2,
       y2020.start_price1 AS y2020_start_price1,
       y2020.end_price1 AS y2020_end_price1,
       y2020.start_price2 AS y2020_start_price2,
       y2020.end_price2 AS y2020_end_price2,
       y2021.period_pct1 AS y2021_period_pct1,
       y2021.period_pct2 AS y2021_period_pct2,
       y2021.start_price1 AS y2021_start_price1,
       y2021.end_price1 AS y2021_end_price1,
       y2021.start_price2 AS y2021_start_price2,
       y2021.end_price2 AS y2021_end_price2,
       y2022.period_pct1 AS y2022_period_pct1,
       y2022.period_pct2 AS y2022_period_pct2,
       y2022.start_price1 AS y2022_start_price1,
       y2022.end_price1 AS y2022_end_price1,
       y2022.start_price2 AS y2022_start_price2,
       y2022.end_price2 AS y2022_end_price2,
       y2023.period_pct1 AS y2023_period_pct1,
       y2023.period_pct2 AS y2023_period_pct2,
       y2023.start_price1 AS y2023_start_price1,
       y2023.end_price1 AS y2023_end_price1,
       y2023.start_price2 AS y2023_start_price2,
       y2023.end_price2 AS y2023_end_price2,
       y2024.period_pct1 AS y2024_period_pct1,
       y2024.period_pct2 AS y2024_period_pct2,
       y2024.start_price1 AS y2024_start_price1,
       y2024.end_price1 AS y2024_end_price1,
       y2024.start_price2 AS y2024_start_price2,
       y2024.end_price2 AS y2024_end_price2,
       y2025.period_pct1 AS y2025_period_pct1,
       y2025.period_pct2 AS y2025_period_pct2,
       y2025.start_price1 AS y2025_start_price1,
       y2025.end_price1 AS y2025_end_price1,
       y2025.start_price2 AS y2025_start_price2,
       y2025.end_price2 AS y2025_end_price2,
       y2026.period_pct1 AS y2026_period_pct1,
--       y2026.period_pct2 AS y2026_period_pct2,
       y2026.start_price1 AS y2026_start_price1,
       y2026.end_price1 AS y2026_end_price1
--       y2026.start_price2 AS y2026_start_price2,
--       y2026.end_price2 AS y2026_end_price2
FROM y2026
JOIN dm_baostock dm ON y2026.code = dm.code
FULL OUTER JOIN y2025 ON y2026.code = y2025.code
FULL OUTER JOIN y2024 ON y2026.code = y2024.code
FULL OUTER JOIN y2023 ON y2026.code = y2023.code
FULL OUTER JOIN y2022 ON y2026.code = y2022.code
FULL OUTER JOIN y2021 ON y2026.code = y2021.code
FULL OUTER JOIN y2020 ON y2026.code = y2020.code
ORDER BY y2026.period_pct1 DESC;

SPOOL OFF
EXIT

