# 🧰 InfraBox - DevOps Infrastructure Bootstrapper

**InfraBox** is an open-source infrastructure-as-code project that provides a reusable Terraform baseline for setting up cloud environments using best practices. It is designed for DevOps engineers who want to quickly bootstrap clean, consistent environments — starting with Azure and expanding to other platforms.

## 🌍 Project Goals

- Provide an **end-to-end template** for deploying modern infrastructure using Terraform
- Serve as a **learning platform** for DevOps engineers to practice real-world provisioning
- Make it easy to expand to **Test, Stage, and Prod environments** by following a naming convention

## 🧱 Provisioned Resources

Currently, InfraBox provisions the following in Azure:

- Resource Group: `InfraBox-Dev-RG`
- Virtual Network and Subnet
- Network Interface
- Static Public IP
- Linux Virtual Machine (Ubuntu 20.04 LTS)
- DNS A Record for VM using Azure DNS

## 🌐 Resource Naming Convention

InfraBox-\<Environment\>-\<ResourceType\>

Example: `InfraBox-Dev-VM`, `InfraBox-Dev-PublicIP`, etc.  
This allows for easy scaling across environments like *Test*, *Stage*, and *Prod*.


## ⚙️ Getting Started

### 🔧 Prerequisites

- [Terraform CLI](https://developer.hashicorp.com/terraform/downloads)
- Azure CLI (logged in and configured)
- RSA SSH key (required for VM access)
- A registered domain in Azure DNS (optional for DNS record)

### 📂 Setup Instructions

```bash
git clone https://github.com/<your-username>/infrabox.git && cd infrabox

# Create RSA SSH key (if needed)
ssh-keygen -t rsa -b 4096 -f ~/.ssh/infrabox_key

# Initialize Terraform
terraform init

# Preview changes
terraform plan

# Apply infrastructure
terraform apply
```

#### 📄 Create a terraform.tfvars file
Add the following to a file called terraform.tfvars (DO NOT COMMIT THIS FILE):

```hcl
ssh_public_key_path = "~/.ssh/infrabox_key.pub"
dns_zone_name       = "example.com"
resource_group_name = "InfraBox-Dev-RG"
```

### 📁 Project Structure

```yaml
.
├── main.tf                # Core infrastructure definitions
├── variables.tf           # Input variable declarations
├── outputs.tf             # Output values
├── versions.tf            # Provider and Terraform version constraints
├── terraform.tfvars       # Local-only variable values (ignored)
├── README.md              # Project overview
└── .gitignore             # Git exclusions
```

### 🔒 Security

No secrets, passwords, or tokens should be hardcoded.
All sensitive values must go in terraform.tfvars (gitignored)
.terraform and state files are never committed.

### 🤝 Contributions

Open to issues and pull requests! Future goals include:

- Modular environment support
- Integration with CI/CD pipelines
- Kubernetes (CKA) and Terraform examples

### 🪪 License

MIT License. See LICENSE.txt file.

### 📌 Author
Created by Andrei-Călin Georgescu, with the goal of making infrastructure provisioning more accessible to others in the software development community.