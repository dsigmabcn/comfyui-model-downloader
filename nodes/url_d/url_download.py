from ..base_downloader import BaseModelDownloader, get_model_dirs
from ..download_utils import DownloadManager
import os
from urllib.parse import urlparse

class URLDownloader(BaseModelDownloader):
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {       
                "url": ("STRING", {"multiline": False, "default": "", "placeholder": "Enter download URL"}),
                "save_dir": (get_model_dirs(), {"default": "loras"}),
            },
            "hidden": {
                "node_id": "UNIQUE_ID"
            }
        }
        
    FUNCTION = "download"
    
    def get_filename_from_url(self, url):
        """Extract filename from URL"""
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        
        # If no filename in URL, use a default
        if not filename or '.' not in filename:
            filename = "downloaded_file"
            
        return filename
    
    def download(self, url, save_dir, node_id):
        print(f"Starting download from URL: {url}")
        self.node_id = node_id
        
        if not url.strip():
            raise Exception("URL cannot be empty")
            
        filename = self.get_filename_from_url(url)
        save_path = self.prepare_download_path(save_dir, filename)
        
        return self.handle_download(
            DownloadManager.download_with_progress,
            url=url,
            save_path=save_path,
            filename=filename,
            progress_callback=self
        )