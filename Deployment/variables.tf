
variable "bearer_token" {
    description = "Token to be used when consuming from Twitter API"
    type        = string
}

variable "region" {
    description = "Region to be deployed"
    type        = string
    default     = "us-east-1"
}

variable "db_admin"{
    description = "Admin user for RDS MySQL"
    type        = string
    default     = "admin" 
}

variable "db_pass"{
    description = "Admin user's password for RDS MySQL"
    type        = string
    default     = "admin123" 
}