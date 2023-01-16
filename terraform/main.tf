module "network" {
  source          = "./network"
  access_ip       = var.access_ip
  vpc_cidr        = local.vpc_cidr
  security_groups = local.security_groups
}


module "ec2" {
  source        = "./ec2"
  public_sg     = module.network.public_sg
  public_subnet = module.network.public_subnet
}

# output "ec2_public_ip" {
#   # for_each = [{"1","2"}]
#   # value = aws_instance."node'${each.key}'".ec2_public_ip
#   value = { for k, v in module.ec2.aws_instance.node : k => v.associate_public_ip_address }
# }


output "ec2_public_ip" {
  value = module.ec2.ec2_public_ip
}

# output "ec2_public_dns" {
#   value = module.ec2.ec2_public_dns
# }