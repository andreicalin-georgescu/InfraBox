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

```text
## 📁 Project Structure

```text
InfraBox/
├── environments/
│   └── dev/                        # Development environment configuration
│       ├── main.tf                 # References reusable modules for provisioning
│       ├── variables.tf            # Inputs specific to the Dev environment
│       ├── outputs.tf              # Outputs exposed after provisioning
│       └── backend.tf              # Remote state backend config (e.g., Azure Storage)
│
├── modules/                        # Reusable, environment-agnostic Terraform modules
│   ├── resource_group/
│   │   ├── main.tf                 # Resource group creation logic
│   │   ├── variables.tf            # Inputs like name and location
│   │   └── outputs.tf              # Outputs like resource_group_name
│
│   ├── network/
│   │   ├── main.tf                 # VNet, Subnet, Public IP, NIC, DNS Zone & A Record
│   │   ├── variables.tf
│   │   └── outputs.tf
│
│   ├── virtual_machine/
│   │   ├── main.tf                 # Linux VM setup with SSH key auth
│   │   ├── variables.tf
│   │   └── outputs.tf
│
│   └── storage_account/
│       ├── main.tf                 # Azure Storage account for app/data use
│       ├── variables.tf
│       └── outputs.tf
│
├── shared/
│   └── provider.tf                 # Shared provider config (used via symlinks or duplication)
│
├── versions.tf                     # Defines required Terraform and provider versions
├── .gitignore                      # Ignores .terraform/, .tfstate, secrets, etc.
├── .gitattributes                  # Normalizes line endings across platforms
└── README.md                       # You are here 🌍

```
#### 📝 Notes on Best Practices Reflected:

- Modules are **resource-type scoped**, keeping them reusable and scalable.
- environments/ uses a clear separation per environment (dev, test, etc.).
- A single provider.tf is shared via safe reuse strategies (symlink from shared into environment/ directories or duplicated in root for consistency).
- DRY and clarity are balanced — each folder does one thing well.

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