USE DATABASE MEETUP_DB;

CREATE SCHEMA IF NOT EXISTS GOLD;

USE SCHEMA GOLD;

-- =====================================================
-- DIM_CITY
-- =====================================================

CREATE TABLE IF NOT EXISTS DIM_CITY
(
    CITY_KEY NUMBER AUTOINCREMENT,

    CITY_ID NUMBER,
    CITY VARCHAR,
    COUNTRY VARCHAR,
    STATE VARCHAR,
    ZIP VARCHAR,

    LOAD_TIMESTAMP TIMESTAMP_NTZ
        DEFAULT CURRENT_TIMESTAMP()
);

-- =====================================================
-- DIM_GROUP
-- =====================================================

CREATE TABLE IF NOT EXISTS DIM_GROUP
(
    GROUP_KEY NUMBER AUTOINCREMENT,

    GROUP_ID NUMBER,
    GROUP_NAME VARCHAR,

    CATEGORY_ID NUMBER,
    CATEGORY_NAME VARCHAR,

    CITY_ID NUMBER,

    MEMBERS NUMBER,
    RATING FLOAT,

    LOAD_TIMESTAMP TIMESTAMP_NTZ
        DEFAULT CURRENT_TIMESTAMP()
);

-- =====================================================
-- DIM_VENUE
-- =====================================================

CREATE TABLE IF NOT EXISTS DIM_VENUE
(
    VENUE_KEY NUMBER AUTOINCREMENT,

    VENUE_ID NUMBER,
    VENUE_NAME VARCHAR,

    CITY VARCHAR,
    COUNTRY VARCHAR,
    STATE VARCHAR,

    LOAD_TIMESTAMP TIMESTAMP_NTZ
        DEFAULT CURRENT_TIMESTAMP()
);

-- =====================================================
-- DIM_DATE
-- =====================================================

CREATE TABLE IF NOT EXISTS DIM_DATE
(
    DATE_KEY NUMBER,

    FULL_DATE DATE,

    YEAR NUMBER,
    QUARTER NUMBER,
    MONTH NUMBER,
    MONTH_NAME VARCHAR(20),

    DAY NUMBER,

    DAY_OF_WEEK NUMBER,
    DAY_NAME VARCHAR(20),

    LOAD_TIMESTAMP TIMESTAMP_NTZ
        DEFAULT CURRENT_TIMESTAMP()
);
-- =====================================================
-- FACT_EVENTS
-- =====================================================

CREATE TABLE IF NOT EXISTS FACT_EVENTS
(
    EVENT_ID VARCHAR,

    DATE_KEY NUMBER,

    GROUP_KEY NUMBER,

    VENUE_KEY NUMBER,

    YES_RSVP_COUNT NUMBER,
    MAYBE_RSVP_COUNT NUMBER,
    WAITLIST_COUNT NUMBER,
    HEADCOUNT NUMBER,

    RATING_AVERAGE FLOAT,

    LOAD_TIMESTAMP TIMESTAMP_NTZ
        DEFAULT CURRENT_TIMESTAMP()
);