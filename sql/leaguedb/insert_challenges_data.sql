INSERT INTO challenges_data (
    puuid,
    challenge_id,
    percentile,
    challenge_tier,
    challenge_value,
    achieved_time,
    position,
    players_in_level,
    last_updated
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
    CURRENT_TIMESTAMP
) AS new
ON DUPLICATE KEY UPDATE
    percentile = new.percentile,
    challenge_tier = new.challenge_tier,
    challenge_value = new.challenge_value,
    achieved_time = new.achieved_time,
    position = new.position,
    players_in_level = new.players_in_level,
    last_updated = CURRENT_TIMESTAMP