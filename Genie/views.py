import json
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import ollama


def home(request):
    return render(request, 'index.html')


def dockerfile_form(request):
    error = ''
    if request.method == 'POST':
        language = request.POST.get('language', '').strip()
        if language:
            request.session['gen_type'] = 'dockerfile'  # Set gen_type explicitly
            request.session['user_input'] = language    # Store language as user_input
            return redirect('generate_output')
        else:
            error = 'Please enter a programming language.'
    return render(request, 'dockerfile_form.html', {'error': error})

def jenkinsfile_form(request):
    if request.method == 'POST':
        language = request.POST.get('language', '').strip()
        repo_url = request.POST.get('repo_url', '').strip()
        branch = request.POST.get('branch', '').strip()
        docker_path = request.POST.get('docker_path', '').strip()
        deployment_manifest = request.POST.get('deployment_manifest', '').strip()
        git_username = request.POST.get('git_username', '').strip()
        git_email = request.POST.get('git_email', '').strip()
        sonarqube_url = request.POST.get('sonarqube_url', '').strip()

        # Validate required fields
        if language and repo_url and branch and docker_path and deployment_manifest:
            user_input = {
                'language': language,
                'repo_url': repo_url,
                'branch': branch,
                'docker_path': docker_path,
                'deployment_manifest': deployment_manifest,
                'git_username': git_username,
                'git_email': git_email,
                'sonarqube_url': sonarqube_url,
            }
            request.session['gen_type'] = 'jenkinsfile'
            request.session['user_input'] = user_input
            return redirect('generate_output')
        else:
            error = "Please fill in all required fields: language, repo URL, branch, docker file path, deployment manifest path."
            return render(request, 'jenkinsfile_form.html', {'error': error})

    return render(request, 'jenkinsfile_form.html')


def terraform_form(request):
    if request.method == 'POST':
        provider = request.POST.get('provider', '').strip()
        region = request.POST.get('region', '').strip()
        project_name = request.POST.get('project_name', '').strip()
        resources = request.POST.get('resources', '').strip()
        use_remote_state = request.POST.get('use_remote_state') == 'on'

        if provider and region and project_name and resources:
            user_input = {
                'provider': provider,
                'region': region,
                'project_name': project_name,
                'resources': resources,
                'use_remote_state': use_remote_state
            }
            request.session['gen_type'] = 'terraform'
            request.session['user_input'] = user_input
            return redirect('generate_output')
        else:
            error = "Please fill in all required fields: provider, region, project name, and resources."
            return render(request, 'terraform_form.html', {'error': error})

    return render(request, 'terraform_form.html')


def ansible_form(request):
    if request.method == 'POST':
        playbook_name = request.POST.get('playbook_name', '').strip()
        hosts = request.POST.get('hosts', '').strip()
        become = request.POST.get('become') == 'on'  # checkbox
        tasks = request.POST.get('tasks', '').strip()  # e.g. "install nginx, start service"
        vars_section = request.POST.get('vars_section', '').strip()  # optional vars as JSON or YAML string

        if playbook_name and hosts and tasks:
            user_input = {
                'playbook_name': playbook_name,
                'hosts': hosts,
                'become': become,
                'tasks': tasks,
                'vars_section': vars_section,
            }
            request.session['gen_type'] = 'ansible'
            request.session['user_input'] = user_input
            return redirect('generate_output')
        else:
            error = "Please fill in all required fields: playbook name, hosts, and tasks."
            return render(request, 'ansible_form.html', {'error': error})

    return render(request, 'ansible_form.html')


def k8s_form(request):
    if request.method == 'POST':
        app_name = request.POST.get('app_name', '').strip()
        image = request.POST.get('image', '').strip()
        replicas = request.POST.get('replicas', '1').strip()
        container_port = request.POST.get('container_port', '80').strip()
        service_type = request.POST.get('service_type', 'ClusterIP').strip()
        service_port = request.POST.get('service_port', '80').strip()
        target_port = request.POST.get('target_port', container_port).strip()

        if app_name and image:
            user_input = {
                'app_name': app_name,
                'image': image,
                'replicas': replicas,
                'container_port': container_port,
                'service_type': service_type,
                'service_port': service_port,
                'target_port': target_port,
            }
            request.session['gen_type'] = 'k8s'
            request.session['user_input'] = user_input
            return redirect('generate_output')
        else:
            error = "Please fill in all required fields: app name and image."
            return render(request, 'k8s_form.html', {'error': error})

    return render(request, 'k8s_form.html')

