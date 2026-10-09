USE DATABASE MEETUP_DB;
USE SCHEMA BRONZE;

-- =====================================================
-- CATEGORIES
-- =====================================================

COPY INTO CATEGORIES_RAW
FROM (
    SELECT
        $1,
        $2,
        $3,
        $4,
        CURRENT_TIMESTAMP(),
        METADATA$FILENAME,
        CURRENT_DATE()
    FROM @MEETUP_DB.INTEGRATION.RAW_MEETUP_STAGE/meetup/initial/categories.csv
)
FILE_FORMAT = (
    FORMAT_NAME = MEETUP_DB.INTEGRATION.CSV_FORMAT
)
ON_ERROR = CONTINUE;

-- =====================================================
-- CITIES
-- =====================================================

COPY INTO CITIES_RAW
FROM (
    SELECT
        $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,
        CURRENT_TIMESTAMP(),
        METADATA$FILENAME,
        CURRENT_DATE()
    FROM @MEETUP_DB.INTEGRATION.RAW_MEETUP_STAGE/meetup/initial/cities.csv
)
FILE_FORMAT = (
    FORMAT_NAME = MEETUP_DB.INTEGRATION.CSV_FORMAT
)
ON_ERROR = CONTINUE;

-- =====================================================
-- TOPICS
-- =====================================================

COPY INTO TOPICS_RAW
FROM (
    SELECT
        $1,$2,$3,$4,$5,$6,$7,
        CURRENT_TIMESTAMP(),
        METADATA$FILENAME,
        CURRENT_DATE()
    FROM @MEETUP_DB.INTEGRATION.RAW_MEETUP_STAGE/meetup/initial/topics.csv
)
FILE_FORMAT = (
    FORMAT_NAME = MEETUP_DB.INTEGRATION.CSV_FORMAT
)
ON_ERROR = CONTINUE;

-- =====================================================
-- GROUPS_TOPICS
-- =====================================================

COPY INTO GROUPS_TOPICS_RAW
FROM (
    SELECT
        $1,$2,$3,$4,
        CURRENT_TIMESTAMP(),
        METADATA$FILENAME,
        CURRENT_DATE()
    FROM @MEETUP_DB.INTEGRATION.RAW_MEETUP_STAGE/meetup/initial/groups_topics.csv
)
FILE_FORMAT = (
    FORMAT_NAME = MEETUP_DB.INTEGRATION.CSV_FORMAT
)
ON_ERROR = CONTINUE;

-- =====================================================
-- MEMBERS_TOPICS
-- =====================================================

COPY INTO MEMBERS_TOPICS_RAW
FROM (
    SELECT
        $1,$2,$3,$4,
        CURRENT_TIMESTAMP(),
        METADATA$FILENAME,
        CURRENT_DATE()
    FROM @MEETUP_DB.INTEGRATION.RAW_MEETUP_STAGE/meetup/initial/members_topics.csv
)
FILE_FORMAT = (
    FORMAT_NAME = MEETUP_DB.INTEGRATION.CSV_FORMAT
)
ON_ERROR = CONTINUE;

-- =====================================================
-- MEMBERS
-- =====================================================

COPY INTO MEMBERS_RAW
FROM (
    SELECT
        $1,
        $2,
        $3,
        $4,
        $5,
        $6,
        $7,
        $8,
        $9,
        $10,
        $11,
        $12,
        $13,
        $14,
        CURRENT_TIMESTAMP(),
        METADATA$FILENAME,
        CURRENT_DATE()
    FROM @MEETUP_DB.INTEGRATION.RAW_MEETUP_STAGE/meetup/initial/members.csv
)
FILE_FORMAT = (
    FORMAT_NAME = MEETUP_DB.INTEGRATION.CSV_FORMAT
)
ON_ERROR = CONTINUE;

-- =====================================================
-- VENUES
-- =====================================================

COPY INTO VENUES_RAW
FROM (
    SELECT
        $1,
        $2,
        $3,
        $4,
        $5,
        $6,
        $7,
        $8,
        $9,
        $10,
        $11,
        $12,
        $13,
        $14,
        CURRENT_TIMESTAMP(),
        METADATA$FILENAME,
        CURRENT_DATE()
    FROM @MEETUP_DB.INTEGRATION.RAW_MEETUP_STAGE/meetup/initial/venues.csv
)
FILE_FORMAT = (
    FORMAT_NAME = MEETUP_DB.INTEGRATION.CSV_FORMAT
)
ON_ERROR = CONTINUE;

-- =====================================================
-- GROUPS
-- =====================================================

COPY INTO GROUPS_RAW
FROM (
    SELECT
        $1,$2,$3,$4,$5,
        $6,$7,$8,$9,$10,
        $11,$12,$13,$14,$15,
        $16,$17,$18,$19,$20,
        $21,$22,$23,$24,$25,
        $26,$27,$28,$29,$30,
        $31,$32,$33,$34,$35,
        $36,
        CURRENT_TIMESTAMP(),
        METADATA$FILENAME,
        CURRENT_DATE()
    FROM @MEETUP_DB.INTEGRATION.RAW_MEETUP_STAGE/meetup/initial/groups.csv
)
FILE_FORMAT = (
    FORMAT_NAME = MEETUP_DB.INTEGRATION.CSV_FORMAT
)
ON_ERROR = CONTINUE;

-- =====================================================
-- EVENTS
-- =====================================================

COPY INTO EVENTS_RAW
FROM (
    SELECT
        $1,$2,$3,$4,$5,
        $6,$7,$8,$9,$10,
        $11,$12,$13,$14,$15,
        $16,$17,$18,$19,$20,
        $21,$22,$23,$24,$25,
        $26,$27,$28,$29,$30,
        $31,$32,$33,$34,$35,
        $36,$37,$38,$39,$40,
        $41,$42,$43,$44,$45,
        $46,$47,$48,
        CURRENT_TIMESTAMP(),
        METADATA$FILENAME,
        CURRENT_DATE()
    FROM @MEETUP_DB.INTEGRATION.RAW_MEETUP_STAGE/meetup/initial/events.csv
)
FILE_FORMAT = (
    FORMAT_NAME = MEETUP_DB.INTEGRATION.CSV_FORMAT
)
ON_ERROR = CONTINUE;