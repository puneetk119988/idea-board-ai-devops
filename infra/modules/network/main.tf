# ================= AWS NETWORK (Multi-AZ) =================

resource "aws_vpc" "vpc" {
  count      = var.cloud == "aws" ? 1 : 0
  cidr_block = "10.0.0.0/16"
}

# -------- Public Subnets --------
resource "aws_subnet" "public_a" {
  count                   = var.cloud == "aws" ? 1 : 0
  vpc_id                  = aws_vpc.vpc[0].id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = true
}

resource "aws_subnet" "public_b" {
  count                   = var.cloud == "aws" ? 1 : 0
  vpc_id                  = aws_vpc.vpc[0].id
  cidr_block              = "10.0.3.0/24"
  availability_zone       = "${var.aws_region}b"
  map_public_ip_on_launch = true
}

# -------- Private Subnets --------
resource "aws_subnet" "private_a" {
  count             = var.cloud == "aws" ? 1 : 0
  vpc_id            = aws_vpc.vpc[0].id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "${var.aws_region}a"
}

resource "aws_subnet" "private_b" {
  count             = var.cloud == "aws" ? 1 : 0
  vpc_id            = aws_vpc.vpc[0].id
  cidr_block        = "10.0.4.0/24"
  availability_zone = "${var.aws_region}b"
}

# -------- IGW + NAT --------
resource "aws_internet_gateway" "igw" {
  count  = var.cloud == "aws" ? 1 : 0
  vpc_id = aws_vpc.vpc[0].id
}

resource "aws_eip" "nat" {
  count  = var.cloud == "aws" ? 1 : 0
  domain = "vpc"
}

resource "aws_nat_gateway" "nat" {
  count         = var.cloud == "aws" ? 1 : 0
  allocation_id = aws_eip.nat[0].id
  subnet_id     = aws_subnet.public_a[0].id
  depends_on    = [aws_internet_gateway.igw]
}

# -------- Route Tables --------
resource "aws_route_table" "public" {
  count  = var.cloud == "aws" ? 1 : 0
  vpc_id = aws_vpc.vpc[0].id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw[0].id
  }
}

resource "aws_route_table" "private" {
  count  = var.cloud == "aws" ? 1 : 0
  vpc_id = aws_vpc.vpc[0].id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat[0].id
  }
}

resource "aws_route_table_association" "public_a" {
  count          = var.cloud == "aws" ? 1 : 0
  subnet_id      = aws_subnet.public_a[0].id
  route_table_id = aws_route_table.public[0].id
}

resource "aws_route_table_association" "public_b" {
  count          = var.cloud == "aws" ? 1 : 0
  subnet_id      = aws_subnet.public_b[0].id
  route_table_id = aws_route_table.public[0].id
}

resource "aws_route_table_association" "private_a" {
  count          = var.cloud == "aws" ? 1 : 0
  subnet_id      = aws_subnet.private_a[0].id
  route_table_id = aws_route_table.private[0].id
}

resource "aws_route_table_association" "private_b" {
  count          = var.cloud == "aws" ? 1 : 0
  subnet_id      = aws_subnet.private_b[0].id
  route_table_id = aws_route_table.private[0].id
}