def github_action_form(request):
    if request.method == 'POST':
        language = request.POST.get('language', '').strip()
        repo_url = request.POST.get('repo_url', '').strip()
        branch = request.POST.get('branch', '').strip()
        docker_path = request.POST.get('docker_path', '').strip()
        deployment_manifest = request.POST.get('deployment_manifest', '').strip()
        git_username = request.POST.get('git_username', '').strip()
        git_email = request.POST.get('git_email', '').strip()
        sonarqube_url = request.POST.get('sonarqube_url', '').strip()

        if language and repo_url and branch and docker_path and deployment_manifest:
            user_input = {
                'language': language,
                'repo_url': repo_url,
                'branch': branch,
                'docker_path': docker_path,
                'deployment_manifest': deployment_manifest,
                'git_username': git_username,
                'git_email': git_email,
                'sonarqube_url': sonarqube_url,
            }
            request.session['gen_type'] = 'github_action'
            request.session['user_input'] = user_input
            return redirect('generate_output')
        else:
            error = "Please fill in all required fields."
            return render(request, 'github_action_form.html', {'error': error})

    return render(request, 'github_action_form.html')

@csrf_exempt
def generate_output(request):
    gen_type = request.session.get('gen_type')
    user_input = request.session.get('user_input')

    if not gen_type or not user_input:
        return render(request, 'error.html', {'message': 'Missing parameters'})

    output_code = None
    title = None

    if gen_type == 'dockerfile':
        PROMPT = f"""
        ONLY Generate an ideal Dockerfile for {user_input} with best practices. Do not provide any description
        - Do not include explanations, comments outside the Dockerfile, or extra text—only the Dockerfile content.
        Include:
        - Base image
        - Copying dependencies
        - Installing dependencies
        - Setting working directory
        - Adding source code
        - Running the application
        """
        response = ollama.chat(model='llama3.2:3b', messages=[{'role': 'user', 'content': PROMPT}])
        output_code = response['message']['content']
        title = f"Optimized Dockerfile for {user_input.capitalize()}"

    elif gen_type == 'jenkinsfile':
        PROMPT = f"""
            ONLY generate a fully functional declarative Jenkins pipeline Jenkinsfile for a {user_input['language']} project following best practices.
            - Do not include explanations, comments outside the Jenkinsfile, or extra text—only the Jenkinsfile content.
            Use these inputs:
            - Git repository URL: {user_input['repo_url']}
            - Git branch: {user_input['branch']}
            - Dockerfile path: {user_input['docker_path']}
            - Deployment manifest directory path: {user_input['deployment_manifest']}
            - Git username/email (if provided): {user_input.get('git_username', 'Jenkins')} / {user_input.get('git_email', 'jenkins@ci.com')}
            - SonarQube URL (if provided): {user_input.get('sonarqube_url', '')}
            - Jenkins credential IDs: Use 'docker-cred' for Docker registry, 'github' for GitHub token, 'sonarqube' for SonarQube authentication token.

            Requirements:
            - Use a global Docker agent with a dynamically chosen Docker image based on the project language and requirements (e.g., 'maven:3.9.6-eclipse-temurin-17' for Java/Maven, 'node:20' for Node.js, 'python:3.11' for Python, 'docker:24.0.7-dind' for projects requiring Docker-in-Docker with additional tools installed).
            - If the base image lacks required tools (e.g., Git, Trivy, kubectl), include an 'Install Dependencies' stage to install them using the appropriate package manager (e.g., apk for Alpine-based images, apt for Debian-based images).
            - Mount the Docker socket using args '--user root --privileged -v /var/run/docker.sock:/var/run/docker.sock' to support Docker operations.
            - Define environment variables for:
            - DOCKER_REGISTRY: 'docker.io'
            - DOCKER_CREDENTIALS_ID: 'docker-cred'
            - IMAGE_NAME: "${{DOCKER_REGISTRY}}/my-org/my-app" (replace 'my-org/my-app' with a suitable default or derive from repo if possible)
            - IMAGE_TAG: "${{BUILD_NUMBER}}"
            - GIT_REPO: {user_input['repo_url']}
            - DEPLOYMENT_MANIFEST_PATH: {user_input['deployment_manifest']}
            - SONARQUBE_URL: credentials('sonarqube-url') (if provided)
            - JENKINS_GITHUB_TOKEN: credentials('github')
            - Include these stages, in order:
            1. Install Dependencies (if needed): Install Git, Trivy, kubectl, and language-specific tools (e.g., Maven, npm, pip) if not included in the base image.
            2. Checkout: Clone the repo and branch using 'github' credentials.
            3. Build and Test: Run standard build and test commands for the project language (e.g., 'mvn clean package' and 'mvn test' for Java/Maven, 'npm install && npm run build' and 'npm test' for Node.js, 'pip install -r requirements.txt' and 'pytest' for Python). Publish test results (e.g., JUnit for Java, Mocha for Node.js).
            4. Static Code Analysis: If SONARQUBE_URL is provided, run SonarQube analysis with 'sonarqube' credentials, appropriate language scanner (e.g., 'mvn sonar:sonar' for Java), and wait for quality gate with a 10-minute timeout.
            5. Docker Build: Build Docker image using the Dockerfile at {user_input['docker_path']}, tag with ${{IMAGE_TAG}}.
            6. Docker Scan: Run Trivy scan on the image (${{IMAGE_NAME}}:${{IMAGE_TAG}}) for HIGH and CRITICAL vulnerabilities, using '--exit-code 1 --severity HIGH,CRITICAL --format table'. Fail the build if vulnerabilities are found.
            7. Docker Push: Push both ${{IMAGE_NAME}}:${{IMAGE_TAG}} and ${{IMAGE_NAME}}:latest to the registry using 'docker-cred' credentials.
            8. Update Deployment Manifests: Update Kubernetes manifests in {user_input['deployment_manifest']} (e.g., replace 'image: ${{IMAGE_NAME}}:.*' with 'image: ${{IMAGE_NAME}}:${{IMAGE_NAME}}'). Configure Git with user.name and user.email, commit changes, and push to the repo using 'github' credentials.
            - Include a post block with:
            - always: Clean workspace using cleanWs().
            - success: Echo 'Build Successful!'.
            - failure: Echo 'Build Failed!'.
            - Ensure secure handling of credentials using withCredentials and withDockerRegistry for Git and Docker operations.
            - Use appropriate shebang (#!/bin/sh or #!/bin/bash) in shell commands if needed.

            - Do not include explanations, comments outside the Jenkinsfile, or extra text—only the Jenkinsfile content.

            """
                

        response = ollama.chat(model='llama3.2:3b', messages=[{'role': 'user', 'content': PROMPT}])
        output_code = response['message']['content']
        title = f"Optimized Jenkinsfile for {user_input['language'].capitalize()}"

    elif gen_type == 'terraform':
        PROMPT = f"""
            ONLY generate Terraform code (no explanations, no extra text).

            Project:
            - Provider: {user_input['provider']}
            - Region: {user_input['region']}
            - Project Name: {user_input['project_name']}
            - Resources: {user_input['resources']}

            Generate the following files in one output, each preceded by a commented heading with the file name:

            # ===== main.tf =====
            # Define the provider configuration and requested resources

            # ===== variables.tf =====
            # Define input variables used in the project

            # ===== terraform.tfvars =====
            # Provide example values for the variables

            # ===== outputs.tf =====
            # Export key outputs like IP addresses, resource IDs, names

            # ===== backend.tf =====
            # {"Configure remote backend (e.g., AWS S3 + DynamoDB locking)" if user_input.get("use_remote_state") else "Use local backend or leave empty."}

            Follow Terraform and HCL best practices strictly.
            """

        response = ollama.chat(model='llama3.2:3b', messages=[{'role': 'user', 'content': PROMPT}])
        output_code = response['message']['content']
        title = f"Terraform Configuration for {user_input['project_name']} ({user_input['provider'].upper()})"

    elif gen_type == 'ansible':
        PROMPT = f"""
            ONLY generate a valid Ansible playbook YAML file content named '{user_input['playbook_name']}.yaml' without any explanations or extra text.

            Requirements:
            - Playbook name: {user_input['playbook_name']}
            - Hosts: {user_input['hosts']}
            - Become (privilege escalation): {"yes" if user_input['become'] else "no"}
            - Tasks: {user_input['tasks']}
            - Include a 'vars' section if provided (YAML or JSON format): {user_input['vars_section'] if user_input['vars_section'] else 'none'}

            Tasks description: parse the task list (comma-separated) and generate corresponding Ansible tasks with best practices.
            Use appropriate modules for common tasks (e.g., apt/yum for package installs, service for managing services).
            Ensure proper YAML syntax.
            """

        response = ollama.chat(model='llama3.2:3b', messages=[{'role': 'user', 'content': PROMPT}])
        output_code = response['message']['content']
        title = f"Ansible Playbook: {user_input['playbook_name']}.yaml"

    elif gen_type == 'k8s':
        PROMPT = f"""
            ONLY generate Kubernetes YAML manifests without any explanations or extra text ,each preceded by a commented heading with the file name

            Create a Deployment and a Service for an application with the following specs:

            Deployment:
            - apiVersion: apps/v1
            - kind: Deployment
            - metadata:
                name: {user_input['app_name']}
                labels:
                app: {user_input['app_name']}
            - spec:
                replicas: {user_input['replicas']}
                selector:
                matchLabels:
                    app: {user_input['app_name']}
                template:
                metadata:
                    labels:
                    app: {user_input['app_name']}
                spec:
                    containers:
                    - name: {user_input['app_name']}
                    image: {user_input['image']}
                    ports:
                    - containerPort: {user_input['container_port']}

            Service:
            - apiVersion: v1
            - kind: Service
            - metadata:
                name: {user_input['app_name']}-service
            - spec:
                type: {user_input['service_type']}
                ports:
                - port: {user_input['service_port']}
                targetPort: {user_input['target_port']}
                protocol: TCP
                name: http
                selector:
                app: {user_input['app_name']}
            """
        response = ollama.chat(model='llama3.2:3b', messages=[{'role': 'user', 'content': PROMPT}])
        output_code = response['message']['content']
        title = f"Kubernetes Deployment and Service for {user_input['app_name']}"

    elif gen_type == 'github_action':
        PROMPT = f"""
            ONLY generate a fully functional GitHub Actions CI workflow YAML file for the project language provided as input ({user_input['language']}).

        Use these inputs:
        - GitHub repo URL: {user_input['repo_url']}
        - Git branch: {user_input['branch']}
        - Dockerfile path: {user_input['docker_path']}
        - Kubernetes deployment manifest path: {user_input['deployment_manifest']}
        - Git username/email: {user_input.get('git_username', 'GitHub Actions')} / {user_input.get('git_email', 'actions@github.com')}
        - SonarQube URL (optional): {user_input.get('sonarqube_url', '')}

        Requirements:
        - Trigger workflow on push to {user_input['branch']} and on pull_request
        - Detect the project language dynamically based on the input language string (case-insensitive)
        - Automatically select the appropriate environment setup, build, and test steps for the detected language, including:
        - Choosing the best official setup actions or Docker base images
        - Installing dependencies and running tests accordingly
        - If the language is unknown or unsupported, skip language-specific steps gracefully
        - Define environment variables:
        - IMAGE_NAME: docker.io/my-org/my-app
        - IMAGE_TAG: ${{ github.run_number }}
        - DEPLOYMENT_MANIFEST_PATH: {user_input['deployment_manifest']}
        - Use GitHub Secrets where appropriate for authentication (DOCKER_USERNAME, DOCKER_PASSWORD, SONARQUBE_TOKEN, GITHUB_TOKEN)
        - Workflow jobs and steps:
        1. Checkout the code
        2. Setup environment and run build/test steps for the detected language only
        3. Run SonarQube analysis if SonarQube URL is provided
        4. Build Docker image using the provided Dockerfile path
        5. Scan Docker image with Trivy; fail if HIGH or CRITICAL vulnerabilities found
        6. Push Docker image with tags :${{ env.IMAGE_TAG }} and :latest
        7. Deploy to Kubernetes using kubectl and the deployment manifest path
        8. Commit and push any deployment manifest changes with the provided Git username/email using GITHUB_TOKEN

        Output only valid YAML content for `.github/workflows/ci.yml`. Do not include any explanations or extra text.

        """

        response = ollama.chat(model='llama3.2:3b', messages=[{'role': 'user', 'content': PROMPT}])
        output_code = response['message']['content']
        title = f"GitHub Actions Workflow for {user_input['language'].capitalize()}"


    else:
        return render(request, 'error.html', {'message': 'Invalid generation type'})

    return render(request, 'output_code.html', {
        'output_code': output_code,
        'title': title,
    })
