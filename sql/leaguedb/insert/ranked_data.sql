INSERT INTO ranked_data (
    puuid, league_id, queue_type, tier, division, league_points, wins, losses,
    veteran, inactive, fresh_blood, hot_streak, snapshot_time
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW()
);