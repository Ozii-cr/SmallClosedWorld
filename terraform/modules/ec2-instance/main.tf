resource "aws_key_pair" "key_pair" {
  key_name   = var.key_name
  public_key = var.ssh_public_key
}

resource "aws_instance" "server" {
  ami                    = var.ami
  instance_type          = var.instance_type
  key_name               = aws_key_pair.key_pair.key_name
  vpc_security_group_ids = [var.security_group_id]
  subnet_id              = var.subnet_id

  root_block_device {
    volume_size = var.volume_size
  }
  tags = {
    Name = var.instance_name
  }
}

resource "aws_eip" "eip" {
  count = var.enable_eip ? 1 : 0
}

resource "aws_eip_association" "eip_assoc" {
  count = var.enable_eip ? 1 : 0

  instance_id   = aws_instance.server.id
  allocation_id = aws_eip.eip[0].id
}

resource "aws_ec2_instance_state" "state" {
  instance_id = aws_instance.server.id
  state       = var.instance_state
}