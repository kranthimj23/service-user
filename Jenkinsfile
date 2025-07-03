def image_repo = ''
def image_tag = ''

pipeline {
    agent any

    environment {
        PROJECT_ID = 'devops-ai-labs-1'
        CLUSTER = 'demo-gke-cluster'
        ZONE = 'asia-south1'
       //GCP_KEY = 'C:\\Users\\devops-ai-labs-1-ffe9cbe45593.json'
        GCP_KEY = devops-ai-labs-1-ffe9cbe45593.json
        PYTHON_EXEC = python
        GIT_CREDENTIALS_ID = credentials('jenkins-token')
        //PYTHON_EXEC = 'C:\\Users\\himan\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'
    }

    stages {
 
        stage('Checkout with credentials') {
            steps {
                deleteDir()
                script {
                    withCredentials([string(credentialsId: 'jenkins-token', variable: 'GIT_TOKEN')]) {
                        checkout([
                            $class: 'GitSCM',
                            branches: [[name: "*/dev"]],
                            userRemoteConfigs: [[
                                url: "https://${GIT_TOKEN}@github.com/kranthimj23/aerospike-app.git"
                            ]]
                        ])
                    }
                }
            }
        }
        
        stage('Authenticate with GCP') {
            steps {
                sh """
                    gcloud auth activate-service-account --key-file="C:\\Users\\devops-ai-labs-1-ffe9cbe45593.json"
                    gcloud config set project devops-ai-labs-1
                    gcloud auth configure-docker asia-south1-docker.pkg.dev --quiet
                    gcloud auth list
                """
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    image_repo = "asia-south1-docker.pkg.dev/${env.PROJECT_ID}/service-user/user"
                    image_tag = "${BUILD_NUMBER}-${env.env_namespace}"
                    def image_full = "${image_repo}:${image_tag}"

                    sh """
                        gcloud auth print-access-token | docker login -u oauth2accesstoken --password-stdin https://asia-south1-docker.pkg.dev
                        echo " docker build -t ${image_full} . "
                        echo " docker push ${image_full} "
                        docker build -t ${image_full} .
                        docker push ${image_full}
                    """
                }
            }
        }

        stage('Deploy to GKE') {
            steps {
                sh """
                    gcloud container clusters get-credentials ${env.CLUSTER} --zone ${env.ZONE} --project ${env.PROJECT_ID}
                """

                configFileProvider([configFile(fileId: 'deploy_to_gke', targetLocation: 'deploy_to_gke.py')]) {
                     script {
                            def pythonCommand = """
                                set CLUSTER=${env.CLUSTER}
                                set ZONE=${env.ZONE}
                                set PROJECT_ID=${env.PROJECT_ID}
                                echo Running Python script...
                                ${env.PYTHON_EXEC} deploy_to_gke.py ${env.env_namespace} ${image_repo} ${image_tag} ${env.github_url} ${env.microservice}
                            """
                        
                            echo "Executing Python Deployment Script..."
                        
                            def result = bat(script: pythonCommand, returnStdout: true).trim()
                            echo "Deployment Output:\n${result}"
                        }
                }
            }
        }
    }
}
