INSERT INTO champion_mastery_data (
    puuid,
    champion_id,
    champion_level,
    champion_points,
    last_play_time,
    last_updated
)
VALUES (
    %s,
    %s,
    %s,
    %s,
    %s,
    CURRENT_TIMESTAMP
) AS new
ON DUPLICATE KEY UPDATE
    champion_level = new.champion_level,
    champion_points = new.champion_points,
    last_play_time = new.last_play_time,
    last_updated = CURRENT_TIMESTAMP;