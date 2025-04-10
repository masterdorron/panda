pipeline {
    agent any
    environment {
        IMAGE_TAG = "my-python-app:build-${BUILD_NUMBER}"
        CONTAINER_NAME = "test-my-python-app-build-${BUILD_NUMBER}"
    }
    stages {
        stage('Build') {
            steps {
                sh "docker build -t ${IMAGE_TAG} ."
            }
        }
        stage('Test') {
            steps {
                sh "docker run -d -p 5000:5000 --name ${CONTAINER_NAME} ${IMAGE_TAG}"
                sh 'sleep 5'
                sh 'curl --fail http://host.docker.internal:5000/api || exit 1'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker-compose down || true'
                sh "IMAGE_TAG=${IMAGE_TAG} docker-compose up -d"
            }
        }
    }
    post {
        always {
            sh "docker stop ${CONTAINER_NAME} || true"
            sh "docker rm ${CONTAINER_NAME} || true"
        }
    }
}
