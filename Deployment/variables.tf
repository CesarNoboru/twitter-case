variable "account_id" {
    description = "Account to be deployed"
    type        = string
    default     = "020834795051"
}

variable "bearer_token" {
    description = "Token to be used when consuming from Twitter API"
    type        = string
    default     = "AAAAAAAAAAAAAAAAAAAAAHeYKwEAAAAAqtWmWFb%2BH3Rp1Yu0BW8YfM7yGKc%3Dof6VSt8LQua4KKEzEop6aI7TIOMXz8vLcsbwmA1NVsiJsChPXI"
}

variable "region" {
    description = "Region to be deployed"
    type        = string
    default     = "us-east-1"
}