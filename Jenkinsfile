pipeline {
agent any
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
