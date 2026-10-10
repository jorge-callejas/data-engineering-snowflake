USE DATABASE MEETUP_DB;
USE SCHEMA SILVER;

-- =====================================================
-- QUARANTINE
-- =====================================================

INSERT INTO QUARANTINE.TOPICS_QUARANTINE
(
    TOPIC_ID,
    DESCRIPTION,
    LINK,
    MEMBERS,
    TOPIC_NAME,
    URLKEY,
    MAIN_TOPIC_ID,
    REJECTION_REASON,
    PIPELINE_RUN_ID
)
SELECT
    TOPIC_ID,
    DESCRIPTION,
    LINK,
    MEMBERS,
    TOPIC_NAME,
    URLKEY,
    MAIN_TOPIC_ID,
    'TOPIC_ID_IS_NULL',
    '{pipeline_run_id}'
FROM BRONZE.TOPICS_RAW
WHERE TOPIC_ID IS NULL;

-- =====================================================
-- DEDUPLICATION
-- =====================================================



-- =====================================================
-- MERGE
-- =====================================================

MERGE INTO SILVER.TOPICS_SILVER AS T

USING
(
    WITH TOPICS AS
    (
        SELECT
            TOPIC_ID,
            DESCRIPTION,
            LINK,
            MEMBERS,
            TOPIC_NAME,
            URLKEY,
            MAIN_TOPIC_ID,
            ROW_NUMBER() OVER
            (
                PARTITION BY TOPIC_ID
                ORDER BY TOPIC_ID
            ) AS RN
        FROM BRONZE.TOPICS_RAW
    )
    SELECT
        TOPIC_ID,
        DESCRIPTION,
        LINK,
        MEMBERS,
        TOPIC_NAME,
        URLKEY,
        MAIN_TOPIC_ID
    FROM TOPICS
    WHERE RN = 1
      AND TOPIC_ID IS NOT NULL
) AS S

ON T.TOPIC_ID = S.TOPIC_ID

WHEN MATCHED
AND (
       COALESCE(T.DESCRIPTION,'') <> COALESCE(S.DESCRIPTION,'')
    OR COALESCE(T.LINK,'') <> COALESCE(S.LINK,'')
    OR COALESCE(T.MEMBERS,-1) <> COALESCE(S.MEMBERS,-1)
    OR COALESCE(T.TOPIC_NAME,'') <> COALESCE(S.TOPIC_NAME,'')
    OR COALESCE(T.URLKEY,'') <> COALESCE(S.URLKEY,'')
    OR COALESCE(T.MAIN_TOPIC_ID,-1) <> COALESCE(S.MAIN_TOPIC_ID,-1)
)

THEN UPDATE SET

    T.DESCRIPTION = S.DESCRIPTION,
    T.LINK = S.LINK,
    T.MEMBERS = S.MEMBERS,
    T.TOPIC_NAME = S.TOPIC_NAME,
    T.URLKEY = S.URLKEY,
    T.MAIN_TOPIC_ID = S.MAIN_TOPIC_ID,
    T.UPDATED_TIMESTAMP = CURRENT_TIMESTAMP(),
    T.PIPELINE_RUN_ID = '{pipeline_run_id}'

WHEN NOT MATCHED THEN

INSERT
(
    TOPIC_ID,
    DESCRIPTION,
    LINK,
    MEMBERS,
    TOPIC_NAME,
    URLKEY,
    MAIN_TOPIC_ID,
    PIPELINE_RUN_ID
)

VALUES
(
    S.TOPIC_ID,
    S.DESCRIPTION,
    S.LINK,
    S.MEMBERS,
    S.TOPIC_NAME,
    S.URLKEY,
    S.MAIN_TOPIC_ID,
    '{pipeline_run_id}'
);