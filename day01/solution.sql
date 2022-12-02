DROP TABLE IF EXISTS elf_calories;

CREATE TABLE elf_calories (
  calories INT NULL
);

COPY elf_calories (calories) FROM '/tmp/aoc_day01.input' NULL AS '';

WITH item_id_added AS (
  SELECT
    ROW_NUMBER() OVER () AS item_id,
    calories AS calories
  FROM
    elf_calories
),
elf_id_added AS (
  SELECT
    calories,
    SUM(CASE WHEN calories IS NULL
      THEN 1
      ELSE 0
    END) OVER (ORDER BY item_id) AS elf_id
  FROM item_id_added
),
top_calorie_cariers AS (
  SELECT SUM(calories) AS most_calories
  FROM elf_id_added
  GROUP BY elf_id
  ORDER BY SUM(calories) DESC
)
SELECT
  SUM(most_calories) AS most_calories
FROM
  (SELECT most_calories FROM top_calorie_cariers LIMIT 1) t
UNION
SELECT
  SUM(most_calories) AS most_calories
FROM
  (SELECT most_calories FROM top_calorie_cariers LIMIT 3) t
;
