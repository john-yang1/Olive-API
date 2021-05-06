import os

import threading
import requests
import boto3

s3_bucket_name = os.getenv('DJANGO_AWS_S3_BUCKET')
access_key_id = os.getenv('DJANG0_AWS_ACCESS_KEY')
secret_access_key = os.getenv('DJANG0_AWS_SECRET_ACCESS_KEY')
region = os.getenv('DJANGO_AWS_REGION')
aws_app = "s3"


def process_urls_from_input():
    try:
        print("Starting URL download..")
        urls = get_url_list_from_input_file()
        s3 = create_s3_connection()
        threads = []
        for url in urls:
            x = threading.Thread(
                target=write_url_contents_to_firebase, args=(url, s3))
            x.start()
            threads.append(x)
        for thread in threads:
            thread.join()
        print("Finished URL downloads.")
    except Exception as e:
        print(e)


def get_url_list_from_input_file():
    try:
        with open("scripts/input.txt") as f:
            urls = f.readlines()
        f.close()
        urls = [url.strip() for url in urls]
        print("Created list of URLs..")
        return urls
    except Exception as e:
        print("Exception occurred while obtaining urls: " + e)


def create_s3_connection():
    try:
        s3 = boto3.resource(aws_app, region_name=region,
                            aws_access_key_id=access_key_id,
                            aws_secret_access_key=secret_access_key)
        print("Connected to S3..")
        return s3
    except Exception as e:
        print("Exception occurred while trying to connect to the AWS S3 bucket: " + e)


def write_url_contents_to_firebase(url, s3):
    try:
        r = requests.get(url, verify=False)
        s3.Object(s3_bucket_name,
                  f"{'__'.join(url.split('/')[2:])}.html").put(Body=r.text)
        print(f"Saved {url} to S3..")
    except Exception as e:
        print("Exception occurred while writing to firebase: " + e)


if __name__ == "__main__":
    process_urls_from_input()
