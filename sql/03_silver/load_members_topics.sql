USE DATABASE MEETUP_DB;
USE SCHEMA SILVER;

-- =====================================================
-- QUARANTINE
-- =====================================================

INSERT INTO QUARANTINE.MEMBERS_TOPICS_QUARANTINE
(
    TOPIC_ID,
    TOPIC_KEY,
    TOPIC_NAME,
    MEMBER_ID,
    REJECTION_REASON,
    PIPELINE_RUN_ID
)
SELECT
    TOPIC_ID,
    TOPIC_KEY,
    TOPIC_NAME,
    MEMBER_ID,
    CASE
        WHEN TOPIC_ID IS NULL THEN 'TOPIC_ID_IS_NULL'
        WHEN MEMBER_ID IS NULL THEN 'MEMBER_ID_IS_NULL'
    END,
    '{pipeline_run_id}'
FROM BRONZE.MEMBERS_TOPICS_RAW
WHERE TOPIC_ID IS NULL
   OR MEMBER_ID IS NULL;

-- =====================================================
-- DEDUPLICATION
-- =====================================================

-- =====================================================
-- MERGE
-- =====================================================

MERGE INTO SILVER.MEMBERS_TOPICS_SILVER AS T

USING
(   
    WITH MEMBERS_TOPICS AS
    (
        SELECT
            TOPIC_ID,
            TOPIC_KEY,
            TOPIC_NAME,
            MEMBER_ID,
            ROW_NUMBER() OVER
            (
                PARTITION BY MEMBER_ID, TOPIC_ID
                ORDER BY LOAD_TIMESTAMP DESC
            ) AS RN
        FROM BRONZE.MEMBERS_TOPICS_RAW
    )
    SELECT
        TOPIC_ID,
        TOPIC_KEY,
        TOPIC_NAME,
        MEMBER_ID
    FROM MEMBERS_TOPICS
    WHERE RN = 1
      AND TOPIC_ID IS NOT NULL
      AND MEMBER_ID IS NOT NULL
) AS S

ON T.MEMBER_ID = S.MEMBER_ID
AND T.TOPIC_ID = S.TOPIC_ID

WHEN MATCHED
AND (
       COALESCE(T.TOPIC_KEY,'') <> COALESCE(S.TOPIC_KEY,'')
    OR COALESCE(T.TOPIC_NAME,'') <> COALESCE(S.TOPIC_NAME,'')
)

THEN UPDATE SET

    T.TOPIC_KEY = S.TOPIC_KEY,
    T.TOPIC_NAME = S.TOPIC_NAME,
    T.UPDATED_TIMESTAMP = CURRENT_TIMESTAMP(),
    T.PIPELINE_RUN_ID = '{pipeline_run_id}'

WHEN NOT MATCHED THEN

INSERT
(
    TOPIC_ID,
    TOPIC_KEY,
    TOPIC_NAME,
    MEMBER_ID,
    PIPELINE_RUN_ID
)

VALUES
(
    S.TOPIC_ID,
    S.TOPIC_KEY,
    S.TOPIC_NAME,
    S.MEMBER_ID,
    '{pipeline_run_id}'
);