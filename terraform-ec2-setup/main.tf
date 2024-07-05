# Configure the AWS provider
provider "aws" {
  region = "ap-south-1"  # Replace with your desired AWS region
}

# Define an AWS EC2 instance resource
resource "aws_instance" "my-ec2-tcc" {
  ami           = "ami-0ad21ae1d0696ad58"  # Replace with your desired AMI ID
  instance_type = "t2.small"
  key_name      = var.key_name    # Use a variable for the SSH key pair name

  tags = {
    Name = "my-ec2-tcc"
  }

  # Optional: Define SSH connection settings
  connection {
    type        = "ssh"
    user        = "ubuntu"          # Replace with your instance's SSH user
    private_key = file(var.private_key_path)  # Use a variable for the SSH private key path
    host        = aws_instance.my-ec2-tcc.public_ip  # Use the public IP of the instance
  }

  # Provisioner to install Docker and configure AWS CLI
  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update -y",
      "sudo apt-get upgrade -y",
      "curl -fsSL https://get.docker.com -o get-docker.sh",
      "sudo sh get-docker.sh",
      "sudo usermod -aG docker $USER",
      "sudo apt-get install -y curl unzip",
      "curl 'https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip' -o 'awscliv2.zip'",
      "unzip awscliv2.zip",
      "sudo ./aws/install",
      "aws --version",
      # Add more commands as needed
    ]

    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file(var.private_key_path)
      host        = aws_instance.my-ec2-tcc.public_ip
    }
  }
}
