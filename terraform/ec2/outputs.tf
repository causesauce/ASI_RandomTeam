/* Output values make information about your infrastructure available on the command line
 , and can expose information for other Terraform configurations to use. Output values are similar to return values in programming languages.

 Output values have several uses:

 A child module can use outputs to expose a subset of its resource attributes to a parent module.
 A root module can use outputs to print certain values in the CLI output after running terraform apply.
 When using remote state, root module outputs can be accessed by other configurations via a terraform_remote_state data source.
*/



# output "ec2_public_dns" {
#   value = aws_instance.node.public_dns
# }

output "ec2_public_ip" {
  # for_each = [{"1","2"}]
  # value = aws_instance."node'${each.key}'".ec2_public_ip
  value = { for k, v in aws_instance.node : k => v.public_ip }
  # value = "Hello"
}

