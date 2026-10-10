USE DATABASE MEETUP_DB;
USE SCHEMA SILVER;

-- =====================================================
-- QUARANTINE
-- =====================================================

INSERT INTO QUARANTINE.VENUES_QUARANTINE
(
    VENUE_ID,
    ADDRESS_1,
    CITY,
    COUNTRY,
    DISTANCE,
    LAT,
    LOCALIZED_COUNTRY_NAME,
    LON,
    VENUE_NAME,
    RATING,
    RATING_COUNT,
    STATE,
    ZIP,
    NORMALISED_RATING,
    REJECTION_REASON,
    PIPELINE_RUN_ID
)
SELECT
    VENUE_ID,
    ADDRESS_1,
    CITY,
    COUNTRY,
    DISTANCE,
    LAT,
    LOCALIZED_COUNTRY_NAME,
    LON,
    VENUE_NAME,
    RATING,
    RATING_COUNT,
    STATE,
    ZIP,
    NORMALISED_RATING,
    'VENUE_ID_IS_NULL',
    '{pipeline_run_id}'
FROM BRONZE.VENUES_RAW
WHERE VENUE_ID IS NULL;

-- =====================================================
-- DEDUPLICATION
-- =====================================================



-- =====================================================
-- MERGE
-- =====================================================

MERGE INTO SILVER.VENUES_SILVER AS T

USING
(   
    WITH VENUES AS
    (
        SELECT
            VENUE_ID,
            ADDRESS_1,
            CITY,
            COUNTRY,
            DISTANCE,
            LAT,
            LOCALIZED_COUNTRY_NAME,
            LON,
            VENUE_NAME,
            RATING,
            RATING_COUNT,
            STATE,
            ZIP,
            NORMALISED_RATING,

            ROW_NUMBER() OVER
            (
                PARTITION BY VENUE_ID
                ORDER BY LOAD_TIMESTAMP DESC
            ) AS RN

        FROM BRONZE.VENUES_RAW
    )
    SELECT
        VENUE_ID,
        ADDRESS_1,
        CITY,
        COUNTRY,
        DISTANCE,
        LAT,
        LOCALIZED_COUNTRY_NAME,
        LON,
        VENUE_NAME,
        RATING,
        RATING_COUNT,
        STATE,
        ZIP,
        NORMALISED_RATING
    FROM VENUES
    WHERE RN = 1
      AND VENUE_ID IS NOT NULL
) AS S

ON T.VENUE_ID = S.VENUE_ID

WHEN MATCHED
AND (
       COALESCE(T.ADDRESS_1,'') <> COALESCE(S.ADDRESS_1,'')
    OR COALESCE(T.CITY,'') <> COALESCE(S.CITY,'')
    OR COALESCE(T.COUNTRY,'') <> COALESCE(S.COUNTRY,'')
    OR COALESCE(T.DISTANCE,-1) <> COALESCE(S.DISTANCE,-1)
    OR COALESCE(T.LAT,-99999) <> COALESCE(S.LAT,-99999)
    OR COALESCE(T.LOCALIZED_COUNTRY_NAME,'') <> COALESCE(S.LOCALIZED_COUNTRY_NAME,'')
    OR COALESCE(T.LON,-99999) <> COALESCE(S.LON,-99999)
    OR COALESCE(T.VENUE_NAME,'') <> COALESCE(S.VENUE_NAME,'')
    OR COALESCE(T.RATING,-1) <> COALESCE(S.RATING,-1)
    OR COALESCE(T.RATING_COUNT,-1) <> COALESCE(S.RATING_COUNT,-1)
    OR COALESCE(T.STATE,'') <> COALESCE(S.STATE,'')
    OR COALESCE(T.ZIP,'') <> COALESCE(S.ZIP,'')
    OR COALESCE(T.NORMALISED_RATING,-1) <> COALESCE(S.NORMALISED_RATING,-1)
)

THEN UPDATE SET

    T.ADDRESS_1 = S.ADDRESS_1,
    T.CITY = S.CITY,
    T.COUNTRY = S.COUNTRY,
    T.DISTANCE = S.DISTANCE,
    T.LAT = S.LAT,
    T.LOCALIZED_COUNTRY_NAME = S.LOCALIZED_COUNTRY_NAME,
    T.LON = S.LON,
    T.VENUE_NAME = S.VENUE_NAME,
    T.RATING = S.RATING,
    T.RATING_COUNT = S.RATING_COUNT,
    T.STATE = S.STATE,
    T.ZIP = S.ZIP,
    T.NORMALISED_RATING = S.NORMALISED_RATING,
    T.UPDATED_TIMESTAMP = CURRENT_TIMESTAMP(),
    T.PIPELINE_RUN_ID = '{pipeline_run_id}'

WHEN NOT MATCHED THEN

INSERT
(
    VENUE_ID,
    ADDRESS_1,
    CITY,
    COUNTRY,
    DISTANCE,
    LAT,
    LOCALIZED_COUNTRY_NAME,
    LON,
    VENUE_NAME,
    RATING,
    RATING_COUNT,
    STATE,
    ZIP,
    NORMALISED_RATING,
    PIPELINE_RUN_ID
)

VALUES
(
    S.VENUE_ID,
    S.ADDRESS_1,
    S.CITY,
    S.COUNTRY,
    S.DISTANCE,
    S.LAT,
    S.LOCALIZED_COUNTRY_NAME,
    S.LON,
    S.VENUE_NAME,
    S.RATING,
    S.RATING_COUNT,
    S.STATE,
    S.ZIP,
    S.NORMALISED_RATING,
    '{pipeline_run_id}'
);