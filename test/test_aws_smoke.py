import tempfile
from pathlib import Path

import boto3

from config.settings import settings


def print_header(title: str):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def get_s3_client():

    return boto3.client(
        "s3",
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        region_name=settings.aws_region
    )


def test_bucket_exists(s3):

    print_header("1. VALIDANDO BUCKET")

    s3.head_bucket(
        Bucket=settings.s3_bucket_name
    )

    print(
        f"✅ Bucket encontrado: {settings.s3_bucket_name}"
    )


def test_create_folder_structure(s3):

    print_header("2. CREANDO ESTRUCTURA DEL DATA LAKE")

    folders = [
        "raw/meetup/initial/",
        "raw/meetup/incremental/",
        "exports/gold/",
        "control/"
    ]

    for folder in folders:

        s3.put_object(
            Bucket=settings.s3_bucket_name,
            Key=folder
        )

        print(f"✅ {folder}")

    print("✅ Estructura creada")


def test_upload_text_file(s3):

    print_header("3. SUBIENDO ARCHIVO DE PRUEBA")

    s3.put_object(
        Bucket=settings.s3_bucket_name,
        Key="control/test.txt",
        Body="AWS connection successful"
    )

    print("✅ Archivo cargado")


def test_download_text_file(s3):

    print_header("4. DESCARGANDO ARCHIVO DE PRUEBA")

    response = s3.get_object(
        Bucket=settings.s3_bucket_name,
        Key="control/test.txt"
    )

    content = (
        response["Body"]
        .read()
        .decode()
    )

    print(f"✅ Contenido: {content}")


def test_upload_csv(s3):

    print_header("5. SUBIENDO CSV DE PRUEBA")

    csv_content = (
        "id,name\n"
        "1,Jorge\n"
        "2,Copilot\n"
    )

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".csv",
        delete=False
    ) as temp_file:

        temp_file.write(csv_content)

        temp_path = temp_file.name

    s3.upload_file(
        temp_path,
        settings.s3_bucket_name,
        "raw/meetup/initial/sample.csv"
    )

    Path(temp_path).unlink()

    print("✅ CSV cargado")


def test_file_metadata(s3):

    print_header("6. LEYENDO METADATA DEL CSV")

    response = s3.head_object(
        Bucket=settings.s3_bucket_name,
        Key="raw/meetup/initial/sample.csv"
    )

    print(
        f"✅ Tamaño archivo: "
        f"{response['ContentLength']} bytes"
    )


def test_list_files(s3):

    print_header(
        "7. LISTANDO ARCHIVOS EN raw/meetup/initial/"
    )

    response = s3.list_objects_v2(
        Bucket=settings.s3_bucket_name,
        Prefix="raw/meetup/initial/"
    )

    for obj in response.get("Contents", []):

        print(
            f"✅ {obj['Key']}"
        )


def test_initial_load_marker(s3):

    print_header(
        "8. CREANDO MARCADOR INITIAL LOAD"
    )

    marker = "control/_INITIAL_LOAD_COMPLETE"

    s3.put_object(
        Bucket=settings.s3_bucket_name,
        Key=marker,
        Body="OK"
    )

    s3.head_object(
        Bucket=settings.s3_bucket_name,
        Key=marker
    )

    print(
        f"✅ Marcador creado: {marker}"
    )


def test_list_bucket(s3):

    print_header(
        "9. RESUMEN ESTRUCTURA DEL BUCKET"
    )

    response = s3.list_objects_v2(
        Bucket=settings.s3_bucket_name
    )

    for obj in response.get("Contents", []):

        print(obj["Key"])


def main():

    print(
        f"\nBucket: {settings.s3_bucket_name}"
    )

    s3 = get_s3_client()

    test_bucket_exists(s3)

    test_create_folder_structure(s3)

    test_upload_text_file(s3)

    test_download_text_file(s3)

    test_upload_csv(s3)

    test_file_metadata(s3)

    test_list_files(s3)

    test_initial_load_marker(s3)

    test_list_bucket(s3)

    print_header("RESULTADO FINAL")

    print("✅ AWS listo para el proyecto Meetup")


if __name__ == "__main__":

    main()