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

CREATE TABLE challenges_profile_data (

    puuid               VARCHAR(100)        NOT NULL,

    challenges_level    VARCHAR(20)         NOT NULL,
    current_points      INT                 NOT NULL,
    max_points          INT                 NOT NULL,
    percentile          DECIMAL(5,4)        NULL,

    title               INT                 NULL, -- riot api returns a string, need to transform before insert
    challenges_picked   VARCHAR(255)        NULL, -- riot api returns a list, need to transform before insert 'id,id,id'

    CONSTRAINT fk_challenges_account FOREIGN KEY (puuid)
        REFERENCES account_summoner_data(puuid)
);


CREATE TABLE challenges_category_points_data ();

CREATE TABLE challenges_data ();