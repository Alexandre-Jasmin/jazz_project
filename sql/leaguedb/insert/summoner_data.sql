-- insert/summoner_data.sql
INSERT INTO summoner_data (
    puuid,
    profile_icon_id,
    revision_date,
    summoner_level,
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
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
) AS new
ON DUPLICATE KEY UPDATE
    profile_icon_id = new.profile_icon_id,
    revision_date = new.revision_date,
    summoner_level = new.summoner_level,
    last_updated = CURRENT_TIMESTAMP;