-- account_data
CREATE TABLE account_data(

    puuid               VARCHAR(100)            PRIMARY KEY,
    game_name           VARCHAR(50)             NOT NULL,
    tag_line            VARCHAR(10)             NOT NULL,

    first_seen          TIMESTAMP               NOT NULL            DEFAULT CURRENT_TIMESTAMP,
    last_updated        TIMESTAMP               NOT NULL            DEFAULT CURRENT_TIMESTAMP,

    UNIQUE KEY unique_name_tag (game_name, tag_line)
    
);

-- summoner_data
CREATE TABLE summoner_data(

    puuid               VARCHAR(100)            PRIMARY KEY,
    profile_icon_id     INT                     NOT NULL,
    revision_date       TIMESTAMP               NOT NULL,
    summoner_level      INT                     NOT NULL,
    riot_server         VARCHAR(10)             NOT NULL,

    first_seen          TIMESTAMP               NOT NULL            DEFAULT CURRENT_TIMESTAMP,
    last_updated        TIMESTAMP               NOT NULL            DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_summoner FOREIGN KEY (puuid)
        REFERENCES account_data(puuid)

);

-- champion_mastery_data
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
        REFERENCES summoner_data (puuid)

);

-- ranked_data
CREATE TABLE ranked_data (

    id                  BIGINT          AUTO_INCREMENT PRIMARY KEY,
    
    -- unique Riot account ID
	puuid			    VARCHAR(100)	NOT NULL,
    
    -- ranked information
    league_id       VARCHAR(100) NOT NULL,
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
        REFERENCES summoner_data (puuid),

    -- prevent inserting exact duplicate snapshots
    UNIQUE KEY uq_ranked_snapshot (puuid, queue_type, snapshot_time)

);

CREATE TABLE challenges_total_points_data(

    puuid               VARCHAR(100)    PRIMARY KEY,
    challenge_level     VARCHAR(25)     NOT NULL,
    current             INT             NOT NULL,
    challenge_max       INT             NOT NULL,
    percentile          DECIMAL(6, 5)   NOT NULL,

    last_updated        TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP, 

    CONSTRAINT fk_challenges FOREIGN KEY (puuid)
        REFERENCES summoner_data(puuid)    

);


CREATE TABLE challenges_category_points_data(

    puuid               VARCHAR(100)    NOT NULL,
    category            VARCHAR(50)     NOT NULL,
    challenge_level     VARCHAR(25)     NOT NULL,
    current             INT             NOT NULL,
    max                 INT             NOT NULL,
    percentile          DECIMAL(6, 5)   NOT NULL,

    CONSTRAINT fk_challenges_category FOREIGN KEY (puuid)
        REFERENCES summoner_data(puuid),

    PRIMARY KEY (puuid, category)

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

    CONSTRAINT fk_challenges_data FOREIGN KEY (puuid)
        REFERENCES summoner_data (puuid)
);