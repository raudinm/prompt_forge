resource "null_resource" "deploy_promptforge" {

  # Step: compress project directory into tar.gz archive
  provisioner "local-exec" {
    command = <<EOT
      echo "${var.ssh_private_key}" > /tmp/deploy_key
      chmod 600 /tmp/deploy_key

      rsync -avz --exclude='.git' ../ \
        -e "ssh -i /tmp/deploy_key -o StrictHostKeyChecking=no" \
        ${var.deploy_user}@${var.deploy_host}:/tmp/promptforge/
    EOT
  }

  # Step: copy tar archive to remote server
  # provisioner "file" {
  #   source      = "promptforge.tar.gz"
  #   destination = "/tmp/promptforge.tar.gz"
  #   connection {
  #     type        = "ssh"
  #     host        = var.deploy_host
  #     user        = var.deploy_user
  #     private_key = var.ssh_private_key
  #   }
  # }

  # Step: copy deployment script
  provisioner "file" {
    source      = "scripts/deploy.sh"
    destination = "/tmp/deploy.sh"
    connection {
      type        = "ssh"
      host        = var.deploy_host
      user        = var.deploy_user
      private_key = var.ssh_private_key
    }
  }

  # Step: execute deployment script remotely
  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/deploy.sh",
      "sudo /tmp/deploy.sh"
    ]
    connection {
      type        = "ssh"
      host        = var.deploy_host
      user        = var.deploy_user
      private_key = var.ssh_private_key
      timeout     = "20m"
    }
  }
}
