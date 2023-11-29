import os
from client.nextflow_tower_api_client import AuthenticatedClient
from client.nextflow_tower_api_client.api.default import list_compute_envs, describe_compute_env
from client.nextflow_tower_api_client.models.list_compute_envs_response import ListComputeEnvsResponse
from core.client import AuthenticatedPlatformClient

class SeqeraComputeEnvsWrapperInterface:
    def list_compute_envs(self, workspace_id: int, status: str) -> list:
        pass

    def get_compute_env_id(self, compute_env_list: list) -> list:
        pass
    
    def get_compute_env(self, workspace_id: int, compute_env_id: str) -> dict:
        pass 

class SeqeraComputeEnvsWrapper(SeqeraComputeEnvsWrapperInterface):
    def __init__(self, client: AuthenticatedPlatformClient, workspace_id=None):
        """
        Initializes the SeqeraComputeEnvsWrapper class.

        Args:
            client (AuthenticatedPlatformClient): An instance of AuthenticatedPlatformClient.
        """
        self.client = client
        self.workspace_id = workspace_id or os.getenv('WORKSPACE_ID')
        if not self.workspace_id:
            raise ValueError("Please set the WORKSAPCE_ID in your enviornment variables")


    def list_compute_envs(self, workspace_id: int, status: str) -> list:
        """
        List compute environments for a workspace.

        Args:
            workspace_id (int): The ID of the workspace.
            status (str): The status of compute environments to filter.

        Returns:
            list: A list of compute environments or an empty list in case of an error.
        """
        try:
            compute_env_json_list = list_compute_envs.sync(client=self.client, workspace_id=workspace_id, status=status)
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
            

                
            
    
