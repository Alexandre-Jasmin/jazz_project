-- insert/account_data.sql
INSERT INTO account_data (
    puuid,
    game_name,
    tag_line,
    first_seen,
    last_updated
)
VALUES (
    %s,
    %s,
    %s,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
) AS new
ON DUPLICATE KEY UPDATE
    game_name       = new.game_name,
    tag_line        = new.tag_line,
    last_updated    = CURRENT_TIMESTAMP;