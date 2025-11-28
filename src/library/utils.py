from pathlib import Path
from slugify import slugify
import yaml
import json

class Utils:
    @staticmethod
    def get_repo_dir():
        return Path(__file__).resolve().parents[2]

    @staticmethod
    def get_challenges_dir():
        return Utils.get_repo_dir().joinpath('challenges')
    
    @staticmethod
    def get_pages_dir():
        return Utils.get_repo_dir().joinpath('pages')
    
    @staticmethod
    def get_challenge_dir(category: str, slug: str):        
        return Utils.get_challenges_dir().joinpath(Utils.slugify(category) or "").joinpath(slug)

    @staticmethod
    def get_page_dir(page: str):
        return Utils.get_pages_dir().joinpath(Utils.slugify(page) or "")

    @staticmethod
    def get_challenge_dir_str(category: str, slug: str):
        return f"challenges/{Utils.slugify(category)}/{slug}"
    
    @staticmethod
    def get_page_dir_str(page: str):
        return f"pages/{Utils.slugify(page)}"
    
    @staticmethod
    def get_k8s_dir(category: str, slug: str):
        return Utils.get_challenge_dir(category, slug).joinpath('k8s')
    
    @staticmethod
    def get_k8s_page_dir(page: str):
        return Utils.get_page_dir(page).joinpath('k8s')
    
    @staticmethod
    def get_challenge_render_dir(category: str, slug: str):
        return Utils.get_k8s_dir(category, slug).joinpath('challenge')
    
    @staticmethod
    def get_configmap_dir(category: str, slug: str):
        return Utils.get_k8s_dir(category, slug).joinpath('config')
    
    @staticmethod
    def get_template_dir():
        return Utils.get_repo_dir().joinpath('template')
        
    @staticmethod
    def slugify(text):
        if (text == None):
            return None
        
        return slugify(text.strip()).strip('-').strip('_').strip('.')
    
    @staticmethod
    def validate_length(text, min_length, max_length, identifier):
        if text == None:
            print(f"{identifier.capitalize()} must be provided.")
            return False
        
        if len(text) < min_length:
            print(f"{identifier.capitalize()} must be at least {min_length} characters long.")
            return False
        
        if len(text) > max_length:
            print(f"{identifier.capitalize()} cannot be longer than {max_length} characters.")
            return False
        
        return True
    
    @staticmethod
    def load_yaml(file):
        with open(file, 'r') as f:
            return yaml.safe_load(f)
    
    @staticmethod
    def load_json(file):
        with open(file, 'r') as f:
            return json.load(f)
