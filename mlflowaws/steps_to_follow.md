### Steps
1. Code everything required
2. login to AWS Management Console
3. create a user - provide only the administrator access and just attach them to the policy
4. go into the user
5. go to security credentials
6. get access key - get it for CLI
7. search for AWS CLI download latest - download .pkg and install
8. runw `aws configure` in the terminal
9. we set up our region - `ap-southeast-2` and output format name - `json`
10. We will create a s3 bucket - search s3, name one, uncheck the 'block public access'
11. now we need the EC2 machine - pretty much intuitive. just tick 2 HTTP options
12. get a key-value pair.
13. once the instance is up and running, go in then security
14. go to inbound rules - security group and add 5000 as the tcp
15. after installing everything from the documentations we can do the following
16. go to the instance, get the PUBLIC DNS. paste that and go to 5000 port, our mlflow should run
17. we should put that in the app.py where we have the tracking uri