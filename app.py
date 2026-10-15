import os
import boto3
from flask import Flask

app = Flask(__name__)

# Nom de ton compartiment S3 défini dans le projet
BUCKET_NAME = "creativeflow-docs-davy"

s3_client = boto3.client("s3")


@app.route("/")
def home():
  try:
    # Récupération de la liste des dossiers/fichiers dans le compartiment S3
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
    contents = response.get("Contents", [])
    files = [item["Key"] for item in contents]

    html = f"""
        <h1>Bienvenue sur CreativeFlow 🚀</h1>
        <p>Connexion réussie au compartiment S3 : <b>{BUCKET_NAME}</b></p>
        <h3>Fichiers et dossiers actuels dans S3 :</h3>
        <ul>
        """
    for file in files:
      html += f"<li>{file}</li>"
    html += "</ul>"
    return html
  except Exception as e:
    return (
        f"<h1>Erreur de connexion S3</h1><p>{str(e)}</p>"
        "<p>Vérifie que le rôle IAM EC2-Developer-Role est bien attaché à"
        " l'instance.</p>"
    )


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)
