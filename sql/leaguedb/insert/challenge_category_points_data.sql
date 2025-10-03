INSERT INTO challenges_category_points_data (
    puuid,
    category,
    challenge_level,
    current,
    max,
    percentile
)
VALUES (
    %s,
    %s,
    %s,
    %s,
    %s,
    %s
) AS new
ON DUPLICATE KEY UPDATE
    challenge_level = new.challenge_level,
    current = new.current,
    max = new.max,
    percentile = new.percentile;