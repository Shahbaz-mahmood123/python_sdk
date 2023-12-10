import os
from client.nextflow_tower_api_client import AuthenticatedClient
from client.nextflow_tower_api_client.api.default import list_compute_envs, describe_compute_env
from client.nextflow_tower_api_client.models.list_compute_envs_response import ListComputeEnvsResponse
# from core.client import AuthenticatedPlatformClient

class SeqeraComputeEnvsWrapperInterface:
    def list_compute_envs(self, workspace_id: int, status: str) -> list:
        pass

    def get_compute_env_id(self, compute_env_list: list) -> list:
        pass
    
    def get_compute_env(self, workspace_id: int, compute_env_id: str) -> dict:
        pass 

class SeqeraComputeEnvsWrapper(SeqeraComputeEnvsWrapperInterface):
    def __init__(self, workspace_id=None, platform_token=None, platform_url=None ):
        """
        Initializes the SeqeraComputeEnvsWrapper class.

        Args:
            client (AuthenticatedPlatformClient): An instance of AuthenticatedPlatformClient
            workspace_id: The workspace id for Seqera platform.
        """
            
        self.workspace_id = os.getenv('WORKSPACE_ID')
        if not self.workspace_id:
              raise ValueError("Please set the WORKSPACE_ID in your enviornment variables")
        
        
        self.platform_token = platform_token or os.getenv('PLATFORM_TOKEN')
        self.platform_url = platform_url or os.getenv('PLATFORM_URL')

        # Check if both platform_token and platform_url are provided  
        if not self.platform_token or not self.platform_url:
            raise ValueError("Both platform_token and platform_url are required.")
        
        self.client = AuthenticatedClient(token=self.platform_token, base_url=self.platform_url)


    def list_compute_envs(self, status: str) -> list:
        """
        List compute environments for a workspace.

        Args:
            workspace_id (int): The ID of the workspace.
            status (str): The status of compute environments to filter.

        Returns:
            list: A list of compute environments or an empty list in case of an error.
        """
        try:
            compute_env_json_list = list_compute_envs.sync(client=self.client, workspace_id=self.workspace_id, status=status)
            return compute_env_json_list
        except Exception as e:
            # Handle the error as needed, e.g., log it or return an empty list.
            print(f"Error while listing compute environments: {str(e)}")
            return []

    def get_compute_env_id(self, compute_env_list: list) -> list:
        """
        Get the IDs of compute environments from a list of compute environments.

        Args:
            compute_env_list (list): A list of compute environments.

        Returns:
            list: A list of compute environment IDs or an empty list in case of an error.
        """
        try:
            id_list = [compute_env.id for compute_env in compute_env_list.compute_envs]
            return id_list
        except Exception as e:
            # Handle the error as needed, e.g., log it or return an empty list.
            print(f"Error while getting compute environment IDs: {str(e)}")
            return []
        
    def get_compute_env(self, compute_env_id: str) -> dict:
        if compute_env_id:
            compute_env = describe_compute_env.sync(client=self.client, compute_env_id=compute_env_id, workspace_id=self.workspace_id)
            return compute_env
        else:
            print("Please ensure the compute env ID is valid")
            
    def get_tower_compute_envs_id_list(self, status: str) -> list:
        """
        Get a list of Tower compute environment IDs.

        Args:
            workspace_id (str): The Seqera platform workspace ID.
            status (str): The status of compute environments to filter.

        Returns:
            list: A list of compute environment IDs.
        """
        compute_envs = self.list_compute_envs(status)
        compute_envs_id_list = self.get_compute_env_id(compute_envs)

        # Add "TowerForge-" prefix and "-head" suffix to each element in the list, changed for convinience
        modified_id_list = [f'ShahbazCompute-{env_id}-head' for env_id in compute_envs_id_list]
        return modified_id_list
            
    
