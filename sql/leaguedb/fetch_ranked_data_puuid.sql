SELECT r.*
FROM ranked_data r
JOIN (
    SELECT puuid, queue_type, MAX(snapshot_time) AS latest_time
    FROM ranked_data
    WHERE puuid = %s
    GROUP BY puuid, queue_type
) latest
  ON r.puuid = latest.puuid
 AND r.queue_type = latest.queue_type
 AND r.snapshot_time = latest.latest_time;
