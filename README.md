# 🚀 InfraBox - DevOps Infrastructure Bootstrapper

**InfraBox** is a secure, modular, and reusable infrastructure-as-code boilerplate using **Terraform on Azure**. It is designed to make provisioning cloud infrastructure fast, predictable, and accessible — especially for teams and developers who want to spin up fully working environments with minimal friction.

---

## 📦 Project Goals

- 🛠️ Modular, scalable, and DRY Terraform code
- 🔐 Strong DevSecOps and input validation principles
- ⚙️ CLI wrapper for simplified provisioning and teardown
- 🧪 Integrated with GitHub Actions for linting, validation and security scanning
- 🧰 Support for multiple environments (e.g., `dev`, `test`, `prod`)

---

## 📁 Project Structure

```bash
InfraBox/
│
├── environments/
│   └── dev/                  # Example environment
│       ├── main.tf
│       ├── variables.tf
│       ├── terraform.tfvars
│       └── backend.tf
│
├── modules/
│   ├── networking/
│   ├── virtual_machine/
│   ├── storage_account/
│   └── resource_group/
│
├── shared/
│   └── provider.tf           # Common provider configuration
│
├── cli/                      # Python CLI wrapper logic
│   ├── __init__.py
│   ├── parser.py             # Argument parser
│   ├── utils.py              # Secure command runner, path validation
│   ├── terraform_utils.py    # Terraform-specific wrappers
│   └── commands/
│       ├── __init__.py
│       ├── create.py         # Implements 'create' command
│       └── destroy.py        # Implements 'destroy' command
│
├── InfraBox.py               # Entry point for the CLI
├── .github/
│   └── workflows/            # GitHub Actions for linting, security, smoke tests
│
├── .gitignore
├── README.md
└── requirements.txt
```

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
- Python 3.8+
- Azure CLI (logged in and configured)
- RSA SSH key (required for VM access)
- A registered domain in Azure DNS (optional for DNS record)
- virtualenv (recommended for encapsulation of future project dependencies)

#### 🔧 Install Python Requirements
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

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
Infrabox can be used with native terraform from each of the environments directory, or using the InfraBox CLI wrapper.

### 🧑‍💻 Using the CLI

InfraBox comes with a secure, extensible Python CLI that abstracts Terraform commands.

#### 🔨 Create an environment
``` bash
python InfraBox.py create dev
```

- This will validate the target environment
- Run terraform plan
- Ask for confirmation before applying changes
- Skips apply if no changes are detected
- Output environment details once provisioned

#### 🧨 Destroy an environment
``` bash
python InfraBox.py destroy dev
```
- Validates the environment
- Runs terraform plan -destroy
- Asks for confirmation before applying
- Skips apply -destroy if no changes are required

#### 🧪 Dry-run mode
To preview what InfraBox would do without making changes:

```bash
python InfraBox.py create dev --dry-run
```

### 🛡️ Security Considerations

- All CLI commands are validated for path traversal and injection
- Sensitive output (Terraform secrets, tokens) is never printed
- All subprocesses use safe execution patterns

### 🤖 GitHub Actions

InfraBox includes CI workflows for:

- ✅ Terraform linting, formatting, and validation (.tf, .tfvars)
- ✅ Static analysis using tflint and tfsec
- ✅ Required checks enforced before merging to main

### 📌 DevSecOps Best Practices Followed

- ✅ Shift-left security with early validation
- ✅ Separation of config, code, and secrets
- ✅ Secure CLI with strict input handling
- ✅ Continuous security scanning via GitHub Actions
- ✅ Explicit terraform.required_version and provider constraints

🔄 Roadmap

 - Add environment-specific SSH key pair generation and management
 - Extend CLI to support selective module provisioning
 - Add support for multiple cloud providers (future)
 - Add wrapper output renderer for non-technical users
 - Auto-generate documentation from modules

#### 📝 Notes on Coding Best Practices Reflected:

- Modules are **resource-type scoped**, keeping them reusable and scalable.
- environments/ uses a clear separation per environment (dev, test, etc.).
- A single provider.tf is shared via safe reuse strategies (symlink from shared into environment/ directories or duplicated in root for consistency).
- DRY and clarity are balanced — each folder does one thing well.

### 🤝 Contributions

Open to issues and pull requests! Future goals include:

- Modular environment support
- Integration with CI/CD pipelines
- Kubernetes (CKA) and Terraform examples

### 🪪 License

MIT License. See LICENSE.txt file.

### 📌 Author
Created by Andrei-Călin Georgescu, with the goal of making infrastructure provisioning more accessible to others in the software development community.