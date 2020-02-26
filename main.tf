#This main.tf will create a blueprint in an existing Project.
# You can create a project as well if you want by changing --- data "vra_project" to resource "vra_project" and project ID will need to reflect that as well.

provider "vra" {
  url           = var.vra_url
  refresh_token = var.vra_refresh_token
  insecure      = var.insecure
}

data "vra_project" "this" {
  name = var.project_name
}

resource "vra_blueprint" "this" {
  name        = var.blueprint_name
  description = "Created by vRA terraform provider"

  project_id = data.vra_project.this.id

  content = <<-EOT
    formatVersion: 1
    inputs:
      image:
        type: string
        description: "Image"
      flavor:
        type: string
        description: "Flavor"
    resources:
      Machine:
        type: Cloud.Machine
        properties:
          image: $${input.image}
          flavor: $${input.flavor}
  EOT
}