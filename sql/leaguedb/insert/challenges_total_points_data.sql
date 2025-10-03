INSERT INTO challenges_total_points_data (
    puuid,
    challenge_level,
    current,
    challenge_max,
    percentile,
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
    challenge_level = new.challenge_level,
    current = new.current,
    challenge_max = new.challenge_max,
    percentile = new.percentile,
    last_updated = CURRENT_TIMESTAMP;