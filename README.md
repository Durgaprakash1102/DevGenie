# DevGenie 🧞‍♂️

DevGenie is an experimental web application that leverages local Large Language Models (LLMs) to assist with DevOps tasks by generating essential infrastructure and automation files such as:

- Dockerfile  
- Jenkinsfile  
- Terraform  
- Ansible Playbook
- Kubernetes YAMLs  
- GitHub Actions workflows  

This project is designed to showcase the intersection of AI, DevOps knowledge, and full-stack development using open-source tools.

---

## 🚀 Tech Stack

- Backend: Django (Python)  
- LLM Integration: Ollama running locally  
- AI Model: LLaMA 3.2 (3B parameters)  
- Frontend: HTML/CSS/Js

---

## 📦 Installation Steps

Follow the instructions below to run DevGenie locally:

1. Install Ollama  
   Download Ollama from: https://ollama.com/download

2. Pull the LLaMA 3.2 (3B) model  
* Open terminal and run:
  - ollama pull llama3:3b

3. Create a virtual environment
  - python -m venv venv

4. Activate the virtual environment

   * On Windows:
    - venv\Scripts\activate
     
   * On macOS/Linux:
     - source venv/bin/activate

5. Clone this repository
  - [https://github.com/Durgaprakash1102/DevGenie.git](https://github.com/Durgaprakash1102/DevGenie.git)
  - cd DevGenie

6. Install Python dependencies
   - pip install -r requirements.txt

7. Apply Django migrations
  - python manage.py makemigrations
  - python manage.py migrate

8. Run the development server
  - python manage.py runserver

9. Open your browser and visit:
  - [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## ⚠️ Important Notes

* The AI-generated files are not production-ready.
* The LLaMA 3.2 3B model is a relatively small model; its responses may be inaccurate or incomplete.
* All generated outputs (Dockerfiles, Kubernetes YAMLs, etc.) should be reviewed and validated by a professional developer or DevOps engineer before use.
  
* Output quality may improve significantly with:
  * Larger parameter LLMs
  * More refined and domain-specific prompt engineering
    
* This project is a prototype and serves as a learning and experimentation tool to combine:

  * Development skills
  * DevOps practices
  * LLM-powered automation

## 🤝 Contributing

Feel free to fork the repository, raise issues, or submit pull requests.
All contributions to improve functionality, accuracy, and UI are welcome!

## 📸 Project Screenshots
![Screenshot 2025-05-27 at 09-56-43 DevGenie – AI-powered DevOps Automation Assistant](https://github.com/user-attachments/assets/c17f23c9-471e-45aa-98c1-2ae20cbf1872)
![Screenshot 2025-05-27 at 09-57-30 Generate Dockerfile – DevGenie](https://github.com/user-attachments/assets/78bab426-4b4d-42ed-83d5-75e8f2d55a25)
![Screenshot 2025-05-27 at 09-57-46 Generate Terraform Config – DevGenie](https://github.com/user-attachments/assets/7bbbb19f-11c1-4bcd-b688-9c3496bceaf1)
![Screenshot 2025-05-27 at 09-59-22 Generate Jenkinsfile – DevGenie](https://github.com/user-attachments/assets/79c7b8ca-50ba-4ed5-88b4-257268c13c85)
![Screenshot 2025-05-27 at 09-59-44 Generate Ansible Playbook – DevGenie](https://github.com/user-attachments/assets/0fe2c137-84da-4568-9ee1-a7d91bd27ed8)
![Screenshot 2025-05-27 at 09-59-57 Generate Kubernetes YAML – DevGenie](https://github.com/user-attachments/assets/af38f773-94fd-4800-aafc-f2984f4c8833)
![Screenshot 2025-05-27 at 10-00-15 Generate GitHub Actions Workflow – DevGenie](https://github.com/user-attachments/assets/c32520b3-f323-429c-8a59-5bcedbdbe13c)

## ⚙️ LLaMA Model Sample Outputs
![Screenshot 2025-05-27 at 10-17-19 Optimized Jenkinsfile for Java – DevGenie](https://github.com/user-attachments/assets/0f767e92-195a-4320-a49b-45c618e0e550)
![Screenshot 2025-05-27 at 10-05-01 Optimized Dockerfile for Django – DevGenie](https://github.com/user-attachments/assets/7bf3e53a-639a-4874-816b-a6eceea49e83)
![Screenshot 2025-05-27 at 10-35-49 GitHub Actions Workflow for Java – DevGenie](https://github.com/user-attachments/assets/e6a530df-671c-4d04-b906-f52485da6bf8)
![Screenshot 2025-05-27 at 10-28-59 Kubernetes Deployment and Service for DevGenie – DevGenie](https://github.com/user-attachments/assets/3d96b9d8-a3d7-4942-870e-72b589b30499)
![Screenshot 2025-05-27 at 10-24-02 Ansible Playbook DevGenie yaml – DevGenie](https://github.com/user-attachments/assets/62a135df-9422-4a8c-b390-d58b8321aa8a)
![Screenshot 2025-05-27 at 10-21-24 Terraform Configuration for DevGenie (AWS) – DevGenie](https://github.com/user-attachments/assets/bf34521c-16cb-4e4d-aab5-60a1eda9e9b5)




## 🙌 Thanks

Thanks to **Abhishek Veermalla** whose tutorial helped me understand and implement LLM integration in this prototype.


