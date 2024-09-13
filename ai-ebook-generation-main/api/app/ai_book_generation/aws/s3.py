import boto3

""" Class for S3 operations """


class S3:
    def __init__(self, bucket, region):
        self.s3 = boto3.client("s3")
        self.bucket = bucket
        self.region = region

    def try_permissions(self):
        # Attempt to get S3 buckets
        # This operation doesn't change any settings, but will fail if credentials are not available
        self.s3.list_buckets()

    def upload_file(self, file_path, s3_file_name) -> str:
        if " " in s3_file_name:
            raise ValueError("s3_file_name cannot contain spaces")
        with open(file_path, "rb") as data:
            self.s3.put_object(
                Bucket=self.bucket,
                Key=s3_file_name,
                Body=data,
                ContentType="application/pdf",
                Metadata={"Content-Disposition": "inline"},
            )
        file_url = self._get_file_url(self.bucket, s3_file_name)
        return file_url

    def _get_file_url(self, bucket_name, s3_file_name):
        file_url = f"https://{bucket_name}.s3.{self.region}.amazonaws.com/{s3_file_name}"
        return file_url
