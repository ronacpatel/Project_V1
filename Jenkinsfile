pipeline {
agent { docker { image 'python:3.11.5' } }
stages {
stage('build') {
steps {
sh 'python3 --version'
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
