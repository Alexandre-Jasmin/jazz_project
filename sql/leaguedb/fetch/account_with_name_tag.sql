-- fetch/account_with_name_tag.sql
SELECT *
FROM account_data
WHERE game_name = %s
  AND tag_line  = %s;
