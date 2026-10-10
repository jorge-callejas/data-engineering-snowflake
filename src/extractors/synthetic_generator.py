import uuid
import random
from pathlib import Path
from datetime import datetime, timedelta

import boto3
import pandas as pd

from config.settings import settings
from src.utils.snowflake_client import SnowflakeClient


class SyntheticGenerator:

    NEW_EVENTS = 20
    UPDATE_EVENTS = 100

    EVENT_COLUMNS = [
        "EVENT_ID",
        "CREATED",
        "DESCRIPTION",
        "DURATION",
        "EVENT_URL",
        "FEE_ACCEPTS",
        "FEE_AMOUNT",
        "FEE_CURRENCY",
        "FEE_DESCRIPTION",
        "FEE_LABEL",
        "FEE_REQUIRED",
        "GROUP_CREATED",
        "GROUP_GROUP_LAT",
        "GROUP_GROUP_LON",
        "GROUP_ID",
        "GROUP_JOIN_MODE",
        "GROUP_NAME",
        "GROUP_URLNAME",
        "GROUP_WHO",
        "HEADCOUNT",
        "HOW_TO_FIND_US",
        "MAYBE_RSVP_COUNT",
        "EVENT_NAME",
        "PHOTO_URL",
        "RATING_AVERAGE",
        "RATING_COUNT",
        "RSVP_LIMIT",
        "EVENT_STATUS",
        "EVENT_TIME",
        "UPDATED",
        "UTC_OFFSET",
        "VENUE_ADDRESS_1",
        "VENUE_ADDRESS_2",
        "VENUE_CITY",
        "VENUE_COUNTRY",
        "VENUE_ID",
        "VENUE_LAT",
        "VENUE_LOCALIZED_COUNTRY_NAME",
        "VENUE_LON",
        "VENUE_NAME",
        "VENUE_PHONE",
        "VENUE_REPINNED",
        "VENUE_STATE",
        "VENUE_ZIP",
        "VISIBILITY",
        "WAITLIST_COUNT",
        "WHY",
        "YES_RSVP_COUNT"
    ]

    def __init__(self):

        self.snowflake = SnowflakeClient()

        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region
        )

    def load_events(self):

        query = """
        SELECT

            EVENT_ID,
            CREATED,
            DESCRIPTION,
            DURATION,

            EVENT_URL,

            FEE_ACCEPTS,
            FEE_AMOUNT,
            FEE_CURRENCY,
            FEE_DESCRIPTION,
            FEE_LABEL,
            FEE_REQUIRED,

            GROUP_CREATED,
            GROUP_GROUP_LAT,
            GROUP_GROUP_LON,

            GROUP_ID,
            GROUP_JOIN_MODE,
            GROUP_NAME,
            GROUP_URLNAME,
            GROUP_WHO,

            HEADCOUNT,
            HOW_TO_FIND_US,

            MAYBE_RSVP_COUNT,

            EVENT_NAME,

            PHOTO_URL,

            RATING_AVERAGE,
            RATING_COUNT,

            RSVP_LIMIT,

            EVENT_STATUS,

            EVENT_TIME,

            UPDATED,

            UTC_OFFSET,

            VENUE_ADDRESS_1,
            VENUE_ADDRESS_2,
            VENUE_CITY,
            VENUE_COUNTRY,
            VENUE_ID,
            VENUE_LAT,
            VENUE_LOCALIZED_COUNTRY_NAME,
            VENUE_LON,
            VENUE_NAME,
            VENUE_PHONE,
            VENUE_REPINNED,
            VENUE_STATE,
            VENUE_ZIP,

            VISIBILITY,

            WAITLIST_COUNT,

            WHY,

            YES_RSVP_COUNT

        FROM SILVER.EVENTS_SILVER
        """

        result = self.snowflake.execute(query)

        return pd.DataFrame(
            result,
            columns=self.EVENT_COLUMNS
        )

    def generate_updates(
        self,
        events_df: pd.DataFrame
    ):

        updates = events_df.sample(
            min(
                self.UPDATE_EVENTS,
                len(events_df)
            )
        ).copy()

        updates["YES_RSVP_COUNT"] = (
            updates["YES_RSVP_COUNT"]
            .fillna(0)
            .astype(int)
            + [
                random.randint(1, 25)
                for _ in range(len(updates))
            ]
        )

        updates["MAYBE_RSVP_COUNT"] = (
            updates["MAYBE_RSVP_COUNT"]
            .fillna(0)
            .astype(int)
            + [
                random.randint(0, 10)
                for _ in range(len(updates))
            ]
        )

        updates["WAITLIST_COUNT"] = (
            updates["WAITLIST_COUNT"]
            .fillna(0)
            .astype(int)
            + [
                random.randint(0, 5)
                for _ in range(len(updates))
            ]
        )

        updates["HEADCOUNT"] = (
            updates["YES_RSVP_COUNT"]
            +
            updates["MAYBE_RSVP_COUNT"]
        )

        updates["UPDATED"] = datetime.utcnow()

        return updates

    def generate_new_events(
        self,
        events_df: pd.DataFrame
    ):

        templates = events_df.sample(
            min(
                self.NEW_EVENTS,
                len(events_df)
            )
        ).copy()

        rows = []

        for _, row in templates.iterrows():

            record = row.to_dict()

            record["EVENT_ID"] = str(
                uuid.uuid4()
            )

            record["EVENT_NAME"] = (
                f"Generated Meetup Event "
                f"{random.randint(1000,9999)}"
            )

            record["EVENT_TIME"] = (
                datetime.utcnow()
                + timedelta(
                    days=random.randint(
                        1,
                        30
                    )
                )
            )

            record["CREATED"] = datetime.utcnow()

            record["UPDATED"] = datetime.utcnow()

            record["YES_RSVP_COUNT"] = random.randint(
                10,
                150
            )

            record["MAYBE_RSVP_COUNT"] = random.randint(
                0,
                50
            )

            record["WAITLIST_COUNT"] = random.randint(
                0,
                20
            )

            record["HEADCOUNT"] = (
                record["YES_RSVP_COUNT"]
                +
                record["MAYBE_RSVP_COUNT"]
            )

            rows.append(
                record
            )

        return pd.DataFrame(
            rows
        )

    def save_file(
        self,
        incremental_df: pd.DataFrame
    ):

        Path(
            "tmp"
        ).mkdir(
            exist_ok=True
        )

        file_name = (
            f"events_incremental_"
            f"{datetime.utcnow():%Y%m%d_%H%M%S}.csv"
        )

        local_file = (
            f"tmp/{file_name}"
        )

        incremental_df = incremental_df[
            self.EVENT_COLUMNS
        ]

        incremental_df.to_csv(
            local_file,
            index=False
        )

        return (
            local_file,
            file_name
        )

    def upload_to_s3(
        self,
        local_file,
        file_name
    ):

        s3_key = (
            "raw/meetup/incremental/events/"
            f"{file_name}"
        )

        self.s3.upload_file(
            local_file,
            settings.s3_bucket_name,
            s3_key
        )

        return s3_key

    def run(self):

        events_df = self.load_events()

        updates = self.generate_updates(
            events_df
        )

        new_events = self.generate_new_events(
            events_df
        )

        #temporal
        datetime_columns = [
            "CREATED",
            "GROUP_CREATED",
            "EVENT_TIME",
            "UPDATED"
        ]

        for col in datetime_columns:

            updates[col] = pd.to_datetime(
                updates[col]
            ).astype(
                "datetime64[ns]"
            )

            new_events[col] = pd.to_datetime(
                new_events[col]
            ).astype(
                "datetime64[ns]"
            )


        incremental_df = pd.concat(
            [
                updates,
                new_events
            ],
            ignore_index=True
        )

        local_file, file_name = self.save_file(
            incremental_df
        )

        s3_key = self.upload_to_s3(
            local_file,
            file_name
        )

        print(
            f"Generated "
            f"{len(incremental_df)} records"
        )

        print(
            f"Uploaded to s3://"
            f"{settings.s3_bucket_name}/"
            f"{s3_key}"
        )

        return {
            "records": len(
                incremental_df
            ),
            "s3_key": s3_key
        }