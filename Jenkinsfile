pipeline {
agent any
    stages {
        stage('build') {
          steps {
            sh 'python3 --version'
           }
        }
    stages {
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: 'main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/ronacpatel/Project_V1']]])
                }
            } 
            stage('Build') {
            steps {
                git branch: 'main', url: 'https://github.com/ronacpatel/Project_V1'
                sh 'python3 ops.py'
            }
        }
      stage('Deploy Image') {
                steps{
                  echo 'Deploying the Docker Image'
                  script {
                    docker.withRegistry( '', registryCredential ) {
                      dockerImage.push()
                    }
                } 
                        stage('Test') {
                            steps {
                                sh 'python3 -m pytest'
            }
        }
      }
    }   
}
