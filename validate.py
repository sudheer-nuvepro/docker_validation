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
import socket
import requests


class Activity:

    def testcase_check_docker_file(self, test_object):
        import os
        testcase_description = "Check for creation of Dockerfile"
        expected_result = "Dockerfile is created"
        actual = "Dockerfile is not created"
        marks = 5
        test_object.update_pre_result(testcase_description, expected_result)
        try:
            docker_file_path = r"C:\Users\vmadmin\Desktop\Project\Dockerfile"
            if os.path.exists(docker_file_path):
                actual = "Dockerfile is created"
                return test_object.update_result(1, expected_result, actual, testcase_description, "N/A", marks)
            else:
                return test_object.update_result(0, expected_result, actual, testcase_description, "N/A", marks)
        except Exception:
            test_object.update_result(0, expected_result, actual, testcase_description, "N/A", marks)


    def testcase_check_base_images(self, test_object):
        testcase_description = "Check base images for build and runtime stages"
        expected_result = "Maven and OpenJDK used as base images"
        actual = "Base images incorrect or not found"
        marks = 5
        test_object.update_pre_result(testcase_description, expected_result)
        try:
            dockerfile_path = r"C:\Users\vmadmin\Desktop\Project\Dockerfile"
            if os.path.exists(dockerfile_path):
                with open(dockerfile_path, "r") as file:
                    content = file.read()
                    if "FROM maven:3.9.9-eclipse-temurin-17" in content and "FROM openjdk:17-jdk-slim" in content:
                        actual = "Maven and OpenJDK used as base images"
                        return test_object.update_result(1, expected_result, actual, testcase_description, "N/A", marks)
            return test_object.update_result(0, expected_result, actual, testcase_description, "N/A", marks)
        except Exception as e:
            return test_object.update_result(0, expected_result, actual, testcase_description, "N/A", marks)


    def testcase_check_exposed_port(self, test_object):
        testcase_description = "Check for 'EXPOSE 8080' in Dockerfile"
        expected_result = "Dockerfile should contain 'EXPOSE 8080'"
        actual = "'EXPOSE 8080' not found"
        marks = 5
        test_object.update_pre_result(testcase_description, expected_result)

        try:
            with open(r"C:\Users\vmadmin\Desktop\Project\Dockerfile", 'r') as file:
                content = file.read().upper()
                if "EXPOSE 8080" in content or "EXPOSE\t8080" in content:
                    actual = "'EXPOSE 8080' found in Dockerfile"
                    return test_object.update_result(1, expected_result, actual, testcase_description, "N/A", marks)
                else:
                    return test_object.update_result(0, expected_result, actual, testcase_description, "N/A", 0)
        except Exception as e:
            return test_object.update_result(0, expected_result, str(e), testcase_description, "N/A", 0)


    def testcase_check_jar_inclusion(self, test_object):
        testcase_description = "Check for application JAR inclusion in Dockerfile"
        expected_result = "Application JAR is included"
        actual = "JAR inclusion not found"
        marks = 5
        test_object.update_pre_result(testcase_description, expected_result)
        try:
            with open(r"C:\Users\vmadmin\Desktop\Project\Dockerfile", 'r') as file:
                content = file.read()
                if "COPY --from=build" in content and ".jar" in content:
                    actual = "Application JAR is included"
                    return test_object.update_result(1, expected_result, actual, testcase_description, "N/A", marks)
                else:
                    return test_object.update_result(0, expected_result, actual, testcase_description, "N/A", marks)
        except Exception:
            test_object.update_result(0, expected_result, actual, testcase_description, "N/A", marks)


    def testcase_check_entrypoint(self, test_object):
        testcase_description = "Check for ENTRYPOINT  in Dockerfile"
        expected_result = "ENTRYPOINT is present"
        actual = "ENTRYPOINT not found"
        marks = 5
        test_object.update_pre_result(testcase_description, expected_result)
        try:
            with open(r"C:\Users\vmadmin\Desktop\Project\Dockerfile", 'r') as file:
                content = file.read().upper()
                if ("ENTRYPOINT" in content or "CMD" in content) and "H2" in content:
                    actual = "ENTRYPOINT is present"
                    return test_object.update_result(1, expected_result, actual, testcase_description, "N/A", marks)
                else:
                    return test_object.update_result(0, expected_result, actual, testcase_description, "N/A", marks)
        except Exception:
            return test_object.update_result(0, expected_result, actual, testcase_description, "N/A", marks)



    def testcase_check_docker_image(self, test_object):
        import subprocess
        testcase_description = "Check if Docker image is created"
        expected_result = "Docker image exists with name 'incident-report'"
        actual = "Docker image not found with name 'incident-report'"
        marks = 5
        test_object.update_pre_result(testcase_description, expected_result)
        try:
            result = subprocess.getoutput("docker images -q incident-report")
            if result.strip():
                actual = "Docker image exists with name 'incident-report'"
                return test_object.update_result(1, expected_result, actual, testcase_description, "N/A", marks)
            else:
                return test_object.update_result(0, expected_result, actual, testcase_description, "N/A", marks)
        except Exception:
            test_object.update_result(0, expected_result, actual, testcase_description, "N/A", marks)


    def testcase_check_swagger_and_then_h2(self,test_object):
        testcase_description = "Check Swagger UI first, then H2 Console if Swagger is available"
        expected_result = "Swagger UI and H2 Console should return HTTP 200"
        marks = 20
        test_object.update_pre_result(testcase_description, expected_result)

        swagger_pass = False
        h2_pass = False
        actual_msgs = []

        container_name = "incident-report-container"

        def start_container():
            subprocess.run(["docker", "rm", "-f", container_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["docker", "run", "-d", "--name", container_name, "-p", "8081:8080", "incident-report"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        def stop_container():
            subprocess.run(["docker", "rm", "-f", container_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        try:
            # Try checking Swagger UI first
            try:
                response = requests.get("http://localhost:8081/swagger-ui/index.html", timeout=3)
                if response.status_code == 200:
                    swagger_pass = True
            except requests.exceptions.RequestException:
                # Start container and retry Swagger UI
                start_container()
                for _ in range(10):
                    time.sleep(3)
                    try:
                        response = requests.get("http://localhost:8081/swagger-ui/index.html", timeout=3)
                        if response.status_code == 200:
                            swagger_pass = True
                            break
                    except requests.exceptions.RequestException:
                        continue
                if not swagger_pass:
                    actual_msgs.append("Swagger UI not reachable after retries")

            # If Swagger passed, check H2 Console
            if swagger_pass:
                try:
                    response = requests.get("http://localhost:8081/h2-console", timeout=3)
                    if response.status_code == 200:
                        h2_pass = True
                    else:
                        actual_msgs.append(f"H2 Console returned HTTP {response.status_code}")
                except Exception as e:
                    actual_msgs.append(f"H2 Console check failed: {str(e)}")
            else:
                actual_msgs.append("Swagger UI failed. Skipping H2 Console check.")

        finally:
            stop_container()

        # Final evaluation
        if swagger_pass and h2_pass:
            actual = "Swagger UI and H2 Console are both accessible"
            return test_object.update_result(1, expected_result, actual, testcase_description, "N/A", 20)
        elif swagger_pass:
            actual = "Swagger UI accessible; H2 Console failed or skipped. " + "; ".join(actual_msgs)
            return test_object.update_result(1, expected_result, actual, testcase_description, "N/A", 10)
        else:
            actual = "Swagger UI not accessible. " + "; ".join(actual_msgs)
            return test_object.update_result(0, expected_result, actual, testcase_description, "N/A", 0)


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
    challenge_test.testcase_check_docker_file(test_object)
    challenge_test.testcase_check_base_images(test_object)
    challenge_test.testcase_check_exposed_port(test_object)
    challenge_test.testcase_check_jar_inclusion(test_object)
    challenge_test.testcase_check_entrypoint(test_object)
    challenge_test.testcase_check_docker_image(test_object)
    challenge_test.testcase_check_swagger_and_then_h2(test_object)  

    result = json.dumps(test_object.result_final())
    print(json.loads(result))


def main():

    args = sys.argv[2]
    start_tests(args)


if __name__ == "__main__":
    main()
