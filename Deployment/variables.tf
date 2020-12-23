variable "account_id" {
    description = "Account to be deployed"
    type        = string
    default     = "020834795051"
}

variable "bearer_token" {
    description = "Token to be used when consuming from Twitter API"
    type        = string
    default     = "AAAAAAAAAAAAAAAAAAAAANUAKwEAAAAAqSfAa1p%2BYb%2Byfgc3Yo%2FC4efg8Yw%3DH8TFRh9WwZzkwsxwcyTJ8xd4qywTfn6JNFKKeCIMdGeISZWJWn"
}

variable "region" {
    description = "Region to be deployed"
    type        = string
    default     = "us-east-1"
}