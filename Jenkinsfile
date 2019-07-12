pipeline {
  agent { docker { image 'python:3.6.2 ' } }
  stages {
    stage('build') {
      steps {
        sh 'pip install pytest'
        sh 'pip install -r requirements.txt'
      }
    }
    stage('test') {
      steps {
        sh 'py.test --junitxml results.xml tests/'
      }   
    }
  }
}
