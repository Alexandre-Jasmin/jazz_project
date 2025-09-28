INSERT INTO account_summoner_data (
    puuid,
    game_name,
    tag_line,
    summoner_level,
    profile_icon_id,
    riot_server,
    first_seen,
    last_updated
)
VALUES (
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
) AS new
ON DUPLICATE KEY UPDATE
    game_name       = new.game_name,
    tag_line        = new.tag_line,
    summoner_level  = new.summoner_level,
    profile_icon_id = new.profile_icon_id,
    riot_server     = new.riot_server,
    last_updated    = CURRENT_TIMESTAMP;