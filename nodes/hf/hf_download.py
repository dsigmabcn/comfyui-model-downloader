import os
import requests
import huggingface_hub

from ..base_downloader import BaseModelDownloader, get_model_dirs
from ..download_utils import DownloadManager

class HFDownloader(BaseModelDownloader):     
    @classmethod
    def INPUT_TYPES(cls):
        # Read the environment variable, defaulting to an empty string if it's not set
        default_token = os.environ.get("HF_TOKEN", "")
        return {
            "required": {      
                "repo_id": ("STRING", {"multiline": False, "default": "runwayml/stable-diffusion-v1-5"}),
                "filename": ("STRING", {"multiline": False, "default": "v1-5-pruned-emaonly.ckpt"}),
                "local_path": (get_model_dirs(),),
            },
            "optional": {
                "hf_token": ("STRING", {
                    "multiline": False,
                    "default": default_token, 
                    "password": True
                }),
                "overwrite": ("BOOLEAN", {"default": True}),
                "local_path_override": ("STRING", {"default": ""}),
            },
            "hidden": {
                "node_id": "UNIQUE_ID"
            }
        }
        
    FUNCTION = "download"

    def download(self, repo_id, filename, local_path, hf_token, node_id, overwrite=False, local_path_override=""):
        if not repo_id or not filename:
            print(f"Missing required values: repo_id='{repo_id}', filename='{filename}'")
            return {}
        
        final_path = local_path_override if local_path_override else local_path
        
        self.node_id = node_id
        save_path = self.prepare_download_path(final_path, filename)

        if hf_token:
            print(f'Authenticated download from Hugging Face for model {repo_id}/{filename}')
            try:
                # Use huggingface_hub for authenticated downloads
                huggingface_hub.hf_hub_download(
                    repo_id=repo_id,
                    filename=filename,
                    cache_dir=save_path, # Note: hf_hub_download caches differently, this is a simplified path
                    token=hf_token,
                    force_download=overwrite,
                    local_dir_use_symlinks="auto"
                )
                print(f"Successfully downloaded {filename} to {save_path}")
                return {"model": os.path.join(save_path, filename)}
            except Exception as e:
                print(f"Error downloading with Hugging Face token: {str(e)}")
                raise e
        else:
            print(f'Downloading model {repo_id}/{filename} to {final_path}')
            url = f"https://huggingface.co/{repo_id}/resolve/main/{filename}"
            
            return self.handle_download(
                DownloadManager.download_with_progress,
                save_path=save_path,
                filename=filename,
                overwrite=overwrite,
                url=url,
                progress_callback=self
            )
    

class HFAuthDownloader(HFDownloader): # Inherit from HFDownloader to share methods
    def __init__(self):
        super().__init__()
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "repo_id": ("STRING", {"default": "runwayml/stable-diffusion-v1-5"}),
                "filename": ("STRING", {"default": "v1-5-pruned.ckpt"}),
                "local_path": (get_model_dirs(),),
                "hf_token": ("STRING", {
                    "default": "", 
                    "multiline": False, 
                    "password": True
                }),
                "overwrite": ("BOOLEAN", {"default": False}),
            }
        }

    def download_model(self, repo_id, filename, local_path, hf_token, overwrite):
        print(f'downloading model {repo_id} {filename} {local_path} {overwrite}')
        try:
            # Always use token for auth version
            #import huggingface_hub
            huggingface_hub.login(token=hf_token)
            
            result = self.download(
                repo_id=repo_id,
                filename=filename,
                local_path=local_path,
                node_id=self.node_id,
                overwrite=overwrite,
                hf_token=hf_token
            )
            return {}
        except Exception as e:
            print(f"Error in HF Auth Downloader: {str(e)}")
            raise e
