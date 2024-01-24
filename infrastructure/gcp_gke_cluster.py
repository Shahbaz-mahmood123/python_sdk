from pydantic import BaseModel

import pulumi
import pulumi_gcp as gcp 

from .pulumi_infra_config import PulumiInfraConfig
from .pulumi_config import PulumiGKEConfig

# Pydantic model for Node Pool Management
class Management(BaseModel):
    autoRepair: bool
    autoUpgrade: bool
    
class PulumiGKEInterface():
    
    def get_secrets(self):
        pass

class PulumiGKE(PulumiInfraConfig, PulumiGKEInterface):
    
    def __init__(self, config: PulumiGKEConfig) -> None:
        self.project_id = config.project_id 
        self.name = config.name
        self.region = config.region 
        self.zone = config.zone
        self.cluster_name = config.cluster_name
        self.cluster_type = config.cluster_type
        self.nodes = config.nodes 

        
    def pulumi_program(self):        
        
        # Create a VPC 
        network = gcp.compute.Network(f'{self.name}-vpc',
                                      auto_create_subnetworks=False, # We have more control over the network topology when this is False
                                      project = self.project_id)
        
        # Create a GCP subnet
        subnet = gcp.compute.Subnetwork(f'{self.name}-subnet',
                                ip_cidr_range="10.2.0.0/16",
                                network=network.id,
                                region=self.region, 
                                project = self.project_id
                                )
        
        gke_cluster = gcp.container.Cluster(
            self.cluster_name,
            network=network.id,
            subnetwork=subnet.id,
            # Define the node config for the cluster
            node_config=gcp.container.ClusterNodeConfigArgs(
                machine_type="n1-standard-1",  # Standard machine type
                oauth_scopes=[
                    "https://www.googleapis.com/auth/compute",
                    "https://www.googleapis.com/auth/devstorage.read_only",
                    "https://www.googleapis.com/auth/logging.write",
                    "https://www.googleapis.com/auth/monitoring"
                ],
            ),
            initial_node_count = 1,
            remove_default_node_pool=True,
            # Define the location for the cluster
            location=self.region,
            project = self.project_id
        )

        # Create a custom node pool attached to the GKE cluster created above.
        custom_node_pool = gcp.container.NodePool(self.nodes.name,
            location=gke_cluster.location,
            cluster=gke_cluster.name,
            initial_node_count=self.nodes.initial_node_count,
            project = self.project_id,
            # network = network.id,
            # subnetwork=subnet.id,
            node_config=gcp.container.NodePoolNodeConfigArgs(
                machine_type=self.nodes.machine_type, # Specify the machine type for the nodes.
            ),
            autoscaling=gcp.container.NodePoolAutoscalingArgs(
                min_node_count=self.nodes.min_node_count,
                max_node_count=self.nodes.max_node_count,
            ),
            management=gcp.container.NodePoolManagementArgs(
                auto_repair=self.nodes.auto_repair,
                auto_upgrade=self.nodes.auto_upgrade
            ))
        
        pulumi.export('network_id', network.id)
        # Export the Cluster Name
        pulumi.export("cluster_name", gke_cluster.name)
        # Export the Cluster Endpoint
        pulumi.export("cluster_endpoint", gke_cluster.endpoint)
        # Export the Cluster Master Version
        pulumi.export("cluster_master_version", gke_cluster.master_version)
            
    def get_secrets(self):
        pass