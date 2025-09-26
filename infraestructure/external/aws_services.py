import boto3
import os
from dotenv import load_dotenv

load_dotenv()

class S3Client:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION"),
        )
        self.bucket = os.getenv("AWS_BUCKET_NAME")

    def upload_file(self, file: bytes, file_name: str) -> str:
        print(f"☁️ S3: Subiendo archivo {file_name} al bucket {self.bucket}")
        try:
            # Determinar ContentType basado en la extensión
            content_type = "application/pdf" if file_name.lower().endswith('.pdf') else "application/octet-stream"
            
            self.s3.put_object(
                Bucket=self.bucket,
                Key=file_name,
                Body=file,
                ContentType=content_type,
                ContentDisposition=f'inline; filename="{file_name.split("/")[-1]}"'  # Para visualización en el navegador
            )
            
            # Construcción de URL pública (si el bucket es público o tienes CloudFront)
            public_url = f"https://{self.bucket}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{file_name}"
            print(f"S3: Archivo subido - URL: {public_url}")
            return public_url
            
        except Exception as e:
            print(f"S3: Error al subir archivo: {str(e)}")
            raise e
