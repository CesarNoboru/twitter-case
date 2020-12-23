
output "account_id" {
  value = data.aws_caller_identity.current.account_id
}
output "caller_arn" {
  value = data.aws_caller_identity.current.arn
}
output "caller_user" {
  value = data.aws_caller_identity.current.user_id
}
output "RDS" {
  value = aws_db_instance.db.address
}
output "CloudWatch" {
  value = aws_cloudwatch_dashboard.dash.dashboard_name
}
output "API" {
  value = aws_api_gateway_stage.api.invoke_url
}
 output "SG-Modified" {
   value = aws_security_group_rule.rds_access_rule.security_group_id
 }