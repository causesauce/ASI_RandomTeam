# Create a VPC
resource "aws_vpc" "vpc" {
  cidr_block           = var.vpc_cidr
  # enable_dns_hostnames = true
  # enable_dns_support   = true
  instance_tenancy     = "default"

  tags = {
    Name = "ml_proj_vpc"
  }

  lifecycle {
    /*
    meta-argument changes this behavior so that the new replacement object is created first, 
    and the prior object is destroyed after the replacement is created. 
    */
    create_before_destroy = true
  }
}

# Create a Public Subnet
resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.vpc.id
 /* 
   cidrsubnet(prefix, newbits, netnum)
   prefix must be given in CIDR notation, as defined in RFC 4632 section 3.1.
   newbits is the number of additional bits with which to extend the prefix. For example
    , if given a prefix ending in /16 and a newbits value of 4, the resulting subnet address will have length /20.
   netnum is a whole number that can be represented as a binary integer with no more than newbits binary digits
    , which will be used to populate the additional bits added to the prefix.
  */
  # vpc_cidr = 10.0.0.0/24 
  cidr_block              = cidrsubnet(var.vpc_cidr, 4, 15)
  # default: map_public_ip_on_launch = true 
  map_public_ip_on_launch = true
  availability_zone       = data.aws_availability_zones.available.names[0]

  tags = {
    Name = "ml_proj_public_subnet"
  }
}

# Associate the Public Route Table to the Public Subnet
resource "aws_route_table_association" "public_assoc" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_rt.id
}

# Create a Internet Gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "ml_proj_gateway"
  }
}

# Create a Public Route Table
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "public_ml_proj_rt"
  }
}

# Create a Route
resource "aws_route" "default_route" {
  route_table_id         = aws_route_table.public_rt.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id
}

# Create Security Groups
resource "aws_security_group" "sg" {
  for_each    = var.security_groups
  name        = each.value.name
  description = each.value.description
  vpc_id      = aws_vpc.vpc.id

# Ingress - inbound rules 
  dynamic "ingress" {
    for_each = each.value.ingress

    content {
    /* Example
        protocol = “tcp”
        from_port = 80
        to_port = 80
        cidr_blocks = [ “0.0.0.0/0” ]
    */
      from_port   = ingress.value.from
      to_port     = ingress.value.to
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
    }
  }
# Ingress - outbound rules
  egress {
    /* Example
        protocol = “tcp”
        from_port = 80
        to_port = 80
        cidr_blocks = [ “0.0.0.0/0” ]
    */    
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }
}