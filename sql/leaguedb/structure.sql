USE leaguedb;

-- account_summoner_data.sql
CREATE TABLE account_summoner_data (
    
    -- unique Riot account ID
	puuid			    VARCHAR(100)	PRIMARY KEY,
    
    -- display name + tagline (together unique)
    game_name		    VARCHAR(50)     NOT NULL,
    tag_line		    VARCHAR(10)		NOT NULL,
    summoner_level      INT             NOT NULL,
    profile_icon_id     INT             NOT NULL,
    riot_server         VARCHAR(10)     NOT NULL,
    
    first_seen		    TIMESTAMP		NOT NULL    DEFAULT CURRENT_TIMESTAMP,
    last_updated	    TIMESTAMP		NOT NULL    DEFAULT CURRENT_TIMESTAMP,
    
    -- unique constrain on (game_name, tag_line)
    UNIQUE KEY unique_name_tag (game_name, tag_line)
);

-- champion_mastery_data.sql
CREATE TABLE champion_mastery_data (
    
    -- unique Riot account ID
	puuid			    VARCHAR(100)	NOT NULL,
    
    -- champion information
    champion_id		    INT             NOT NULL,
    champion_level		INT     		NOT NULL,
    champion_points     INT             NOT NULL,
    last_play_time      TIMESTAMP       NOT NULL,
    
    -- tracking
    last_updated	    TIMESTAMP		NOT NULL    DEFAULT CURRENT_TIMESTAMP,
    
    -- puuid+champion_id is unique
    PRIMARY KEY (puuid, champion_id),

    CONSTRAINT fk_mastery_account FOREIGN KEY (puuid)
        REFERENCES account_summoner_data (puuid)
);

-- ranked_data.sql
CREATE TABLE ranked_data (

    id                  BIGINT          AUTO_INCREMENT PRIMARY KEY,
    
    -- unique Riot account ID
	puuid			    VARCHAR(100)	NOT NULL,
    
    -- ranked information
    queue_type		VARCHAR(50)  NOT NULL,
    tier		    VARCHAR(20)  NOT NULL,
    division        VARCHAR(5)   NOT NULL,
    league_points   INT          NOT NULL,
    wins            INT          NOT NULL,
    losses          INT          NOT NULL,
    veteran         BOOLEAN      NOT NULL,
    inactive        BOOLEAN      NOT NULL,
    fresh_blood     BOOLEAN      NOT NULL,
    hot_streak      BOOLEAN      NOT NULL,

    snapshot_time   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_ranked_account FOREIGN KEY (puuid)
        REFERENCES account_summoner_data (puuid),

    -- prevent inserting exact duplicate snapshots
    UNIQUE KEY uq_ranked_snapshot (puuid, queue_type, snapshot_time),

    INDEX idx_ranked_puuid_queue_time (puuid, queue_type, snapshot_time)
);

CREATE TABLE challenges_data (

    -- unique Riot account ID
	puuid			    VARCHAR(100)	NOT NULL,

    challenge_id        INT             NOT NULL,
    percentile          DECIMAL(6, 5)   NOT NULL,
    challenge_tier      VARCHAR(25)     NOT NULL,
    challenge_value     INT             NOT NULL,
    achieved_time       TIMESTAMP       NULL,
    position            INT             NULL,
    players_in_level    INT             NULL,

    last_updated	    TIMESTAMP		NOT NULL    DEFAULT CURRENT_TIMESTAMP,

    -- puuid+champion_id is unique
    PRIMARY KEY (puuid, challenge_id),

    CONSTRAINT fk_challenges_account FOREIGN KEY (puuid)
        REFERENCES account_summoner_data (puuid)
);

