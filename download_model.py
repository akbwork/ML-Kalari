import os
from dotenv import load_dotenv
from huggingface_hub import snapshot_download


load_dotenv()

class DownloadModel:
    def __init__(self):
        self.local_dir = os.getenv("MODEL_STORE")
        self.model_names = os.getenv("MODEL_NAMES")
        raw_token = os.getenv("HF_TOKEN")
        self.hf_token = raw_token.strip() if raw_token and raw_token.strip() else None



        if not self.local_dir:
            raise ValueError("Environment variable MODEL_STORE is not set.")
        if not self.model_names:
            raise ValueError("Environment variable MODEL_NAMES is not set.")
        if self.hf_token:
            print("HF_TOKEN found — will authenticate with Hugging Face.")
        else:
            print("No HF_TOKEN found — proceeding without authentication (gated models will fail).")
            os.environ.pop("HF_TOKEN", None)

    def run_download(self):
        # Support one or multiple comma-separated model names
        model_list = [name.strip() for name in self.model_names.split(",") if name.strip()]

        for model_repo in model_list:
            target_dir = os.path.join(self.local_dir, model_repo.replace("/", "_"))
            print(f"Downloading {model_repo} -> {target_dir}")

            snapshot_download(
                repo_id=model_repo,
                local_dir=target_dir,
                token=self.hf_token
            )

            print(f"Finished downloading {model_repo}")


if __name__ == "__main__":
    downloader = DownloadModel()
    downloader.run_download()