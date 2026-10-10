USE DATABASE MEETUP_DB;
USE SCHEMA SILVER;

-- ==========================================
-- QUARANTINE
-- ==========================================

INSERT INTO QUARANTINE.CITIES_QUARANTINE
(
    CITY,
    CITY_ID,
    COUNTRY,
    DISTANCE,
    LATITUDE,
    LOCALIZED_COUNTRY_NAME,
    LONGITUDE,
    MEMBER_COUNT,
    RANKING,
    STATE,
    ZIP,
    REJECTION_REASON,
    PIPELINE_RUN_ID
)
SELECT
    CITY,
    CITY_ID,
    COUNTRY,
    DISTANCE,
    LATITUDE,
    LOCALIZED_COUNTRY_NAME,
    LONGITUDE,
    MEMBER_COUNT,
    RANKING,
    STATE,
    ZIP,
    'CITY_ID_IS_NULL',
    '{pipeline_run_id}'
FROM BRONZE.CITIES_RAW
WHERE CITY_ID IS NULL;

-- ==========================================
-- MERGE
-- ==========================================

MERGE INTO SILVER.CITIES_SILVER T

USING
(
    WITH CITIES AS
    (
        SELECT
            CITY,
            CITY_ID,
            COUNTRY,
            DISTANCE,
            LATITUDE,
            LOCALIZED_COUNTRY_NAME,
            LONGITUDE,
            MEMBER_COUNT,
            RANKING,
            STATE,
            ZIP,
            ROW_NUMBER() OVER
            (
                PARTITION BY CITY_ID
                ORDER BY CITY_ID
            ) AS RN
        FROM BRONZE.CITIES_RAW
    )
    SELECT *
    FROM CITIES
    WHERE RN = 1
    AND CITY_ID IS NOT NULL
) S

ON T.CITY_ID = S.CITY_ID

WHEN MATCHED
AND (
       COALESCE(T.CITY,'') <> COALESCE(S.CITY,'')
    OR COALESCE(T.COUNTRY,'') <> COALESCE(S.COUNTRY,'')
    OR COALESCE(T.STATE,'') <> COALESCE(S.STATE,'')
    OR COALESCE(T.ZIP,'') <> COALESCE(S.ZIP,'')
)
THEN UPDATE SET

    T.CITY = S.CITY,
    T.COUNTRY = S.COUNTRY,
    T.DISTANCE = S.DISTANCE,
    T.LATITUDE = S.LATITUDE,
    T.LOCALIZED_COUNTRY_NAME = S.LOCALIZED_COUNTRY_NAME,
    T.LONGITUDE = S.LONGITUDE,
    T.MEMBER_COUNT = S.MEMBER_COUNT,
    T.RANKING = S.RANKING,
    T.STATE = S.STATE,
    T.ZIP = S.ZIP,
    T.UPDATED_TIMESTAMP = CURRENT_TIMESTAMP(),
    T.PIPELINE_RUN_ID = '{pipeline_run_id}'

WHEN NOT MATCHED THEN
INSERT
(
    CITY,
    CITY_ID,
    COUNTRY,
    DISTANCE,
    LATITUDE,
    LOCALIZED_COUNTRY_NAME,
    LONGITUDE,
    MEMBER_COUNT,
    RANKING,
    STATE,
    ZIP,
    PIPELINE_RUN_ID
)
VALUES
(
    S.CITY,
    S.CITY_ID,
    S.COUNTRY,
    S.DISTANCE,
    S.LATITUDE,
    S.LOCALIZED_COUNTRY_NAME,
    S.LONGITUDE,
    S.MEMBER_COUNT,
    S.RANKING,
    S.STATE,
    S.ZIP,
    '{pipeline_run_id}'
);