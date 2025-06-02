#!/bin/python3
from result_output import ResultOutput
import re
import os
import sys
import json
import time
import shutil
import subprocess
import importlib.util
from sys import platform
import requests
import socket
from jenkinsapi.jenkins import Jenkins


class Activity:

    def testcase_check_docker_image(self, test_object):
        image_name = "todo-application-image"
        testcase_description = f"Checking if the Docker image '{image_name}' is created"
        expected = f"The Docker image '{image_name}' is present"
        actual = f"The Docker image '{image_name}' is not present"
        marks = 5
        test_passed = "Congrats!"
        test_failed = "Check the docker image name"
        error = "Exception"
        test_object.update_pre_result(testcase_description, expected)
        
        def run_command(command):
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            return result
        
        try:
            # List all Docker images
            image_check = run_command(f'docker images -q {image_name}')
            
            if image_check.stdout.strip():  # If output is not empty, the image exists
                actual = expected
                return test_object.update_result(1, expected, actual, test_passed, "N/A",marks)
            else:
                return test_object.update_result(0, expected, actual, test_failed, "N/A",marks)
        
        except Exception as e:
            test_object.update_result(0, expected, actual, testcase_description, "N/A",marks)
            test_object.eval_message["testcase_check_docker_image"] = str(e)

    def testcase_check_docker_image_tagged_correctly(self, test_object):
        image_name = "todo-application-image"
        tag = "latest"
        testcase_description = f"Checking if the Docker image '{image_name}' is tagged correctly with '{tag}'"
        expected = f"The Docker image '{image_name}' is tagged correctly with '{tag}'"
        actual = f"The Docker image '{image_name}' is not tagged correctly with '{tag}'"
        marks = 5
        test_passed = "Congrats!"
        test_failed = "Check the docker image tag name"
        test_object.update_pre_result(testcase_description, expected)
        
        def run_command(command):
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            return result
        
        try:
            # Check if the Docker image is tagged correctly
            image_tag_check = run_command(f"docker images --filter=reference='{image_name}:{tag}' --format '{{{{.Repository}}}}:{{{{.Tag}}}}'")
            
            if f"{image_name}:{tag}" in image_tag_check.stdout.strip():
                actual = expected
                return test_object.update_result(1, expected, actual, test_passed, "N/A", marks)
            else:
                return test_object.update_result(0, expected, actual, test_failed, "N/A", marks)
        
        except Exception as e:
            test_object.update_result(0, expected, actual, testcase_description, "N/A", marks)
            test_object.eval_message["testcase_check_docker_image_tagged_correctly"] = str(e)


    def testcase_check_docker_volume_name_after_jenkins_pipeline(self, test_object):
        expected_volume_name = "mysql-data"  # Expected volume name substring
        testcase_description = f"Checking if a Docker volume containing '{expected_volume_name}' is created after executing the Jenkins pipeline"
        expected = f"A Docker volume containing '{expected_volume_name}' is created after executing the Jenkins pipeline"
        actual = f"No Docker volume containing '{expected_volume_name}' was found after executing the Jenkins pipeline"
        marks = 5
        test_passed = "Congrats! A matching volume exists."
        test_failed = "No matching volume exists. Please verify the Jenkins pipeline execution."
        test_object.update_pre_result(testcase_description, expected)

        def run_command(command):
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            return result

        try:
            # List all Docker volumes and check if any contains the expected substring
            volume_check = run_command("docker volume ls --format '{{.Name}}'")
            volume_names = volume_check.stdout.strip().splitlines()

            # Check if any volume name contains the expected substring
            matching_volumes = [v for v in volume_names if expected_volume_name in v]

            if matching_volumes:
                actual = expected
                return test_object.update_result(1, expected, actual, test_passed, "N/A", marks)
            else:
                return test_object.update_result(0, expected, actual, test_failed, "N/A", marks)

        except Exception as e:
            test_object.update_result(0, expected, actual, testcase_description, "N/A", marks)
            test_object.eval_message["testcase_check_docker_volume_name_after_jenkins_pipeline"] = str(e)




    def testcase_check_docker_network_name_after_jenkins_pipeline(self, test_object):
        expected_network_name = "todo-network"  # Expected network name substring
        testcase_description = f"Checking if a Docker network containing '{expected_network_name}' is created after executing the Jenkins pipeline"
        expected = f"A Docker network containing '{expected_network_name}' is created after executing the Jenkins pipeline"
        actual = f"No Docker network containing '{expected_network_name}' was found after executing the Jenkins pipeline"
        marks = 5
        test_passed = "Congrats! A matching network exists."
        test_failed = "No matching network exists. Please verify the Jenkins pipeline execution."
        test_object.update_pre_result(testcase_description, expected)

        def run_command(command):
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            return result

        try:
            # List all Docker networks and check if any contains the expected substring
            network_check = run_command("docker network ls --format '{{.Name}}'")
            network_names = network_check.stdout.strip().splitlines()

            # Check if any network name contains the expected substring
            matching_networks = [n for n in network_names if expected_network_name in n]

            if matching_networks:
                actual = expected
                return test_object.update_result(1, expected, actual, test_passed, "N/A", marks)
            else:
                return test_object.update_result(0, expected, actual, test_failed, "N/A", marks)

        except Exception as e:
            test_object.update_result(0, expected, actual, testcase_description, "N/A", marks)
            test_object.eval_message["testcase_check_docker_network_name_after_jenkins_pipeline"] = str(e)



    def testcase_check_jenkins_user_in_docker_group(self, test_object):
        user = "jenkins"
        group = "docker"
        testcase_description = f"Checking if the user '{user}' is part of the '{group}' group"
        expected = f"The user '{user}' is part of the '{group}' group"
        actual = f"The user '{user}' is not part of the '{group}' group"
        marks = 5
        test_passed = "Congrats!"
        test_failed = "Check if the user 'jenkins' is added to the 'docker' group"
        test_object.update_pre_result(testcase_description, expected)

        def run_command(command):
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            return result

        try:
            # Check if the user is part of the docker group
            group_check = run_command(f"groups {user}")

            # If the docker group is listed in the output, the user is part of it
            if group in group_check.stdout.strip().split():
                actual = expected
                return test_object.update_result(1, expected, actual, test_passed, "N/A", marks)
            else:
                return test_object.update_result(0, expected, actual, test_failed, "N/A", marks)

        except Exception as e:
            test_object.update_result(0, expected, actual, testcase_description, "N/A", marks)
            test_object.eval_message["testcase_check_jenkins_user_in_docker_group"] = str(e)


    def testcase_check_application_status_after_jenkins_pipeline(self, test_object):
        testcase_description = (
            "Checking if the application created as part of the Jenkins pipeline execution is active in the Docker container"
        )
        expected = "The application created by the Jenkins pipeline is active in the Docker container"
        actual = "The application created by the Jenkins pipeline is not active in the Docker container"
        # container_name = "webapp_container" Replace with your Docker container name
        application_url = "http://localhost:8082"  # Replace with your application's URL
        marks = 10
        test_object.update_pre_result(testcase_description, expected)

        def is_port_open(host, port):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                try:
                    s.connect((host, port))
                    return True
                except socket.error:
                    return False

        try:
            # Check if the application is running on port 8082 in the Docker container
            if is_port_open("localhost", 8082):
                # If the port is open, check if the application is accessible via HTTP request
                response = requests.get(application_url)

                if response.status_code == 200:
                    actual = expected
                    return test_object.update_result(1, expected, actual, testcase_description, "N/A", marks)
                else:
                    actual = f"The application is not active. HTTP Status Code: {response.status_code}"
                    return test_object.update_result(0, expected, actual, testcase_description, "N/A", marks)
            else:
                actual = "The application is not running on port 8082"
                return test_object.update_result(0, expected, actual, testcase_description, "N/A", marks)

        except Exception as e:
            test_object.update_result(0, expected, actual, testcase_description, "N/A", marks)
            test_object.eval_message["testcase_check_application_status_after_jenkins_pipeline"] = str(e)



    def testcase_check_mysql_db_creation_after_jenkins_pipeline(self, test_object):
        container_name_substring = "mysql-db"
        testcase_description = (
            f"Checking if a MySQL database container containing '{container_name_substring}' in its name was created as part of the Jenkins pipeline execution"
        )
        expected = f"A MySQL database container containing '{container_name_substring}' in its name exists and was created by the Jenkins pipeline"
        actual = f"No MySQL database container containing '{container_name_substring}' in its name exists or was not created by the Jenkins pipeline"
        marks = 5
        test_passed = "Congrats! A matching MySQL database container exists."
        test_failed = "No matching MySQL database container exists. Please verify the Jenkins pipeline setup."
        test_object.update_pre_result(testcase_description, expected)

        def run_command(command):
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
            return result

        try:
            # Get the list of running containers
            command = "docker ps -a --format '{{.Names}}'"
            result = run_command(command)

            if result.returncode == 0:
                containers = result.stdout.strip().split("\n")
                # Check if any container name contains the expected substring
                matching_containers = [c for c in containers if container_name_substring in c]
                
                if matching_containers:
                    actual = expected
                    return test_object.update_result(1, expected, actual, test_passed, "N/A", marks)
                else:
                    return test_object.update_result(0, expected, actual, test_failed, "N/A", marks)
            else:
                raise Exception(f"Error fetching container names: {result.stderr.strip()}")

        except Exception as e:
            test_object.update_result(0, expected, actual, testcase_description, "N/A", marks)
            test_object.eval_message["testcase_check_mysql_db_creation_after_jenkins_pipeline"] = str(e)



    def testcase_check_todo_application_container_after_jenkins_pipeline(self, test_object):
        container_name = "todo-application"
        testcase_description = (
            f"Checking if a To-Do application container containing '{container_name}' was created and exists as part of the Jenkins pipeline execution"
        )
        expected = f"A To-Do application container containing '{container_name}' exists and was created by the Jenkins pipeline"
        actual = f"No To-Do application container containing '{container_name}' was found or created by the Jenkins pipeline"
        marks = 5
        test_passed = "Congrats! A matching To-Do application container exists."
        test_failed = "No matching To-Do application container exists. Please verify the Jenkins pipeline setup."
        test_object.update_pre_result(testcase_description, expected)

        def run_command(command):
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
            return result

        try:
            # Get the list of running containers
            command = "docker ps -a --format '{{.Names}}'"
            result = run_command(command)

            if result.returncode == 0:
                containers = result.stdout.strip().split("\n")
                # Check if any container name contains the expected substring
                matching_containers = [c for c in containers if container_name in c]

                if matching_containers:
                    actual = expected
                    return test_object.update_result(1, expected, actual, test_passed, "N/A", marks)
                else:
                    return test_object.update_result(0, expected, actual, test_failed, "N/A", marks)
            else:
                raise Exception(f"Error fetching container names: {result.stderr.strip()}")

        except Exception as e:
            test_object.update_result(0, expected, actual, testcase_description, "N/A", marks)
            test_object.eval_message["testcase_check_todo_application_container_after_jenkins_pipeline"] = str(e)


    def testcase_check_kubernetes_secret_my_registry_secret(self, test_object):
        secret_name = "my-registry-secret"
        testcase_description = f"Checking if the Kubernetes secret with the name '{secret_name}' exists"
        expected = f"The Kubernetes secret with the name '{secret_name}' exists"
        actual = f"The Kubernetes secret with the name '{secret_name}' does not exist"
        marks = 5
        test_passed = "Congrats! The secret exists."
        test_failed = "The specified secret does not exist. Please verify the secret setup."
        test_object.update_pre_result(testcase_description, expected)

        def run_command(command):
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
            return result

        try:
            # Get the list of secrets in the default namespace
            command = "sudo -H -u labuser kubectl get secrets --no-headers -o custom-columns=NAME:.metadata.name"
            result = run_command(command)

            if result.returncode == 0:
                secrets = result.stdout.strip().split("\n")
                # Check if the target secret name exists in the list
                if secret_name in secrets:
                    actual = expected
                    return test_object.update_result(1, expected, actual, test_passed, "N/A", marks)
                else:
                    return test_object.update_result(0, expected, actual, test_failed, "N/A", marks)
            else:
                raise Exception(f"Error fetching secrets: {result.stderr.strip()}")

        except Exception as e:
            test_object.update_result(0, expected, actual, testcase_description, "N/A", marks)
            test_object.eval_message["testcase_check_kubernetes_secret_my_registry_secret"] = str(e)

    def testcase_check_application_on_minikube_ip(self, test_object):
        testcase_description = "Checking if the application is running on Minikube at port 30080"
        expected = "Application is accessible at http://<minikube-ip>:30080"
        actual = "Application is not accessible at http://<minikube-ip>:30080"
        marks = 10
        test_passed = "Congrats! The application is accessible."
        test_failed = "The application is not accessible. Please check Minikube IP and port configuration."
        test_object.update_pre_result(testcase_description, expected)

        def run_command(command):
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
            return result

        try:
            # Step 1: Get the Minikube IP
            command_get_minikube_ip = "sudo -H -u labuser minikube ip"
            result_minikube_ip = run_command(command_get_minikube_ip)

            if result_minikube_ip.returncode != 0:
                raise Exception(f"Error fetching Minikube IP: {result_minikube_ip.stderr.strip()}")

            minikube_ip = result_minikube_ip.stdout.strip()
            application_url = f"http://{minikube_ip}:30080"
            
            # Step 2: Check if the application is accessible at the generated URL
            try:
                response = requests.get(application_url)

                if response.status_code == 200:
                    actual = expected
                    return test_object.update_result(1, expected, actual, test_passed, "N/A", marks)
                else:
                    actual = f"Application is not accessible. HTTP Status Code: {response.status_code}"
                    return test_object.update_result(0, expected, actual, test_failed, "N/A", marks)

            except requests.ConnectionError as e:
                actual = f"Connection error: {str(e)}"
                return test_object.update_result(0, expected, actual, test_failed, "N/A", marks)

        except Exception as e:
            test_object.update_result(0, expected, actual, testcase_description, "N/A", marks)
            test_object.eval_message["testcase_check_application_on_minikube_ip"] = str(e)

    def testcase_check_application_content_on_minikube_site(self, test_object):
        testcase_description = (
            "Checking if the application hosted on Minikube at port 30080 serves the expected content"
        )
        expected = "The application site serves the expected content"
        actual = "The application site does not serve the expected content"
        marks = 15
        test_passed = "Congrats! The application content is served correctly."
        test_failed = (
            "The application content is not served as expected. Please verify the deployment."
        )
        test_object.update_pre_result(testcase_description, expected)

        def run_command(command):
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
            return result

        try:
            # Step 1: Get the Minikube IP
            command_get_minikube_ip = "sudo -H -u labuser minikube ip"
            result_minikube_ip = run_command(command_get_minikube_ip)

            if result_minikube_ip.returncode != 0:
                raise Exception(f"Error fetching Minikube IP: {result_minikube_ip.stderr.strip()}")

            minikube_ip = result_minikube_ip.stdout.strip()
            application_url = f"http://{minikube_ip}:30080"

            # Step 2: Check if the application is accessible and serves the expected content
            try:
                response = requests.get(application_url)

                if response.status_code == 200:
                    # Verify content (generic validation of expected content existence)
                    if "Task List" in response.text:  # Example keyword for validation
                        actual = expected
                        return test_object.update_result(1, expected, actual, test_passed, "N/A", marks)
                    else:
                        actual = "The application content is not as expected"
                        return test_object.update_result(0, expected, actual, test_failed, "N/A", marks)
                else:
                    actual = f"Application is not accessible. HTTP Status Code: {response.status_code}"
                    return test_object.update_result(0, expected, actual, test_failed, "N/A", marks)

            except requests.ConnectionError as e:
                actual = f"Connection error: {str(e)}"
                return test_object.update_result(0, expected, actual, test_failed, "N/A", marks)

        except Exception as e:
            test_object.update_result(0, expected, actual, testcase_description, "N/A", marks)
            test_object.eval_message["testcase_check_application_content_on_minikube_site"] = str(e)



    def testcase_check_pipeline_latest_build_successful(self, test_object):
        testcase_description = "Checking if the latest build of 'todo-application-pipeline' is successful"
        expected = "The latest build of 'todo-application-pipeline' is successful"
        actual = "The latest build of 'todo-application-pipeline' is not successful or job not found"
        marks = 10
        test_object.update_pre_result(testcase_description, expected)

        try:
            jenkins_url = "http://localhost:8080"
            server = Jenkins(jenkins_url, username='jenkinsuser', password='Jenkinsuser@123')
            
            # Get the job (project) object for "maven-project"
            job = server.get_job('todo-application-pipeline')
            
            if job:
                # Get the latest build number
                last_build_number = job.get_last_buildnumber()
                
                # Get the build information
                last_build = job.get_build(last_build_number)
                
                # Check if the latest build was successful
                if last_build.is_good():
                    actual = expected
                    return test_object.update_result(1, expected, actual, testcase_description, "N/A",marks)
                else:
                    actual = "The latest build of 'todo-application-pipeline' failed or was unstable"
                    return test_object.update_result(0, expected, actual, testcase_description, "N/A",marks)
            else:
                actual = "The job 'todo-application-pipeline' was not found"
                return test_object.update_result(0, expected, actual, testcase_description, "N/A",marks)

        except Exception as e:
            test_object.update_result(0, expected, actual, testcase_description, "N/A",marks)
            test_object.eval_message["testcase_check_pipeline_latest_build_successful"] = str(e)

    def testcase_check_pod_states(self, test_object):
        testcase_description = "Check if the pods are in Running status"
        expected_result = "Pods are in Running status"
        actual = "Pods are not in Running status"
        marks = 5
        test_object.update_pre_result(testcase_description, expected_result)
        def run_command(command):
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
            return result
        
        try:
            command_copy_kubeconfig = "cp /home/labuser/.kube/config /root/.kube/config"
            result_copy_kubeconfig = run_command(command_copy_kubeconfig)
            result = subprocess.run("sudo -H -u labuser kubectl get pods", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            pods_output = result.stdout.strip().split("\n")
            # Skip the header line and check each pod's status
            for line in pods_output[1:]:
                columns = line.split()
                if "Running" in columns[2]:
                    actual = expected_result
                    return test_object.update_result(1, expected_result, actual, testcase_description, "N/A", marks)
            return test_object.update_result(0, expected_result, actual, testcase_description, "N/A", marks)
        except Exception as e:
            return test_object.update_result(0, expected_result, actual, testcase_description, str(e), marks)



    def testcase_check_database_name_in_mysql_container(self, test_object):
        testcase_description = "Checking if the database 'tododb' exists in the MySQL container"
        expected = "The database 'tododb' exists in the MySQL container"
        actual = "The database 'tododb' does not exist in the MySQL container"
        marks = 5
        test_passed = "Congrats! The database 'tododb' exists."
        test_failed = "The database 'tododb' does not exist. Please verify the MySQL setup and database creation."
        test_object.update_pre_result(testcase_description, expected)

        container_name_filter = "mysql-db"  # Part of the container name to filter
        db_username = "root"
        db_password = "Root@123"
        expected_database_name = "tododb"

        def run_command(command):
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
            return result

        try:
            # Step 1: Get the container name containing 'mysql-db' and 'todo-application-pipeline'
            command_list_containers = (
                "docker ps -a --filter 'name=todo-application-pipeline' --format '{{.Names}}'"
            )
            result_list_containers = run_command(command_list_containers)

            if result_list_containers.returncode != 0:
                raise Exception(f"Error fetching container names: {result_list_containers.stderr.strip()}")

            containers = result_list_containers.stdout.strip().splitlines()
            mysql_container_name = next(
                (name for name in containers if container_name_filter in name), None
            )

            if not mysql_container_name:
                raise Exception("No MySQL container matching the criteria was found.")

            # Step 2: Check the database inside the container
            command_check_database = (
                f"docker exec -i {mysql_container_name} mysql -u{db_username} -p{db_password} "
                f"-e 'SHOW DATABASES;'"
            )
            result_check_database = run_command(command_check_database)

            if result_check_database.returncode != 0:
                stderr_output = result_check_database.stderr.strip()
                # Check for authentication error
                if "Access denied for user" in stderr_output:
                    actual = "Authentication failed: Invalid username or password."
                    test_failed = (
                        "Authentication issue detected. Please check the username and password."
                    )
                else:
                    actual = f"Error accessing MySQL: {stderr_output}"
                return test_object.update_result(0, expected, actual, test_failed, "N/A", marks)

            databases = result_check_database.stdout.strip().splitlines()
            if expected_database_name in databases:
                actual = expected
                return test_object.update_result(1, expected, actual, test_passed, "N/A", marks)
            else:
                actual = f"The database '{expected_database_name}' was not found. Available databases: {', '.join(databases)}"
                return test_object.update_result(0, expected, actual, test_failed, "N/A", marks)

        except Exception as e:
            test_object.update_result(0, expected, actual, testcase_description, "N/A", marks)
            test_object.eval_message["testcase_check_database_name_in_mysql_container"] = str(e)


def start_tests(args):
    args = args.replace("{", "")
    args = args.replace("}", "")
    args = args.split(":")
    args = {"token": args[1]}
    args = json.dumps(args)
    if "result_output" not in sys.modules:
        importlib.import_module("result_output")
    else:
        importlib.reload(sys.modules["result_output"])

    test_object = ResultOutput(args, Activity)
    challenge_test = Activity()

    # time.sleep(3)

    # Running all test cases
    challenge_test.testcase_check_docker_image(test_object)
    challenge_test.testcase_check_jenkins_user_in_docker_group(test_object)
    challenge_test.testcase_check_docker_image_tagged_correctly(test_object)
    challenge_test.testcase_check_pipeline_latest_build_successful(test_object)
    challenge_test.testcase_check_docker_volume_name_after_jenkins_pipeline(test_object)
    challenge_test.testcase_check_docker_network_name_after_jenkins_pipeline(test_object)
    challenge_test.testcase_check_application_status_after_jenkins_pipeline(test_object)
    challenge_test.testcase_check_mysql_db_creation_after_jenkins_pipeline(test_object)
    challenge_test.testcase_check_todo_application_container_after_jenkins_pipeline(test_object)
    challenge_test.testcase_check_kubernetes_secret_my_registry_secret(test_object)
    challenge_test.testcase_check_pod_states(test_object)
    challenge_test.testcase_check_application_on_minikube_ip(test_object)
    challenge_test.testcase_check_application_content_on_minikube_site(test_object)
    challenge_test.testcase_check_database_name_in_mysql_container(test_object)


    result = json.dumps(test_object.result_final())
    print(json.loads(result))


def main():

    args = sys.argv[1]
    start_tests(args)


if __name__ == "__main__":
    main()
