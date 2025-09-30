INSERT IGNORE INTO match_data (
    match_id, game_creation, game_duration, game_end_timestamp, game_start_timestamp,
    game_version, game_id, platform_id, queue_id, game_mode, game_name, game_type,
    map_id, tournament_code
)
VALUES (
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s
);