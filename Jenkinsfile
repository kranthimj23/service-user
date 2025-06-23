pipeline {
 
    agent any
 
    environment {
 
        PROJECT_ID = 'bamboo-diode-456912-p9'
        CLUSTER = 'autopilot-cluster-1'
        ZONE = 'asia-south1'
        GCP_KEY = 'C:\\Users\\himan\\Downloads\\devops-lab-ci\\flask-gke-helm\\jenkins-sa-key.json'  
 
        PYTHON_EXEC = 'C:\\Users\\himan\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'
 
        
// ⚠️ Ensure this path exists
 
    }
 
    stages {
 
        stage('Checkout') {
 
            steps {
 
                checkout scm
 
            }
 
        }
 
        stage('Authenticate with GCP') {
 
            steps {
 
                bat """
 
                gcloud auth activate-service-account --key-file="${env.GCP_KEY}"
 
                gcloud config set project ${env.PROJECT_ID}
 
                gcloud auth configure-docker asia-south1-docker.pkg.dev --quiet
 
                """
 
            }
 
        }
 
        stage('Build Docker Image') {
 
            steps {
 
                def image_repo = "asia-south1-docker.pkg.dev/${env.PROJECT_ID}/service-user/user"
                def image_tag = "${BUILD_NUMBER}-${env.env_namespace}"
 
                bat """
                
                docker build -f ./app/Dockerfile -t ${image_repo}:${image_tag} .
                docker push ${image_repo}:${image_tag}
 
                """
 
            }
 
        }
 
        stage('Deploy to GKE-1') {
 
            steps {
 
                bat """
 
                gcloud container clusters get-credentials ${env.CLUSTER} --zone ${env.ZONE} --project ${env.PROJECT_ID}
 
                """
 
                configFileProvider([configFile(fileId: 'deploy_to_gke', targetLocation: 'deploy_to_gke.py')]) {
 
                        script {
 
                            def result = bat(
 
                                script: "${env.PYTHON_EXEC} deploy_to_gke.py ${env.env_namespace} ${image_repo} ${image_tag} ${env.github_url} ",
 
                                returnStdout: true
 
                            ).trim()
 
                            echo "Deployment Output:\n${result}"
 
                        }
                }
            }
        }
    }
}
 
