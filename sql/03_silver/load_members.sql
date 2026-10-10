USE DATABASE MEETUP_DB;
USE SCHEMA SILVER;

-- =====================================================
-- QUARANTINE
-- =====================================================

INSERT INTO QUARANTINE.MEMBERS_QUARANTINE
(
    MEMBER_ID,
    BIO,
    CITY,
    COUNTRY,
    HOMETOWN,
    JOINED,
    LAT,
    LINK,
    LON,
    MEMBER_NAME,
    STATE,
    MEMBER_STATUS,
    VISITED,
    GROUP_ID,
    REJECTION_REASON,
    PIPELINE_RUN_ID
)
SELECT
    MEMBER_ID,
    BIO,
    CITY,
    COUNTRY,
    HOMETOWN,
    JOINED,
    LAT,
    LINK,
    LON,
    MEMBER_NAME,
    STATE,
    MEMBER_STATUS,
    VISITED,
    GROUP_ID,
    CASE
        WHEN MEMBER_ID IS NULL THEN 'MEMBER_ID_IS_NULL'
        WHEN GROUP_ID IS NULL THEN 'GROUP_ID_IS_NULL'
    END,
    '{pipeline_run_id}'
FROM BRONZE.MEMBERS_RAW
WHERE MEMBER_ID IS NULL
   OR GROUP_ID IS NULL;

-- =====================================================
-- DEDUPLICATION
-- =====================================================


-- =====================================================
-- MERGE
-- =====================================================

MERGE INTO SILVER.MEMBERS_SILVER AS T

USING
(
    WITH MEMBERS AS
    (
        SELECT
            MEMBER_ID,
            BIO,
            CITY,
            COUNTRY,
            HOMETOWN,
            JOINED,
            LAT,
            LINK,
            LON,
            MEMBER_NAME,
            STATE,
            MEMBER_STATUS,
            VISITED,
            GROUP_ID,
            ROW_NUMBER() OVER
            (
                PARTITION BY MEMBER_ID
                ORDER BY LOAD_TIMESTAMP DESC
            ) AS RN
        FROM BRONZE.MEMBERS_RAW
    )

    SELECT
        MEMBER_ID,
        BIO,
        CITY,
        COUNTRY,
        HOMETOWN,
        JOINED,
        LAT,
        LINK,
        LON,
        MEMBER_NAME,
        STATE,
        MEMBER_STATUS,
        VISITED,
        GROUP_ID
    FROM MEMBERS
    WHERE RN = 1
      AND MEMBER_ID IS NOT NULL
      AND GROUP_ID IS NOT NULL
) AS S

ON T.MEMBER_ID = S.MEMBER_ID

WHEN MATCHED
AND (
       COALESCE(T.BIO,'') <> COALESCE(S.BIO,'')
    OR COALESCE(T.CITY,'') <> COALESCE(S.CITY,'')
    OR COALESCE(T.COUNTRY,'') <> COALESCE(S.COUNTRY,'')
    OR COALESCE(T.HOMETOWN,'') <> COALESCE(S.HOMETOWN,'')
    OR COALESCE(T.LAT,-99999) <> COALESCE(S.LAT,-99999)
    OR COALESCE(T.LON,-99999) <> COALESCE(S.LON,-99999)
    OR COALESCE(T.LINK,'') <> COALESCE(S.LINK,'')
    OR COALESCE(T.MEMBER_NAME,'') <> COALESCE(S.MEMBER_NAME,'')
    OR COALESCE(T.STATE,'') <> COALESCE(S.STATE,'')
    OR COALESCE(T.MEMBER_STATUS,'') <> COALESCE(S.MEMBER_STATUS,'')
    OR COALESCE(T.GROUP_ID,-1) <> COALESCE(S.GROUP_ID,-1)
    OR COALESCE(T.JOINED,'1900-01-01'::TIMESTAMP_NTZ)
       <> COALESCE(S.JOINED,'1900-01-01'::TIMESTAMP_NTZ)
    OR COALESCE(T.VISITED,'1900-01-01'::TIMESTAMP_NTZ)
       <> COALESCE(S.VISITED,'1900-01-01'::TIMESTAMP_NTZ)
)

THEN UPDATE SET

    T.BIO = S.BIO,
    T.CITY = S.CITY,
    T.COUNTRY = S.COUNTRY,
    T.HOMETOWN = S.HOMETOWN,
    T.JOINED = S.JOINED,
    T.LAT = S.LAT,
    T.LINK = S.LINK,
    T.LON = S.LON,
    T.MEMBER_NAME = S.MEMBER_NAME,
    T.STATE = S.STATE,
    T.MEMBER_STATUS = S.MEMBER_STATUS,
    T.VISITED = S.VISITED,
    T.GROUP_ID = S.GROUP_ID,
    T.UPDATED_TIMESTAMP = CURRENT_TIMESTAMP(),
    T.PIPELINE_RUN_ID = '{pipeline_run_id}'

WHEN NOT MATCHED THEN

INSERT
(
    MEMBER_ID,
    BIO,
    CITY,
    COUNTRY,
    HOMETOWN,
    JOINED,
    LAT,
    LINK,
    LON,
    MEMBER_NAME,
    STATE,
    MEMBER_STATUS,
    VISITED,
    GROUP_ID,
    PIPELINE_RUN_ID
)

VALUES
(
    S.MEMBER_ID,
    S.BIO,
    S.CITY,
    S.COUNTRY,
    S.HOMETOWN,
    S.JOINED,
    S.LAT,
    S.LINK,
    S.LON,
    S.MEMBER_NAME,
    S.STATE,
    S.MEMBER_STATUS,
    S.VISITED,
    S.GROUP_ID,
    '{pipeline_run_id}'
);