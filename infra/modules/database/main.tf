resource "aws_db_subnet_group" "rds_subnet" {
  count = var.cloud == "aws" ? 1 : 0
  name  = "${var.project_name}-rds-subnet"
  subnet_ids = var.private_subnet_id
}

resource "aws_security_group" "rds_sg" {
  count  = var.cloud == "aws" ? 1 : 0
  vpc_id = var.vpc_id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "postgres" {
  count                     = var.cloud == "aws" ? 1 : 0
  identifier                = "${var.project_name}-postgres"
  db_name                   = "ideas"
  engine                    = "postgres"
  engine_version            = "15.15"
  instance_class            = "db.t3.micro"
  allocated_storage         = 20
  username                  = var.db_username
  password                  = var.db_password
  db_subnet_group_name      = aws_db_subnet_group.rds_subnet[0].name
  vpc_security_group_ids    = [aws_security_group.rds_sg[0].id]
  skip_final_snapshot       = true
}