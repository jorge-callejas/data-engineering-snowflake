import os
import boto3

from kaggle.api.kaggle_api_extended import KaggleApi

from config.settings import settings
from src.utils.slack_client import SlackClient


EXPECTED_FILES = {
    "categories.csv",
    "cities.csv",
    "events.csv",
    "groups.csv",
    "groups_topics.csv",
    "members.csv",
    "members_topics.csv",
    "topics.csv",
    "venues.csv"
}


def init_kaggle_api() -> KaggleApi:
    """
    Inicializa la API de Kaggle con credenciales dinámicas.
    """

    os.environ["KAGGLE_USERNAME"] = settings.kaggle_username
    os.environ["KAGGLE_KEY"] = settings.kaggle_key

    api = KaggleApi()

    api.authenticate()

    return api


def get_s3_client():

    return boto3.client(
        "s3",
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        region_name=settings.aws_region
    )


def initial_load_already_executed() -> bool:

    s3_client = get_s3_client()

    try:

        s3_client.head_object(
            Bucket=settings.s3_bucket_name,
            Key=settings.s3_initial_marker
        )

        return True

    except Exception:

        return False


def download_from_kaggle(
    dataset_handle: str,
    target_dir: str
):
    """
    Descarga y descomprime los archivos del dataset de Kaggle.
    """

    api = init_kaggle_api()

    os.makedirs(target_dir, exist_ok=True)

    print(
        f"[Kaggle Extractor] Descargando dataset "
        f"'{dataset_handle}' en '{target_dir}'..."
    )

    api.dataset_download_files(
        dataset_handle,
        path=target_dir,
        unzip=True
    )

    print(
        "[Kaggle Extractor] Descarga y descompresión completadas."
    )


def validate_downloaded_files(local_dir: str):

    found_files = {
        file
        for file in os.listdir(local_dir)
        if file.endswith(".csv")
    }

    missing_files = EXPECTED_FILES - found_files

    if missing_files:

        raise RuntimeError(
            f"Archivos faltantes: {missing_files}"
        )

    print(
        f"[Validator] "
        f"{len(found_files)} archivos CSV validados."
    )


def upload_directory_to_s3(
    local_dir: str,
    bucket: str,
    s3_prefix: str
) -> list[str]:
    """
    Sube todos los archivos de un directorio local a S3.
    """

    uploaded_files = []

    s3_client = get_s3_client()

    for root, _, files in os.walk(local_dir):

        for file in files:

            local_path = os.path.join(
                root,
                file
            )

            relative_path = (
                os.path.relpath(
                    local_path,
                    local_dir
                )
                .replace("\\", "/")
            )

            s3_key = (
                os.path.join(
                    s3_prefix,
                    relative_path
                )
                .replace("\\", "/")
            )

            print(
                f"[S3 Uploader] "
                f"Subiendo {local_path} "
                f"-> s3://{bucket}/{s3_key}"
            )

            s3_client.upload_file(
                local_path,
                bucket,
                s3_key
            )

            uploaded_files.append(
                s3_key
            )

    return uploaded_files


def create_s3_initial_marker(
    bucket: str,
    marker_key: str
):
    """
    Crea archivo marcador de carga inicial.
    """

    s3_client = get_s3_client()

    s3_client.put_object(
        Bucket=bucket,
        Key=marker_key,
        Body=b"INITIAL_LOAD_SUCCESSFUL",
    )

    print(
        f"[S3 Uploader] Marcador creado "
        f"en s3://{bucket}/{marker_key}"
    )


def notify_success(
    uploaded_files: list[str]
):

    SlackClient().send_message(
        f"""
    Initial Meetup Load Completed

Files Uploaded: {len(uploaded_files)}

Bucket:
{settings.s3_bucket_name}

Prefix:
{settings.s3_raw_prefix}

Status:
SUCCESS
"""
    )


def run_kaggle_initial_extraction():

    if initial_load_already_executed():

        print(
            "[Initial Load] "
            "Carga inicial ya ejecutada."
        )

        return []

    download_from_kaggle(
        settings.kaggle_dataset_handle,
        settings.local_tmp_dir
    )

    validate_downloaded_files(
        settings.local_tmp_dir
    )

    uploaded_files = (
        upload_directory_to_s3(
            settings.local_tmp_dir,
            settings.s3_bucket_name,
            settings.s3_raw_prefix
        )
    )

    create_s3_initial_marker(
        settings.s3_bucket_name,
        settings.s3_initial_marker
    )

    notify_success(
        uploaded_files
    )

    print(
        f"[Initial Load] "
        f"Proceso completado. "
        f"Archivos cargados: "
        f"{len(uploaded_files)}"
    )

    return uploaded_files


if __name__ == "__main__":

    run_kaggle_initial_extraction()