CREATE TABLE match_data(

    match_id                VARCHAR(25)     PRIMARY KEY,

    game_creation           TIMESTAMP       NOT NULL,
    game_duration           INT             NOT NULL,
    game_end_timestamp      TIMESTAMP       NOT NULL,
    game_start_timestamp    TIMESTAMP       NOT NULL,
    game_version            VARCHAR(25)     NOT NULL,
    game_id                 BIGINT          NOT NULL,
    platform_id             VARCHAR(10)     NOT NULL,
    queue_id                INT             NOT NULL,
    game_mode               VARCHAR(20)     NOT NULL,
    game_name               VARCHAR(50)     NOT NULL,
    game_type               VARCHAR(25)     NOT NULL,
    map_id                  INT             NOT NULL,
    tournament_code         VARCHAR(50)     NULL,

    first_seen           TIMESTAMP       NOT NULL    DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE match_data_participants (

    match_id            VARCHAR(25)     NOT NULL,
    participant_index   INT             NOT NULL,
    puuid               VARCHAR(100)    NOT NULL,

    -- match info
    all_in_pings                            INT             NOT NULL,
    assist_me_pings                         INT             NOT NULL,
    assists                                 INT             NOT NULL,
    bait_pings                              INT             NOT NULL,
    baron_kills                             INT             NOT NULL,
    basic_pings                             INT             NOT NULL,
    bounty_level                            INT             NOT NULL,
    champ_exp                               INT             NOT NULL,
    champ_level                             INT             NOT NULL,
    champ_id                                INT             NOT NULL,
    champ_name                              VARCHAR(50)     NOT NULL,
    champ_transform                         INT             NOT NULL,
    command_pings                           INT             NOT NULL,
    consumables_purchased                   INT             NOT NULL,
    damage_to_buildings                     INT             NOT NULL,
    damage_to_objectives                    INT             NOT NULL,
    damage_to_turrets                       INT             NOT NULL,
    damage_self_mitigated                   INT             NOT NULL,
    danger_pings                            INT             NOT NULL,
    deaths                                  INT             NOT NULL,
    detector_wards_placed                   INT             NOT NULL,
    double_kills                            INT             NOT NULL,
    dragon_kills                            INT             NOT NULL,
    eligible_for_progression                BOOLEAN         NOT NULL,
    enemy_missing_pings                     INT             NOT NULL,
    enemy_vision_pings                      INT             NOT NULL,
    first_blood_assist                      BOOLEAN         NOT NULL,
    first_blood_kill                        BOOLEAN         NOT NULL,
    first_tower_assist                      BOOLEAN         NOT NULL,
    first_tower_kill                        BOOLEAN         NOT NULL,
    game_ended_in_early_surrender           BOOLEAN         NOT NULL,
    game_ended_in_surrender                 BOOLEAN         NOT NULL,
    get_back_pings                          INT             NOT NULL,
    gold_earned                             INT             NOT NULL,
    gold_spent                              INT             NOT NULL,
    hold_pings                              INT             NOT NULL,
    individual_position                     VARCHAR(50)     NOT NULL,
    inhibitor_kills                         INT             NOT NULL,
    inhibitor_takedowns                     INT             NOT NULL,
    inhibitors_lost                         INT             NOT NULL,
    item0                                   INT             NOT NULL,
    item1                                   INT             NOT NULL,
    item2                                   INT             NOT NULL,
    item3                                   INT             NOT NULL,
    item4                                   INT             NOT NULL,
    item5                                   INT             NOT NULL,
    item6                                   INT             NOT NULL,
    items_purchased                         INT             NOT NULL,
    killing_sprees                          INT             NOT NULL,
    kills                                   INT             NOT NULL,
    lane                                    VARCHAR(10)     NOT NULL,
    largest_crit_strike                     INT             NOT NULL,
    largest_killing_spree                   INT             NOT NULL,
    largest_multi_kill                      INT             NOT NULL,
    longest_time_spent_living               INT             NOT NULL,
    magic_dmg_dealt                         INT             NOT NULL,
    magic_dmg_dealt_to_champions            INT             NOT NULL,
    magic_dmg_taken                         INT             NOT NULL,
    need_vision_pings                       INT             NOT NULL,
    neutral_minions_killed                  INT             NOT NULL,
    nexus_kills                             INT             NOT NULL,
    nexus_lost                              INT             NOT NULL,
    nexus_takedowns                         INT             NOT NULL,
    objective_stolen                        INT             NOT NULL,
    objective_stolen_assists                INT             NOT NULL,
    on_my_way_pings                         INT             NOT NULL,
    participant_id                          INT             NOT NULL,
    penta_kills                             INT             NOT NULL,
    physical_damage_dealt                   INT             NOT NULL,
    physical_damage_dealt_to_champions      INT             NOT NULL,
    physical_damage_taken                   INT             NOT NULL,
    placement                               INT             NOT NULL,
    player_augment1                         INT             NOT NULL,
    player_augment2                         INT             NOT NULL,
    player_augment3                         INT             NOT NULL,
    player_augment4                         INT             NOT NULL,
    player_score0                           INT             NOT NULL,
    player_score1                           INT             NOT NULL,
    player_score10                          INT             NOT NULL,
    player_score11                          INT             NOT NULL,
    player_score2                           INT             NOT NULL,
    player_score3                           INT             NOT NULL,
    player_score4                           INT             NOT NULL,
    player_score5                           INT             NOT NULL,
    player_score6                           INT             NOT NULL,
    player_score7                           INT             NOT NULL,
    player_score8                           INT             NOT NULL,
    player_score9                           INT             NOT NULL,
    player_sub_team_id                      INT             NOT NULL,
    profile_icon                            INT             NOT NULL,
    push_pings                              INT             NOT NULL,
    quadra_kills                            INT             NOT NULL,
    riot_id_game_name                       VARCHAR(50)     NOT NULL,
    riot_id_tag_line                        VARCHAR(10)     NOT NULL,
    riot_role                               VARCHAR(20)     NOT NULL,
    sight_wards_bought_in_game              INT             NOT NULL,
    spell1_casts                            INT             NOT NULL,
    spell2_casts                            INT             NOT NULL,
    spell3_casts                            INT             NOT NULL,
    spell4_casts                            INT             NOT NULL,
    sub_team_placement                      INT             NOT NULL,
    summoner1_casts                         INT             NOT NULL,
    summoner1_id                            INT             NOT NULL,
    summoner2_casts                         INT             NOT NULL,
    summoner2_id                            INT             NOT NULL,
    summoner_id                             VARCHAR(50)     NOT NULL,
    summoner_level                          INT             NOT NULL,
    summoner_name                           VARCHAR(50)     NOT NULL,
    team_early_surrendered                  BOOLEAN         NOT NULL,
    team_id                                 INT             NOT NULL,
    team_position                           VARCHAR(100)    NOT NULL,
    time_ccing_others                       INT             NOT NULL,
    time_played                             INT             NOT NULL,
    total_ally_jungle_minions_killed        INT             NOT NULL,
    total_dmg_dealt                         INT             NOT NULL,
    total_dmg_dealt_to_champions            INT             NOT NULL,
    total_dmg_shieled_on_teammates          INT             NOT NULL,
    total_dmg_taken                         INT             NOT NULL,
    total_enemy_jungle_minions_killed       INT             NOT NULL,
    total_heal                              INT             NOT NULL,
    total_heal_on_teammates                 INT             NOT NULL,
    total_minions_killed                    INT             NOT NULL,
    total_time_cc_dealt                     INT             NOT NULL,
    total_time_spent_dead                   INT             NOT NULL,
    total_units_healed                      INT             NOT NULL,
    triple_kills                            INT             NOT NULL,
    true_damage_dealt                       INT             NOT NULL,
    true_damage_dealt_to_champions          INT             NOT NULL,
    true_damage_taken                       INT             NOT NULL,
    turret_kills                            INT             NOT NULL,
    turret_takedowns                        INT             NOT NULL,
    turrets_lost                            INT             NOT NULL,
    unreal_kills                            INT             NOT NULL,
    vision_cleared_pings                    INT             NOT NULL,
    vision_score                            INT             NOT NULL,
    vision_wards_bought_in_game             INT             NOT NULL,   
    wards_killed                            INT             NOT NULL,
    wards_placed                            INT             NOT NULL,
    win                                     BOOLEAN         NOT NULL,

    first_seen          TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (match_id, puuid),

    INDEX idx_match_id (match_id),
    INDEX idx_puuid (puuid),

    CONSTRAINT fk_match FOREIGN KEY (match_id) 
        REFERENCES match_data(match_id) ON DELETE CASCADE
);


CREATE TABLE match_data_teams(

);